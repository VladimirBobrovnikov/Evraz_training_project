from classic.components import component
from classic.http_auth import (
    authenticate,
    authenticator_needed,
    authorize,
)

from messanger.application import services

from .auth import Groups, Permissions
from .join_points import join_point


@authenticator_needed
@component
class Messanger:
    messanger: services.Messanger

    @join_point
    def on_get_chat(self, request, response):
        chat = self.messanger.get_chats_info(**request.params)
        response.media = {
            'id': chat.id,
            'title': chat.title,
            'description': chat.description
        }

    @join_point
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
    def on_get_chats_users(self, request, response):
        users = self.messanger.get_chats_users(**request.params)
        response.media = [
            {
                'id': user.id,
                'login': user.login,
                'email': user.email,
                'date_registration': user.date_registration
            } for user in users
        ]

    @join_point
    def on_get_chats_message(self, request, response):
        messages = self.messanger.get_chats_message(**request.params)
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
    def on_post_create_chat(self, request, response):
        self.messanger.create_chat(**request.params)

    @join_point
    def on_post_add_user_to_chat(self, request, response):
        self.messanger.add_user_to_chat(**request.params)

    @join_point
    def on_post_change_chat_info(self, request, response):
        self.messanger.change_chat_info(**request.params)

    @join_point
    def on_post_send_message(self, request, response):
        self.messanger.send_message(**request.params)

    @join_point
    def on_post_left(self, request, response):
        self.messanger.left(**request.params)

    @join_point
    def on_post_return_to_chat(self, request, response):
        self.messanger.return_to_chat(**request.params)


@component
class Profil:
    profil: services.Profil

    @join_point
    def on_post_create_user(self, request, response):
        self.profil.create_user(**request.params)

    @join_point
    def on_get_user(self, request, response):
        if request.context['id']:
            user = self.profil.get_user_by_id(int(request.context['id']))
        elif request.context['login']:
            user = self.profil.get_user_by_login(request.context['login'])
        else:
            raise Exception
        #TODO Exception
        response.media = {
            'id': user.id,
            'login': user.login,
            'email': user.email,
            'date_registration': user.date_registration
        }
