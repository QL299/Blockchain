from blockchain.pow_block import PoWBlock
from p2p.interfaces import transaction as tx_interface
from blockchain.util import remove_empties

def string_to_block(blockstring, blockclass=PoWBlock):
    """ Takes a string as input and deserializes it into a
        block object for receipt over network.
        !!! WARNING !!!
        (don't ever do anything like this in production, it's not secure).

        Args:
            blockstring (str): String representing the input block.
            blockclass (:obj:`Block`, optional): Class to use to parse the block.
            Default is PoW block.

        Returns:
            Block object of type blockclass, False or exception thrown on failure.
    """

    parsed_blockstring = blockstring.split('`')
    if not (len(parsed_blockstring) == 8):
        return False
    block = False
    try:
        height = int(parsed_blockstring[0])
        timestamp = float(parsed_blockstring[1])
        target = int(parsed_blockstring[2])
        parent_hash = parsed_blockstring[3]
        is_genesis = parsed_blockstring[4] == "True"
        merkle = parsed_blockstring[5]
        seal_data = parsed_blockstring[6]

        # parse transactions using tx interface
        transaction_strings = remove_empties(parsed_blockstring[7].split("!"))
        transactions = [tx_interface.string_to_transaction(tx_string) for tx_string in transaction_strings]
        if False in transactions:
            return False

        block = blockclass(height, transactions, parent_hash, is_genesis=is_genesis, timestamp=timestamp,
            target=target, merkle=merkle, seal_data=seal_data)
    except:
        block = False
    print("[p2p] Blockhash imported", block.hash)
    return block
