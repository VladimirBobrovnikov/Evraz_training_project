from classic.app.errors import AppError


class NoChat(AppError):
	msg_template = "No chats with id '{id}'"
	code = 'messanger.no_chat'


class NoChats(AppError):
	msg_template = "No chats with '{word}' in title"
	code = 'messanger.no_chats'


class NoMessage(AppError):
	msg_template = "No message with id '{id}'"
	code = 'messanger.no_message'


class NoUser(AppError):
	msg_template = "No users with id '{id}'"
	code = 'messanger.no_user'


class NoMessages(AppError):
	msg_template = "No message in chat '{chat_id}'"
	code = 'messanger.no_messages'


class NoCreatorsPermissions(AppError):
	msg_template = "No Creators Permissions in chats '{chat_id}'"
	code = 'messanger.no_creator_permissions'


class NoPermissionsForChange(AppError):
	msg_template = "No permissions for change Participant '{user_id}'"
	code = 'messanger.no_permissions_for_change'



class NoChatParticipant(AppError):
	msg_template = "No participant with id '{id}' in chat"
	code = 'messanger.no_chat_participant'

# class EmptyCart(AppError):
#     msg_template = "Cart is empty"
#     code = 'shop.cart_is_empty'
