from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Product:
    titulo: str
    marca: str
    categoria: str
    precio_usd: float
    descuento_pct: float
    precio_final_usd: float
    rating: float
    stock: int
    descripcion: str
    fecha_busqueda: str

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_api_item(item: dict) -> "Product":
        precio_original = item.get("price", 0)
        descuento = item.get("discountPercentage", 0)
        precio_final = round(precio_original * (1 - descuento / 100), 2)

        return Product(
            titulo=item.get("title", ""),
            marca=item.get("brand", ""),
            categoria=item.get("category", ""),
            precio_usd=precio_original,
            descuento_pct=descuento,
            precio_final_usd=precio_final,
            rating=item.get("rating", 0),
            stock=item.get("stock", 0),
            descripcion=item.get("description", "")[:80],
            fecha_busqueda=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )
