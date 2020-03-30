import unittest
from p2p import gossip

class GossipTest(unittest.TestCase):

    messages_sent = set()

    def send_message(to, type, message):
        GossipTest.messages_sent.add((to, type, message))

    def test_gossip(self):
        # test that universal gossip works with all nodes
        gossip.send_message = GossipTest.send_message
        gossip.gossip_message("whee", "test")
        expected_output = set([('http://127.0.0.1:5001/', 'whee', 'test'), ('http://127.0.0.1:5006/', 'whee', 'test'), ('http://127.0.0.1:5002/', 'whee', 'test'), ('http://127.0.0.1:5003/', 'whee', 'test'), ('http://127.0.0.1:5004/', 'whee', 'test'), ('http://127.0.0.1:5005/', 'whee', 'test')])
        self.assertEqual(GossipTest.messages_sent, expected_output)
        GossipTest.messages_sent = set()
        # make sure nodes don't gossip to own ID
        gossip.config.node_id = 1
        gossip.gossip_message("whee", "test")
        expected_output = set([('http://127.0.0.1:5006/', 'whee', 'test'), ('http://127.0.0.1:5002/', 'whee', 'test'), ('http://127.0.0.1:5003/', 'whee', 'test'), ('http://127.0.0.1:5004/', 'whee', 'test'), ('http://127.0.0.1:5005/', 'whee', 'test')])
        self.assertEqual(GossipTest.messages_sent, expected_output)
        GossipTest.messages_sent = set()
        gossip.config.node_id = 6
        gossip.gossip_message("whee", "test")
        expected_output = set([('http://127.0.0.1:5001/', 'whee', 'test'), ('http://127.0.0.1:5002/', 'whee', 'test'), ('http://127.0.0.1:5003/', 'whee', 'test'), ('http://127.0.0.1:5004/', 'whee', 'test'), ('http://127.0.0.1:5005/', 'whee', 'test')])
        self.assertEqual(GossipTest.messages_sent, expected_output)

if __name__ == '__main__':
    unittest.main()


