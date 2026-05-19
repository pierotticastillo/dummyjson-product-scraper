"""
Scraper de productos - API pública real
Fuente: dummyjson.com (productos de prueba, siempre disponible)

Este script permite extraer datos de productos de diversas categorías desde la API pública
dummyjson.com. Proporciona funcionalidades para buscar productos por categoría, analizar
datos estadísticos y exportar los resultados a archivos CSV.

Características principales:
- Búsqueda de productos por categoría o todos los productos
- Cálculo de precios con descuentos aplicados
- Análisis estadístico de precios y ratings
- Exportación de datos en formato CSV
- Manejo de errores robusto para conexiones y categorías inválidas

Uso:
    python3 scraper.py smartphones
    python3 scraper.py laptops --cantidad 10
    python3 scraper.py                     (trae todos mezclados)
    python3 scraper.py --categorias        (muestra categorías disponibles)

Ejemplos avanzados:
    python3 scraper.py smartphones --cantidad 50
    python3 scraper.py all --cantidad 100

Requisitos:
    - Python 3.7+
    - Bibliotecas: requests (se instala automáticamente si no está presente)
"""

import requests
import csv
import sys
import argparse
from datetime import datetime


# URL base de la API pública dummyjson.com
# Esta API proporciona datos de prueba de productos de comercio electrónico
BASE_URL = "https://dummyjson.com"


def listar_categorias() -> list[str]:
    """
    Obtiene la lista de categorías disponibles en la API.

    Realiza una solicitud GET al endpoint de categorías de la API dummyjson.com
    y devuelve la lista de categorías disponibles para buscar productos.

    Returns:
        list[str]: Lista de nombres de categorías disponibles

    Raises:
        requests.exceptions.RequestException: Si hay problemas de conexión o la solicitud falla
    """
    resp = requests.get(f"{BASE_URL}/products/category-list", timeout=10)
    resp.raise_for_status()
    return resp.json()


def buscar_productos(categoria: str, cantidad: int = 20) -> list[dict]:
    """
    Busca productos de una categoría específica en la API.

    Args:
        categoria (str): Categoría de productos a buscar ('all' para todos los productos)
        cantidad (int, optional): Número máximo de productos a obtener. Defaults to 20.

    Returns:
        list[dict]: Lista de productos con información procesada (precios con descuentos, etc.)

    Raises:
        SystemExit: Si hay errores de conexión o categoría no encontrada
    """
    # Construir URL según si se buscan todos los productos o una categoría específica
    if categoria == "all":
        url = f"{BASE_URL}/products?limit={cantidad}"
    else:
        url = f"{BASE_URL}/products/category/{categoria}?limit={cantidad}"

    print(f"\n🔍 Buscando categoría '{categoria}'...")

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("❌ Sin conexión a internet.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 404:
            print(f"❌ Categoría '{categoria}' no existe.")
            print("   Corré  python3 scraper.py --categorias  para ver las disponibles.")
        else:
            print(f"❌ Error HTTP: {e}")
        sys.exit(1)

    data = resp.json()
    items = data.get("products", [])
    total = data.get("total", len(items))

    print(f"✅ {total} productos en total. Procesando {len(items)}...\n")

    productos = []
    for item in items:
        # Calcular precio final aplicando descuento
        precio_original = item.get("price", 0)
        descuento = item.get("discountPercentage", 0)
        precio_final = round(precio_original * (1 - descuento / 100), 2)

        # Construir diccionario con información del producto
        productos.append({
            "titulo":           item.get("title", ""),
            "marca":            item.get("brand", ""),
            "categoria":        item.get("category", ""),
            "precio_usd":       precio_original,
            "descuento_pct":    descuento,
            "precio_final_usd": precio_final,
            "rating":           item.get("rating", 0),
            "stock":            item.get("stock", 0),
            "descripcion":      item.get("description", "")[:80],  # Truncar a 80 caracteres
            "fecha_busqueda":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    return productos


def mostrar_resumen(productos: list[dict], categoria: str):
    """
    Muestra un resumen estadístico de los productos encontrados.

    Genera un informe detallado con estadísticas de precios, ratings y rankings,
    incluyendo los top 5 productos más baratos y mejor valorados.

    Args:
        productos (list[dict]): Lista de productos a analizar
        categoria (str): Nombre de la categoría para mostrar en el encabezado

    Returns:
        None: Imprime el resumen directamente en la consola
    """
    if not productos:
        print("No hay productos.")
        return

    # Filtrar precios y ratings válidos (mayores que 0)
    precios = [p["precio_final_usd"] for p in productos if p["precio_final_usd"] > 0]
    ratings = [p["rating"] for p in productos if p["rating"] > 0]

    # Encabezado del resumen
    print("=" * 57)
    print(f"  📊 RESUMEN: {categoria.upper()}")
    print("=" * 57)
    print(f"  Productos analizados : {len(productos)}")
    print(f"  Precio más bajo      : USD {min(precios):.2f}")
    print(f"  Precio más alto      : USD {max(precios):.2f}")
    print(f"  Precio promedio      : USD {sum(precios)/len(precios):.2f}")
    print(f"  Rating promedio      : {sum(ratings)/len(ratings):.2f} / 5.0")
    print(f"  En stock total       : {sum(p['stock'] for p in productos)} unidades")
    print("=" * 57)

    # Top 5 productos más baratos
    print("\n  TOP 5 MÁS BARATOS (precio con descuento):")
    print("  " + "-" * 55)
    for i, p in enumerate(sorted(productos, key=lambda x: x["precio_final_usd"])[:5], 1):
        titulo = p["titulo"][:35] + "..." if len(p["titulo"]) > 35 else p["titulo"]
        print(f"  {i}. USD {p['precio_final_usd']:>7.2f}  {titulo}")

    # Top 5 productos mejor valorados
    print("\n  TOP 5 MEJOR VALORADOS:")
    print("  " + "-" * 55)
    for i, p in enumerate(sorted(productos, key=lambda x: x["rating"], reverse=True)[:5], 1):
        titulo = p["titulo"][:35] + "..." if len(p["titulo"]) > 35 else p["titulo"]
        print(f"  {i}. ⭐ {p['rating']:.2f}  {titulo}")
    print()


def guardar_csv(productos: list[dict], categoria: str) -> str:
    """
    Guarda la lista de productos en un archivo CSV.

    Genera un archivo CSV con nombre basado en la categoría y fecha actual,
    incluyendo todos los campos de información de los productos.

    Args:
        productos (list[dict]): Lista de productos a guardar
        categoria (str): Nombre de la categoría para el nombre del archivo

    Returns:
        str: Nombre del archivo CSV generado

    Note:
        El archivo se guarda en el directorio actual con formato:
        productos_{categoria}_{YYYY-MM-DD}.csv
    """
    nombre = f"productos_{categoria.replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d')}.csv"
    campos = list(productos[0].keys())

    with open(nombre, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos, delimiter=';')
        writer.writeheader()
        writer.writerows(productos)

    return nombre


def main():
    """
    Función principal del script.

    Parses los argumentos de línea de comandos y coordina el flujo principal:
    1. Lista categorías si se solicita
    2. Busca productos de la categoría especificada
    3. Muestra resumen estadístico
    4. Guarda resultados en CSV
    """
    parser = argparse.ArgumentParser(description="Scraper de productos con API pública")
    parser.add_argument("categoria", nargs="?", default="all",
                        help="Categoría a buscar (default: all)")
    parser.add_argument("--cantidad", type=int, default=20,
                        help="Cuántos productos traer (default: 20)")
    parser.add_argument("--categorias", action="store_true",
                        help="Listar todas las categorías disponibles")
    args = parser.parse_args()

    if args.categorias:
        # Modo lista de categorías
        print("\n📋 Categorías disponibles:\n")
        try:
            cats = listar_categorias()
            for cat in cats:
                print(f"   python3 scraper.py {cat}")
        except Exception as e:
            print(f"Error: {e}")
        print()
        return

    # Flujo principal: buscar, analizar y guardar
    productos = buscar_productos(args.categoria, args.cantidad)
    mostrar_resumen(productos, args.categoria)
    archivo = guardar_csv(productos, args.categoria)
    print(f"  💾 Guardado en: {archivo}")
    print(f"     Abrilo con: libreoffice --calc {archivo}\n")


if __name__ == "__main__":
    main()
