from typing import Optional, Union

from pytoniq_core import StateInit, Cell, Address, begin_cell, MessageAny, ExternalMsgInfo, CurrencyCollection, \
    InternalMsgInfo


class Contract:
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
    def create_external_msg(
            cls,
            src: Optional[str] = None,
            dest: Optional[str] = None,
            import_fee: int = 0,
            state_init: Optional[StateInit] = None,
            body: Cell = None,
    ) -> MessageAny:
        info = ExternalMsgInfo(
            src=Address(src) if src else None,
            dest=Address(dest) if dest else None,
            import_fee=import_fee,
        )

        if body is None:
            body = Cell.empty()

        message = MessageAny(
            info=info,
            init=state_init,
            body=body,
        )
        return message

    @classmethod
    def create_internal_msg(
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
            value = CurrencyCollection(
                grams=value,
                other=None,
            )

        if bounce is None:
            bounce = dest.is_bounceable

        info = InternalMsgInfo(
            ihr_disabled=ihr_disabled,
            bounce=bounce,
            bounced=bounced,
            src=src,
            dest=dest,
            value=value,
            ihr_fee=ihr_fee,
            fwd_fee=fwd_fee,
            created_lt=created_lt,
            created_at=created_at,
        )

        if body is None:
            body = Cell.empty()

        message = MessageAny(
            info=info,
            init=state_init,
            body=body,
        )

        return message
