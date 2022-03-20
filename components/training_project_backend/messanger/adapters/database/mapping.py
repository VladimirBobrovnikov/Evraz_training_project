from sqlalchemy.orm import registry, relationship

from messanger.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.user)

mapper.map_imperatively(
	dataclasses.Chat,
	tables.chat,
	properties={
		'chat_participant': relationship(dataclasses.ChatParticipant, cascade='all, delete-orphan'),
		'messages': relationship(dataclasses.Message, cascade='all, delete-orphan')
	})

mapper.map_imperatively(dataclasses.Message, tables.message,
						# properties={
						# 	'user': relationship(
						# 		dataclasses.User,
						# 		lazy='joined',
						# 		uselist=False)
						# }
						)

mapper.map_imperatively(dataclasses.ChatParticipant, tables.chat_participant)

