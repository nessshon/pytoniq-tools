from __future__ import annotations

import time
from typing import Optional, List, Union, Tuple

from pytonapi.utils import amount_to_nano
from pytoniq_core import Address, Cell, StateInit, MessageAny, WalletMessage, begin_cell
from pytoniq_core.crypto.keys import mnemonic_new, mnemonic_to_private_key
from pytoniq_core.crypto.signature import sign_message

from .data import WalletV3Data, WalletV4Data
from ..client import Client, LiteClient, TonapiClient, ToncenterClient
from ..contract import Contract
from ..exceptions import UnknownClientError
from ..utils import message_to_boc_hex


class Wallet(Contract):

    def __init__(
            self,
            client: Client,
            public_key: bytes,
            private_key: bytes,
            seqno: Optional[int] = 0,
            wallet_id: Optional[int] = 698983191,
    ) -> None:
        self.client = client
        self.public_key = public_key
        self.private_key = private_key

        self._data = self._create_data(public_key, seqno, wallet_id).serialize()
        self._code = Cell.one_from_boc(self.CODE_HEX)

    @classmethod
    def _create_data(
            cls,
            public_key: bytes,
            seqno: int,
            wallet_id: int,
    ) -> WalletV3Data | WalletV4Data:
        raise NotImplementedError

    async def _create_deploy_msg(self) -> MessageAny:
        body = self._raw_create_transfer_msg(
            private_key=self.private_key,
            seqno=0,
            messages=[],
        )

        return self._create_external_msg(
            dest=self.address,
            state_init=self.state_init,
            body=body,
        )

    @classmethod
    def _raw_create_transfer_msg(
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

        if op_code is not None:
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
    def _create_wallet_internal_message(
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

        message = cls._create_internal_msg(
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

    @classmethod
    def from_mnemonic(
            cls,
            mnemonic: List[str],
            client: Optional[Client] = None,
    ) -> Tuple[Wallet, bytes, bytes, List[str]]:
        public_key, private_key = mnemonic_to_private_key(mnemonic)
        return cls(client, public_key, private_key), public_key, private_key, mnemonic

    @classmethod
    def create(cls) -> Tuple[Wallet, bytes, bytes, List[str]]:
        mnemonic = mnemonic_new(24)
        return cls.from_mnemonic(mnemonic)

    async def deploy(self) -> str:
        message = await self._create_deploy_msg()
        message_boc_hex, message_hash = message_to_boc_hex(message)
        await self.client.send_message(message_boc_hex)

        return message_hash

    async def get_seqno(self) -> int:
        method_result = await self.client.run_get_method(
            address=self.address.to_str(),
            method_name="seqno",
        )

        if isinstance(self.client, TonapiClient):
            seqno = int(method_result.decoded.get("state", 0))
        elif isinstance(self.client, ToncenterClient):
            seqno = int(method_result.stack[0].value, 16)
        elif isinstance(self.client, LiteClient):
            seqno = int(method_result[0])
        else:
            raise UnknownClientError(self.client.__class__.__name__)

        return seqno

    async def raw_transfer(
            self,
            messages: Optional[List[WalletMessage]] = None,
    ) -> str:
        assert len(messages) <= 4, 'For common wallet maximum messages amount is 4'
        seqno = await self.get_seqno()

        body = self._raw_create_transfer_msg(
            private_key=self.private_key,
            seqno=seqno,
            messages=messages or [],
        )

        message = self._create_external_msg(dest=self.address, body=body)
        message_boc_hex, message_hash = message_to_boc_hex(message)
        await self.client.send_message(message_boc_hex)

        return message_hash

    async def transfer(
            self,
            destination: Union[Address, str],
            amount: Union[int, float] = 0,
            body: Optional[Cell, str] = Cell.empty(),
            state_init: Optional[StateInit] = None,
    ) -> str:
        if isinstance(destination, str):
            destination = Address(destination)

        message_hash = await self.raw_transfer(
            messages=[
                self._create_wallet_internal_message(
                    destination=destination,
                    value=amount_to_nano(amount),
                    body=body,
                    state_init=state_init,
                ),
            ],
        )

        return message_hash
