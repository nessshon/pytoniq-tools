import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.content import OffchainContent
from pytoniq_tools.nft.royalty_params import RoyaltyParams
from pytoniq_tools.nft.standard.collection import (
    CollectionStandard,
    CollectionDataStandard,
)

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

OWNER_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    collection = CollectionStandard(
        data=CollectionDataStandard(
            owner_address=OWNER_ADDRESS,
            next_item_index=0,
            content=OffchainContent(
                uri="ipfs://QmYb6XduLLjFXhkbz4ggDHVfPyG6gapYzzLH7tGj9vFprH",
                suffix_uri="ipfs://QmTWEGggE2j4mnX4kMjBLzhV3K5RDxyJTby8ZPb4RjV1Ug/",
            ),
            royalty_params=RoyaltyParams(
                base=1000,
                factor=55,  # 5.5% royalty
                address=OWNER_ADDRESS,
            ),
        )
    )

    await wallet.transfer(
        destination=collection.address,
        state_init=collection.state_init,
        amount=int(0.05 * 1e9),
    )

    print(f"Deployed collection: {collection.address.to_str()}")


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
