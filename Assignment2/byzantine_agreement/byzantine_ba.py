import config
from byzantine_agreement.simple_ba import SimplePKIBA

class ByzantineSimplePKIBA(SimplePKIBA):

    def calculate_votes_for(self, round):
        """ Evil/Byzantine voting function that will sign using an invalid signature for our node.
            Only one example of many possible types of Byzantine behavior.
        """

        print("[byz-ag] Byzantine node ID", config.node_id, "voting in", round)
        votes = super().calculate_votes_for(round)
        for proposal in self.signatures:
            for signature_index in range(len(self.signatures[proposal])):
                signature = self.signatures[proposal][signature_index]
                if signature[0] == config.node_id:
                    # change the last bit of any signature we've produced to 'f'
                    altered_signature = (signature[0], signature[1][:-1] + 'f') 
                    # (this is wrong with probability 1/16 and is Byzantine behavior)
                    self.signatures[proposal][signature_index] = altered_signature

        return votes
