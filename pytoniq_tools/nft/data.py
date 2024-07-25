from __future__ import annotations

from typing import Optional

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
            nft_item_code: Optional[str] = None,
    ) -> None:
        self.owner_address = owner_address
        self.next_item_index = next_item_index
        self.content = content
        self.nft_item_code = Cell.one_from_boc(nft_item_code)
        self.royalty_params = royalty_params

    def serialize(self) -> Cell:
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
        pass


class ItemData(TlbScheme):

    def __init__(
            self,
            index: int,
            collection_address: Address,
    ) -> None:
        self.index = index
        self.collection_address = collection_address

    def serialize(self) -> Cell:
        return (
            begin_cell()
            .store_uint(self.index, 64)
            .store_address(self.collection_address)
            .end_cell()
        )

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ItemData:
        pass
