import argparse
import logging
import sys

from src.api import (
    listar_categorias,
    buscar_productos,
    ConnectionError_,
    CategoryNotFoundError,
    HTTPError_,
)
from src.history import guardar_historial, cargar_historial, comparar_precios
from src.analysis import calcular_resumen
from src.visualization import plot_product_stats, plot_precio_tendencias
from src.export import guardar_csv

logger = logging.getLogger(__name__)


def configurar_logging(verbose: bool = False) -> None:
    nivel = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=nivel,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )


def mostrar_resumen(productos, categoria: str) -> None:
    if not productos:
        print("No hay productos.")
        return

    r = calcular_resumen(productos)

    print("=" * 57)
    print(f"  📊 RESUMEN: {categoria.upper()}")
    print("=" * 57)
    print(f"  Productos analizados : {r.total}")
    print(f"  Precio más bajo      : USD {r.precio_min:.2f}")
    print(f"  Precio más alto      : USD {r.precio_max:.2f}")
    print(f"  Precio promedio      : USD {r.precio_promedio:.2f}")
    print(f"  Rating promedio      : {r.rating_promedio:.2f} / 5.0")
    print(f"  En stock total       : {r.stock_total} unidades")
    print("=" * 57)

    print("\n  TOP 5 MÁS BARATOS (precio con descuento):")
    print("  " + "-" * 55)
    for i, p in enumerate(r.top_baratos, 1):
        titulo = p.titulo[:35] + "..." if len(p.titulo) > 35 else p.titulo
        print(f"  {i}. USD {p.precio_final_usd:>7.2f}  {titulo}")

    print("\n  TOP 5 MEJOR VALORADOS:")
    print("  " + "-" * 55)
    for i, p in enumerate(r.top_valorados, 1):
        titulo = p.titulo[:35] + "..." if len(p.titulo) > 35 else p.titulo
        print(f"  {i}. ⭐ {p.rating:.2f}  {titulo}")
    print()


def mostrar_comparacion_precios(cambios: dict) -> None:
    if not cambios.get("subidos") and not cambios.get("bajados"):
        print("No se detectaron cambios significativos en los precios.")
        return

    print("=" * 70)
    print(f"  📈 COMPARACIÓN DE PRECIOS")
    print(f"  Desde: {cambios['fecha_antigua']}")
    print(f"  Hasta: {cambios['fecha_reciente']}")
    print("=" * 70)

    for etiqueta, simbolo, items in [
        ("PRODUCTOS QUE SUBIERON DE PRECIO", "🔺", cambios.get("subidos", [])),
        ("PRODUCTOS QUE BAJARON DE PRECIO", "🔻", cambios.get("bajados", [])),
    ]:
        if items:
            print(f"\n  {simbolo} {etiqueta} ({len(items)}):")
            print("  " + "-" * 68)
            for i, prod in enumerate(items[:10], 1):
                titulo = (
                    prod["titulo"][:40] + "..."
                    if len(prod["titulo"]) > 40
                    else prod["titulo"]
                )
                signo = "+" if prod["cambio_porcentual"] > 0 else ""
                print(f"  {i}. {titulo}")
                print(
                    f"     USD {prod['precio_anterior']:.2f} → "
                    f"USD {prod['precio_final_usd']:.2f} "
                    f"({signo}{prod['cambio_porcentual']:.1f}%)"
                )
                print(f"     {prod['marca']} - {prod['categoria']}")

    print("\n" + "=" * 70)


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scraper de productos con API pública")
    parser.add_argument(
        "categoria",
        nargs="?",
        default="all",
        help="Categoría a buscar (default: all)",
    )
    parser.add_argument(
        "--cantidad",
        type=int,
        default=20,
        help="Cuántos productos traer (default: 20)",
    )
    parser.add_argument(
        "--categorias",
        action="store_true",
        help="Listar todas las categorías disponibles",
    )
    parser.add_argument(
        "--comparar",
        action="store_true",
        help="Comparar precios con historial anterior",
    )
    parser.add_argument(
        "--tendencias",
        action="store_true",
        help="Generar gráfico de tendencias de precios",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar información de depuración",
    )
    return parser


def main() -> None:
    parser = setup_parser()
    args = parser.parse_args()

    configurar_logging(args.verbose)

    if args.categorias:
        print("\n📋 Categorías disponibles:\n")
        try:
            for cat in listar_categorias():
                print(f"   python3 scraper.py {cat}")
        except Exception as e:
            logger.error("Error al listar categorías: %s", e)
        print()
        return

    print(f"\n🔍 Buscando categoría '{args.categoria}'...")
    try:
        productos = buscar_productos(args.categoria, args.cantidad)
    except ConnectionError_:
        print("❌ Sin conexión a internet.")
        sys.exit(1)
    except CategoryNotFoundError as e:
        print(f"❌ {e}")
        print("   Corré  python3 scraper.py --categorias  para ver las disponibles.")
        sys.exit(1)
    except HTTPError_ as e:
        print(f"❌ {e}")
        sys.exit(1)

    print(f"✅ {len(productos)} productos procesados.\n")

    mostrar_resumen(productos, args.categoria)

    if not productos:
        return

    archivo = guardar_csv(productos, args.categoria)
    print(f"  💾 Guardado en: {archivo}")
    print(f"     Abrilo con: libreoffice --calc {archivo}\n")

    guardar_historial(productos)

    try:
        plot_product_stats(productos, args.categoria)
    except Exception as e:
        logger.error("Error al generar gráfico: %s", e)

    if args.comparar:
        print("\n🔍 Comparando precios con historial...")
        historial = cargar_historial()
        if not historial or len(historial) < 2:
            print("⚠️ No hay suficiente historial para comparar precios.")
        else:
            mostrar_comparacion_precios(comparar_precios(historial))

    if args.tendencias:
        print("\n📊 Generando gráfico de tendencias...")
        historial = cargar_historial()
        if not historial or len(historial) < 2:
            print("⚠️ No hay suficiente historial para graficar tendencias.")
        else:
            plot_precio_tendencias(historial, args.categoria)
