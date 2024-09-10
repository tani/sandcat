import unittest

from category import Atom
from sandcat import check as sympyCheck
from sandcat_z3 import check as z3Check

A, B, C = Atom("A"), Atom("B"), Atom("C")


class TestSandcatSympy(unittest.TestCase):
    def test_case_1(self):
        self.assertFalse(sympyCheck([C << A, B, A], C))

    def test_case_2(self):
        self.assertTrue(sympyCheck([C << A, A, B], C))

    def test_case_3(self):
        self.assertTrue(sympyCheck([C << A, A, C >> C], C))

class TestSandcatZ3(unittest.TestCase):
    def test_case_1(self):
        self.assertFalse(z3Check([C << A, B, A], C))

    def test_case_2(self):
        self.assertFalse(z3Check([C << A, A, B], C))

    def test_case_3(self):
        self.assertTrue(z3Check([C << A, A, C >> C], C))

if __name__ == "__main__":
    unittest.main()
