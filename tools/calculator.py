"""
Calculator Tool for ResearchMate.
Performs safe mathematical calculations using sympy.
"""

from typing import Union


class CalculatorTool:
    """Tool that evaluates mathematical expressions safely."""

    def calculate(self, expression: str) -> dict:
        """
        Evaluate a mathematical expression safely.

        Args:
            expression: A math expression string (e.g., "2 + 3 * 4", "sqrt(16)").

        Returns:
            A dict with 'result' (the computed value), 'expression', and 'success'.
        """
        if not expression or len(expression.strip()) == 0:
            return {
                "result": None,
                "expression": expression,
                "success": False,
                "error": "Empty expression provided.",
            }

        try:
            result = self._safe_eval(expression)
            return {
                "result": str(result),
                "expression": expression,
                "success": True,
                "error": None,
            }
        except Exception as e:
            return {
                "result": None,
                "expression": expression,
                "success": False,
                "error": f"Calculation error: {e}",
            }

    def _safe_eval(self, expression: str) -> Union[int, float, str]:
        """
        Safely evaluate a math expression using sympy.

        Args:
            expression: The expression to evaluate.

        Returns:
            The result of the calculation.
        """
        try:
            from sympy import sympify
            result = sympify(expression)
            # Try to convert to a number
            float_result = float(result)
            if float_result == int(float_result):
                return int(float_result)
            return round(float_result, 6)
        except ImportError:
            raise ImportError(
                "sympy is required for calculations. "
                "Install it with: pip install sympy"
            )

    def percentage(self, part: float, whole: float) -> dict:
        """
        Calculate what percentage 'part' is of 'whole'.

        Args:
            part: The partial value.
            whole: The total value.

        Returns:
            A dict with the percentage result.
        """
        if whole == 0:
            return {
                "result": None,
                "success": False,
                "error": "Cannot divide by zero.",
            }

        pct = round((part / whole) * 100, 2)
        return {
            "result": f"{pct}%",
            "success": True,
            "error": None,
        }
