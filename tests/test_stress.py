import unittest
from telephone_router.main import CheapestOpFinder
from random import sample, uniform
from uuid import uuid4
from constants import RANDOM_GEN_FOLDER
import csv
from os.path import isfile, join
from os import listdir, remove
import time
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s -  %(name)s: %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class TestStress(unittest.TestCase):
    def generate_test_data(
        self,
        number_of_operator: int,
        pricing_each_op: int,
        prefix_max_length: int
    ) -> None:
        """Generate csv files for testing purposes

        Args:
            number_of_operator (int): number of csv files create
            pricing_each_op (int): number of lines each file
            prefix_max_length (int): prefixes's max length
        """

        for _ in range(number_of_operator):
            filename = uuid4()
            prefixes = sample(range(10 ** prefix_max_length), pricing_each_op)
            # 2 digit behind period for visibility
            prices = [round(uniform(0, 10), 2)
                      for _ in range(pricing_each_op)]
            with open(f'{RANDOM_GEN_FOLDER}/{filename}.csv', 'w+') as f:
                writer = csv.writer(f)
                writer.writerows([(prefixes[i], prices[i])
                                  for i in range(pricing_each_op)])

    def test_logic_multiple(self):
        """
        # Generate prefix list A = [1->10] B = [5->15] C = [10->20]
         where price in C is strictly lower than B and B strictly lower than A
        """
        for i in range(10):
            filename = f"file_{i}"
            prefixes = range(i*5, i*5 + 10)
            # 2 digit behind period for visibility
            prices = [6-(round(uniform(i*5, i*5 + 4) / 10, 2))
                      for _ in range(10)]
            with open(f'{RANDOM_GEN_FOLDER}/{filename}.csv', 'w+') as f:
                writer = csv.writer(f)
                writer.writerows([(prefixes[i], prices[i])
                                  for i in range(10)])
        finder = CheapestOpFinder(RANDOM_GEN_FOLDER)
        for i in range(9):
            # 1st item should be in file_i{}
            node = finder.query(f"{i*5}")
            assert node.operator == f"{RANDOM_GEN_FOLDER}/file_{i}.csv"
            # 2nd item should belong in file i+1 cause over lap
            # and price of i+1 is cheaper than i
            node = finder.query(f"{i*5 + 7}")
            assert node.operator == f"{RANDOM_GEN_FOLDER}/file_{i+1}.csv"

    def test_10_100_7(self):
        self.generate_test_data(10, 100, 7)
        finder = CheapestOpFinder(RANDOM_GEN_FOLDER)
        t0 = time.time()
        # Test 100 different query
        for number in sample(range(10 ** 10), 100):
            finder.query(f"{number}")
        t1 = time.time()
        logger.info(f"test_10_100_7 time: {t1-t0}")

    def test_100_1000_10(self):
        self.generate_test_data(100, 1000, 10)
        finder = CheapestOpFinder(RANDOM_GEN_FOLDER)
        t0 = time.time()
        # Test 100 different query
        for number in sample(range(10 ** 10), 100):
            finder.query(f"{number}")
        t1 = time.time()
        logger.info(f"test_100_1000_10 time: {t1-t0}")

    def tearDown(self) -> None:
        files_to_delete = [join(RANDOM_GEN_FOLDER, f)
                           for f in listdir(RANDOM_GEN_FOLDER)
                           if isfile(join(RANDOM_GEN_FOLDER, f))
                           and f[-4:].lower() == ".csv"]
        for file in files_to_delete:
            remove(file)


if __name__ == "__main__":
    unittest.main()
