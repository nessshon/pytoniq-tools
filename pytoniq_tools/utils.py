from typing import Tuple

from pytoniq_core import MessageAny


def message_to_boc_hex(message: MessageAny) -> Tuple[str, str]:
    """
    Serialize a message to its Bag of Cells (BoC) representation and return its hexadecimal strings.

    :param message: The message to be serialized.
    :return: A tuple containing the BoC hexadecimal string and the hash hexadecimal string of the message.
    """
    message_cell = message.serialize()
    message_boc = message_cell.to_boc()

    return message_boc.hex(), message_cell.hash.hex()
