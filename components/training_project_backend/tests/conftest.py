import pytest
import datetime
from messanger.application import dataclasses


@pytest.fixture(scope='function')
def user_with_id_1():
    return dataclasses.User(
        login='Vova',
        password='1234',
        email='email@mail.ru',
        id=1,
        date_registration=1647751559.734642
    )


@pytest.fixture(scope='function')
def user_with_id_2():
    return dataclasses.User(
        login='vasya',
        password='2222',
        email='vasya@mail.ru',
        id=2,
        date_registration=datetime.datetime.utcnow().timestamp()
    )

@pytest.fixture(scope='function')
def user_with_id_3():
    return dataclasses.User(
        login='vitya',
        password='3333',
        email='vitya@mail.ru',
        id=3,
        date_registration=1647751559.734642
    )

@pytest.fixture(scope='function')
def user_with_id_4():
    return dataclasses.User(
        login='pasha',
        password='4444',
        email='pasha@mail.ru',
        id=4,
        date_registration=1647751559.734642
    )


@pytest.fixture(scope='function')
def chat_with_id_1():
    return dataclasses.Chat(
        id=1,
        title='Title',
        description='Description'
    )


@pytest.fixture(scope='function')
def chat_with_id_2():
    return dataclasses.Chat(
        id=2,
        title='Title2',
        description='Description2'
    )


@pytest.fixture(scope='function')
def chat_participant_with_id_1():
    return dataclasses.ChatParticipant(
        id=1,
        chat_id=1,
        user_id=1,
        creator=True,
        banned=False,
        left=False,
        date_added=1647751559.734642,
        message_id=None
    )


@pytest.fixture(scope='function')
def chat_participant_with_id_2():
    return dataclasses.ChatParticipant(
        id=2,
        chat_id=1,
        user_id=2,
        creator=False,
        banned=False,
        left=False,
        date_added=datetime.datetime.utcnow().timestamp(),
        message_id=None
    )


@pytest.fixture(scope='function')
def chat_participant_with_id_3():
    return dataclasses.ChatParticipant(
        id=3,
        chat_id=1,
        user_id=3,
        creator=False,
        banned=datetime.datetime.utcnow().timestamp() - 0.002,
        left=False,
        date_added=datetime.datetime.utcnow().timestamp() - 0.01,
        message_id=None
    )


@pytest.fixture(scope='function')
def chat_participant_with_id_4():
    return dataclasses.ChatParticipant(
        id=4,
        chat_id=1,
        user_id=4,
        creator=False,
        banned=False,
        left=datetime.datetime.utcnow().timestamp() - 0.002,
        date_added=datetime.datetime.utcnow().timestamp() - 0.01,
        message_id=None
    )


@pytest.fixture(scope='function')
def chat2_participant_with_id_5():
    return dataclasses.ChatParticipant(
        id=5,
        chat_id=2,
        user_id=1,
        creator=True,
        banned=False,
        left=False,
        date_added=1647751559.734642,
        message_id=None
    )


@pytest.fixture(scope='function')
def chat2_participant_with_id_6():
    return dataclasses.ChatParticipant(
        id=6,
        chat_id=2,
        user_id=2,
        creator=False,
        banned=False,
        left=False,
        date_added=datetime.datetime.utcnow().timestamp(),
        message_id=None
    )


@pytest.fixture(scope='function')
def message_with_id_1():
    return dataclasses.Message(
        id=1,
        chat_id=1,
        user_id=1,
        text='Text message1',
        date_created=datetime.datetime.utcnow().timestamp(),
    )


@pytest.fixture(scope='function')
def message_with_id_2():
    return dataclasses.Message(
        id=2,
        chat_id=1,
        user_id=2,
        text='Text message2',
        date_created=datetime.datetime.utcnow().timestamp(),
    )
