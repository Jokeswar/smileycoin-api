from http import HTTPStatus

from fastapi import FastAPI, Header, HTTPException, Body, APIRouter, Path

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
    username: str = Path(),
    body: RewardsRequestBody = Body(),
    x_api_key: str = Header(),
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
    if response.error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f"Something happend: {response.error}")

    return ""


@router.get("/wallets")
async def wallet_info(x_api_key: str = Header()) -> object:
    api_key_repository = NodeRepository(database=get_database())
    api_key = api_key_repository.find_one_by({"api_key": x_api_key})
    if not api_key:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"No node assigned to the API key '{x_api_key}'")

    rpc_client = RPCClient(api_key.node_address, api_key.node_port, api_key.node_username, api_key.node_password)
    smiley_coin_client = SmileyCoinClient(rpc_client)

    balance_response = smiley_coin_client.get_balance()
    if balance_response.error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Something happend while retriving the balance: {balance_response.error}",
        )

    address_response = smiley_coin_client.get_account_address()
    if address_response.error:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f"Something happend while retriving the address: {address_response.error}",
        )

    return {"amount": balance_response.result, "address": address_response.result}


app.include_router(router)
