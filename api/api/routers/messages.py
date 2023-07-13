from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..data_management import (
    MessageRead, MessageCreate, MessageUpdate, crud, Database
)

tags_metadata = [
    {
        "name": "messages",
        "description": "Endpoints to manage messages."
    }
]

router = APIRouter(tags=["Messages"])


@router.get("/messages", status_code=200, response_model=List[MessageRead])
def list_messages(session: Session = Depends(Database.get_session)):
    return crud.read_messages(session=session)


@router.post("/messages", status_code=201, response_model=MessageRead)
def add_message(
        message: MessageCreate,
        session: Session = Depends(Database.get_session)
):
    return crud.create_message(session=session, message=message)


@router.get("/messages/{id}", status_code=200, response_model=MessageRead)
def get_message(id: int, session: Session = Depends(Database.get_session)):
    message = crud.read_message(session=session, id=id)
    if message is None:
        raise HTTPException(
            status_code=404, detail=f"No message with id '{id}'"
        )
    return message


@router.patch("/messages/{id}", status_code=200, response_model=MessageRead)
def update_message(
        id: int,
        update: MessageUpdate,
        session: Session = Depends(Database.get_session)
):
    message = crud.update_message(session=session, id=id, update=update)
    if message is None:
        raise HTTPException(
            status_code=404, detail=f"No message with id '{id}'"
        )
    return message


@router.delete("/messages/{id}", status_code=204, response_model=None)
def delete_message(id: int, session: Session = Depends(Database.get_session)):
    message = crud.delete_message(session=session, id=id)
    if message is None:
        raise HTTPException(
            status_code=404, detail=f"No message with id '{id}'"
        )
    return None
