from __future__ import annotations

from typing import Optional, Union

from pytoniq_core import Builder, Cell, Slice, TlbScheme, WalletMessage, HashMap, begin_cell, Address, StateInit


class TransferData:

    def __init__(
            self,
            destination: Union[Address, str],
            amount: Union[int, float],
            body: Optional[Union[Cell, str]] = Cell.empty(),
            state_init: Optional[StateInit] = None,
            **kwargs,
    ) -> None:
        if isinstance(destination, str):
            destination = Address(destination)

        self.destination = destination
        self.amount = amount
        self.body = body
        self.state_init = state_init
        self.other = kwargs


class TransferItemData:

    def __init__(
            self,
            destination: Union[Address, str],
            item_address: Union[Address, str],
            amount: Union[int, float] = 0.05,
    ) -> None:
        if isinstance(destination, str):
            destination = Address(destination)

        if isinstance(item_address, str):
            item_address = Address(item_address)

        self.destination = destination
        self.item_address = item_address
        self.amount = amount


class TransferJettonData:

    def __init__(
            self,
            destination: Union[Address, str],
            jetton_master_address: Union[Address, str],
            jetton_amount: Union[int, float],
            comment: Optional[str] = None,
            amount: Union[int, float] = 0.05,
    ) -> None:
        if isinstance(destination, str):
            destination = Address(destination)

        if isinstance(jetton_master_address, str):
            jetton_master_address = Address(jetton_master_address)

        if comment is not None:
            forward_payload = (
                begin_cell()
                .store_uint(0, 32)
                .store_snake_string(comment)
                .end_cell()
            )
        else:
            forward_payload = Cell.empty()

        self.destination = destination
        self.jetton_master_address = jetton_master_address
        self.jetton_amount = jetton_amount
        self.amount = amount
        self.forward_payload = forward_payload


class WalletData(TlbScheme):

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def serialize(self) -> Cell:
        raise NotImplementedError

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> WalletData:
        raise NotImplementedError


class WalletV3Data(WalletData):

    def __init__(
            self,
            public_key: bytes,
            seqno: Optional[int] = 0,
            wallet_id: Optional[int] = 698983191
    ) -> None:
        super().__init__(
            wallet_id=wallet_id,
            seqno=seqno,
            public_key=public_key,
        )

        self.public_key = public_key
        self.seqno = seqno
        self.wallet_id = wallet_id

    def serialize(self) -> Cell:
        return (
            Builder()
            .store_uint(self.seqno, 32)
            .store_uint(self.wallet_id, 32)
            .store_bytes(self.public_key)
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> WalletV3Data:
        return cls(
            seqno=cell_slice.load_uint(32),
            wallet_id=cell_slice.load_uint(32),
            public_key=cell_slice.load_bytes(32),
        )


class WalletV4Data(WalletData):

    def __init__(
            self,
            public_key: bytes,
            seqno: Optional[int] = 0,
            wallet_id: Optional[int] = 698983191,
            plugins: Optional[Cell] = None,
    ) -> None:
        super().__init__(
            wallet_id=wallet_id,
            seqno=seqno,
            public_key=public_key,
            plugins=plugins,
        )

        self.public_key = public_key
        self.seqno = seqno
        self.wallet_id = wallet_id
        self.plugins = plugins

    def serialize(self) -> Cell:
        return (
            Builder()
            .store_uint(self.seqno, 32)
            .store_uint(self.wallet_id, 32)
            .store_bytes(self.public_key)
            .store_dict(self.plugins)
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> WalletV4Data:
        return cls(
            seqno=cell_slice.load_uint(32),
            wallet_id=cell_slice.load_uint(32),
            public_key=cell_slice.load_bytes(32),
            plugins=cell_slice.load_maybe_ref(),
        )


class HighloadWalletV2Data(WalletData):

    def __init__(
            self,
            public_key: bytes,
            wallet_id: Optional[int] = 698983191,
            last_cleaned: Optional[int] = None,
            old_queries: Optional[dict] = None,
    ) -> None:
        super().__init__(
            wallet_id=wallet_id,
            last_cleaned=last_cleaned,
            public_key=public_key,
            old_queries=old_queries,
        )

        self.public_key = public_key
        self.wallet_id = wallet_id
        self.last_cleaned = last_cleaned
        self.old_queries = old_queries

    @classmethod
    def old_queries_serializer(cls, src: WalletMessage, dest: Builder) -> None:
        dest.store_cell(src.serialize())

    @classmethod
    def old_queries_deserializer(cls, src: Slice) -> WalletMessage:
        return WalletMessage.deserialize(src)

    def serialize(self) -> Cell:
        return (
            begin_cell()
            .store_uint(self.wallet_id, 32)
            .store_uint(self.last_cleaned, 64)
            .store_bytes(self.public_key)
            .store_dict(
                HashMap(
                    key_size=64,
                    value_serializer=self.old_queries_serializer,
                ).serialize(),
            )
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> HighloadWalletV2Data:
        return cls(
            wallet_id=cell_slice.load_uint(32),
            last_cleaned=cell_slice.load_uint(64),
            public_key=cell_slice.load_bytes(32),
            old_queries=cell_slice.load_dict(
                key_length=64,
                value_deserializer=cls.old_queries_deserializer,
            )
        )
