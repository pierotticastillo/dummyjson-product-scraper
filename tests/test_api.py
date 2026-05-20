from unittest import mock

import pytest
import requests

from src.api import (
    buscar_productos,
    listar_categorias,
    ConnectionError_,
    CategoryNotFoundError,
    HTTPError_,
)


@mock.patch("src.api.requests.get")
def test_listar_categorias(mock_get):
    mock_get.return_value.json.return_value = ["smartphones", "laptops"]
    mock_get.return_value.raise_for_status.return_value = None

    cats = listar_categorias()
    assert cats == ["smartphones", "laptops"]
    mock_get.assert_called_once_with(
        "https://dummyjson.com/products/category-list", timeout=10
    )


@mock.patch("src.api.requests.get")
def test_buscar_productos_all(mock_get):
    mock_get.return_value.json.return_value = {
        "products": [
            {
                "title": "Test",
                "brand": "T",
                "category": "test",
                "price": 100,
                "discountPercentage": 10,
                "rating": 4,
                "stock": 5,
                "description": "Desc",
            }
        ]
    }
    mock_get.return_value.raise_for_status.return_value = None

    productos = buscar_productos("all", cantidad=1)
    assert len(productos) == 1
    assert productos[0].titulo == "Test"
    mock_get.assert_called_once_with(
        "https://dummyjson.com/products?limit=1", timeout=10
    )


@mock.patch("src.api.requests.get")
def test_buscar_productos_por_categoria(mock_get):
    mock_get.return_value.json.return_value = {"products": []}
    mock_get.return_value.raise_for_status.return_value = None

    buscar_productos("smartphones")
    mock_get.assert_called_once_with(
        "https://dummyjson.com/products/category/smartphones?limit=20", timeout=10
    )


@mock.patch("src.api.requests.get")
def test_buscar_productos_sin_conexion(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError()
    with pytest.raises(ConnectionError_):
        buscar_productos("all")


@mock.patch("src.api.requests.get")
def test_buscar_productos_404(mock_get):
    resp = mock.MagicMock()
    resp.status_code = 404
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error", response=resp
    )
    mock_get.return_value = resp

    with pytest.raises(CategoryNotFoundError):
        buscar_productos("xyz")


@mock.patch("src.api.requests.get")
def test_buscar_productos_500(mock_get):
    resp = mock.MagicMock()
    resp.status_code = 500
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error", response=resp
    )
    mock_get.return_value = resp

    with pytest.raises(HTTPError_):
        buscar_productos("all")
