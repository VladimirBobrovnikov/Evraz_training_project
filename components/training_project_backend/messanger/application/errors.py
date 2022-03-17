from evraz.classic.app.errors import AppError


class NoProduct(AppError):
    msg_template = "No product with SKU '{sku}'"
    code = 'shop.no_product'


class NoOrder(AppError):
    msg_template = "No order with number '{number}'"
    code = 'shop.no_order'


class NoCustomer(AppError):
    msg_template = "No customer with id '{id}'"
    code = 'shop.no_customer'


class EmptyCart(AppError):
    msg_template = "Cart is empty"
    code = 'shop.cart_is_empty'
