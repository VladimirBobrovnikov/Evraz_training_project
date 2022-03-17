from typing import Tuple, Union

import falcon

from classic.http_api import App
from classic.http_auth import Authenticator
from classic.http_auth import strategies as auth_strategies

from simple_shop.application import services

from . import auth, controllers


def create_app(
    is_dev_mode: bool,
    allow_origins: Union[str, Tuple[str, ...]],
    catalog: services.Catalog,
    checkout: services.Checkout,
    orders: services.Orders,
    customers: services.Customers,
) -> App:

    authenticator = Authenticator(app_groups=auth.ALL_GROUPS)

    if is_dev_mode:
        cors_middleware = falcon.CORSMiddleware(allow_origins='*')
        authenticator.set_strategies(auth.dummy_strategy)
    else:
        cors_middleware = falcon.CORSMiddleware(allow_origins=allow_origins)
        authenticator.set_strategies(auth_strategies.KeycloakOpenId())

    middleware = [cors_middleware]

    app = App(middleware=middleware, prefix='/api')

    app.register(controllers.Catalog(catalog=catalog))
    app.register(
        controllers.Checkout(authenticator=authenticator, checkout=checkout)
    )
    app.register(controllers.Orders(authenticator=authenticator, orders=orders))
    app.register(
        controllers.Customers(authenticator=authenticator, customers=customers)
    )

    return app
