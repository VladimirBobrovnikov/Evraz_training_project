from classic.sql_storage import TransactionContext
from sqlalchemy import create_engine

from messanger.adapters import messager_api, database
from messanger.application import services


class Settings:
	db = database.Settings()
	app = messager_api.Settings()


class DB:
	engine = create_engine(Settings.db.DB_URL)
	database.metadata.create_all(engine)

	context = TransactionContext(bind=engine, expire_on_commit=False)

	user_repo = database.repositories.UsersRepo(context=context)
	chat_repo = database.repositories.ChatRepo(context=context)
	chats_participant_repo = database.repositories.ChatParticipantRepo(context=context)
	message_repo = database.repositories.MessageRepo(context=context)


class Application:
	messanger = services.Messanger(
		chat_repo=DB.chat_repo,
		user_repo=DB.user_repo,
		chat_participant_repo=DB.chats_participant_repo,
		message_repo=DB.message_repo,
	)
	profil = services.Profil(
		user_repo=DB.user_repo,
	)


class Aspects:
	services.join_points.join(DB.context)
	messager_api.join_points.join(DB.context)


app = messager_api.create_app(
	is_dev_mode=Settings.app.IS_DEV_MODE,
	allow_origins=Settings.app.ALLOW_ORIGINS,
	messanger=Application.messanger,
	profil=Application.profil)

if __name__ == "__main__":
	from wsgiref import simple_server

	with simple_server.make_server('', 8000, app=app) as server:
		print('server with port 8000')
		server.serve_forever()
