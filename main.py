from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Body

from src.db import get_database
from src.models import NodeRepository, RewardsRequestBody
from src.rpc.client import RPCClient
from src.rpc.smileycoin import SmileyCoinClient

app = FastAPI()


@app.get("/users/{username}")
async def usernames(username: str) -> object:
    raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED)


@app.post("/users/{username}/rewards")
async def rewards(
    username: str, x_api_key: Optional[str] = Header(default=None), body: RewardsRequestBody = Body()
) -> object:
    api_key_repository = NodeRepository(database=get_database())
    api_key = api_key_repository.find_one_by({"api_key": x_api_key})
    if not api_key:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"No node assigned to the API key '{x_api_key}'")

    rpc_client = RPCClient(api_key.node_address, api_key.node_port, api_key.node_username, api_key.node_password)
    smiley_coin_client = SmileyCoinClient(rpc_client)

    smiley_coin_client.ping()

    return ""
