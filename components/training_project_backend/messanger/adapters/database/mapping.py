from sqlalchemy.orm import registry, relationship

from messanger.application import dataclasses

from . import tables

mapper = registry()

mapper.map_imperatively(dataclasses.User, tables.user)

mapper.map_imperatively(dataclasses.Chat, tables.chat)

mapper.map_imperatively(dataclasses.Message, tables.message)

mapper.map_imperatively(dataclasses.ChatParticipant, tables.chat_participant)

