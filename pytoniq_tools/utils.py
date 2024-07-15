from typing import Tuple

from pytoniq_core import MessageAny


def message_to_boc_hex(message: MessageAny) -> Tuple[str, str]:
    message_cell = message.serialize()
    message_boc = message_cell.to_boc()

    return message_boc.hex(), message_cell.hash.hex()
