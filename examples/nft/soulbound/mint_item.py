import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.content import OffchainCommonContent
from pytoniq_tools.nft.soulbound.collection import CollectionSoulbound
from pytoniq_tools.nft.soulbound.item import ItemSoulbound, ItemDataSoulbound

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

OWNER_ADDRESS = Address("EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess")  # noqa

COLLECTION_ADDRESS = Address("EQC5FNhcIyExh-fmu6EZSpd4L63M6B3JuMgeVhPnlZDNBhD_")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    index = 100
    body = CollectionSoulbound.build_mint_body(
        index=index,
        owner_address=OWNER_ADDRESS,
        content=OffchainCommonContent(
            uri=f"{index}.json"
        ),
    )

    await wallet.transfer(
        destination=COLLECTION_ADDRESS,
        body=body,
        amount=int(0.02 * 1e9),
    )

    item = ItemSoulbound(
        data=ItemDataSoulbound(
            index=index,
            collection_address=COLLECTION_ADDRESS,
        )
    )

    print(f"Minted item: {item.address.to_str()}")


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
