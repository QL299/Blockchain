from byzantine_agreement.simple_ba import SimplePKIBA
import unittest


class BAProposalsTest(unittest.TestCase):

    def test_ba_proposals(self):
        SimplePKIBA.run_protocol_loop = lambda x : x # disable protocol loop to prevent hanging thread
        curr_ba = SimplePKIBA(1)
        import config
        config.node_id = 4
        self.assertEqual(curr_ba.get_proposals_with_threshold(0), [])
        self.assertEqual(curr_ba.get_proposals_with_threshold(1000), [])
        self.assertEqual(curr_ba.get_proposals_with_threshold(-1), [])
        # single proposal, some votes
        curr_ba.votes = {"hi": set([1,2])}
        self.assertEqual(curr_ba.get_proposals_with_threshold(0), ['hi'])
        self.assertEqual(curr_ba.get_proposals_with_threshold(1), ['hi'])
        self.assertEqual(curr_ba.get_proposals_with_threshold(2), ['hi'])
        self.assertEqual(curr_ba.get_proposals_with_threshold(3), [])
        self.assertEqual(curr_ba.get_proposals_with_threshold(-1), ['hi'])
        self.assertEqual(curr_ba.get_proposals_with_threshold(100), [])
        # single proposal, no votes
        curr_ba.votes = {"hi": set([])}
        self.assertEqual(curr_ba.get_proposals_with_threshold(100), [])
        self.assertEqual(curr_ba.get_proposals_with_threshold(0), [])
        # multi proposal, mixed votes
        curr_ba.votes = {"hi": set([1,2,3,4]), "a": set([1,2]), "64": set([6])}
        self.assertEqual(set(curr_ba.get_proposals_with_threshold(0)), set(["hi", "a"]))
        self.assertEqual(set(curr_ba.get_proposals_with_threshold(1)), set(["hi", "a"]))
        self.assertEqual(curr_ba.get_proposals_with_threshold(3), ["hi"])
        self.assertEqual(curr_ba.get_proposals_with_threshold(10), [])

if __name__ == '__main__':
    unittest.main()


