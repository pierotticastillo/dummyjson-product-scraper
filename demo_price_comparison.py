#!/usr/bin/env python3
"""
Demo script to show how the price comparison works with simulated price changes.
This creates artificial price history data to demonstrate the comparison functionality.
"""

import json
import os
from datetime import datetime, timedelta

# Configuration
HISTORY_DIR = "price_history"
HISTORY_FILE = os.path.join(HISTORY_DIR, "price_history.json")

def create_demo_history():
    """Create a demo price history with simulated price changes"""
    os.makedirs(HISTORY_DIR, exist_ok=True)

    # Create demo data with different timestamps and prices
    demo_history = {}

    # First run - 3 days ago
    fecha_1 = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
    demo_history[fecha_1] = {
        "iPhone 5s_Apple_smartphones": {
            "titulo": "iPhone 5s",
            "marca": "Apple",
            "categoria": "smartphones",
            "precio_final_usd": 200.00,
            "fecha": fecha_1
        },
        "iPhone 6_Apple_smartphones": {
            "titulo": "iPhone 6",
            "marca": "Apple",
            "categoria": "smartphones",
            "precio_final_usd": 300.00,
            "fecha": fecha_1
        },
        "Samsung Galaxy S22_Samsung_smartphones": {
            "titulo": "Samsung Galaxy S22",
            "marca": "Samsung",
            "categoria": "smartphones",
            "precio_final_usd": 800.00,
            "fecha": fecha_1
        }
    }

    # Second run - 2 days ago (some prices changed)
    fecha_2 = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
    demo_history[fecha_2] = {
        "iPhone 5s_Apple_smartphones": {
            "titulo": "iPhone 5s",
            "marca": "Apple",
            "categoria": "smartphones",
            "precio_final_usd": 180.00,  # Price dropped
            "fecha": fecha_2
        },
        "iPhone 6_Apple_smartphones": {
            "titulo": "iPhone 6",
            "marca": "Apple",
            "categoria": "smartphones",
            "precio_final_usd": 320.00,  # Price increased
            "fecha": fecha_2
        },
        "Samsung Galaxy S22_Samsung_smartphones": {
            "titulo": "Samsung Galaxy S22",
            "marca": "Samsung",
            "categoria": "smartphones",
            "precio_final_usd": 750.00,  # Price dropped
            "fecha": fecha_2
        }
    }

    # Third run - 1 day ago (more changes)
    fecha_3 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    demo_history[fecha_3] = {
        "iPhone 5s_Apple_smartphones": {
            "titulo": "iPhone 5s",
            "marca": "Apple",
            "categoria": "smartphones",
            "precio_final_usd": 170.00,  # Price dropped more
            "fecha": fecha_3
        },
        "iPhone 6_Apple_smartphones": {
            "titulo": "iPhone 6",
            "marca": "Apple",
            "categoria": "smartphones",
            "precio_final_usd": 350.00,  # Price increased more
            "fecha": fecha_3
        },
        "Samsung Galaxy S22_Samsung_smartphones": {
            "titulo": "Samsung Galaxy S22",
            "marca": "Samsung",
            "categoria": "smartphones",
            "precio_final_usd": 700.00,  # Price dropped more
            "fecha": fecha_3
        }
    }

    # Save the demo history
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(demo_history, f, indent=2, ensure_ascii=False)

    print(f"✅ Demo price history created with simulated price changes!")
    print(f"   File: {HISTORY_FILE}")
    print(f"   Dates: {fecha_1} to {fecha_3}")
    print(f"   Products: 3 smartphones with varying price trends")
    print("\nNow run: python3 scraper.py --comparar")
    print("To see the price comparison in action!")

if __name__ == "__main__":
    create_demo_history()