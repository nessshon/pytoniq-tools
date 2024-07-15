from __future__ import annotations

from typing import Optional

from pytoniq_core import Builder, Cell, Slice, TlbScheme, WalletMessage, HashMap, begin_cell


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
        self.public_key = public_key
        self.seqno = seqno
        self.wallet_id = wallet_id

        super().__init__(
            wallet_id=self.wallet_id,
            seqno=self.seqno,
            public_key=self.public_key,
        )

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
        self.public_key = public_key
        self.seqno = seqno
        self.wallet_id = wallet_id
        self.plugins = plugins

        super().__init__(
            wallet_id=self.wallet_id,
            seqno=self.seqno,
            public_key=self.public_key,
            plugins=self.plugins,
        )

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


class HighloadWalletData(WalletData):

    def __init__(
            self,
            public_key: bytes,
            wallet_id: Optional[int] = 698983191,
            last_cleaned: Optional[int] = None,
            old_queries: Optional[dict] = None
    ) -> None:
        self.public_key = public_key
        self.wallet_id = wallet_id
        self.last_cleaned = last_cleaned
        self.old_queries = old_queries

        super().__init__(
            wallet_id=self.wallet_id,
            last_cleaned=self.last_cleaned,
            public_key=self.public_key,
            old_queries=self.old_queries,
        )

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
    def deserialize(cls, cell_slice: Slice) -> HighloadWalletData:
        return cls(
            wallet_id=cell_slice.load_uint(32),
            last_cleaned=cell_slice.load_uint(64),
            public_key=cell_slice.load_bytes(32),
            old_queries=cell_slice.load_dict(
                key_length=64,
                value_deserializer=cls.old_queries_deserializer,
            )
        )
