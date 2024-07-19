from __future__ import annotations

from typing import List, Optional, Tuple, Union

from pytonapi.utils import amount_to_nano
from pytoniq.contract.utils import generate_query_id
from pytoniq_core import WalletMessage, Cell, begin_cell, HashMap, MessageAny
from pytoniq_core.crypto.signature import sign_message

from ...client import Client
from ...jetton import Jetton
from ...nft import ItemStandard
from ...utils import message_to_boc_hex
from ...wallet import Wallet
from ...wallet.data import HighloadWalletV2Data, TransferData, TransferItemData, TransferJettonData


class HighloadWalletV2(Wallet):
    CODE_HEX = "b5ee9c720101090100e5000114ff00f4a413f4bcf2c80b010201200203020148040501eaf28308d71820d31fd33ff823aa1f5320b9f263ed44d0d31fd33fd3fff404d153608040f40e6fa131f2605173baf2a207f901541087f910f2a302f404d1f8007f8e16218010f4786fa5209802d307d43001fb009132e201b3e65b8325a1c840348040f4438ae63101c8cb1f13cb3fcbfff400c9ed54080004d03002012006070017bd9ce76a26869af98eb85ffc0041be5f976a268698f98e99fe9ff98fa0268a91040207a0737d098c92dbfc95dd1f140034208040f4966fa56c122094305303b9de2093333601926c21e2b3"  # noqa

    def __init__(
            self,
            client: Client,
            public_key: bytes,
            private_key: bytes,
            seqno: Optional[int] = 0,
            wallet_id: Optional[int] = 698983191,
    ) -> None:
        super().__init__(
            client=client,
            public_key=public_key,
            private_key=private_key,
            seqno=seqno,
            wallet_id=wallet_id,
        )
        self._data = self._create_data(public_key).serialize()
        self._code = Cell.one_from_boc(self.CODE_HEX)

    @classmethod
    def create(cls) -> Tuple[HighloadWalletV2, bytes, bytes, List[str]]:
        return super().create()  # type: ignore

    @classmethod
    def from_mnemonic(
            cls,
            mnemonic: Union[List[str], str],
            client: Optional[Client] = None,
    ) -> Tuple[HighloadWalletV2, bytes, bytes, List[str]]:
        return super().from_mnemonic(mnemonic, client)  # type: ignore

    @classmethod
    def _create_data(
            cls,
            public_key: bytes,
            wallet_id: Optional[int] = 698983191,
            last_cleaned: Optional[int] = 0,
            old_queries: Optional[dict] = None,
    ) -> HighloadWalletV2Data:
        return HighloadWalletV2Data(
            public_key=public_key,
            wallet_id=wallet_id,
            last_cleaned=last_cleaned,
            old_queries=old_queries,
        )

    async def _create_deploy_msg(self) -> MessageAny:
        body = self._raw_create_transfer_msg(
            private_key=self.private_key,
            messages=[],
        )

        return self._create_external_msg(
            dest=self.address,
            state_init=self.state_init,
            body=body,
        )

    @classmethod
    def _raw_create_transfer_msg(  # noqa
            cls,
            private_key: bytes,
            messages: List[WalletMessage],
            wallet_id: int = 698983191,
            query_id: int = 0,
            offset: int = 7200,
    ) -> Cell:
        signing_message = begin_cell().store_uint(wallet_id, 32)

        if not query_id:
            signing_message.store_uint(generate_query_id(offset), 64)
        else:
            signing_message.store_uint(query_id, 64)

        def value_serializer(src, dest):
            dest.store_cell(src.serialize())

        messages_dict = HashMap(key_size=16, value_serializer=value_serializer)

        for i in range(len(messages)):
            messages_dict.set_int_key(i, messages[i])

        signing_message.store_dict(messages_dict.serialize())

        signing_message = signing_message.end_cell()
        signature = sign_message(signing_message.hash, private_key)

        return (
            begin_cell()
            .store_bytes(signature)
            .store_cell(signing_message)
            .end_cell()
        )

    async def raw_transfer(
            self,
            messages: Optional[List[WalletMessage]] = None,
    ) -> str:
        assert len(messages) <= 254, 'for highload wallet maximum messages amount is 254'
        body = self._raw_create_transfer_msg(
            private_key=self.private_key,
            messages=messages or [],
        )

        message = self._create_external_msg(dest=self.address, body=body)
        message_boc_hex, message_hash = message_to_boc_hex(message)
        await self.client.send_message(message_boc_hex)

        return message_hash

    async def transfer(self, data_list: List[TransferData]) -> str:  # noqa
        messages = [
            self.create_wallet_internal_message(
                destination=data.destination,
                value=amount_to_nano(data.amount),
                body=data.body,
                state_init=data.state_init,
                **data.other,
            ) for data in data_list
        ]

        message_hash = await self.raw_transfer(messages=messages)

        return message_hash

    async def transfer_nft(self, data_list: List[TransferItemData]) -> str:  # noqa
        messages = [
            self.create_wallet_internal_message(
                destination=data.item_address,
                value=amount_to_nano(data.amount),
                body=ItemStandard.build_transfer_body(
                    new_owner_address=data.destination,
                ),
            ) for data in data_list
        ]

        message_hash = await self.raw_transfer(messages=messages)

        return message_hash

    async def transfer_jetton(self, data_list: List[TransferJettonData]) -> str:  # noqa
        messages = []
        jetton_master_address = None
        jetton_wallet_address = None

        for data in data_list:
            if jetton_master_address is None or jetton_master_address != data.jetton_master_address:
                jetton_wallet_address = await Jetton(self.client).get_jetton_wallet_address(
                    jetton_master_address=data.jetton_master_address.to_str(),
                    owner_address=self.address.to_str(),
                )
                jetton_master_address = data.jetton_master_address
                jetton_wallet_address = jetton_wallet_address

            messages.append(
                self.create_wallet_internal_message(
                    destination=jetton_wallet_address,
                    value=amount_to_nano(data.amount),
                    body=Jetton.build_transfer_body(
                        recipient_address=data.destination,
                        response_address=self.address,
                        jetton_amount=amount_to_nano(data.jetton_amount),
                        forward_payload=data.forward_payload,
                        forward_amount=1,
                    ),
                )
            )

        message_hash = await self.raw_transfer(messages=messages)

        return message_hash
