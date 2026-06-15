"""
test_highlands.py
-----------------
Unit tests for Highlands Mini POS business logic.

Run with:
    python -m unittest test_highlands.py -v
"""

import unittest

from pos_logic import (
    DRINK_MENU,
    InvalidQuantityError,
    ItemNotFoundError,
    add_to_order,
    calculate_total,
    clear_order,
    current_order,
)


class TestHighlandsPOS(unittest.TestCase):
    """Test suite for core POS logic functions."""

    def setUp(self) -> None:
        """Clear the shared order list before each test."""
        clear_order()

    # ------------------------------------------------------------------
    # calculate_total
    # ------------------------------------------------------------------
    def test_calculate_total(self) -> None:
        """calculate_total must return the correct grand total."""
        mock_order = [
            {"code": "P1", "name": "Phin Sữa Đá",
             "price": 35_000, "quantity": 2},
            {"code": "F1", "name": "Freeze Trà Xanh",
             "price": 55_000, "quantity": 1},
        ]
        result = calculate_total(mock_order)
        self.assertEqual(result, 125_000)

    def test_calculate_total_empty_order(self) -> None:
        """calculate_total of an empty order must return 0."""
        self.assertEqual(calculate_total([]), 0)

    def test_calculate_total_single_item(self) -> None:
        """calculate_total with one item must equal price × quantity."""
        mock_order = [
            {"code": "T1", "name": "Trà Sen Vàng",
             "price": 45_000, "quantity": 3},
        ]
        self.assertEqual(calculate_total(mock_order), 135_000)

    # ------------------------------------------------------------------
    # add_to_order — invalid quantity
    # ------------------------------------------------------------------
    def test_invalid_quantity_negative(self) -> None:
        """add_to_order must raise InvalidQuantityError for negative qty."""
        with self.assertRaises(InvalidQuantityError):
            add_to_order("P1", -1)

    def test_invalid_quantity_zero(self) -> None:
        """add_to_order must raise InvalidQuantityError for zero qty."""
        with self.assertRaises(InvalidQuantityError):
            add_to_order("P1", 0)

    # ------------------------------------------------------------------
    # add_to_order — unknown drink code
    # ------------------------------------------------------------------
    def test_item_not_found(self) -> None:
        """add_to_order must raise ItemNotFoundError for unknown code."""
        with self.assertRaises(ItemNotFoundError):
            add_to_order("A1", 2)

    def test_item_not_found_case_insensitive(self) -> None:
        """add_to_order must accept lowercase codes without error."""
        add_to_order("p1", 1)
        self.assertEqual(len(current_order), 1)
        self.assertEqual(current_order[0]["code"], "P1")

    # ------------------------------------------------------------------
    # add_to_order — happy path
    # ------------------------------------------------------------------
    def test_add_to_order_success(self) -> None:
        """A valid add_to_order call must append exactly one item."""
        add_to_order("P1", 2)
        self.assertEqual(len(current_order), 1)
        self.assertEqual(current_order[0]["quantity"], 2)
        self.assertEqual(current_order[0]["price"], 35_000)

    def test_add_multiple_items(self) -> None:
        """Multiple add_to_order calls must each append an entry."""
        add_to_order("P1", 2)
        add_to_order("F1", 1)
        self.assertEqual(len(current_order), 2)
        self.assertEqual(
            calculate_total(current_order), 125_000
        )

    # ------------------------------------------------------------------
    # clear_order
    # ------------------------------------------------------------------
    def test_clear_order(self) -> None:
        """clear_order must empty the current_order list."""
        add_to_order("T1", 3)
        clear_order()
        self.assertEqual(len(current_order), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
