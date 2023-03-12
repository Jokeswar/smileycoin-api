from typing import Optional
from dataclasses import dataclass

from .client import RPCClient


@dataclass
class SmileyCoinResponse:
    ok: bool
    reason: Optional[str]


class SmileyCoinClient:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client

    def send_to_address(
        self, smiley_coin_address: str, amount: float, comment: Optional[str], comment_to: Optional[str]
    ) -> SmileyCoinResponse:
        response = self.rpc_client.call(
            "sendtoaddress", [smiley_coin_address, amount, comment if comment else "", comment_to if comment_to else ""]
        )

        return SmileyCoinResponse(response.ok, response.text)

    def ping(self) -> bool:
        response = self.rpc_client.call("ping", [])

        return response.ok
