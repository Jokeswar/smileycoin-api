import json
from typing import Optional
from pydantic import BaseModel

from .client import RPCClient


class SmileyCoinResponseError(BaseModel):
    code: int
    message: str


class SmileyCoinResponse(BaseModel):
    result: Optional[str]
    error: Optional[SmileyCoinResponseError]
    id: Optional[str]


DEFAULT_ACCOUNT = ""


class SmileyCoinClient:
    def __init__(self, rpc_client: RPCClient):
        self.rpc_client = rpc_client

    def send_to_address(
        self, smiley_coin_address: str, amount: float, comment: Optional[str], comment_to: Optional[str]
    ) -> SmileyCoinResponse:
        response = self.rpc_client.call(
            "sendtoaddress", [smiley_coin_address, amount, comment if comment else "", comment_to if comment_to else ""]
        )

        return SmileyCoinResponse(**json.loads(response.text))

    def ping(self) -> bool:
        response = self.rpc_client.call("ping", [])

        return response.ok

    def get_balance(self) -> SmileyCoinResponse:
        response = self.rpc_client.call("getbalance", [])

        return SmileyCoinResponse(**json.loads(response.text))

    def get_account_address(self) -> SmileyCoinResponse:
        response = self.rpc_client.call("getaccountaddress", [DEFAULT_ACCOUNT])

        return SmileyCoinResponse(**json.loads(response.text))
