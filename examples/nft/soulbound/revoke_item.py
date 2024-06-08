import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.soulbound.item import ItemSoulbound

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

ITEM_ADDRESS = Address("EQB6U56wUiIhPRrqH2fPmO_Oiv3pMOG7Yx0t3qng6MRkZefK")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    body = ItemSoulbound.build_revoke_body()

    await wallet.transfer(
        destination=ITEM_ADDRESS,
        body=body,
        amount=int(0.02 * 1e9),
    )

    print(f"Revoked item: {ITEM_ADDRESS.to_str()}")


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
