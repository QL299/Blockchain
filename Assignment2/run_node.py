import os
import sys

if __name__ == '__main__':

    # Validate arguments and show help if failed
    try:
        int(sys.argv[1])
    except:
        print("Usage: python3 run_node.py [node id, 1-6]")
        exit(1)

    node_id = int(sys.argv[1].strip())
    receiving_port = 5000 + node_id
    if node_id != "0":
        import config
        # store node-specific values in config; should probably move these to a node class
        config.DB_PATH = "database" + os.sep + str(node_id) + os.sep + "node.db"
        config.node_id = node_id
        config.receiving_port = receiving_port
        del config.PEERS[node_id]

    from webapp.app import app
    app.run(port=config.receiving_port, debug=True)
