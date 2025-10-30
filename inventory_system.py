"""inventory_system

Simple inventory management for the SE_Lab_5 assignment.
Handles adding/removing items, checking stock, and saving/loading data.
"""

import json
import logging
from datetime import datetime

# Global inventory dictionary
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Add quantity of a specific item to the inventory.

    Args:
        item (str): Name of the item to add.
        qty (int): Quantity to add.
        logs (list, optional): List to store action logs.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.warning(
            "Invalid input types for add_item: item=%s, qty=%s",
            item,
            qty,
        )
        return

    if qty < 0:
        logging.warning("Quantity cannot be negative for item: %s", item)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """Remove quantity of a specific item from inventory.

    Args:
        item (str): Item name.
        qty (int): Quantity to remove.
    """
    try:
        if item not in stock_data:
            logging.warning("Attempted to remove non-existent item: %s", item)
            return

        if qty <= 0:
            logging.warning("Quantity to remove must be positive: %s", item)
            return

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("Removed item completely: %s", item)
        else:
            logging.info("Removed %d of %s", qty, item)
    except KeyError as exc:
        logging.error("Error removing item %s: %s", item, exc)


def get_qty(item):
    """Return the quantity of a specific item."""
    return stock_data.get(item, 0)


def load_data(file_name="inventory.json"):
    """Load inventory data from a JSON file."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            stock_data.clear()
            stock_data.update(data)
            logging.info("Loaded inventory data from %s", file_name)
    except FileNotFoundError:
        logging.warning(
            "File not found: %s, starting with empty inventory.",
            file_name,
        )
        stock_data.clear()
    except json.JSONDecodeError as exc:
        logging.error("Invalid JSON in %s: %s", file_name, exc)
        stock_data.clear()


def save_data(file_name="inventory.json"):
    """Save inventory data to a JSON file."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(stock_data, file, indent=4)
            logging.info("Saved inventory data to %s", file_name)
    except OSError as exc:
        logging.error("Error saving file %s: %s", file_name, exc)


def print_data():
    """Print all items and their quantities."""
    print("Items Report")
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")


def check_low_items(threshold=5):
    """Return a list of items with quantity below threshold."""
    result = [item for item, qty in stock_data.items() if qty < threshold]
    logging.info(
        "Checked low-stock items below threshold: %d",
        threshold,
    )
    return result


def run_demo():
    """Run a short demonstration of inventory operations."""
    add_item("apple", 10)
    add_item("banana", 2)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()


def main():
    """Entry point for the inventory system demo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    run_demo()
    logging.info("Inventory demo completed successfully.")


if __name__ == "__main__":
    main()
