"""migration

Revision ID: b18314c83d94
Revises: 
Create Date: 2022-02-04 13:32:00.776056+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'b18314c83d94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customers', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_customers'))
    )
    op.create_table(
        'products', sa.Column('sku', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('sku', name=op.f('pk_products'))
    )
    op.create_table(
        'carts', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['customer_id'], ['customers.id'],
            name=op.f('fk_carts_customer_id_customers')
        ), sa.PrimaryKeyConstraint('id', name=op.f('pk_carts'))
    )
    op.create_table(
        'orders', sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['customer_id'], ['customers.id'],
            name=op.f('fk_orders_customer_id_customers')
        ), sa.PrimaryKeyConstraint('number', name=op.f('pk_orders'))
    )
    op.create_table(
        'cart_positions', sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('product_sku', sa.String(), nullable=False),
        sa.Column('cart_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['cart_id'], ['carts.id'],
            name=op.f('fk_cart_positions_cart_id_carts')
        ),
        sa.ForeignKeyConstraint(
            ['product_sku'], ['products.sku'],
            name=op.f('fk_cart_positions_product_sku_products')
        ), sa.PrimaryKeyConstraint('id', name=op.f('pk_cart_positions'))
    )
    op.create_table(
        'order_lines', sa.Column('order_number', sa.Integer(), nullable=False),
        sa.Column('product_sku', sa.String(), nullable=False),
        sa.Column('product_title', sa.String(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['order_number'], ['orders.number'],
            name=op.f('fk_order_lines_order_number_orders')
        ), sa.PrimaryKeyConstraint('order_number', name=op.f('pk_order_lines'))
    )


def downgrade():
    op.drop_table('order_lines')
    op.drop_table('cart_positions')
    op.drop_table('orders')
    op.drop_table('carts')
    op.drop_table('products')
    op.drop_table('customers')
