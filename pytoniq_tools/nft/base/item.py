from __future__ import annotations

from pytoniq_core import Address, Cell, StateInit, begin_cell

from ..op_codes import *


class Item:
    _code: Cell
    _data: Cell

    @property
    def code(self) -> Cell:
        return self.state_init.code

    @property
    def data(self) -> Cell:
        return self.state_init.data

    @property
    def address(self) -> Address:
        return Address((0, self.state_init.serialize().hash))

    @property
    def state_init(self) -> StateInit:
        return StateInit.deserialize(
            begin_cell()
            .store_uint(0, 2)
            .store_dict(self._code)
            .store_dict(self._data)
            .store_uint(0, 1)
            .end_cell()
            .to_slice()
        )

    @classmethod
    def build_transfer_body(
            cls,
            new_owner_address: Address,
            response_address: Address = None,
            custom_payload: Cell = Cell.empty(),
            forward_payload: Cell = Cell.empty(),
            forward_amount: int = 0,
            query_id: int = 0,
    ) -> Cell:
        return (
            begin_cell()
            .store_uint(TRANSFER_ITEM_OPCODE, 32)
            .store_uint(query_id, 64)
            .store_address(new_owner_address)
            .store_address(response_address or new_owner_address)
            .store_maybe_ref(custom_payload)
            .store_coins(forward_amount)
            .store_maybe_ref(forward_payload)
            .end_cell()
        )
