import datetime
import os
from typing import List, Optional
import jwt
from dotenv import load_dotenv

from classic.app import DTO, validate_with_dto
from classic.aspects import PointCut
from classic.components import component
from pydantic import validate_arguments

from . import errors, interfaces
from .dataclasses import User, Chat, Message, ChatParticipant

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)


join_points = PointCut()
join_point = join_points.join_point


class UserInfo(DTO):
    login: str
    password: str
    email: Optional[str] = None
    id: Optional[int] = None


class ChatInfoForCreate(DTO):
    user_id: int
    title: str
    description: Optional[str] = None
    id: Optional[int] = None


class ChatInfoForChange(DTO):
    user_id: int
    chat_id: int
    title: Optional[str] = None
    description: Optional[str] = None


class MessageInfo(DTO):
    chat_id: int
    user_id: int
    text: str
    id: Optional[int] = None


class ChatParticipantInfo(DTO):
    chat_id: int
    user_id: int
    creator: bool = False
    banned: bool = False
    came_out: bool = False
    date_added: float = datetime.datetime.utcnow().timestamp()
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
    def create_chat(self, chat_info: ChatInfoForCreate):
        chat = Chat(chat_info.title, chat_info.description)
        chat_id = self.chat_repo.create(chat)
        chat_participant = ChatParticipant(
            chat_id=chat_id,
            user_id=chat_info.user_id,
            creator=True,
            date_added=datetime.datetime.utcnow().timestamp())
        self.chat_participant_repo.add_user_to_chat(chat_participant)

    # @join_point
    # @validate_arguments
    # def delete_chat(self, chat_id: id):
    #     self.chat_repo.delete(chat_id)


    @join_point
    @validate_arguments()
    def add_user_to_chat(self, user_id: int, chat_id: int, user_id_to_added: int) -> int:
        chat_participant = self.chat_participant_repo.search_chat_participant(chat_id, user_id)
        if chat_participant and chat_participant.creator:
            new_chat_participant = ChatParticipant(chat_id, user_id=user_id_to_added)
            return self.chat_participant_repo.add_user_to_chat(new_chat_participant)

    @join_point
    @validate_arguments
    def get_chats_info(self, chat_id: int) -> Chat:
        chat = self.chat_repo.get_by_id(chat_id)
        if chat is None:
            raise errors.NoChat(id=chat_id)
        return chat

    @join_point
    @validate_with_dto
    def change_chat_info(self, chat_info: ChatInfoForChange):
        chat_participant = self.chat_participant_repo.search_chat_participant(chat_info.chat_id, chat_info.user_id)
        if chat_participant and chat_participant.creator:
            old_chat = self.chat_repo.get_by_id(chat_info.chat_id)
            if chat_info.title:
                old_chat.title = chat_info.title
            if chat_info.description:
                old_chat.description = chat_info.description
            self.chat_repo.update(chat_info.chat_id, old_chat)

    @join_point
    @validate_with_dto
    def block_user(self, chat_participant_info: ChatParticipantInfo):
        chat_participant = chat_participant_info.create_obj(ChatParticipant)
        self.chat_participant_repo.block_user(chat_participant)

    @join_point
    @validate_arguments
    def get_chats_users(self, user_id: int, chat_id: int) -> List[User]:
        chat_participant = self.chat_participant_repo.search_chat_participant(chat_id, user_id)
        if chat_participant:
            participants = self.chat_participant_repo.get_chats_users(chat_id)
            return [self.user_repo.get_by_id(participant.user_id) for participant in participants]

    @join_point
    @validate_with_dto
    def send_message(self, message_info: MessageInfo):
        message = message_info.create_obj(Message)
        self.message_repo.add_message(message)

    @join_point
    @validate_arguments()
    def get_chats_message(self, user_id: int, chat_id: int) -> Optional[List[Message]]:
        chat_participant = self.chat_participant_repo.search_chat_participant(chat_id, user_id)
        if chat_participant:
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
    @validate_with_dto
    def left(self, chat_participant_info: ChatParticipantInfo):
        chat_participant = chat_participant_info.create_obj(ChatParticipant)
        self.chat_participant.left(chat_participant)

    @join_point
    @validate_with_dto
    def return_to_chat(self, chat_participant_info: ChatParticipantInfo):
        chat_participant = chat_participant_info.create_obj(ChatParticipant)
        self.chat_participant.return_to_chat(chat_participant)


@component
class Profil:
    user_repo: interfaces.UsersRepo

    @join_point
    @validate_with_dto
    def create_user(self, user_info: UserInfo) -> str:
        user = user_info.create_obj(User)
        user = self.user_repo.add(user)
        # return create_token(user.id, user.login, user.password)
        payload = {
            "sub": user.id,
            'login': user.login,
            'name': user.login,
            'password': user.password,
            'groups': 'admins',
        }
        token = jwt.encode(payload=payload, key='Very secret_key')
        return token

    @join_point
    @validate_arguments
    def get_user_by_id(self, user_id: int):
        return self.user_repo.get_by_id(user_id)

    @join_point
    @validate_arguments
    def get_user_by_login(self, login: str) -> Optional[User]:
        return self.user_repo.get_by_login(login)


