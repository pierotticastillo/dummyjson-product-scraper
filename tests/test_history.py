import json
import tempfile
from unittest import mock

from src.history import comparar_precios


def _build_historial(entries: list[tuple[str, str, float]]) -> dict:
    """
    Construye un historial simulado.
    Cada entrada es (fecha, producto_id, precio_final_usd).
    """
    historial = {}
    for fecha, pid, precio in entries:
        if fecha not in historial:
            historial[fecha] = {}
        historial[fecha][pid] = {
            "titulo": f"Product {pid}",
            "marca": "Test",
            "categoria": "test",
            "precio_final_usd": precio,
            "fecha": fecha,
        }
    return historial


def test_comparar_sin_historial():
    assert comparar_precios({}) == {"subidos": [], "bajados": []}


def test_comparar_con_una_fecha():
    h = _build_historial([("2025-01-01", "p1", 100.0)])
    r = comparar_precios(h)
    assert r == {"subidos": [], "bajados": []}


def test_comparar_precio_subio():
    h = _build_historial([
        ("2025-01-01", "p1", 100.0),
        ("2025-02-01", "p1", 150.0),
    ])
    r = comparar_precios(h)
    assert len(r["subidos"]) == 1
    assert len(r["bajados"]) == 0
    assert r["subidos"][0]["cambio_porcentual"] == 50.0


def test_comparar_precio_bajo():
    h = _build_historial([
        ("2025-01-01", "p1", 100.0),
        ("2025-02-01", "p1", 80.0),
    ])
    r = comparar_precios(h)
    assert len(r["subidos"]) == 0
    assert len(r["bajados"]) == 1
    assert r["bajados"][0]["cambio_porcentual"] == -20.0


def test_comparar_precio_sin_cambio():
    h = _build_historial([
        ("2025-01-01", "p1", 100.0),
        ("2025-02-01", "p1", 100.0),
    ])
    r = comparar_precios(h)
    assert len(r["subidos"]) == 0
    assert len(r["bajados"]) == 0


def test_comparar_producto_aparece_despues():
    """Producto que no está en la primera fecha se ignora."""
    h = _build_historial([
        ("2025-01-01", "p1", 100.0),
        ("2025-02-01", "p1", 120.0),
        ("2025-02-01", "p2", 50.0),
    ])
    r = comparar_precios(h)
    # p2 no está en fecha_1, se ignora
    assert len(r["subidos"]) == 1
    assert r["subidos"][0]["titulo"] == "Product p1"


def test_comparar_varios_productos():
    h = _build_historial([
        ("2025-01-01", "p1", 100.0),
        ("2025-01-01", "p2", 50.0),
        ("2025-02-01", "p1", 120.0),
        ("2025-02-01", "p2", 40.0),
    ])
    r = comparar_precios(h)
    assert len(r["subidos"]) == 1  # p1 subió
    assert len(r["bajados"]) == 1  # p2 bajó
    assert r["subidos"][0]["cambio_porcentual"] == 20.0
    assert r["bajados"][0]["cambio_porcentual"] == -20.0


def test_fechas_en_resultado():
    h = _build_historial([
        ("2025-01-01", "p1", 100.0),
        ("2025-02-01", "p1", 150.0),
    ])
    r = comparar_precios(h)
    assert "fecha_antigua" in r
    assert "fecha_reciente" in r
    assert r["fecha_antigua"] < r["fecha_reciente"]
