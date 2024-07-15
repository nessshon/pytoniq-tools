from typing import Optional, Any, List

from pytonapi import AsyncTonapi

from ._base import Client


class TonapiClient(Client):
    def __init__(
            self,
            api_key: str,
            is_testnet: Optional[bool] = False,
    ) -> None:
        self.client = AsyncTonapi(api_key, is_testnet)

    async def run_get_method(
            self,
            address: str,
            method_name: str,
            stack: Optional[List[Any]] = None,
    ) -> Any:
        return await self.client.blockchain.execute_get_method(
            address,
            method_name,
            *stack or []
        )

    async def send_message(self, boc: str) -> None:
        await self.client.blockchain.send_message({"boc": boc})
