from __future__ import annotations

from pytoniq_core import Address, Cell, StateInit, begin_cell


class Collection:
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
