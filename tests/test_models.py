from src.models import Product


SAMPLE_ITEM = {
    "title": "iPhone 13 Pro",
    "brand": "Apple",
    "category": "smartphones",
    "price": 1099.99,
    "discountPercentage": 9.37,
    "rating": 4.12,
    "stock": 56,
    "description": "The iPhone 13 Pro is a cutting-edge smartphone with advanced features.",
}


def test_from_api_item():
    p = Product.from_api_item(SAMPLE_ITEM)
    assert p.titulo == "iPhone 13 Pro"
    assert p.marca == "Apple"
    assert p.categoria == "smartphones"
    assert p.precio_usd == 1099.99
    assert p.descuento_pct == 9.37
    assert p.precio_final_usd == 996.92  # 1099.99 * (1 - 9.37/100)
    assert p.rating == 4.12
    assert p.stock == 56
    assert "cutting-edge" in p.descripcion
    assert len(p.descripcion) <= 80
    assert p.fecha_busqueda is not None


def test_from_api_item_empty_values():
    p = Product.from_api_item({})
    assert p.titulo == ""
    assert p.marca == ""
    assert p.precio_usd == 0
    assert p.descuento_pct == 0
    assert p.precio_final_usd == 0
    assert p.rating == 0
    assert p.stock == 0


def test_to_dict():
    p = Product.from_api_item(SAMPLE_ITEM)
    d = p.to_dict()
    assert d["titulo"] == "iPhone 13 Pro"
    assert d["precio_final_usd"] == 996.92
    assert "fecha_busqueda" in d


def test_precio_final_con_descuento():
    item = SAMPLE_ITEM.copy()
    item["price"] = 100
    item["discountPercentage"] = 25
    p = Product.from_api_item(item)
    assert p.precio_final_usd == 75.00


def test_precio_final_sin_descuento():
    item = SAMPLE_ITEM.copy()
    item["price"] = 100
    item["discountPercentage"] = 0
    p = Product.from_api_item(item)
    assert p.precio_final_usd == 100.00
