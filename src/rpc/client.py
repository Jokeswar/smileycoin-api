import json
import uuid
from typing import Union, List

import requests


class RPCClient:
    def __init__(self, client_address: str, client_port: int, username: str, password: str):
        self.client_address = client_address
        self.client_port = client_port
        self.username = username
        self.password = password

    def call(self, method: str, args: List[Union[str, int, float]]) -> requests.Response:
        return requests.post(
            f"http://{self.client_address}:{self.client_port}/",
            headers=self.__get_default_headers(),
            data=self.__get_data(method, args),
            auth=(self.username, self.password),
        )

    def __get_default_headers(self):
        return {
            "content-type": "text/plain;",
        }

    def __get_data(self, method: str, args: List[Union[str, int, float]]) -> str:
        data = {"jsonrpc": 1.0, "id": uuid.uuid1().hex, "method": method, "params": args}

        return json.dumps(data)
