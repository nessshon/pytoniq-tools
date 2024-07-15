from __future__ import annotations

import time
from typing import Optional, List, Tuple, Union

from pytoniq_core import Address, Cell, StateInit, WalletMessage, begin_cell, MessageAny, ExternalMsgInfo
from pytoniq_core.crypto.keys import mnemonic_new, mnemonic_to_private_key
from pytoniq_core.crypto.signature import sign_message

from .data import WalletV3Data, WalletV4Data
from ..contract import Contract


class Wallet(Contract):
    CODE_HEX: str

    def __init__(
            self,
            public_key: bytes,
            private_key: bytes,
            seqno: Optional[int] = 0,
            wallet_id: Optional[int] = 698983191,
    ) -> None:
        self._data = self.create_data(public_key, seqno, wallet_id).serialize()
        self._code = Cell.one_from_boc(self.CODE_HEX)

        self.public_key = public_key
        self.private_key = private_key

    @classmethod
    def create_data(
            cls,
            public_key: bytes,
            seqno: int,
            wallet_id: int,
    ) -> WalletV3Data | WalletV4Data:
        raise NotImplementedError

    @classmethod
    def from_mnemonics(cls, mnemonics: List[str]) -> Tuple[List[str], bytes, bytes, Wallet]:
        public_key, private_key = mnemonic_to_private_key(mnemonics)
        return mnemonics, public_key, private_key, cls(public_key, private_key)

    @classmethod
    def create(cls) -> Tuple[List[str], bytes, bytes, Wallet]:
        mnemonics = mnemonic_new(24)
        return cls.from_mnemonics(mnemonics)

    def create_deploy_msg(self) -> MessageAny:
        body = self.raw_create_transfer_msg(
            private_key=self.private_key,
            seqno=0,
            messages=[],
        )

        return self.create_external_msg(
            dest=self.address.to_str(),
            state_init=self.state_init,
            body=body,
        )

    @classmethod
    def create_external_msg(
            cls,
            src: Optional[Address] = None,
            dest: Optional[Address] = None,
            import_fee: int = 0,
            state_init: Optional[StateInit] = None,
            body: Cell = None,
    ) -> MessageAny:
        info = ExternalMsgInfo(src, dest, import_fee)

        if body is None:
            body = Cell.empty()
        message = MessageAny(info=info, init=state_init, body=body)

        return message

    @classmethod
    def raw_create_transfer_msg(
            cls,
            private_key: bytes,
            messages: List[WalletMessage],
            seqno: int = 0,
            wallet_id: int = 698983191,
            valid_until: Optional[int] = None,
            op_code: Optional[int] = None,
    ) -> Cell:
        signing_message = begin_cell().store_uint(wallet_id, 32)

        if seqno == 0:
            signing_message.store_bits('1' * 32)
        else:
            if valid_until is not None:
                signing_message.store_uint(valid_until, 32)
            else:
                signing_message.store_uint(int(time.time()) + 60, 32)

        signing_message.store_uint(seqno, 32)

        if op_code:
            signing_message.store_uint(op_code, 8)

        for m in messages:
            signing_message.store_cell(m.serialize())

        signing_message = signing_message.end_cell()
        signature = sign_message(signing_message.hash, private_key)

        return (
            begin_cell()
            .store_bytes(signature)
            .store_cell(signing_message)
            .end_cell()
        )

    @classmethod
    def create_wallet_internal_message(
            cls,
            destination: Address,
            send_mode: int = 3,
            value: int = 0,
            body: Union[Cell, str] = None,
            state_init: Optional[StateInit] = None,
            **kwargs,
    ) -> WalletMessage:
        if isinstance(body, str):
            body = (
                begin_cell()
                .store_uint(0, 32)
                .store_snake_string(body)
                .end_cell()
            )

        message = cls.create_internal_msg(
            dest=destination,
            value=value,
            body=body,
            state_init=state_init,
            **kwargs,
        )

        return WalletMessage(
            send_mode=send_mode,
            message=message,
        )
