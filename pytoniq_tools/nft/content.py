from __future__ import annotations

from pytoniq_core import Cell, Slice, TlbScheme, begin_cell


class OffchainBaseContent(TlbScheme):

    def __init__(self, uri: str) -> None:
        self.uri = uri

    def serialize(self, *args) -> Cell:
        return (
            begin_cell()
            .store_uint(0x01, 8)
            .store_snake_string(self.uri)
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> OffchainBaseContent:
        return cls(uri=cell_slice.load_snake_string())


class OffchainCommonContent(TlbScheme):

    def __init__(self, uri: str) -> None:
        self.uri = uri

    def serialize(self, *args) -> Cell:
        return (
            begin_cell()
            .store_snake_string(self.uri)
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> OffchainCommonContent:
        return cls(uri=cell_slice.load_snake_string())


class OffchainContent(TlbScheme):

    def __init__(self, uri: str, suffix_uri: str) -> None:
        self.uri = uri
        self.suffix_uri = suffix_uri

    def serialize(self, *args) -> Cell:
        return (
            begin_cell()
            .store_ref(OffchainBaseContent(self.uri).serialize())
            .store_ref(OffchainCommonContent(self.suffix_uri).serialize())
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> OffchainContent:
        return cls(
            uri=OffchainBaseContent.deserialize(cell_slice.load_ref().begin_parse()).uri,
            suffix_uri=OffchainCommonContent.deserialize(cell_slice.load_ref().begin_parse()).uri,
        )
