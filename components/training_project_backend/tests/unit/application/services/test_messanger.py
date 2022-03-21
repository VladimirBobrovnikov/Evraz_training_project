import pytest
from pydantic import ValidationError
from attr import asdict
from messanger.application import errors
from messanger.application.services import Messanger


@pytest.fixture(scope='function')
def service1(user_repo, chat_repo, chat_participant_repo1, message_repo):
	return Messanger(
		user_repo=user_repo,
		chat_repo=chat_repo,
		chat_participant_repo=chat_participant_repo1,
		message_repo=message_repo)


@pytest.fixture(scope='function')
def service2(user_repo, chat_repo_with_empty_get_by_id, chat_participant_repo2, message_repo):
	return Messanger(
		user_repo=user_repo,
		chat_repo=chat_repo_with_empty_get_by_id,
		chat_participant_repo=chat_participant_repo2,
		message_repo=message_repo)


data_chat = {
	'id': 1,
	'title': 'Title',
	'description': 'Description'
}

data_chat_without_id = {
	'title': 'Title',
	'description': 'Description'
}

data_chat_for_chang = {
	'user_id': 1,
	'chat_id': 1,
	'title': 'new_Title',
	'description': 'new_Description'
}

def test__get_chats_info(service1):
	id_ = 1
	chat = service1.get_chats_info(id_)
	assert asdict(chat) == data_chat


def test__broken_get_chats_info(service2):
	id_ = 4
	with pytest.raises(errors.NoChat):
		service2.get_chats_info(id_)


def test__create_chat(service1):
	service1.create_chat(user_id=1, **data_chat_without_id)
	service1.chat_repo.create.assert_called_once()


def test__add_user_to_chat(service1):
	service1.add_user_to_chat(user_id=1, chat_id=1, user_id_to_added=2)
	service1.chat_participant_repo.add_user_to_chat.assert_called_once()


def test__broken_add_user_to_chat(service2):
	with pytest.raises(errors.NoCreatorsPermissions):
		service2.add_user_to_chat(user_id=2, chat_id=1, user_id_to_added=2)


def test__change_chat_info(service1):
	service1.change_chat_info(**data_chat_for_chang)
	service1.chat_repo.update.assert_called_once()


def test__broken_change_chat_info(service2):
	with pytest.raises(errors.NoCreatorsPermissions):
		service2.change_chat_info(**data_chat_for_chang)


def test__get_chats_users(service1):
	service1.get_chats_users(user_id=1, chat_id=1)
	service1.chat_participant_repo.get_chats_users.assert_called_once()

