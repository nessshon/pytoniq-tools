from pytoniq_tools.client import TonapiClient
from pytoniq_tools.wallet import HighloadWalletV2
from pytoniq_tools.wallet.data import TransferJettonData

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = HighloadWalletV2.from_mnemonic(MNEMONIC, client)

    tx_hash = await wallet.transfer_jetton(
        data_list=[
            TransferJettonData(
                destination="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",
                jetton_master_address="EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY0to",
                jetton_amount=0.01,
                forward_payload="Hello from pytoniq-tools!"
            ),
            TransferJettonData(
                destination="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",
                jetton_master_address="EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY0to",
                jetton_amount=0.01,
                forward_payload="Hello from pytoniq-tools!"
            ),
            TransferJettonData(
                destination="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",
                jetton_master_address="EQAiboDEv_qRrcEdrYdwbVLNOXBHwShFbtKGbQVJ2OKxY0to",
                jetton_amount=0.01,
                forward_payload="Hello from pytoniq-tools!"
            )
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
