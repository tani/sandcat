import unittest

import sandcat_sympy as sympy
import sandcat_z3 as z3
from category import Atom

A, B, C = Atom("A"), Atom("B"), Atom("C")


class TestSandcatSympy(unittest.TestCase):
    def test_case_1(self):
        self.assertFalse(sympy.check([C << A, B, A], C))

    def test_case_2(self):
        self.assertTrue(sympy.check([C << A, A, B], C))

    def test_case_3(self):
        self.assertTrue(sympy.check([C << A, A, C >> C], C))

class TestSandcatZ3(unittest.TestCase):
    def test_case_1(self):
        self.assertFalse(z3.check([C << A, B, A], C))

    def test_case_2(self):
        self.assertFalse(z3.check([C << A, A, B], C))

    def test_case_3(self):
        self.assertTrue(z3.check([C << A, A, C >> C], C))

if __name__ == "__main__":
    unittest.main()
