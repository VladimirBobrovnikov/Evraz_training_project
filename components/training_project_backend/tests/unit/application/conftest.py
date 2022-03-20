from unittest.mock import Mock

import pytest

from messanger.application import interfaces


@pytest.fixture(scope='function')
def user_repo(user_with_id_1, user_with_id_2, user_with_id_3, user_with_id_4):
    user_repo = Mock(interfaces.UsersRepo)
    user_repo.get_by_id = Mock(return_value=user_with_id_1)

    return user_repo


@pytest.fixture(scope='function')
def chat_repo(chat_with_id_1, chat_with_id_2):
    chat_repo = Mock(interfaces.ChatsRepo)
    chat_repo.get_by_id = Mock(return_value=chat_with_id_1)

    return chat_repo


@pytest.fixture(scope='function')
def chat_participant_repo1(chat_participant_with_id_1,
                           chat_participant_with_id_2,
                           chat_participant_with_id_3,
                           chat_participant_with_id_4,
                           chat2_participant_with_id_5,
                           chat2_participant_with_id_6):
    chat_participant_repo = Mock(interfaces.ChatParticipantRepo)
    chat_participant_repo.search_chat_participant = Mock(return_value=chat_participant_with_id_1)
    chat_participant_repo.get_chats_users = Mock(return_value=[chat_participant_with_id_1,
                                                               chat_participant_with_id_2,
                                                               chat_participant_with_id_3,
                                                               chat_participant_with_id_4])

    return chat_participant_repo


@pytest.fixture(scope='function')
def chat_participant_repo2(chat_participant_with_id_1,
                           chat_participant_with_id_2,
                           chat_participant_with_id_3,
                           chat_participant_with_id_4,
                           chat2_participant_with_id_5,
                           chat2_participant_with_id_6):
    chat_participant_repo = Mock(interfaces.ChatParticipantRepo)
    chat_participant_repo.search_chat_participant = Mock(return_value=chat_participant_with_id_2)

    return chat_participant_repo


@pytest.fixture(scope='function')
def message_repo(message_with_id_1,
                 message_with_id_2):
    message_repo = Mock(interfaces.MessageRepo)
    message_repo.get_messages_by_chat = Mock(return_value=[message_with_id_1,
                                                           message_with_id_2])

    return message_repo
