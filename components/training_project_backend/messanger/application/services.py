from typing import List, Optional, Tuple
import datetime
from pydantic import validate_arguments

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component


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


class ChatParticipantInfo(DTO):
    chat_id: int
    user_id: int
    creator: bool = False
    banned: bool = False
    came_out: bool = False
    date_added: datetime.datetime = datetime.datetime.utcnow()
    id: Optional[int] = None


@component
class Messanger:
    chat_repo: interfaces.ChatsRepo
    user_repo: interfaces.UsersRepo
    chat_participant_repo: interfaces.ChatParticipantRepo
    message_repo: interfaces.MessageRepo

    @join_point
    @validate_arguments
    def search_chats(
        self,
        search: str = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Chat]:
        chats = self.chat_repo.find_by_keywords(search, limit, offset)
        if chats is None:
            raise errors.NoChats(word=search)
        return chats

    @join_point
    @validate_with_dto
    def create_chat(self, chat_info: ChatInfo) -> int:
        chat = chat_info.create_obj(Chat)
        return self.chat_repo.create(chat)

    # @join_point
    # @validate_arguments
    # def delete_chat(self, chat_id: id):
    #     self.chat_repo.delete(chat_id)

    @join_point
    @validate_arguments
    def add_user_to_chat(self, chat_participant_info: ChatParticipantInfo) -> int:
        chat_participant = chat_participant_info.create_obj(ChatParticipant)
        return self.chat_participant.add_user_to_chat(chat_participant)

    @join_point
    @validate_arguments
    def get_chats_info(self, chat_id: int) -> Chat:
        chat = self.chat_repo.get_by_id(chat_id)
        if chat is None:
            raise errors.NoChat(id=chat_id)
        return chat

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
    def send_message(self, message_info: MessageInfo) -> int:
        message = message_info.create_obj(Message)
        return self.message_repo.add_message(message)

    @join_point
    @validate_arguments
    def get_chats_message(self,  chat_participant_info: ChatParticipantInfo) -> Optional[List[Message]]:
        chat_participant_valid = chat_participant_info.create_obj(ChatParticipant)
        chat_participant = self.chat_participant_repo.get_dates_added_and_restrictions(chat_participant_valid)
        data_add = chat_participant.date_added
        if chat_participant.banned and chat_participant.left:
            data_blocked = min(chat_participant.banned, chat_participant.left)
        else:
            data_blocked = chat_participant.banned or chat_participant.left
        messages = self.message_repo.get_messages_by_chat(chat_participant.chat_id, data_add, data_blocked)
        if messages is None:
            raise errors.NoMessages(chat_id=chat_participant.chat_id)
        return messages

    @join_point
    @validate_arguments
    def left(self, chat_participant_info: ChatParticipantInfo):
        chat_participant = chat_participant_info.create_obj(ChatParticipant)
        self.chat_participant.left(chat_participant)

    @join_point
    @validate_arguments
    def return_to_chat(self, chat_participant_info: ChatParticipantInfo):
        chat_participant = chat_participant_info.create_obj(ChatParticipant)
        self.chat_participant.return_to_chat(chat_participant)


@component
class Profil:
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


