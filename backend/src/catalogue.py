# Local commerce catalogue data for BillBhasha AI
# Data source: Local catalogue dataset
# Data status: Live local data
# Last updated: 10 August 2026

from datetime import datetime
from typing import Optional


CATALOGUE = {
    "wireless mouse": {
        "name": "Wireless Mouse",
        "price": 599,
        "stock": 12,
        "category": "Computer Accessories",
        "last_updated": "10 August 2026"
    },
    "keyboard": {
        "name": "Mechanical Keyboard",
        "price": 2499,
        "stock": 8,
        "category": "Computer Accessories",
        "last_updated": "10 August 2026"
    },
    "usb cable": {
        "name": "USB-C Cable",
        "price": 299,
        "stock": 25,
        "category": "Computer Accessories",
        "last_updated": "10 August 2026"
    },
    "power bank": {
        "name": "Power Bank 10000mAh",
        "price": 899,
        "stock": 15,
        "category": "Mobile Accessories",
        "last_updated": "10 August 2026"
    },
    "earphones": {
        "name": "Wireless Earphones",
        "price": 1499,
        "stock": 6,
        "category": "Audio",
        "last_updated": "10 August 2026"
    },
    "hdmi cable": {
        "name": "HDMI Cable 2m",
        "price": 199,
        "stock": 30,
        "category": "Computer Accessories",
        "last_updated": "10 August 2026"
    },
    "webcam": {
        "name": "HD Webcam 1080p",
        "price": 1999,
        "stock": 4,
        "category": "Computer Accessories",
        "last_updated": "10 August 2026"
    },
    "monitor": {
        "name": "24-inch LED Monitor",
        "price": 8999,
        "stock": 3,
        "category": "Computer Accessories",
        "last_updated": "10 August 2026"
    }
}


def lookup_product(product_name: str) -> Optional[dict]:
    """
    Look up a product in the local catalogue.
    
    Args:
        product_name: The name of the product to search for (case-insensitive)
    
    Returns:
        Product information dict if found, None otherwise
    """
    if not product_name:
        return None
    
    # Normalize input for better matching
    search_key = product_name.lower().strip()
    
    # Try exact match first
    if search_key in CATALOGUE:
        return CATALOGUE[search_key]
    
    # Try partial match
    for key, product in CATALOGUE.items():
        if search_key in key or key in search_key:
            return product
    
    return None


def calculate_order_total(product_name: str, quantity: int = 1) -> Optional[dict]:
    """
    Calculate total price for a given product and quantity.
    
    Args:
        product_name: The name of the product
        quantity: Number of units (default: 1)
    
    Returns:
        Order details dict with total price, or None if product not found
    """
    product = lookup_product(product_name)
    if not product:
        return None
    
    total = product["price"] * quantity
    
    return {
        "product": product["name"],
        "unit_price": product["price"],
        "quantity": quantity,
        "total": total,
        "stock_available": product["stock"] >= quantity,
        "last_updated": product["last_updated"]
    }
