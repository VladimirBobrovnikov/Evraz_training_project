from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)

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
    Column('customer_id', ForeignKey('customers.id'), nullable=False),
)

cart_positions = Table(
    'cart_positions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('product_sku', ForeignKey('products.sku'), nullable=False),
    Column('cart_id', ForeignKey('carts.id'), nullable=False),
    Column('quantity', Integer, nullable=False),
)

orders = Table(
    'orders',
    metadata,
    Column('number', Integer, primary_key=True),
    Column('customer_id', ForeignKey('customers.id'), nullable=False),
)

order_lines = Table(
    'order_lines',
    metadata,
    Column('order_number', ForeignKey('orders.number'), primary_key=True),
    Column('product_sku', String, nullable=False),
    Column('product_title', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', Integer, nullable=False),
)

# yapf: enable
