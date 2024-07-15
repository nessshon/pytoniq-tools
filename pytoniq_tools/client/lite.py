from typing import Optional, Any, Dict, List

from pytoniq import LiteBalancer

from ._base import Client


class LiteClient(Client):

    def __init__(
            self,
            config: Optional[Dict[str, Any]] = None,
            is_testnet: Optional[bool] = False,
            trust_level: Optional[int] = 2,
    ) -> None:
        if config is not None:
            self.client = LiteBalancer.from_config(config=config, trust_level=trust_level)
        elif is_testnet:
            self.client = LiteBalancer.from_testnet_config(trust_level=trust_level)
        else:
            self.client = LiteBalancer.from_mainnet_config(trust_level=trust_level)

    async def run_get_method(
            self,
            address: str,
            method_name: str,
            stack: Optional[List[Any]] = None,
    ) -> Any:
        async with self.client:
            return await self.client.run_get_method(address, method_name, stack or [])

    async def send_message(self, boc: str) -> None:
        async with self.client:
            return await self.client.raw_send_message(bytes.fromhex(boc))
