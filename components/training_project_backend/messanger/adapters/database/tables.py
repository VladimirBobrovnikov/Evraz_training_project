from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    DateTime,
    BigInteger,
    Boolean
)

from sqlalchemy.orm import relationship, backref
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

# даем имя схемы только для БД MSSQL, связано с инфраструктурными особенностями
# metadata = MetaData(naming_convention=naming_convention, schema='app')

metadata = MetaData(naming_convention=naming_convention)

# yapf: disable

user = Table(
    'users',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('login', String, unique=True),
    Column('password', String),
    Column('email', String, nullable=True),
    Column('date_registration', Float),
)

chat = Table(
    'chats',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('title', String, unique=True),
    Column('description', String),
)

message = Table(
    'messages',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('chat_id', ForeignKey('chats.id'), unique=True),
    Column('user_id', ForeignKey('users.id'), unique=True),
    Column('text', String),
    Column('date_created', Float),
)

chat_participant = Table(
    'chat_participant',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('chat_id', ForeignKey('chats.id')),
    Column('user_id', ForeignKey('users.id')),
    Column('creator', Boolean),
    Column('banned', Float, nullable=True),
    Column('left', Float, nullable=True),
    Column('date_added', Float),
)
