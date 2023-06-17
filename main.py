from typing_extensions import TypedDict
import logging
from pprint import pprint
from os.path import isfile, join
from os import listdir
import csv

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s -  %(name)s: %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


CSV_FOLDER = "./operators/"


class DigitNode:

    def __init__(self, digit: int) -> None:
        self.next_digit = dict()
        self.cheapest_operator: str = None
        self.cheapest_price: float = None
        self.digit = digit

    def __hash__(self) -> int:
        return self.digit

    def __repr__(self) -> str:
        # return f"DigitNode({self.digit}) @ {hex(id(self))}"
        return f"DigitNode({self.digit})"


class OperatorPrice(TypedDict):
    price: float
    operator: str


class CheapestOpFinder:

    def __init__(self, operator_folder_path: str) -> None:
        assert operator_folder_path
        self.path: str = operator_folder_path
        self.first_digit: dict[int, DigitNode] = dict()
        self.minimum_price_dict: dict[str, OperatorPrice] = dict()

        self._sort_prefix_price()
        self._build_minimum_price_dict()

    def _sort_prefix_price(self) -> None:
        files = [join(self.path, f) for f in listdir(self.path)
                 if isfile(join(self.path, f))]

        for file in files:
            with open(file, newline='') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                for prefix, price in reader:
                    if prefix in self.minimum_price_dict:
                        if price < self.minimum_price_dict[prefix]["price"]:
                            self.minimum_price_dict[prefix]["price"] = price
                            self.minimum_price_dict[prefix]["operator"] = file
                    else:
                        self.minimum_price_dict[prefix]: OperatorPrice = {
                            "price": price,
                            "operator": file
                        }
        pprint(self.minimum_price_dict)

    def _build_minimum_price_dict(self) -> None:
        for i in range(10):
            self.first_digit[i] = DigitNode(i)

        for prefix in self.minimum_price_dict.keys():
            price = self.minimum_price_dict[prefix]["price"]
            operator = self.minimum_price_dict[prefix]["operator"]

            assert prefix and price and operator
            current_node = self.first_digit[int(prefix[0])]

            if len(prefix) == 1:
                current_node.cheapest_operator = operator
                current_node.cheapest_price = price

            for i in range(1, len(prefix)):
                digit = int(prefix[i])
                if digit in current_node.next_digit:
                    current_node = current_node.next_digit[digit]
                else:
                    current_node.next_digit[digit] = DigitNode(digit)
                    current_node = current_node.next_digit[digit]
                if i == len(prefix)-1:
                    current_node.cheapest_operator = operator
                    current_node.cheapest_price = price

    def query(self, phone_number) -> tuple[OperatorPrice, int]:
        assert phone_number
        node = self.first_digit[int(phone_number[0])]
        for digit in phone_number[1:]:
            digit = int(digit)
            if digit in node.next_digit:
                node = node.next_digit[digit]
            else:
                return {
                    "operator": node.cheapest_operator,
                    "price": node.cheapest_price
                }, node.digit


if __name__ == "__main__":
    a = CheapestOpFinder(CSV_FOLDER)
    logger.info(a.query("144234123423"))
