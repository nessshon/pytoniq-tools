from __future__ import annotations

from pytoniq_core import Address, Cell, Slice, TlbScheme, begin_cell

from .content import OffchainContent
from .royalty_params import RoyaltyParams


class CollectionData(TlbScheme):

    def __init__(
            self,
            owner_address: Address,
            next_item_index: int,
            content: OffchainContent,
            royalty_params: RoyaltyParams,
            nft_item_code: str = None,
    ) -> None:
        self.owner_address = owner_address
        self.next_item_index = next_item_index
        self.content = content
        self.nft_item_code = Cell.one_from_boc(nft_item_code)
        self.royalty_params = royalty_params

    def serialize(self, *args) -> Cell:
        return (
            begin_cell()
            .store_address(self.owner_address)
            .store_uint(self.next_item_index, 64)
            .store_ref(self.content.serialize())
            .store_ref(self.nft_item_code)
            .store_ref(self.royalty_params.serialize())
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> CollectionData:
        return cls(
            owner_address=cell_slice.load_address(),
            next_item_index=cell_slice.load_uint(64),
            content=OffchainContent.deserialize(cell_slice.load_ref().begin_parse()),
            nft_item_code=cell_slice.load_ref().begin_parse(),
            royalty_params=RoyaltyParams.deserialize(cell_slice.load_ref().begin_parse()),
        )


class ItemData(TlbScheme):

    def __init__(
            self,
            index: int,
            collection_address: Address,
    ) -> None:
        self.index = index
        self.collection_address = collection_address

    def serialize(self, *args) -> Cell:
        return (
            begin_cell()
            .store_uint(self.index, 64)
            .store_address(self.collection_address)
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ItemData:
        return cls(
            index=cell_slice.load_uint(64),
            collection_address=cell_slice.load_address(),
        )
