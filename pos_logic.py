"""
pos_logic.py
------------
Core business logic for Highlands Mini POS.

Contains:
    - DRINK_MENU: default product catalogue
    - Custom exceptions: ItemNotFoundError, InvalidQuantityError
    - Order management functions
    - Calculation helpers
"""

import logging

# ---------------------------------------------------------------------------
# Logging configuration — output to terminal (StreamHandler default)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DRINK_MENU: dict = {
    "P1": {"name": "Phin Sữa Đá", "price": 35_000},
    "F1": {"name": "Freeze Trà Xanh", "price": 55_000},
    "T1": {"name": "Trà Sen Vàng", "price": 45_000},
}

# In-memory order: list of dicts {code, name, price, quantity}
current_order: list = []


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------
class ItemNotFoundError(Exception):
    """Raised when a drink code is not found in DRINK_MENU."""


class InvalidQuantityError(Exception):
    """Raised when an order quantity is zero or negative."""


# ---------------------------------------------------------------------------
# Menu helpers
# ---------------------------------------------------------------------------
def display_menu() -> None:
    """Print all items in DRINK_MENU to stdout in a formatted table."""
    print("\n--- THỰC ĐƠN HIGHLANDS COFFEE ---")
    for code, item in DRINK_MENU.items():
        print(
            f"[{code}] - {item['name']} - {item['price']:,} VNĐ"
        )


# ---------------------------------------------------------------------------
# Order management
# ---------------------------------------------------------------------------
def add_to_order(drink_code: str, quantity: int) -> None:
    """
    Validate inputs and append an item to *current_order*.

    Args:
        drink_code: Product code (case-insensitive, whitespace stripped).
        quantity:   Number of units (must be a positive integer).

    Raises:
        ItemNotFoundError:    If *drink_code* is not in DRINK_MENU.
        InvalidQuantityError: If *quantity* is <= 0.
    """
    code = drink_code.strip().upper()

    if code not in DRINK_MENU:
        logger.warning("ItemNotFoundError - Code: %s", code)
        raise ItemNotFoundError(code)

    if quantity <= 0:
        logger.warning("InvalidQuantityError - Quantity: %d", quantity)
        raise InvalidQuantityError(quantity)

    item = DRINK_MENU[code]
    current_order.append(
        {
            "code": code,
            "name": item["name"],
            "price": item["price"],
            "quantity": quantity,
        }
    )
    logger.info("Added %d of %s to order", quantity, code)


def calculate_total(order: list) -> int:
    """
    Return the grand total (VND) for all items in *order*.

    Args:
        order: List of order-item dicts, each having 'price' and 'quantity'.

    Returns:
        Integer total in VND.
    """
    return sum(item["price"] * item["quantity"] for item in order)


def clear_order() -> None:
    """Empty the global *current_order* list in place."""
    current_order.clear()


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
def display_order() -> None:
    """
    Print the current order as a formatted table with per-item subtotals.

    If the order is empty, print an appropriate message instead.
    """
    if not current_order:
        print(
            "Giỏ hàng trống, vui lòng chọn món (Chức năng 2)."
        )
        return

    header = (
        f"{'Mã SP':<6}| {'Tên đồ uống':<22}| "
        f"{'Đơn giá':<10}| {'Số lượng':<10}| Thành tiền"
    )
    divider = "-" * 64

    print("\n--- GIỎ HÀNG HIỆN TẠI ---")
    print(header)
    print(divider)

    for item in current_order:
        subtotal = item["price"] * item["quantity"]
        print(
            f"{item['code']:<6}| {item['name']:<22}| "
            f"{item['price']:>8,}  | {item['quantity']:<10}| "
            f"{subtotal:,} VNĐ"
        )

    print(divider)
    total = calculate_total(current_order)
    print(f"Tổng tiền cần thanh toán: {total:,} VNĐ")


# ---------------------------------------------------------------------------
# Checkout
# ---------------------------------------------------------------------------
def checkout() -> None:
    """
    Confirm payment with the cashier and clear the order on success.

    Accepts 'y' to confirm, 'n' to cancel, or any other input to abort.
    If the order is empty, notifies the cashier and returns immediately.
    """
    if not current_order:
        print(
            "Giỏ hàng trống, vui lòng chọn món (Chức năng 2)."
        )
        return

    total = calculate_total(current_order)
    print("\n--- THANH TOÁN ---")
    print(f"Tổng tiền cần thanh toán: {total:,} VNĐ")

    confirm = input(
        f"Xác nhận thanh toán {total:,} VNĐ? (y/n): "
    ).strip().lower()

    if confirm == "y":
        print("Thanh toán thành công.")
        logger.info("Checkout successful")
        clear_order()
        print("Giỏ hàng đã được làm trống.")
    elif confirm == "n":
        print(
            "Đã hủy thao tác thanh toán. Quay lại menu chính."
        )
    else:
        print("Lựa chọn không hợp lệ. Thanh toán đã bị hủy.")
