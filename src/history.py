import json
import os
import logging
from datetime import datetime
from typing import List
from src.config import HISTORY_DIR, HISTORY_FILE
from src.models import Product

logger = logging.getLogger(__name__)


def guardar_historial(productos: List[Product]) -> None:
    """Guarda los precios actuales en el historial JSON."""
    os.makedirs(HISTORY_DIR, exist_ok=True)

    historial = _cargar_historial_raw()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historial[fecha_actual] = {}

    for producto in productos:
        key = f"{producto.titulo}_{producto.marca}_{producto.categoria}"
        historial[fecha_actual][key] = {
            "titulo": producto.titulo,
            "marca": producto.marca,
            "categoria": producto.categoria,
            "precio_final_usd": producto.precio_final_usd,
            "fecha": fecha_actual,
        }

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

    logger.info("Historial guardado: %s", HISTORY_FILE)


def _cargar_historial_raw() -> dict:
    """Carga el archivo JSON del historial si existe."""
    if not os.path.exists(HISTORY_FILE):
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def cargar_historial() -> dict:
    """Carga y devuelve el historial de precios."""
    return _cargar_historial_raw()


def comparar_precios(historial: dict) -> dict:
    """Compara el precio más reciente vs el más antiguo."""
    if not historial or len(historial) < 2:
        return {"subidos": [], "bajados": []}

    fechas = sorted(historial.keys())
    antigua, reciente = fechas[0], fechas[-1]
    productos_antiguos = historial[antigua]
    productos_recientes = historial[reciente]

    subidos, bajados = [], []

    for pid, prod_reciente in productos_recientes.items():
        if pid not in productos_antiguos:
            continue
        prod_antiguo = productos_antiguos[pid]
        precio_anterior = prod_antiguo["precio_final_usd"]
        precio_actual = prod_reciente["precio_final_usd"]

        if precio_anterior <= 0:
            continue

        cambio_pct = ((precio_actual - precio_anterior) / precio_anterior) * 100
        cambio_abs = precio_actual - precio_anterior

        entry = dict(prod_reciente)
        entry.update({
            "precio_anterior": precio_anterior,
            "cambio_porcentual": round(cambio_pct, 2),
            "cambio_absoluto": round(cambio_abs, 2),
            "fecha_anterior": antigua,
            "fecha_actual": reciente,
        })

        if cambio_pct > 0:
            subidos.append(entry)
        elif cambio_pct < 0:
            bajados.append(entry)

    subidos.sort(key=lambda x: x["cambio_porcentual"], reverse=True)
    bajados.sort(key=lambda x: x["cambio_porcentual"])

    return {
        "subidos": subidos,
        "bajados": bajados,
        "fecha_antigua": antigua,
        "fecha_reciente": reciente,
    }
