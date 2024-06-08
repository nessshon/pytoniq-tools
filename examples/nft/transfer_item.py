import asyncio

from pytoniq import LiteBalancer, WalletV4R2
from pytoniq_core import Address

from pytoniq_tools.nft.standard.item import ItemStandard

IS_TESTNET = True

MNEMONICS = "a b c ..."  # noqa

ITEM_ADDRESS = Address("EQAWBEjjyTA7kQTGI__RR1REotRvn3gE8nBW-FfTElsD4Hez")  # noqa

NEW_OWNER_ADDRESS = Address("EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c")  # noqa


async def main() -> None:
    provider = await get_provider()
    wallet = await get_wallet(provider)

    body = ItemStandard.build_transfer_body(
        new_owner_address=NEW_OWNER_ADDRESS,
    )

    # For item editable use:
    """
    body = ItemEditable.build_transfer_body(
        new_owner_address=NEW_OWNER_ADDRESS,
    )
    """

    await wallet.transfer(
        destination=ITEM_ADDRESS,
        body=body,
        amount=int(0.05 * 1e9),
    )

    print(f"Transferred item: {ITEM_ADDRESS.to_str()} to {NEW_OWNER_ADDRESS.to_str()}")


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
