import csv
import logging
from datetime import datetime
from typing import List

from src.config import CSV_DELIMITER
from src.models import Product

logger = logging.getLogger(__name__)


def guardar_csv(productos: List[Product], categoria: str) -> str:
    """Guarda una lista de productos en un archivo CSV."""
    if not productos:
        return ""

    nombre = (
        f"productos_{categoria.replace(' ', '_')}_"
        f"{datetime.now().strftime('%Y-%m-%d')}.csv"
    )
    campos = list(productos[0].to_dict().keys())

    with open(nombre, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, delimiter=CSV_DELIMITER)
        writer.writeheader()
        for p in productos:
            writer.writerow(p.to_dict())

    logger.info("CSV guardado: %s", nombre)
    return nombre
