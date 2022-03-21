from classic.components import component
from classic.http_auth import (
	authenticate,
	authenticator_needed,
	authorize
)

from messanger.application import services

from .auth import Groups, Permissions
from .join_points import join_point


@authenticator_needed
@component
class Messanger:
	messanger: services.Messanger

	@join_point
	@authenticate
	def on_get_chat(self, request, response):
		chat = self.messanger.get_chats_info(**request.params)
		response.media = {
			'id': chat.id,
			'title': chat.title,
			'description': chat.description
		}

	@join_point
	@authenticate
	def on_get_search_chats(self, request, response):
		chats = self.messanger.search_chats(**request.params)
		response.media = [
			{
				'id': chat.id,
				'title': chat.title,
				'description': chat.description
			} for chat in chats
		]

	@join_point
	@authenticate
	def on_get_chats_users(self, request, response):
		users = self.messanger.get_chats_users(user_id=request.context.client.user_id, **request.params)
		response.media = [
			{
				'id': user.id,
				'login': user.login,
				'email': user.email,
				'date_registration': user.date_registration
			} for user in users
		]

	@join_point
	@authenticate
	def on_get_chats_message(self, request, response):
		messages = self.messanger.get_chats_message(user_id=request.context.client.user_id, **request.params)
		response.media = [
			{
				'id': message.id,
				'chat_id': message.chat_id,
				'user_id': message.user_id,
				'text': message.text,
				'date_created': message.date_created
			} for message in messages
		]

	@join_point
	@authenticate
	def on_post_create_chat(self, request, response):
		self.messanger.create_chat(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': 'Сhat successfully created'
		}

	@join_point
	@authenticate
	def on_post_add_user_to_chat(self, request, response):
		self.messanger.add_user_to_chat(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': 'User successfully added'
		}

	@join_point
	@authenticate
	def on_post_change_chat_info(self, request, response):
		self.messanger.change_chat_info(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': 'Сhat successfully changed'
		}

	@join_point
	@authenticate
	def on_post_send_message(self, request, response):
		self.messanger.send_message(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': 'Message successfully send'
		}

	@join_point
	@authenticate
	def on_post_left(self, request, response):
		self.messanger.left(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': 'You have left the chat'
		}

	@join_point
	@authenticate
	def on_post_return_to_chat(self, request, response):
		self.messanger.return_to_chat(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': f'You have return to the chat'
		}


	@join_point
	@authenticate
	def on_post_block_user(self, request, response):
		self.messanger.block_user(user_id=request.context.client.user_id, **request.media)
		response.media = {
			'message': 'You had block the user'
		}


@authenticator_needed
@component
class Profil:
	profil: services.Profil

	@join_point
	def on_post_create_user(self, request, response):
		token = self.profil.create_user(**request.media)
		response.media = {
			'token': token
		}

	@join_point
	@authenticate
	def on_get_user(self, request, response, *args, **kwargs):
		user = self.profil.get_user_by_id(request.context.client.user_id)
		response.media = {
			'id': user.id,
			'login': user.login,
			'email': user.email,
			'date_registration': user.date_registration
		}
