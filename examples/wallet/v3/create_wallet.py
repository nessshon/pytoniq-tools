from pytoniq_tools.wallet import WalletV3R2


def main() -> None:
    wallet, public_key, private_key, mnemonic = WalletV3R2.create()

    print("Wallet created!")
    print(f"Address: {wallet.address.to_str()}\nMnemonic: {mnemonic}\n")


if __name__ == "__main__":
    main()
