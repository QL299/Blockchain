import config
import ZODB, ZODB.FileStorage
import transaction
import importlib
from flask import Flask, render_template, request
from p2p import gossip
import threading

sem = threading.Semaphore()

app = Flask(__name__)

def get_all_blockhashes(chain):
    block_hashes = []
    for height in chain.get_heights_with_blocks():
        for block_hash in chain.get_blockhashes_at_height(height):
            block_hashes.append(block_hash)
    block_hashes.reverse() # show newest block first
    return block_hashes

def get_best_chain_blockhashes(chain):
    return chain.get_chain_ending_with(chain.get_heaviest_chain_tip().hash)

def render_chain(block_hashes_function):
    sem.acquire()
    from blockchain import chaindb
    chaindb.connection.close()
    chaindb.db.close()
    importlib.reload(chaindb)
    chain = chaindb.chain

    block_hashes = block_hashes_function(chain)

    weights=chain.get_all_block_weights()
    output = render_template('chain.html', block_hashes=block_hashes, chain=chain, weights=weights)
    chaindb.connection.close()
    chaindb.db.close()
    sem.release()
    return output

@app.route('/')
def full_chain_view():
    return render_chain(get_all_blockhashes)

@app.route('/best')
def best_chain_view():
    return render_chain(get_best_chain_blockhashes)

# Expose gossip interface in addition to web interface
@app.route('/p2pmessage/<string:type>/<int:reply_port>', methods=['POST'])
def route_message(type, reply_port):
    message = str(request.data.decode("utf8"))
    sender = "http://" + str(request.remote_addr) + ":" + str(reply_port) + "/"
    sem.acquire()
    gossip.handle_message(type, message, sender)
    sem.release()
    return "Yay!"

