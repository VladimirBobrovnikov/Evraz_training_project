"""migration

Revision ID: 141436daef08
Revises: b18314c83d94
Create Date: 2022-02-04 13:44:02.149049+00:00

"""
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import Column, Float, Integer, MetaData, String, Table

revision = '141436daef08'
down_revision = 'b18314c83d94'
branch_labels = None
depends_on = None

# yapf: disable
customers_data = [
    {'id': 1, 'email': 'foo@example.com'},
    {'id': 2, 'email': 'bar@example.com'},
    {'id': 3, 'email': 'spam@example.com'},
    {'id': 4, 'email': None},
]

products_data = [
    {'sku': 'U-001', 'title': 'Отвертка',
     'description': 'Отвертка крестовая', 'price': 234.2},
    {'sku': 'U-002', 'title': 'Ящик для инструментов',
     'description': 'Ящик с органайзером', 'price': 1234.2},
    {'sku': 'U-003', 'title': 'Гитара классическая',
     'description': 'Верхняя дека массив кедра', 'price': 50234.2},
]

carts_data = [
    {'id': 1, 'customer_id': 1},
    {'id': 2, 'customer_id': 2},
    {'id': 3, 'customer_id': 4},
]

cart_positions_data = [
    {'id': 1, 'product_sku': 'U-001', 'cart_id': 1, 'quantity': 1},
    {'id': 2, 'product_sku': 'U-002', 'cart_id': 1, 'quantity': 1},
    {'id': 3, 'product_sku': 'U-001', 'cart_id': 2, 'quantity': 3},
    {'id': 4, 'product_sku': 'U-003', 'cart_id': 3, 'quantity': 1},
]

orders_data = [
    {'number': 1, 'customer_id': 3},
]

order_lines_data = [
    {'order_number': 1, 'product_sku': 'U-001',
     'product_title': 'Отвертка', 'price': 232.1, 'quantity': 1},
]

# yapf: enable

metadata = MetaData()

customers = Table(
    'customers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=True),
)

products = Table(
    'products',
    metadata,
    Column('sku', String, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=False),
    Column('price', Float, nullable=False),
)

carts = Table(
    'carts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('customer_id', Integer, nullable=False),
)

cart_positions = Table(
    'cart_positions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('product_sku', String, nullable=False),
    Column('cart_id', Integer, nullable=False),
    Column('quantity', Integer, nullable=False),
)

orders = Table(
    'orders',
    metadata,
    Column('number', Integer, primary_key=True),
    Column('customer_id', Integer, nullable=False),
)

order_lines = Table(
    'order_lines',
    metadata,
    Column('order_number', Integer, primary_key=True),
    Column('product_sku', String, nullable=False),
    Column('product_title', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Integer, nullable=False),
)


def upgrade():
    op.bulk_insert(customers, customers_data)
    op.bulk_insert(products, products_data)
    op.bulk_insert(carts, carts_data)
    op.bulk_insert(cart_positions, cart_positions_data)
    op.bulk_insert(orders, orders_data)
    op.bulk_insert(order_lines, order_lines_data)


def downgrade():
    op.execute(f'DELETE FROM {customers.fullname}')
    op.execute(f'DELETE FROM {products.fullname}')
    op.execute(f'DELETE FROM {carts.fullname}')
    op.execute(f'DELETE FROM {cart_positions.fullname}')
    op.execute(f'DELETE FROM {orders.fullname}')
    op.execute(f'DELETE FROM {order_lines.fullname}')
