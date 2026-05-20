"""
Scraper de productos - API pública real
Fuente: dummyjson.com (productos de prueba, siempre disponible)

Uso:
    python3 scraper.py smartphones
    python3 scraper.py laptops --cantidad 10
    python3 scraper.py                     (trae todos mezclados)
    python3 scraper.py --categorias        (muestra categorías disponibles)
    python3 scraper.py smartphones --comparar
    python3 scraper.py all --tendencias
"""

from src.cli import main

if __name__ == "__main__":
    main()
