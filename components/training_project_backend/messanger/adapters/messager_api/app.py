from typing import Tuple, Union


from classic.http_api import App
from classic.http_auth import Authenticator

from messanger.application import services

from . import auth, controllers


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    messanger: services.Messanger,
    profil: services.Profil) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    if is_dev_mode:
        authenticator.set_strategies(auth.dummy_strategy)
    else:
        authenticator.set_strategies(auth.jwt_strategy)


    app = App(prefix='/api')

    app.register(controllers.Messanger(authenticator=authenticator, messanger=messanger))
    app.register(controllers.Profil(authenticator=authenticator, profil=profil))

    return app