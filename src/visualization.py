import logging
from datetime import datetime
from typing import List, Optional

from src.models import Product

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    _HAS_MPL = True
except ImportError:
    _HAS_MPL = False


def plot_product_stats(productos: List[Product], categoria: str) -> Optional[str]:
    """Genera histograma de precios y scatter precio vs rating."""
    if not _HAS_MPL:
        logger.warning("matplotlib no está instalado; omitiendo gráficos.")
        return None

    precios = [p.precio_final_usd for p in productos if p.precio_final_usd > 0]
    ratings = [p.rating for p in productos if p.rating > 0]

    if not precios:
        return None

    nombre = (
        f"productos_{categoria.replace(' ', '_')}_"
        f"{datetime.now().strftime('%Y-%m-%d')}.png"
    )

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].hist(precios, bins=10, color="C0", edgecolor="black")
    axs[0].set_title("Distribución de precios (USD)")
    axs[0].set_xlabel("Precio (USD)")
    axs[0].set_ylabel("Frecuencia")

    axs[1].scatter(precios, ratings, alpha=0.7)
    axs[1].set_title("Precio vs Rating")
    axs[1].set_xlabel("Precio (USD)")
    axs[1].set_ylabel("Rating")

    plt.suptitle(f"Productos - {categoria}")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(nombre)
    plt.close(fig)

    logger.info("Gráfico guardado: %s", nombre)
    return nombre


def plot_precio_tendencias(
    historial: dict, categoria: str = "all"
) -> Optional[str]:
    """Genera gráfico de líneas con tendencias de precios en el tiempo."""
    if not _HAS_MPL:
        logger.warning("matplotlib no está instalado; omitiendo tendencias.")
        return None

    if not historial or len(historial) < 2:
        return None

    fechas = sorted(historial.keys())
    productos_para_graficar = {}

    for pid in historial[fechas[0]]:
        producto = historial[fechas[0]][pid]
        if categoria != "all" and producto["categoria"] != categoria:
            continue
        if not all(pid in historial[f] for f in fechas[1:]):
            continue

        precios = [historial[f][pid]["precio_final_usd"] for f in fechas]
        if sum(1 for p in precios if p is not None) < 2:
            continue

        productos_para_graficar[pid] = {
            "titulo": producto["titulo"][:30],
            "precios": precios,
        }

    if not productos_para_graficar:
        return None

    # Limitar a 5 productos para legibilidad
    primeros = dict(list(productos_para_graficar.items())[:5])

    nombre = (
        f"tendencias_precios_{categoria}_"
        f"{datetime.now().strftime('%Y-%m-%d')}.png"
    )

    plt.figure(figsize=(12, 6))
    for pid, datos in primeros.items():
        plt.plot(fechas, datos["precios"], marker="o", label=datos["titulo"])

    plt.title(f"Tendencias de Precios - {categoria}")
    plt.xlabel("Fecha")
    plt.ylabel("Precio (USD)")
    plt.xticks(rotation=45, ha="right")
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(nombre, bbox_inches="tight")
    plt.close()

    logger.info("Gráfico de tendencias guardado: %s", nombre)
    return nombre
