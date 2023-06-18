import unittest
from telephone_router.main import CheapestOpFinder
from constants import OP_A, OP_B, CSV_FOLDER


class TestLogic(unittest.TestCase):
    def setUp(self) -> None:
        self.finder = CheapestOpFinder(CSV_FOLDER)

    def test_logic(self):

        node = self.finder.query("2680")
        assert node.operator == OP_A
        assert node.prefix == "268"
        assert node.price == "5.1"

        node = self.finder.query("260")
        assert node.operator == OP_B
        assert node.prefix == "26"
        assert node.price == "0.5"

        node = self.finder.query("1")
        assert node.operator == OP_A
        assert node.prefix == "1"
        assert node.price == "0.9"

    def test_duplicate(self):
        node = self.finder.query("48")
        assert node.operator == OP_A
        assert node.prefix == "48"
        assert node.price == "1.1"


if __name__ == "__main__":
    unittest.main()
