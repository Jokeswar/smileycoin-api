from http import HTTPStatus
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Body, APIRouter

from src.db import get_database
from src.models import NodeRepository, StudentRepository, RewardsRequestBody
from src.rpc.client import RPCClient
from src.rpc.smileycoin import SmileyCoinClient

app = FastAPI()
router = APIRouter(prefix="/api/v1")


@router.get("/users/{username}")
async def usernames(username: str) -> object:
    raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED)


@router.post("/users/{username}/rewards")
async def rewards(
    username: str,
    body: RewardsRequestBody = Body(),
    x_api_key: Optional[str] = Header(default=None),
) -> object:
    student_repository = StudentRepository(database=get_database())
    student = student_repository.find_one_by({"username": username})
    if not student:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"No user named '{username}'")

    api_key_repository = NodeRepository(database=get_database())
    api_key = api_key_repository.find_one_by({"api_key": x_api_key})
    if not api_key:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"No node assigned to the API key '{x_api_key}'")

    rpc_client = RPCClient(api_key.node_address, api_key.node_port, api_key.node_username, api_key.node_password)
    smiley_coin_client = SmileyCoinClient(rpc_client)

    response = smiley_coin_client.send_to_address(student.wallet_address, body.amount, body.comment, username)
    if not response.ok:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Something happend: {response.reason}")

    return ""


app.include_router(router)
