"""Unit tests for the add_numbers function."""
import unittest

def add_numbers(a, b):
    """
    Function to sum two numbers.

    Args:
    - a: First number.
    - b: Second number.

    Returns:
    - Sum of the two numbers.
    """
    return a + b

# Write a test case for the above function.

class TestSum(unittest.TestCase):
    """
    This class contains test cases for the [add_numbers]
    (cci:1://file:///Users/faddah/Library/Application%20Support/Code/User/globalStorage/amazonwebservices.amazon-q-vscode/Generate_unit_tests.py:2:0-13:16)
    function.
    """
    def test_sum_positive_numbers(self):
        """
        Test the sum function with positive numbers.

        Verify that add_numbers(2, 3) returns 5.
        """

        self.assertEqual(add_numbers(2, 3), 5)

    def test_sum_negative_numbers(self):
        """
        Test the sum function with negative numbers.

        Verify that add_numbers(-1, -1) returns -2.
        """
        self.assertEqual(add_numbers(-1, -1), -2)

    def test_sum_mixed_numbers(self):
        """
        Test case for sum of mixed numbers
        """
        self.assertEqual(add_numbers(-1, 1), 0)

    def test_sum_zero(self):
        """
        Test case for sum of zero
        """
        self.assertEqual(add_numbers(0, 0), 0)
if __name__ == '__main__':
    unittest.main()
