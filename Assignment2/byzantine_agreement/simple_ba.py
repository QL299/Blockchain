import time
import config
import json
import random
from p2p import synchrony, gossip
from blockchain import util
from blockchain.util import run_async

class SimplePKIBA:

    def __init__(self, sender):
        """ A simple PKI based protocol for Byzantine agreement.

            Args:
                sender (int): Node ID of sender in peer list.

            Attributes:
                s_i (list of tuples of str): represents accepted proposals.
                votes (map of str to set of int): represents nodes that broadcasted signatures on a message/proposal.
                signatures (map of str to list of (tuple of int, str)): maps string messages/proposals to
                    accepted signatures; each signature is a tuple of the node ID that signed and string hex signature.
                sender (int): node ID acting as the protocol sender (see protocol description in notes)
                curr_round_number (int): last round processed internally by the BA protocol
        """
        # Pseudocode: All players i maintain a set Si (of possible outputs) that starts off as empty
        self.s_i = []
        self.votes = {} # maps proposed messages to sets of node IDs that voted for that message
        self.signatures = {} # maps proposed messages to list of accepted (node_id, signature) tuples, corresponding to valid votes
        self.sender = sender
        self.curr_round_number = -1

        # Player s (the sender) receiving (s; m) as input computes and multicasts mpks, and adds m to his set Ss.
        if config.node_id == sender:
            string_to_vote_for = str(int(random.random() * 2 ** 256)) # for demo purposes, we'll vote for a random string
            self.votes[string_to_vote_for] = set([config.node_id])
            proposal_sig = util.sign_message(string_to_vote_for, config.SECRET_KEYS[config.node_id])
            self.signatures[string_to_vote_for] = [(config.node_id, proposal_sig)]

        self.run_protocol_loop()

    def calculate_votes_for(self, round):
        """ Calculate what votes a node should gossip out in the provided round.
            These are proposals that match the criteria given in 4.1, and that a
            node has not previously added to its s_i set and broadcast votes for.
            This function should also update the relevant data structures with the
            current node's vote.

            Args:
                round (int): Round to target.

            Returns:
                list of str: Returns a list of proposals to broadcast votes for.
        """
        # Get all proposals with r votes, including sender

        # placeholder for (3.1)
                # proposal is new proposal that has just achieved threshold (m not in Sj)
                # Pseudocode: then j adds m to its set Sj, signs m using its secret key skj, and multicasts...
        votes_for_list = []
        for i in self.get_proposals_with_threshold(round):
            if i not in self.s_i:
                votes_for_list.append(i)
                self.s_i.append(i)
                self.votes[i].add(config.node_id)
                self.signatures[i].append((config.node_id, util.sign_message(i, config.SECRET_KEYS[config.node_id])))

        return votes_for_list

    def get_proposals_with_threshold(self, round):
        """ Gets proposals that have reached the threshold required by a given round.

            Args:
                round (int): Round to target.

            Returns:
                list of str: Returns a list of all proposals eligible for adding to a node's s_i
                (proposals that have achieved required vote thresholds).

            This function *DOES NOT* need to check signatures; assume they are already checked in process_vote.
        """
        # Pseudocode: with signatures from r different players, including player s

        # placeholder for (3.2)
        proposal_list = []
        for i, eachProposal in self.votes.items():
            if len(eachProposal) >= round and len(eachProposal) >= 0 and 1 in eachProposal:
                proposal_list.append(i)
        return proposal_list


    def broadcast_votes_for(self, round, votes):
        """ Broadcast votes on a proposal to all nodes; this happens once a proposal is added to s_i. """
        for proposal in votes:
            gossip.gossip_message("ba-vote", json.dumps([proposal, self.signatures[proposal]]))

    def process_vote(self, vote):
        """ Process an incoming vote and add to relevant datastructures. """
        # authenticate vote signature
        # update data structures
        if len(vote) == 0:
            return
        vote = json.loads(vote)
        proposal = vote[0]
        if not proposal in self.votes:
            # instantiate data structures for proposal
            self.votes[proposal] = set()
            self.signatures[proposal] = []
        # vote for every signature
        signatures = vote[1]
        for signature in signatures:
            node_id = signature[0]
            if node_id in self.votes[proposal]:
                # node has already voted; ignore it
                continue
            proposal_sig = signature[1]
            # check signature on vote and add node to set of votes and signature (for later rebroadcast)
            if util.is_message_signed(proposal, proposal_sig, config.PUBLIC_KEYS[node_id]):
                self.votes[proposal].add(node_id)
                self.signatures[proposal].append((node_id, proposal_sig))
                print("[byz-ag] Signed proposal message accepted", proposal, signature)
            else:
                print("[byz-ag] Error: Signed proposal message rejected", proposal, signature)

    def is_done(self):
        """ Returns True once the protocol has completed, and False before. """
        # run for n+1 rounds; tolerate n failures
        return self.curr_round_number > len(config.PEERS) + 1

    def get_output(self):
        """ Returns the final output of agreement once the protocol has completed, and None before then. """
        # Pseudocode: (Output) Each player i outputs 0 if |Si| > 1 and otherwise outputs the unique element in Si.

        # placeholder for (3.3)

        if self.is_done():
            if len(self.s_i) != 1:
                return 0
            else:
                return self.s_i[0]
        else:
            return None
 

    @run_async
    def run_protocol_loop(self):
        """ Runs the protocol loop; tracks rounds and fires appropriate handler. """
        while synchrony.start_time == None:
            time.sleep(.2)
        while not self.is_done():
            print("[byz-ag] following round", self.curr_round_number)
            if self.curr_round_number == synchrony.get_curr_round():
                time.sleep(.2)
                continue
            self.curr_round_number = synchrony.get_curr_round()
            round_votes = self.calculate_votes_for(self.curr_round_number)
            while not synchrony.should_send():
                time.sleep(.2)
                print("[byz-ag] waiting to send votes in round", self.curr_round_number)
            self.broadcast_votes_for(self.curr_round_number, round_votes)

        print("[byz-ag] done!  output", self.get_output())
