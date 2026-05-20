from src.models import Product
from src.analysis import calcular_resumen


def _make_product(precio: float, rating: float, stock: int = 1) -> Product:
    return Product(
        titulo=f"Product {precio}",
        marca="Test",
        categoria="test",
        precio_usd=precio,
        descuento_pct=0,
        precio_final_usd=precio,
        rating=rating,
        stock=stock,
        descripcion="",
        fecha_busqueda="2025-01-01 00:00",
    )


def test_resumen_vacio():
    r = calcular_resumen([])
    assert r.total == 0


def test_resumen_un_producto():
    p = _make_product(100.0, 4.5, 10)
    r = calcular_resumen([p])
    assert r.total == 1
    assert r.precio_min == 100.0
    assert r.precio_max == 100.0
    assert r.precio_promedio == 100.0
    assert r.rating_promedio == 4.5
    assert r.stock_total == 10


def test_resumen_varios_productos():
    productos = [
        _make_product(10.0, 3.0, 1),
        _make_product(50.0, 4.0, 5),
        _make_product(100.0, 5.0, 10),
    ]
    r = calcular_resumen(productos)
    assert r.total == 3
    assert r.precio_min == 10.0
    assert r.precio_max == 100.0
    assert r.precio_promedio == round(160 / 3, 2)
    assert r.rating_promedio == 4.0
    assert r.stock_total == 16


def test_top_baratos():
    productos = [
        _make_product(100.0, 3.0),
        _make_product(10.0, 4.0),
        _make_product(50.0, 5.0),
    ]
    r = calcular_resumen(productos, top_n=2)
    assert len(r.top_baratos) == 2
    assert r.top_baratos[0].precio_final_usd == 10.0
    assert r.top_baratos[1].precio_final_usd == 50.0


def test_top_valorados():
    productos = [
        _make_product(100.0, 3.0),
        _make_product(10.0, 5.0),
        _make_product(50.0, 4.0),
    ]
    r = calcular_resumen(productos, top_n=2)
    assert len(r.top_valorados) == 2
    assert r.top_valorados[0].rating == 5.0
    assert r.top_valorados[1].rating == 4.0


def test_ignora_productos_sin_precio():
    p = _make_product(0, 4.0, 1)
    r = calcular_resumen([p])
    assert r.total == 1
    assert r.precio_min == 0
    assert r.precio_promedio == 0
