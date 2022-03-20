import datetime
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from .dataclasses import User, Chat, Message, ChatParticipant


class UsersRepo(ABC):

    @abstractmethod
    def get_by_id(self, id_: int) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_login(self, login_: str) -> Optional[User]:
        ...

    @abstractmethod
    def add(self, user: User):
        ...

    @abstractmethod
    def cheng(self, user: User):
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
    def create(self, chat: Chat) -> int:
        ...

    @abstractmethod
    def update(self, id_: int, chat: Chat) -> Chat:
        ...

    # @abstractmethod
    # def delete(self, chat_id: int):
    #     ...


class ChatParticipantRepo(ABC):

    @abstractmethod
    def add_user_to_chat(self, chat_participant: ChatParticipant) -> int:
        ...

    @abstractmethod
    def block_user(self, chat_participant: ChatParticipant):
        ...

    @abstractmethod
    def left(self, chat_participant: ChatParticipant):
        ...

    @abstractmethod
    def get_chats_users(self, chat_id: int) -> List[ChatParticipant]:
        ...


    @abstractmethod
    def return_to_chat(self, chat_participant: ChatParticipant):
        ...

    @abstractmethod
    def search_chat_participant(self, chat_id: int, user_id: int) -> ChatParticipant:
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
                             data_start: Optional[float],
                             data_stop: Optional[float]
                             ) -> Optional[List[Message]]:
        ...

    @abstractmethod
    def add_message(self, message: Message) -> int:
        ...

