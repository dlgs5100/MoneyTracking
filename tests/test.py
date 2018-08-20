import unittest
import calculate.calculator as calculator

class CalculatorTest(unittest.TestCase):                 
    def test_mod_with_remainder(self):
        cal = calculator.calculator()                   
        self.assertEqual(cal.perDaySpending(6000,30), 20)