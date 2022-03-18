from typing import List, Optional
import datetime
import attr


@attr.dataclass
class User:
    login: str
    password: str
    email: Optional[str]
    id: Optional[int] = None
    date_registration:  datetime.datetime = datetime.datetime.utcnow()

@attr.dataclass
class Chat:
    title: str
    description: str
    id: Optional[int] = None

@attr.dataclass
class Message:
    chat_id: int
    user_id: int
    text: str
    date_created:  datetime.datetime = datetime.datetime.utcnow()
    id: Optional[int] = None

@attr.dataclass
class ChatParticipant:
    chat_id: int
    user_id: int
    creator: bool = False
    banned: Optional[datetime.datetime] = None
    left: Optional[datetime.datetime] = None
    date_added: datetime.datetime = datetime.datetime.utcnow()
    id: Optional[int] = None
