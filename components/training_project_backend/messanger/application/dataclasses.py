from typing import List, Optional
import datetime
import attr


@attr.dataclass
class User:
    login: str
    password: str
    email: Optional[str] = None
    id: Optional[int] = None
    date_registration:  float = datetime.datetime.utcnow().timestamp()


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
    date_created:  float = datetime.datetime.utcnow().timestamp()
    user: Optional[User] = None
    id: Optional[int] = None


@attr.dataclass
class ChatParticipant:
    chat_id: int
    user_id: int
    creator: bool = False
    banned: Optional[float] = None
    left: Optional[float] = None
    date_added: float = datetime.datetime.utcnow().timestamp()
    id: Optional[int] = None
