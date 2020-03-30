import time
import config
from p2p import gossip

# Start BA protocol with node 1 as sender (feel free to change sender)
gossip.send_message(config.PEERS[config.sender], "ba-start", "")
time.sleep(1) # Make sure this object is available, we assume it is when synchrony is kicked off
# Start a round-based tracker based on our synchrony assumption in the PDF.
gossip.send_message(config.PEERS[config.sender], "synchrony-start", "")
