from pytoniq_tools.client import TonapiClient
from pytoniq_tools.wallet import WalletV3R2

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []

DESTINATION_ADDRESS = ""
ITEM_ADDRESS = ""


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = WalletV3R2.from_mnemonic(MNEMONIC, client)

    tx_hash = await wallet.transfer_nft(
        destination=DESTINATION_ADDRESS,
        item_address=ITEM_ADDRESS,
        forward_payload="Hello from pytoniq-tools!"
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
