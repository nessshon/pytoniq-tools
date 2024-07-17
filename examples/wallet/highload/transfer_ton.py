from pytoniq_tools.client import TonapiClient
from pytoniq_tools.wallet import HighloadWalletV2
from pytoniq_tools.wallet.data import TransferData

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = HighloadWalletV2.from_mnemonic(MNEMONIC, client)

    tx_hash = await wallet.transfer(
        data_list=[
            TransferData(
                destination="EQBANwCCQiMCjtBhFhnI8q18qetmYIuMqhZJpXCt0cgBj2YK",
                amount=0.01,
                body="Hello from pytoniq-tools!",
            ),
            TransferData(
                destination="EQBANwCCQiMCjtBhFhnI8q18qetmYIuMqhZJpXCt0cgBj2YK",
                amount=0.01,
                body="Hello from pytoniq-tools!",
            ),
            TransferData(
                destination="EQBANwCCQiMCjtBhFhnI8q18qetmYIuMqhZJpXCt0cgBj2YK",
                amount=0.01,
                body="Hello from pytoniq-tools!",
            ),
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
