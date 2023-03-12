from typing import Optional
from bson import ObjectId

from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField


class Node(BaseModel):
    id: Optional[ObjectIdField] = None
    api_key: str
    node_address: str
    node_port: int
    node_username: str
    node_password: str

    class Config:
        # The ObjectIdField creates a bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectId: str}


class NodeRepository(AbstractRepository[Node]):
    class Meta:
        collection_name = "Node"


class Student(BaseModel):
    id: Optional[ObjectIdField] = None
    username: str
    wallet_address: str

    class Config:
        # The ObjectIdField creates a bson ObjectId value, so its necessary to setup the json encoding
        json_encoders = {ObjectId: str}


class StudentRepository(AbstractRepository[Student]):
    class Meta:
        collection_name = "Student"


class RewardsRequestBody(BaseModel):
    amount: float
    comment: Optional[str]
