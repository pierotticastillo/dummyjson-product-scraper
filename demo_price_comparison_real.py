#!/usr/bin/env python3
"""
Demo script to show how the price comparison works with real product data.
This creates artificial price history data using actual products from the API.
"""

import json
import os
import sys
import requests
from datetime import datetime, timedelta

# Configuration
HISTORY_DIR = "price_history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "price_history.json")
BASE_URL = "https://dummyjson.com"

def get_real_products():
    """Get real products from the API to use in our demo"""
    try:
        resp = requests.get(f"{BASE_URL}/products/category/smartphones?limit=5", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("products", [])
    except Exception as e:
        print(f"Error getting real products: {e}")
        return []

def create_realistic_demo_history():
    """Create a demo price history with real products and simulated price changes"""
    products = get_real_products()
    if not products:
        print("❌ Could not get real products from API")
        return

    os.makedirs(HISTORY_DIR, exist_ok=True)

    # Create demo data with different timestamps and prices
    demo_history = {}

    # First run - 3 days ago (base prices)
    fecha_1 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    demo_history[fecha_1] = {}

    for item in products:
        precio_original = item.get("price", 100)
        descuento = item.get("discountPercentage", 0)
        precio_final = round(precio_original * (1 - descuento / 100), 2)

        producto_id = f"{item.get('title', '')}_{item.get('brand', '')}_{item.get('category', '')}"
        demo_history[fecha_1][producto_id] = {
            "titulo": item.get("title", ""),
            "marca": item.get("brand", ""),
            "categoria": item.get("category", ""),
            "precio_final_usd": precio_final * 1.1,  # 10% more expensive 3 days ago
            "fecha": fecha_1
        }

    # Second run - 2 days ago (some price changes)
    fecha_2 = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    demo_history[fecha_2] = {}

    for item in products:
        precio_original = item.get("price", 100)
        descuento = item.get("discountPercentage", 0)
        precio_final = round(precio_original * (1 - descuento / 100), 2)

        producto_id = f"{item.get('title', '')}_{item.get('brand', '')}_{item.get('category', '')}"
        demo_history[fecha_2][producto_id] = {
            "titulo": item.get("title", ""),
            "marca": item.get("brand", ""),
            "categoria": item.get("category", ""),
            "precio_final_usd": precio_final * 1.05,  # 5% more expensive 2 days ago
            "fecha": fecha_2
        }

    # Third run - 1 day ago (current prices)
    fecha_3 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    demo_history[fecha_3] = {}

    for item in products:
        precio_original = item.get("price", 100)
        descuento = item.get("discountPercentage", 0)
        precio_final = round(precio_original * (1 - descuento / 100), 2)

        producto_id = f"{item.get('title', '')}_{item.get('brand', '')}_{item.get('category', '')}"
        demo_history[fecha_3][producto_id] = {
            "titulo": item.get("title", ""),
            "marca": item.get("brand", ""),
            "categoria": item.get("category", ""),
            "precio_final_usd": precio_final,  # Current prices
            "fecha": fecha_3
        }

    # Save the demo history
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(demo_history, f, indent=2, ensure_ascii=False)

    print(f"✅ Demo price history created with real products and simulated price changes!")
    print(f"   File: {HISTORY_FILE}")
    print(f"   Dates: {fecha_1} to {fecha_3}")
    print(f"   Products: {len(products)} real smartphones from the API")
    print(f"   Price trends: Products were more expensive 3 days ago, cheaper now")
    print("\nNow run: python3 scraper.py smartphones --comparar")
    print("To see the price comparison with real products!")

    print("\nOr run: python3 scraper.py smartphones --tendencias")
    print("To see the price trends graph!")

if __name__ == "__main__":
    create_realistic_demo_history()