from pytoniq_tools.client import TonapiClient
from pytoniq_tools.wallet import WalletV3R2
from pytoniq_tools.wallet.data import TransferItemData

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = WalletV3R2.from_mnemonic(MNEMONIC, client)

    tx_hash = await wallet.batch_nft_transfer(
        data_list=[
            TransferItemData(
                destination="Destination address",
                item_address="Item address",
                forward_payload="Hello from pytoniq-tools!",
            ),
            TransferItemData(
                destination="Destination address",
                item_address="Item address",
                forward_payload="Hello from pytoniq-tools!",
            ),
            TransferItemData(
                destination="Destination address",
                item_address="Item address",
                forward_payload="Hello from pytoniq-tools!",
            ),
            TransferItemData(
                destination="Destination address",
                item_address="Item address",
                forward_payload="Hello from pytoniq-tools!",
            )
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
