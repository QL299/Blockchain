from byzantine_agreement.simple_ba import SimplePKIBA
import unittest


class BAOutputTest(unittest.TestCase):

    def test_ba_output(self):
        SimplePKIBA.run_protocol_loop = lambda x : x # disable protocol loop to prevent hanging thread
        curr_ba = SimplePKIBA(1)

        # Check that if done is False, no output is returned regardless of s_i
        # (no matter what, this should be None)
        curr_ba.is_done = lambda : False
        curr_ba.s_i = [1]
        self.assertEqual(curr_ba.get_output(), None)
        curr_ba.s_i = []
        self.assertEqual(curr_ba.get_output(), None)
        curr_ba.s_i = [1,2]
        self.assertEqual(curr_ba.get_output(), None)

        # Check that if done is True, correct output is returned regardless of s_i
        curr_ba.is_done = lambda : True
        curr_ba.s_i = [1]
        self.assertEqual(curr_ba.get_output(), 1)
        curr_ba.s_i = []
        self.assertEqual(curr_ba.get_output(), 0) # no elements in s_i; output 0
        curr_ba.s_i = [1,2]
        self.assertEqual(curr_ba.get_output(), 0) # multiple elements in s_i (Byzantine sender); output 0

if __name__ == '__main__':
    unittest.main()


