from blockchain.transaction import Transaction
from blockchain.util import remove_empties
from p2p.interfaces import transaction_output as txout_interface

def string_to_transaction(txstring):
    """ Takes a string as input and deserializes it into a
        transaction object for receipt over network.
        !!! WARNING !!!
        (don't ever do anything like this in production, it's not secure).

        Args:
            txstring (str): String representing a cryptocurrency transaction.

        Returns:
            :obj:`Transaction`: Parsed transaction object representing input,
            False or exception thrown on failure.
    """
    transaction_parts = txstring.split("-")[1:]
    if len(transaction_parts) != 2:
        return False
    input_refs_str = transaction_parts[0]
    input_refs = remove_empties(input_refs_str.split(";"))

    outputs_as_str = remove_empties(transaction_parts[1].split(";"))
    outputs = [txout_interface.string_to_output(output_string) for output_string in outputs_as_str]
    if False in outputs:
        return False

    return Transaction(input_refs, outputs)
