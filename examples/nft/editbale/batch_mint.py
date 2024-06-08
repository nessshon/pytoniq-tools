import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.content import OffchainCommonContent
from pytoniq_tools.nft.editable.collection import CollectionEditable

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

OWNER_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa

EDITOR_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa

COLLECTION_ADDRESS = Address("EQCulhVWqLmr29muYr-wNM7QvcLiP11E_XzbnMZTPeeU99Fv")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

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

    await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        body=body,
        amount=int((items_count * 0.03) * 1e9),
    )

    print(f"Minted {items_count} items in collection: {COLLECTION_ADDRESS.to_str()}")


async def get_provider() -> LiteBalancer:
    if IS_TESTNET:
        provider = LiteBalancer.from_testnet_config(
            trust_level=2,
        )
    else:
        provider = LiteBalancer.from_mainnet_config(
            trust_level=2,
        )

    await provider.start_up()
    return provider


async def get_wallet(provider: LiteBalancer) -> WalletV4R2:
    return await WalletV4R2.from_mnemonic(
        provider=provider,
        mnemonics=MNEMONICS.split(" "),
    )


if __name__ == "__main__":
    asyncio.run(main())
