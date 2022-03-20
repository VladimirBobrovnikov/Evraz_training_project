import pytest

from simple_shop.adapters.database import tables
from simple_shop.adapters.database.repositories import ProductsRepo


@pytest.fixture(scope='function')
def fill_db(session):
    products_data = [
        {
            'sku': 'U-001',
            'title': 'Отвертка',
            'description': 'Отвертка крестовая',
            'price': 234.2,
        },
        {
            'sku': 'U-002',
            'title': 'Ящик для инструментов',
            'description': 'Ящик с органайзером',
            'price': 1234.2
        },
    ]

    session.execute(tables.products.insert(), products_data)


@pytest.fixture(scope='function')
def repo(transaction_context):
    return ProductsRepo(context=transaction_context)


def test__find_by_keywords(repo, fill_db):
    result = repo.find_by_keywords(search='Ящик')

    assert len(result) == 1
    assert result[0].sku == 'U-002'


def test__find_by_keywords__multiple(repo, fill_db):
    result = repo.find_by_keywords(search='о')

    assert len(result) == 2


def test__find_by_keywords__with_limit(repo, fill_db):
    result = repo.find_by_keywords(search='о', limit=1)

    assert len(result) == 1


def test__find_by_keywords__with_offset(repo, fill_db):
    result = repo.find_by_keywords(search='о', offset=1)

    assert len(result) == 1
    assert result[0].sku == 'U-002'


def test__find_by_keywords__empty_result(repo, fill_db):
    result = repo.find_by_keywords(search='{')

    assert len(result) == 0


def test__add(repo, session, product_1):
    initial_data = session.execute(tables.products.select()).all()
    assert len(initial_data) == 0

    repo.add(product_1)

    data = session.execute(tables.products.select()).all()
    assert len(data) == 1
