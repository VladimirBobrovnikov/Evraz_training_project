from evraz.classic.components import component
from evraz.classic.http_auth import (
    authenticate,
    authenticator_needed,
    authorize,
)

from simple_shop.application import services

from .auth import Groups, Permissions
from .join_points import join_point


@component
class Catalog:
    catalog: services.Catalog

    @join_point
    def on_get_show_product(self, request, response):
        product = self.catalog.get_product(**request.params)
        response.media = {
            'sku': product.sku,
            'title': product.title,
            'description': product.description,
            'price': product.price,
        }

    @join_point
    def on_get_search_products(self, request, response):
        products = self.catalog.search_products(**request.params)
        response.media = [
            {
                'sku': product.sku,
                'title': product.title,
                'description': product.description,
                'price': product.price,
            } for product in products
        ]


@authenticator_needed
@component
class Checkout:
    checkout: services.Checkout

    @join_point
    @authenticate
    def on_get_show_cart(self, request, response):
        cart = self.checkout.get_cart(request.context.client.user_id)
        response.media = {
            'positions': [
                {
                    'product_sku': position.product.sku,
                    'product_price': position.product.price,
                    'quantity': position.quantity,
                } for position in cart.positions
            ]
        }

    @join_point
    @authenticate
    def on_post_add_product_to_cart(self, request, response):
        self.checkout.add_product_to_cart(
            customer_id=request.context.client.user_id,
            **request.media,
        )

    @join_point
    @authenticate
    def on_post_remove_product_from_cart(self, request, response):
        self.checkout.remove_product_from_cart(
            customer_id=request.context.client.user_id,
            **request.media,
        )

    @join_point
    @authenticate
    def on_post_register_order(self, request, response):
        order_number = self.checkout.create_order(
            customer_id=request.context.client.user_id,
        )
        response.media = {'order_number': order_number}


@authenticator_needed
@component
class Orders:
    orders: services.Orders

    @join_point
    @authenticate
    def on_get_show_order(self, request, response):
        order = self.orders.get_order(
            customer_id=request.context.client.user_id,
            **request.params,
        )
        response.media = {
            'number': order.number,
            'positions': [
                {
                    'sku': line.product_sku,
                    'product_title': line.product_title,
                    'quantity': line.quantity,
                    'price': line.price,
                } for line in order.lines
            ]
        }


@authenticator_needed
@component
class Customers:
    customers: services.Customers

    @join_point
    @authenticate
    @authorize(Groups.ADMINS | Permissions.FULL_CONTROL)
    def on_get_show_info(self, request, response):
        customer = self.customers.get_info(**request.params)

        response.media = {
            'customer_id': customer.id,
            'email': customer.email,
        }
