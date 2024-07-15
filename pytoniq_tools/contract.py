from typing import Optional, Union

from pytoniq_core import (
    Address,
    Cell,
    StateInit,
    CurrencyCollection,
    ExternalMsgInfo,
    InternalMsgInfo,
    MessageAny,
    begin_cell,
)


class Contract:
    CODE_HEX: str

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
    def _create_external_msg(
            cls,
            src: Optional[Address] = None,
            dest: Optional[Address] = None,
            import_fee: int = 0,
            state_init: Optional[StateInit] = None,
            body: Cell = Cell.empty(),
    ) -> MessageAny:
        info = ExternalMsgInfo(src, dest, import_fee)
        return MessageAny(info, state_init, body)

    @classmethod
    def _create_internal_msg(
            cls,
            ihr_disabled: bool = True,
            bounce: bool = None,
            bounced: bool = False,
            src: Address = None,
            dest: Address = None,
            value: Union[CurrencyCollection, int] = 0,
            ihr_fee: int = 0,
            fwd_fee: int = 0,
            created_lt: int = 0,
            created_at: int = 0,
            state_init: Optional[StateInit] = None,
            body: Cell = None,
    ) -> MessageAny:
        if isinstance(value, int):
            value = CurrencyCollection(value)

        if bounce is None:
            bounce = dest.is_bounceable

        info = InternalMsgInfo(
            ihr_disabled,
            bounce,
            bounced,
            src,
            dest,
            value,
            ihr_fee,
            fwd_fee,
            created_lt,
            created_at,
        )

        if body is None:
            body = Cell.empty()

        return MessageAny(info, state_init, body)
