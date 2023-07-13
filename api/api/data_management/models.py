from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class MessageLabel(str, Enum):
    unknown = "unknown"
    funny = "funny"
    informative = "informative"


class MessageBase(SQLModel):
    text: str
    label: MessageLabel

    class Config:
        schema_extra = {
            "example": {
                "text": "Let ϵ < 0",
                "label": "funny"
            }
        }


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "text": "Let ϵ < 0",
                "label": "funny",
                "id": 42
            }
        }


class MessageUpdate(SQLModel):
    label: MessageLabel

    class Config:
        schema_extra = {
            "example": {
                "label": "informative",
            }
        }
