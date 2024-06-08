import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.editable.collection import CollectionEditable

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

OWNER_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa

COLLECTION_ADDRESS = Address("EQCulhVWqLmr29muYr-wNM7QvcLiP11E_XzbnMZTPeeU99Fv")  # noqa

NEW_OWNER_ADDRESS = Address("EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    body = CollectionEditable.build_change_owner_body(
        owner_address=NEW_OWNER_ADDRESS,
    )

    await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        body=body,
        amount=int(0.02 * 1e9),
    )

    print(f"Changed owner of collection: {COLLECTION_ADDRESS.to_str()} to {NEW_OWNER_ADDRESS.to_str()}")


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
