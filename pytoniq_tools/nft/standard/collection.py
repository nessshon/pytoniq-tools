from __future__ import annotations

from typing import List, Tuple

from pytoniq_core import Address, Cell, begin_cell, HashMap

from .item import CODE_HEX as ITEM_CODE_HEX
from ..base.collection import Collection
from ..content import OffchainContent, OffchainCommonContent
from ..data import CollectionData
from ..op_codes import *
from ..royalty_params import RoyaltyParams

CODE_HEX = "b5ee9c72410213010001fe000114ff00f4a413f4bcf2c80b0102016204020201200e030025bc82df6a2687d20699fea6a6a182de86a182c40202cd0a050201200706003d45af0047021f005778018c8cb0558cf165004fa0213cb6b12ccccc971fb0080201200908001b3e401d3232c084b281f2fff27420002d007232cffe0a33c5b25c083232c044fd003d0032c0326003ebd10638048adf000e8698180b8d848adf07d201800e98fe99ff6a2687d20699fea6a6a184108349e9ca829405d47141baf8280e8410854658056b84008646582a802e78b127d010a65b509e58fe59f80e78b64c0207d80701b28b9e382f970c892e000f18112e001718119026001f1812f82c207f97840d0c0b002801fa40304144c85005cf1613cb3fccccccc9ed5400a6357003d4308e378040f4966fa5208e2906a4208100fabe93f2c18fde81019321a05325bbf2f402fa00d43022544b30f00623ba9302a402de04926c21e2b3e6303250444313c85005cf1613cb3fccccccc9ed5400603502d33f5313bbf2e1925313ba01fa00d43028103459f0068e1201a44343c85005cf1613cb3fccccccc9ed54925f05e2020120120f0201201110002db4f47da89a1f481a67fa9a9a86028be09e008e003e00b0002fb5dafda89a1f481a67fa9a9a860d883a1a61fa61ff4806100043b8b5d31ed44d0fa40d33fd4d4d43010245f04d0d431d430d071c8cb0701cf16ccc98f34ea10e"  # noqa


class CollectionDataStandard(CollectionData):

    def __init__(
            self,
            owner_address: Address,
            nex_item_index: int,
            content: OffchainContent,
            royalty_params: RoyaltyParams,
    ) -> None:
        super().__init__(
            owner_address=owner_address,
            nex_item_index=nex_item_index,
            content=content,
            royalty_params=royalty_params,
            nft_item_code=ITEM_CODE_HEX,
        )


class CollectionStandard(Collection):

    def __init__(
            self,
            data: CollectionDataStandard,
    ) -> None:
        self._data = data.serialize()
        self._code = Cell.one_from_boc(CODE_HEX)

    @classmethod
    def build_mint_body(
            cls,
            index: int,
            owner_address: Address,
            content: OffchainCommonContent,
            amount: int = 20000000,
            query_id: int = 0,
    ) -> Cell:
        """
        Builds the body of the mint transaction.

        :param index: The index of the item to be minted.
        :param owner_address: The address of the owner.
        :param content: The content of the item to be minted.
        :param amount: The amount of coins in nanoton. Defaults to 20000000.
        :param query_id: The query ID. Defaults to 0.
        :return: The cell representing the body of the mint transaction.
        """
        return (
            begin_cell()
            .store_uint(ITEM_MINT_OPCODE, 32)
            .store_uint(query_id, 64)
            .store_uint(index, 64)
            .store_coins(amount)
            .store_ref(
                begin_cell()
                .store_address(owner_address)
                .store_ref(content.serialize())
                .end_cell()
            )
            .end_cell()
        )

    @classmethod
    def build_batch_mint_body(
            cls,
            data: List[Tuple[OffchainCommonContent, Address]],
            from_index: int,
            amount_per_one: int = 20000000,
    ) -> Cell:
        """
        Builds the body of the batch mint transaction.

        :param data: The list of data for minting. Each tuple contains:
            - OffchainCommonContent: The content of the item to be minted.
            - Address: The address of the owner.
        :param from_index: The starting index for minting.
        :param amount_per_one: The amount of coins in nanoton per item. Defaults to 20000000.
        :return: The cell representing the body of the batch mint transaction.
        """
        items_dict = HashMap(key_size=64)

        for i, (content, owner_address) in enumerate(data, start=0):
            items_dict.set_int_key(
                i + from_index,
                begin_cell()
                .store_coins(amount_per_one)
                .store_ref(
                    begin_cell()
                    .store_address(owner_address)
                    .store_ref(content.serialize())
                    .end_cell()
                )
                .end_cell()
            )

        return (
            begin_cell()
            .store_uint(BATCH_ITEM_MINT_OPCODE, 32)
            .store_uint(0, 64)
            .store_dict(items_dict.serialize())
            .end_cell()
        )
