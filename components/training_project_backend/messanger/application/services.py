from typing import List, Optional, Tuple

from pydantic import conint, validate_arguments

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from classic.messaging import Message, Publisher

from . import errors, interfaces
from .dataclasses import User, Chat, Message, ChatParticipant

join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    login: str
    password: str
    email: Optional[str] = None
    id: Optional[int] = None


class ChatInfo(DTO):
    title: str
    description: Optional[str] = None
    id: Optional[int] = None


class ChatInfoForChange(DTO):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None


class MessageInfo(DTO):
    chat_id: int
    user_id: int
    text: str
    id: Optional[int]


@component
class Messanger:
    chat_repo: interfaces.ChatsRepo
    user_repo: interfaces.UsersRepo
    chat_participant: interfaces.ChatParticipantRepo
    message_repo: interfaces.MessageRepo

    @join_point
    @validate_arguments
    def search_chats(
        self,
        search: str = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Chat]:
        return self.chat_repo.find_by_keywords(search, limit, offset)

    @join_point
    @validate_with_dto
    def create_chat(self, chat_info: ChatInfo) -> Chat:
        chat = chat_info.create_obj(Chat)
        return self.chat_repo.create(chat)

    @join_point
    @validate_arguments
    def delete_chat(self, chat_id: id):
        self.chat_repo.delete(chat_id)

    @join_point
    @validate_arguments
    def add_user_to_chat(self, user_id: int, chat_id: int):
        self.chat_participant.create(user_id, chat_id)

    @join_point
    @validate_arguments
    def get_chats_info(self, chat_id: int) -> Tuple:
        chat = self.chat_repo.get_by_id(chat_id)
        data_in_tuple = (chat.id, chat.title, chat.description)
        return data_in_tuple

    @join_point
    @validate_arguments
    def change_chat_info(self, chat_info: ChatInfoForChange):
        old_chat = self.chat_repo.get_by_id(chat_info.id)
        if chat_info.title:
            old_chat.title = chat_info.title
        if chat_info.description:
            old_chat.description = chat_info.description
        self.chat_repo.update(chat_info.id, old_chat)


    @join_point
    @validate_arguments
    def get_chats_users(self, chat_id: int) -> List[User]:
        return self.chat_participant.get_chats_users(chat_id)

    @join_point
    @validate_arguments
    def send_message(self, message_info: MessageInfo) -> Message:
        message = message_info.create_obj(Message)
        return self.message_repo.add_message(message)

    @join_point
    @validate_arguments
    def get_chats_message(self, chat_id: int, user_id: int) -> Optional[List[Message]]:
        data_add, data_blocked = self.chat_participant.get_dates_added_and_restrictions(chat_id, user_id)
        return self.message_repo.get_messages_by_chat(chat_id, data_add, data_blocked)

    @join_point
    @validate_arguments
    def left(self, chat_id: int, user_id: int):
        self.chat_participant.left(chat_id, user_id)

    @join_point
    @validate_arguments
    def return_to_chat(self, chat_id: int, user_id: int):
        self.chat_participant.return_to_chat(chat_id, user_id)


@component
class Auth:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_arguments
    def create_user(self, user_info: UserInfo) -> Chat:
        user = user_info.create_obj(User)
        return self.user_repo.add(user)

    @join_point
    @validate_arguments
    def get_user_by_id(self, user_id: int):
        return self.user_repo.get_by_id(user_id)

    @join_point
    @validate_arguments
    def get_user_by_login(self, login: str) -> Optional[User]:
        return self.user_repo.get_by_login(login)


