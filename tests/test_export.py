import csv
import os
import tempfile
from unittest import mock

from src.export import guardar_csv
from src.models import Product


def _make_product(precio: float) -> Product:
    return Product(
        titulo="Test",
        marca="TestBrand",
        categoria="test",
        precio_usd=precio,
        descuento_pct=0,
        precio_final_usd=precio,
        rating=4.0,
        stock=10,
        descripcion="A test product",
        fecha_busqueda="2025-01-01 00:00",
    )


@mock.patch("src.export.datetime")
def test_guardar_csv_crea_archivo(mock_dt):
    mock_dt.now.return_value.strftime.return_value = "2025-01-01"
    nombre = guardar_csv([_make_product(50.0)], "test")
    assert nombre == "productos_test_2025-01-01.csv"
    assert os.path.exists(nombre)
    os.unlink(nombre)


@mock.patch("src.export.datetime")
def test_guardar_csv_contenido(mock_dt):
    mock_dt.now.return_value.strftime.return_value = "2025-01-01"
    nombre = guardar_csv([_make_product(50.0)], "test")
    with open(nombre, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        filas = list(reader)
        assert len(filas) == 1
        assert filas[0]["titulo"] == "Test"
        assert filas[0]["precio_final_usd"] == "50.0"
    os.unlink(nombre)
