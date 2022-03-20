from unittest.mock import Mock

import pytest
from falcon import testing

from simple_shop.adapters import shop_api
from simple_shop.application import services


@pytest.fixture(scope='function')
def checkout_service(cart):
    service = Mock(services.Checkout)
    service.get_cart = Mock(return_value=cart)

    return service


@pytest.fixture(scope='function')
def catalog_service(product_1):
    service = Mock(services.Catalog)
    service.get_product = Mock(return_value=product_1)

    return service


@pytest.fixture(scope='function')
def orders_service():
    service = Mock(services.Orders)

    return service


@pytest.fixture(scope='function')
def customers_service():
    service = Mock(services.Customers)

    return service


@pytest.fixture(scope='function')
def client(
    checkout_service,
    catalog_service,
    orders_service,
    customers_service,
):
    app = shop_api.create_app(
        is_dev_mode=True,
        allow_origins='*',
        catalog=catalog_service,
        checkout=checkout_service,
        orders=orders_service,
        customers=customers_service,
    )

    return testing.TestClient(app)
