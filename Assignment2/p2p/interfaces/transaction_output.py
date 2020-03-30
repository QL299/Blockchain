from blockchain.transaction import TransactionOutput

def string_to_output(outputstring):
    """ Takes a string as input and deserializes it into a
        transaction object for receipt over network.
        !!! WARNING !!!
        (don't ever do anything like this in production, it's not secure).

        Args:
            outputstring (str): Transaction output represented as a string.

        Returns:
            :obj:`TransactionOutput`: Parsed transaction output,
            False or exception thrown on failure.
    """

    output_parts = outputstring.split("~")
    if len(output_parts) != 3:
        return False

    return TransactionOutput(output_parts[0], output_parts[1], int(output_parts[2]))
