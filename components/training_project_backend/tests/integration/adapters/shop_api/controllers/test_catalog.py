def test__on_get_show_product(client, catalog_service, product_1):
    product_1.sku = 'FOO'
    product_1.title = 'BAR'
    product_1.description = 'SPAM'
    product_1.price = 100.1

    catalog_service.get_product.return_value = product_1

    expected = {
        'sku': product_1.sku,
        'title': product_1.title,
        'description': product_1.description,
        'price': product_1.price,
    }

    result = client.simulate_get('/api/catalog/show_product')

    assert result.status_code == 200
    assert result.json == expected
