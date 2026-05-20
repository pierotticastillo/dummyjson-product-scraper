import requests
from typing import List
from src.config import BASE_URL
from src.models import Product


class APIError(Exception):
    """Error base para errores de API."""


class ConnectionError_(APIError):
    """Sin conexión a internet."""


class CategoryNotFoundError(APIError):
    """Categoría no encontrada."""


class HTTPError_(APIError):
    """Error HTTP en la solicitud."""


def listar_categorias() -> List[str]:
    """Obtiene la lista de categorías disponibles."""
    resp = requests.get(f"{BASE_URL}/products/category-list", timeout=10)
    resp.raise_for_status()
    return resp.json()


def buscar_productos(categoria: str, cantidad: int = 20) -> List[Product]:
    """Busca productos por categoría y devuelve una lista de Product."""
    if categoria == "all":
        url = f"{BASE_URL}/products?limit={cantidad}"
    else:
        url = f"{BASE_URL}/products/category/{categoria}?limit={cantidad}"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ConnectionError_("Sin conexión a internet.")
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 404:
            raise CategoryNotFoundError(
                f"La categoría '{categoria}' no existe."
            )
        raise HTTPError_(f"Error HTTP: {e}")

    data = resp.json()
    return [Product.from_api_item(item) for item in data.get("products", [])]
