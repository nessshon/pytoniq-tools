import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.content import OffchainContent
from pytoniq_tools.nft.editable.collection import CollectionEditable
from pytoniq_tools.nft.royalty_params import RoyaltyParams

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

OWNER_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa

COLLECTION_ADDRESS = Address("EQCulhVWqLmr29muYr-wNM7QvcLiP11E_XzbnMZTPeeU99Fv")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    body = CollectionEditable.build_edit_content_body(
        content=OffchainContent(
            uri="https://cobuild.ams3.digitaloceanspaces.com/community/ton/nft/data/collection.json",
            suffix_uri="ipfs://QmTWEGggE2j4mnX4kMjBLzhV3K5RDxyJTby8ZPb4RjV1Ug/",
        ),
        royalty_params=RoyaltyParams(
            base=1000,
            factor=50,  # 5% royalty
            address=OWNER_ADDRESS,
        )
    )

    await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        body=body,
        amount=int(0.02 * 1e9),
    )

    print(f"Edited collection: {COLLECTION_ADDRESS.to_str()}")


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
