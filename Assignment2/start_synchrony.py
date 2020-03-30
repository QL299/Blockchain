import config
from p2p import gossip

# Start a round-based tracker based on our synchrony assumption in the PDF.
gossip.send_message(config.PEERS[1], "synchrony-start", "")
