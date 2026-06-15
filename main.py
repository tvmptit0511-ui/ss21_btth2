"""
main.py
-------
Highlands Mini POS — CLI entry point.

Run with:
    python main.py
"""

import logging
import sys

from pos_logic import (
    InvalidQuantityError,
    ItemNotFoundError,
    add_to_order,
    checkout,
    display_menu,
    display_order,
    logger,
)


# ---------------------------------------------------------------------------
# Feature handlers
# ---------------------------------------------------------------------------
def handle_view_menu() -> None:
    """Display the full drink menu (Chức năng 1)."""
    display_menu()


def handle_add_to_order() -> None:
    """
    Prompt the cashier for a drink code and quantity, then add the
    item to the current order (Chức năng 2).

    Handles:
        - ItemNotFoundError  — unknown drink code
        - InvalidQuantityError — quantity <= 0
        - ValueError         — non-numeric quantity input
    """
    print("\n--- THÊM MÓN VÀO GIỎ ---")
    drink_code = input("Nhập mã đồ uống: ")

    # Validate drink code before asking for quantity
    code_upper = drink_code.strip().upper()
    from pos_logic import DRINK_MENU
    if code_upper not in DRINK_MENU:
        try:
            add_to_order(drink_code, 1)   # will raise ItemNotFoundError
        except ItemNotFoundError:
            print(
                "Mã đồ uống không hợp lệ, "
                "vui lòng kiểm tra lại thực đơn!"
            )
        return

    raw_qty = input("Nhập số lượng: ").strip()
    try:
        quantity = int(raw_qty)
    except ValueError:
        logging.getLogger(__name__).error(
            "ValueError - Invalid quantity input"
        )
        print("Vui lòng nhập số lượng là một số nguyên!")
        return

    try:
        add_to_order(drink_code, quantity)
    except InvalidQuantityError:
        print("Số lượng phải lớn hơn 0!")
        return

    from pos_logic import DRINK_MENU as menu
    name = menu[code_upper]["name"]
    print(f"Đã thêm {quantity} x {name} vào giỏ hàng.")


def handle_view_order() -> None:
    """Print order details and total (Chức năng 3)."""
    display_order()


def handle_checkout() -> None:
    """Run the checkout flow (Chức năng 4)."""
    checkout()


def handle_exit() -> None:
    """Log cashier logout and terminate the process (Chức năng 5)."""
    logger.info("Cashier logged out. System shutdown.")
    print("Đã thoát ca làm việc. Hẹn gặp lại!")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Menu display
# ---------------------------------------------------------------------------
def display_main_menu() -> None:
    """Print the main POS menu to stdout."""
    print("\n========== HIGHLANDS MINI POS ==========")
    print("1. Xem thực đơn")
    print("2. Thêm món vào giỏ")
    print("3. Xem giỏ hàng & Tính tổng tiền")
    print("4. Thanh toán & Xóa giỏ hàng")
    print("5. Thoát ca làm việc")
    print("=" * 40)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def run() -> None:
    """
    Start the Highlands Mini POS application.

    Presents the main menu in a loop and dispatches to the appropriate
    handler based on the cashier's input.
    """
    dispatch = {
        "1": handle_view_menu,
        "2": handle_add_to_order,
        "3": handle_view_order,
        "4": handle_checkout,
        "5": handle_exit,
    }

    while True:
        display_main_menu()
        choice = input("Chọn chức năng (1-5): ").strip()
        action = dispatch.get(choice)
        if action:
            action()
        else:
            print(
                "Lựa chọn không hợp lệ. "
                "Vui lòng chọn từ 1 đến 5."
            )


# ---------------------------------------------------------------------------
# Script entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run()
