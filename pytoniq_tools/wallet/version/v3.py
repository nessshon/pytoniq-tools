from __future__ import annotations

from typing import Tuple, List, Optional, Union

from .._base import Wallet
from ..data import WalletV3Data
from ...client import Client


class WalletV3R1(Wallet):
    CODE_HEX = "b5ee9c724101010100620000c0ff0020dd2082014c97ba9730ed44d0d70b1fe0a4f2608308d71820d31fd31fd31ff82313bbf263ed44d0d31fd31fd3ffd15132baf2a15144baf2a204f901541055f910f2a3f8009320d74a96d307d402fb00e8d101a4c8cb1fcb1fcbffc9ed543fbe6ee0"  # noqa

    @classmethod
    def create(cls) -> Tuple[WalletV3R1, bytes, bytes, List[str]]:
        return super().create()  # type: ignore

    @classmethod
    def from_mnemonic(
            cls,
            mnemonic: Union[List[str], str],
            client: Optional[Client] = None,
    ) -> Tuple[WalletV3R1, bytes, bytes, List[str]]:
        return super().from_mnemonic(mnemonic, client)  # type: ignore

    @classmethod
    def _create_data(  # noqa
            cls,
            public_key: bytes,
            seqno: int,
            wallet_id: int,
    ) -> WalletV3Data:
        return WalletV3Data(public_key=public_key, seqno=seqno, wallet_id=wallet_id)


class WalletV3R2(WalletV3R1):
    CODE_HEX = "b5ee9c724101010100710000deff0020dd2082014c97ba218201339cbab19f71b0ed44d0d31fd31f31d70bffe304e0a4f2608308d71820d31fd31fd31ff82313bbf263ed44d0d31fd31fd3ffd15132baf2a15144baf2a204f901541055f910f2a3f8009320d74a96d307d402fb00e8d101a4c8cb1fcb1fcbffc9ed5410bd6dad"  # noqa

    @classmethod
    def create(cls) -> Tuple[WalletV3R2, bytes, bytes, List[str]]:
        return super().create()  # type: ignore

    @classmethod
    def from_mnemonic(
            cls,
            mnemonic: Union[List[str], str],
            client: Optional[Client] = None,
    ) -> Tuple[WalletV3R2, bytes, bytes, List[str]]:
        return super().from_mnemonic(mnemonic, client)  # type: ignore
