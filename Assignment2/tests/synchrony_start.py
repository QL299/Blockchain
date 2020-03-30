import unittest, time
from p2p import synchrony

class SynchronyStartTest(unittest.TestCase):
    logger_ran = False

    def tearDown(self):
        synchrony.start_time = None

    def log_synchrony():
        # mock out call to start logging to capture whether it ran
        SynchronyStartTest.logger_ran = True

    def test_synchrony_start(self):
        # set up mocking
        synchrony.log_synchrony = SynchronyStartTest.log_synchrony

        # make sure start_time is initially none
        self.assertIsNone(synchrony.start_time)
        # make sure ater calling receive_start_message, time is set to right value
        curr_time = time.time()
        synchrony.receive_start_message()
        synchrony.receive_start_message()
        self.assertTrue(curr_time - synchrony.start_time < 1)
        self.assertTrue(SynchronyStartTest.logger_ran)

if __name__ == '__main__':
    unittest.main()


