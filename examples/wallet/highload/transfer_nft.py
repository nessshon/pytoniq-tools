from pytoniq_tools.client import TonapiClient
from pytoniq_tools.wallet import HighloadWalletV2
from pytoniq_tools.wallet.data import TransferItemData

API_KEY = ""
IS_TESTNET = True

MNEMONIC = []


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, public_key, private_key, mnemonic = HighloadWalletV2.from_mnemonic(MNEMONIC, client)

    tx_hash = await wallet.transfer_nft(
        data_list=[
            TransferItemData(
                destination="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",
                item_address="kQDoPmq9iKF3osjRRpINtCTLTYZFNr9k-QkwRdiw1IRUj0fI",
            ),
            TransferItemData(
                destination="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",
                item_address="kQDLWjSFwezDiwSojGlZkaFVu_daicdtQemnBSdOthm5KcIF",
            ),
            TransferItemData(
                destination="EQC-3ilVr-W0Uc3pLrGJElwSaFxvhXXfkiQA3EwdVBHNNess",
                item_address="kQCYGRVH10NsXIZNdpwEkenNMrMpy11SdyyE_B1p6eos7Jdw",
            ),
        ]
    )

    print("Successfully transferred!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
