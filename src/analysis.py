from dataclasses import dataclass, field
from typing import List
from src.models import Product


@dataclass
class Resumen:
    total: int
    precio_min: float
    precio_max: float
    precio_promedio: float
    rating_promedio: float
    stock_total: int
    top_baratos: List[Product] = field(default_factory=list)
    top_valorados: List[Product] = field(default_factory=list)


def calcular_resumen(productos: List[Product], top_n: int = 5) -> Resumen:
    """Calcula estadísticas descriptivas de una lista de productos."""
    if not productos:
        return Resumen(total=0, precio_min=0, precio_max=0,
                       precio_promedio=0, rating_promedio=0, stock_total=0)

    precios = [p.precio_final_usd for p in productos if p.precio_final_usd > 0]
    ratings = [p.rating for p in productos if p.rating > 0]

    if not precios:
        return Resumen(total=len(productos), precio_min=0, precio_max=0,
                       precio_promedio=0, rating_promedio=0, stock_total=0)

    return Resumen(
        total=len(productos),
        precio_min=min(precios),
        precio_max=max(precios),
        precio_promedio=round(sum(precios) / len(precios), 2),
        rating_promedio=round(sum(ratings) / len(ratings), 2) if ratings else 0,
        stock_total=sum(p.stock for p in productos),
        top_baratos=sorted(productos, key=lambda x: x.precio_final_usd)[:top_n],
        top_valorados=sorted(productos, key=lambda x: x.rating, reverse=True)[:top_n],
    )
