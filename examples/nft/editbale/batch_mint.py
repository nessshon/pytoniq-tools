from pytoniq_core import Address

from pytoniq_tools.client import TonapiClient
from pytoniq_tools.nft import CollectionEditable
from pytoniq_tools.nft.content import OffchainCommonContent
from pytoniq_tools.wallet import WalletV4R2

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []

OWNER_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa
EDITOR_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa
COLLECTION_ADDRESS = Address("EQCulhVWqLmr29muYr-wNM7QvcLiP11E_XzbnMZTPeeU99Fv")  # noqa


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(MNEMONIC, client)

    from_index = 0
    items_count = 100

    body = CollectionEditable.build_batch_mint_body(
        data=[
            (
                OffchainCommonContent(
                    uri=f"{index}.json"
                ),
                OWNER_ADDRESS,  # owner address
                EDITOR_ADDRESS,  # editor address
            ) for index in range(from_index, items_count)
        ],
        from_index=from_index,
    )

    tx_hash = await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        amount=items_count * 0.035,
        body=body,
    )

    print(f"Minted {items_count} items in collection {COLLECTION_ADDRESS.to_str()}")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
