from http import HTTPStatus
from typing import Optional

from .client import RPCClient


class SmileyCoinClient:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client

    def send_to_address(self, smiley_coin_address: str, amount: float, comment: Optional[str], comment_to: Optional[str]):
        self.rpc_client.call("sendtoaddress", [smiley_coin_address, amount])

    def ping(self) -> bool:
        response = self.rpc_client.call("ping", [])

        return response.status_code == HTTPStatus.OK
