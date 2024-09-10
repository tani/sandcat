import unittest

from sandcat import Atom, check

A, B, C = Atom("A"), Atom("B"), Atom("C")


class TestSandcat(unittest.TestCase):
    def test_case_1(self):
        self.assertFalse(check([C << A, B, A], C))

    def test_case_2(self):
        self.assertTrue(check([C << A, A, B], C))

    def test_case_3(self):
        self.assertTrue(check([C << A, A, C >> C], C))


if __name__ == "__main__":
    unittest.main()
