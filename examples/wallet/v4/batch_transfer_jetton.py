from pytoniq_tools.client import TonapiClient
from pytoniq_tools.wallet import WalletV4R2
from pytoniq_tools.wallet.data import TransferJettonData

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []

DESTINATION_ADDRESS = "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c"
JETTON_MASTER_ADDRESS = "EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY0to"  # noqa


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = WalletV4R2.from_mnemonic(MNEMONIC, client)

    tx_hash = await wallet.batch_jetton_transfer(
        data_list=[
            TransferJettonData(
                destination=DESTINATION_ADDRESS,
                jetton_master_address=JETTON_MASTER_ADDRESS,
                jetton_amount=0.01,
                forward_payload="Hello from pytoniq-tools!",
            ),
            TransferJettonData(
                destination=DESTINATION_ADDRESS,
                jetton_master_address=JETTON_MASTER_ADDRESS,
                jetton_amount=0.02,
                forward_payload="Hello from pytoniq-tools!",
            ),
            TransferJettonData(
                destination=DESTINATION_ADDRESS,
                jetton_master_address=JETTON_MASTER_ADDRESS,
                jetton_amount=0.03,
                forward_payload="Hello from pytoniq-tools!",
            ),
            TransferJettonData(
                destination=DESTINATION_ADDRESS,
                jetton_master_address=JETTON_MASTER_ADDRESS,
                jetton_amount=0.04,
                forward_payload="Hello from pytoniq-tools!",
            ),
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
