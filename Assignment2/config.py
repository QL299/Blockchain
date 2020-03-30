# Default database path; can be changed
DB_PATH = "database/blockchain.db"

# don't change these; for PoA
# (encoded as hex)
AUTHORITY_SK = "404a28d57118d33f7c59146f512b725b5f1336843ba1c8fe"
AUTHORITY_PK = "356c54fc3e57666eef27547ecf0257f8a27540ff7c145a2bcd8921d6e536f0208cbf98e220048d1e17e69dd587049e72"

# full peer list; MUST include the trailing slash!
# used in gossip, BA, consensus, etc.
PEERS = {
    1: "http://127.0.0.1:5001/",
    2: "http://127.0.0.1:5002/",
    3: "http://127.0.0.1:5003/",
    4: "http://127.0.0.1:5004/",
    5: "http://127.0.0.1:5005/",
    6: "http://127.0.0.1:5006/",
}

# set up PKI for BA protocol
PUBLIC_KEYS = {
    1: "ee99ad3a26ceb4055481b4e98ddcc8fba24085e04ef4e23bdbcb9500b8a0f1f7c615e5c2dfde2aa3a51061844eaaaa37",
    2: "07ab356930dd8f5df2f65c269ff3207ff87dbd36129935ad78ac2ee543823cfd48641e4f7069b932c2385dfc718d90ae",
    3: "4fc525572f28d088a08451f3c7aefd852d34833636e611ff83a564724c2def19c57e7171a9fde3444df393f1dc5936b0",
    4: "2c80afa0f8654b507ae1543fb7f09327aaade6c4f6fb5e129e243eb84fff3e292441fec4338b540486329599ef270639",
    5: "c8c5c70be2d6221ce287900b22b0f81dfb6fc50220123c3e5016b30d8f89e0ba394fff80459725e9849549d83d7c224c",
    6: "bb483e0465577f17b25a9ae5e9290a85d70f92e2070e0b0190e9ce85eaddd9c4c27aaa69579aa6bd2b87a81895bbb6db",
}
SECRET_KEYS = {
    1: "c58d53fb7d13648ebdfeca9d476de64f493404a3d9b1acf7",
    2: "3c256701fdc11fa6d2424fd3db8c8455ec0c2531c39274f1",
    3: "29e993bd987eace11b617d736e4a050c83a64bf0779ee9c8",
    4: "062b38eb401a68da000793a41938144044dcb24073164e18",
    5: "d9b3f048ee496cd9ec605bb79a8122e5bc1001196487ccc8",
    6: "6b522b3e707f4c6608a54187a87ad1966d85dd6415dba8fe",
}

# if a node is in this list, it will run the byzantine version of the software
BYZANTINE_NODES = []
#BYZANTINE_NODES = [3,6] # eg uncomment this to run Byzantine behavior on nodes 3,6

# default values if running without an explicit node ID
node_id = 0
receiving_port = 5000
ba = None # placeholder for future Byzantine agreement protocol object (should likely move this)

sender = 1 # default sender
