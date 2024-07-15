from typing import Any, Optional, List


class Client:

    async def run_get_method(
            self,
            address: str,
            method_name: str,
            stack: Optional[List[Any]] = None,
    ) -> Any:
        raise NotImplementedError

    async def send_message(self, boc: str) -> None:
        raise NotImplementedError
