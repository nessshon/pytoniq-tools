from __future__ import annotations

from pytoniq_core import Address, Cell, begin_cell

from ..base.item import Item
from ..content import OffchainCommonContent
from ..data import ItemData
from ..op_codes import *

CODE_HEX = "b5ee9c72410212010002e5000114ff00f4a413f4bcf2c80b0102016202030202ce0405020120101102012006070201200e0f04f70c8871c02497c0f83434c0c05c6c2497c0f83e903e900c7e800c5c75c87e800c7e800c3c00816ce38596db088d148cb1c17cb865407e90353e900c040d3c00f801f4c7f4cfe08417f30f45148c2ea3a28c8412040dc409841140b820840bf2c9a8948c2eb8c0a0840701104a948c2ea3a28c8412040dc409841140a008090a0b00113e910c1c2ebcb8536001f65136c705f2e191fa4021f001fa40d20031fa00820afaf0801ca121945315a0a1de22d70b01c300209206a19136e220c2fff2e192218e3e821005138d91c8500acf16500ccf1671244a145446b0708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00105894102b385be20c0080135f03333334347082108b77173504c8cbff58cf164430128040708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0001f65134c705f2e191fa4021f001fa40d20031fa00820afaf0801ca121945315a0a1de22d70b01c300209206a19136e220c2fff2e192218e3e8210511a4463c85008cf16500ccf1671244814544690708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00103894102b365be20d0046e03136373782101a0b9d5116ba9e5131c705f2e19a01d4304400f003e05f06840ff2f00082028e3527f0018210d53276db103845006d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0093303335e25503f0030082028e3527f0018210d53276db103848006d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0093303630e25503f00300413b513434cffe900835d27080271fc07e90353e900c040d440d380c1c165b5b5b600025013232cfd400f3c58073c5b30073c5b27b5520000dbf03a78013628c000bbc7e7f80118400cb5c98"  # noqa


class ItemDataEditable(ItemData):
    ...


class ItemEditable(Item):

    def __init__(
            self,
            data: ItemDataEditable,
    ) -> None:
        self._data = data.serialize()
        self._code = Cell.one_from_boc(CODE_HEX)

    @classmethod
    def build_edit_content_body(
            cls,
            content: OffchainCommonContent,
            query_id: int = 0,
    ) -> Cell:
        """
        Builds the body of the edit item content transaction.

        :param content: The new content to be set.
        :param query_id: The query ID. Defaults to 0.
        :return: The cell representing the body of the edit item content transaction.
        """
        return (
            begin_cell()
            .store_uint(EDIT_ITEM_CONTENT_OPCODE, 32)
            .store_uint(query_id, 64)
            .store_ref(content.serialize())
            .end_cell()
        )

    @classmethod
    def build_change_editorship_body(
            cls,
            editor_address: Address,
            response_address: Address = None,
            custom_payload: Cell = Cell.empty(),
            forward_payload: Cell = Cell.empty(),
            forward_amount: int = 0,
            query_id: int = 0,
    ) -> Cell:
        """
        Builds the body of the change item editorship transaction.

        :param editor_address: The address of the new editor.
        :param response_address: The address to respond to. Defaults to the editor address.
        :param custom_payload: The custom payload. Defaults to an empty cell.
        :param forward_payload: The payload to be forwarded. Defaults to an empty cell.
        :param forward_amount: The amount of coins to be forwarded. Defaults to 0.
        :param query_id: The query ID. Defaults to 0.
        :return: The cell representing the body of the change item editorship transaction.
        """
        return (
            begin_cell()
            .store_uint(CHANGE_ITEM_EDITORSHIP_OPCODE, 32)
            .store_uint(query_id, 64)
            .store_address(editor_address)
            .store_address(response_address or editor_address)
            .store_maybe_ref(custom_payload)
            .store_coins(forward_amount)
            .store_maybe_ref(forward_payload)
            .end_cell()
        )
