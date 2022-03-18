from typing import List, Optional

import datetime

from attr import asdict

from sqlalchemy import select, update

from classic.components import component
from classic.sql_storage import BaseRepository

from messanger.application import interfaces
from messanger.application.dataclasses import User, Chat, Message, ChatParticipant


# yapf: disable


@component
class UsersRepo(BaseRepository, interfaces.UsersRepo):
	def get_by_id(self, id_: int) -> Optional[User]:
		query = select(User).where(User.id == id_)
		return self.session.execute(query).scalars().one_or_none()

	def get_by_login(self, login_: str) -> Optional[User]:
		query = select(User).where(User.login == login_)
		return self.session.execute(query).scalars().one_or_none()

	def add(self, user: User):
		self.session.add(user)
		self.session.flush()

	def cheng(self, user: User):
		values = asdict(user)
		del values['id']
		query = update(User).where(User.id == user.id).values(**values)
		self.session.execute(query)


@component
class ChatRepo(BaseRepository, interfaces.ChatsRepo):
	def find_by_keywords(
			self,
			search: str = '',
			limit: int = 10,
			offset: int = 0
	) -> List[Chat]:
		query = (
			select(Chat).order_by(Chat.title).limit(limit).offset(offset)
		)

		if search is not None:
			query = query.where(
				Chat.title.ilike(f'%{search}%')
				| Chat.description.ilike(f'%{search}%')
			)

		return self.session.execute(query).scalars().all()

	def get_by_id(self, id_: int) -> Optional[Chat]:
		query = select(Chat).where(Chat.id == id_)
		return self.session.execute(query).scalars().one_or_none()

	def create(self, chat: Chat) -> int:
		self.session.add(chat)
		self.session.flush()
		self.session.refresh(chat)
		return chat.id

	def update(self, id_: int, chat: Chat):
		values = asdict(chat)
		del values['id']
		query = update(User).where(User.id == id_).values(**values)
		self.session.execute(query)

	# def delete(self, chat_id: int):
	#     pass


@component
class ChatParticipantRepo(BaseRepository, interfaces.ChatParticipantRepo):

	def add_user_to_chat(self, chat_participant: ChatParticipant) -> int:
		self.session.add(chat_participant)
		self.session.flush()
		self.session.refresh(chat_participant)
		return chat_participant.id

	def block_user(self, chat_participant: ChatParticipant):
		values = {'banned': datetime.datetime.utcnow()}
		query = update(ChatParticipant).where(ChatParticipant.chat_id == chat_participant.chat_id
											  | ChatParticipant.user_id == chat_participant.user_id).values(**values)
		self.session.execute(query)

	def left(self, chat_participant: ChatParticipant):
		values = {'left': datetime.datetime.utcnow()}
		query = update(ChatParticipant).where(ChatParticipant.chat_id == chat_participant.chat_id
											  | ChatParticipant.user_id == chat_participant.user_id).values(**values)
		self.session.execute(query)

	def get_chats_users(self, chat_id: int) -> List[User]:
		query = select(ChatParticipant).where(ChatParticipant.chat_id == chat_id)
		return self.session.execute(query).scalars().all()

	def get_dates_added_and_restrictions(self, chat_participant: ChatParticipant) -> ChatParticipant:
		query = select(ChatParticipant).where(ChatParticipant.chat_id == chat_participant.chat_id
											  | ChatParticipant.user_id == chat_participant.user_id)
		return self.session.execute(query).scalars().one_or_none()

	def return_to_chat(self, chat_participant: ChatParticipant):
		values = {'left': None,
				  'date_added': datetime.datetime.utcnow()}
		query = update(ChatParticipant).where(ChatParticipant.chat_id == chat_participant.chat_id
											  | ChatParticipant.user_id == chat_participant.user_id).values(**values)
		self.session.execute(query)


@component
class MessageRepo(BaseRepository, interfaces.MessageRepo):

	# @abstractmethod
	# def find_by_keywords(
	#     self,
	#     search: str = None,
	#     limit: int = 10,
	#     offset: int = 0
	# ) -> List[Message]:
	#     ...

	def get_by_id(self, id_: int) -> Optional[Message]:
		query = select(Message).where(Message.id == id_)
		return self.session.execute(query).scalars().one_or_none()

	def get_messages_by_chat(self,
							 chat_id: int,
							 data_start: Optional[datetime.datetime],
							 data_stop: Optional[datetime.datetime]
							 ) -> Optional[List[Message]]:
		query = (
			select(Message).where(Message.chat_id == chat_id).order_by(Message.date_created)
		)

		if data_start is not None:
			query = query.where(Message.date_created >= data_start)
		if data_stop is not None:
			query = query.where(Message.date_created <= data_stop)
		return self.session.execute(query).scalars().all()

	def add_message(self, message: Message) -> int:
		self.session.add(message)
		self.session.flush()
		self.session.refresh(message)
		return message.id
