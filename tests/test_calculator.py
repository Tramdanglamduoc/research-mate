"""Tests for the Calculator Tool."""

import pytest
from tools.calculator import CalculatorTool


class TestCalculatorTool:
    """Test suite for CalculatorTool."""

    def setup_method(self):
        self.tool = CalculatorTool()

    def test_basic_addition(self):
        result = self.tool.calculate("2 + 3")
        assert result["success"] is True
        assert result["result"] == "5"

    def test_multiplication(self):
        result = self.tool.calculate("7 * 8")
        assert result["success"] is True
        assert result["result"] == "56"

    def test_division(self):
        result = self.tool.calculate("10 / 4")
        assert result["success"] is True
        assert float(result["result"]) == 2.5

    def test_complex_expression(self):
        result = self.tool.calculate("(2 + 3) * 4 - 1")
        assert result["success"] is True
        assert result["result"] == "19"

    def test_empty_expression(self):
        result = self.tool.calculate("")
        assert result["success"] is False

    def test_invalid_expression(self):
        result = self.tool.calculate("hello world")
        assert result["success"] is False

    def test_percentage(self):
        result = self.tool.percentage(25, 200)
        assert result["success"] is True
        assert result["result"] == "12.5%"

    def test_percentage_division_by_zero(self):
        result = self.tool.percentage(10, 0)
        assert result["success"] is False
