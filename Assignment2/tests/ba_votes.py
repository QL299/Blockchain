from byzantine_agreement.simple_ba import SimplePKIBA
import unittest


class BAVotesTest(unittest.TestCase):

    def reset_ba(self, ba):
        ba.s_i = []
        ba.signatures = {}
        ba.votes = {}

    def test_ba_proposals(self):
        SimplePKIBA.run_protocol_loop = lambda x : x # disable protocol loop to prevent hanging thread
        curr_ba = SimplePKIBA(1)
        import config
        config.node_id = 4
        self.assertEqual(curr_ba.calculate_votes_for(0), [])
        self.assertEqual(curr_ba.calculate_votes_for(1000), [])
        self.assertEqual(curr_ba.calculate_votes_for(-1), [])
        # check that relevant data stuctures are still empty
        self.assertEqual(curr_ba.s_i, [])
        self.assertEqual(curr_ba.votes, {})
        self.assertEqual(curr_ba.signatures, {})
        # single proposal, some votes
        self.reset_ba(curr_ba)
        # mock in votes and signatures
        curr_ba.votes = {"hi": set([1,2])}
        curr_ba.signatures = {"hi": [(1, "a"), (2, "b")]}
        self.assertEqual(curr_ba.calculate_votes_for(0), ['hi']) # hi should be added to S_i here (reaches vote threshold)
        # ensure data structures are correctly updated
        self.assertEqual(curr_ba.s_i, ['hi'])
        self.assertEqual(curr_ba.votes['hi'], set([1,2,4]))
        self.assertEqual(set([x[0] for x in curr_ba.signatures['hi']]), set([1,2,4]))
        self.assertEqual(curr_ba.calculate_votes_for(1), [])
        self.assertEqual(curr_ba.calculate_votes_for(2), [])
        self.assertEqual(curr_ba.calculate_votes_for(3), [])
        self.assertEqual(curr_ba.calculate_votes_for(-1), [])
        self.assertEqual(curr_ba.calculate_votes_for(100), [])
        self.assertEqual(curr_ba.s_i, ['hi'])
        self.assertEqual(curr_ba.votes['hi'], set([1,2,4]))
        self.assertEqual(set([x[0] for x in curr_ba.signatures['hi']]), set([1,2,4]))
        # single proposal, no votes
        self.reset_ba(curr_ba)
        curr_ba.votes = {"hi": set([])}
        curr_ba.signatures = {"hi": []}
        self.assertEqual(curr_ba.calculate_votes_for(100), [])
        self.assertEqual(curr_ba.calculate_votes_for(0), [])
        # multi proposal, mixed votes
        self.reset_ba(curr_ba)
        curr_ba.votes = {"hi": set([1,2,3,4]), "a": set([1,2]), "64": set([6])}
        curr_ba.signatures = {"hi": [(1, "a"), (2, "b"), (3, "c"), (4, "d")], "a": [(1, "a"), (2, "b")], "64": [6, "z"]}
        # ensure data structures are correctly updated
        self.assertEqual(set(curr_ba.calculate_votes_for(0)), set(["hi", "a"]))
        self.assertEqual(set(curr_ba.calculate_votes_for(1)), set([]))
        self.assertEqual(curr_ba.calculate_votes_for(3), [])
        self.assertEqual(curr_ba.calculate_votes_for(10), [])

if __name__ == '__main__':
    unittest.main()


