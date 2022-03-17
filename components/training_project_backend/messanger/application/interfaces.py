import datetime
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from .dataclasses import User, Chat, Message, ChatParticipant


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_login(self, login_: int) -> Optional[User]:
        ...

    @abstractmethod
    def add(self, customer: User):
        ...

    @abstractmethod
    def cheng(self, customer: User):
        ...


class ChatsRepo(ABC):

    @abstractmethod
    def find_by_keywords(
        self,
        search: str = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Chat]:
        ...

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Chat]:
        ...

    @abstractmethod
    def add_user(self, user: User, chat: Chat):
        ...

    @abstractmethod
    def create(self, chat: Chat) -> Chat:
        ...

    @abstractmethod
    def update(self, id_: int, chat: Chat) -> Chat:
        ...

    @abstractmethod
    def delete(self, chat_id: int):
        ...


class ChatParticipantRepo(ABC):

    @abstractmethod
    def create(self, user_id: int, chat_id: int) -> ChatParticipant:
        ...

    @abstractmethod
    def block_user(self, user_id: int, chat_id: int):
        ...

    @abstractmethod
    def left(self, user_id: int, chat_id: int):
        ...

    @abstractmethod
    def get_chats_users(self, chat_id: int) -> List[User]:
        ...

    @abstractmethod
    def get_dates_added_and_restrictions(self, chat_id: int, user_id: int) -> Tuple[datetime.datetime, Union[datetime.datetime, None]]:
        ...


    @abstractmethod
    def return_to_chat(self, user_id: int, chat_id: int):
        ...


class MessageRepo(ABC):

    # @abstractmethod
    # def find_by_keywords(
    #     self,
    #     search: str = None,
    #     limit: int = 10,
    #     offset: int = 0
    # ) -> List[Message]:
    #     ...

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[Message]:
        ...

    @abstractmethod
    def get_messages_by_chat(self,
                             chat_id: int,
                             data_start: Optional[datetime.datetime],
                             data_stop: Optional[datetime.datetime]
                             ) -> Optional[List[Message]]:
        ...

    @abstractmethod
    def add_message(self, message: Message) -> Message:
        ...

