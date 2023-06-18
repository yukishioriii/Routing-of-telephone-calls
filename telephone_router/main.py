from typing import Optional
from typing_extensions import TypedDict
import logging
from os.path import isfile, join
from os import listdir
import csv
from constants import CSV_FOLDER

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s -  %(name)s: %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class PrefixNode:
    """
    Node to store cheapest price at this certain point of matching
    eg:
        Op A:
            12, 0.5\n
            123, 0.6
        Op B:
            13, 0.1

        Phone number `12345678` longest matching prefix is `123`
         which belongs to operator A with pricing of $ 0.6
         CheapestOpFinder's query should return PrefixNode(123)
    """

    def __init__(self, digit: Optional[int], prefix: str) -> None:
        self.next_digit = dict()
        self.operator: str = None
        self.price: float = None
        self.digit = digit
        self.prefix = prefix

    def __hash__(self) -> int:
        return self.digit

    def __repr__(self) -> str:
        # return f"DigitNode({self.digit}) @ {hex(id(self))}"
        return f"DigitNode({self.prefix})"


class OperatorPrice(TypedDict):
    """
    Price information dictionary of this operator
    """
    price: float
    operator: str


class CheapestOpFinder:

    def __init__(self, operator_folder_path: str) -> None:
        """
        Cheapest operator finder

        Args:
            operator_folder_path (str): path to folder where
             operator pricing are listed

        Eg:
            finder = CheapestOpFinder(CSV_FOLDER)\n
            finder.query(19565184555)

        Logic:
            + Merge and sort all prefix pricing into `self.minimum_price_dict`
            + Make `self.search_tree` to store DigitNode which can be used to
               query in O(1) time

        Assumption:
            + Phone prefixes are not longer than 7,8 digit
               (at 8 digit storage size will take maximum around 400MB)
            + Prefixes matrix are rather sparse

        """
        assert operator_folder_path
        self.path: str = operator_folder_path
        self.search_tree: dict[int, PrefixNode] = dict()
        self.minimum_price_dict: dict[str, OperatorPrice] = dict()

        self._sort_prefix_price()
        self._build_search_tree()

    def _sort_prefix_price(self) -> None:
        """
        Merge and sort all prefix pricing into `self.minimum_price_dict`
        """

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
        logger.info(self.minimum_price_dict)

    def _build_search_tree(self) -> None:
        """
        Make `self.search_tree` to store DigitNode
        """

        # initialize search tree with 1st digit
        for i in range(10):
            self.search_tree[i] = PrefixNode(i, str(i))

        for prefix in self.minimum_price_dict.keys():
            price = self.minimum_price_dict[prefix]["price"]
            operator = self.minimum_price_dict[prefix]["operator"]

            current_node = self.search_tree[int(prefix[0])]

            if len(prefix) == 1:
                current_node.operator = operator
                current_node.price = price

            for i in range(1, len(prefix)):
                digit = int(prefix[i])
                if digit in current_node.next_digit:
                    current_node = current_node.next_digit[digit]
                else:
                    current_node.next_digit[digit] = PrefixNode(digit, prefix[:i+1])
                    current_node = current_node.next_digit[digit]

                if i == len(prefix)-1:
                    current_node.operator = operator
                    current_node.price = price

    def query(self, phone_number: str) -> PrefixNode:
        """
        Query minimum pricing for this phone number

        Args:
            phone_number (str): phone number

        Returns:
            OperatorPrice: lowest price for this phone number and its operator
        """
        assert phone_number
        node = self.search_tree[int(phone_number[0])]
        for digit in phone_number[1:]:
            digit = int(digit)
            if digit in node.next_digit:
                node = node.next_digit[digit]
            else:
                break
        return node


if __name__ == "__main__":
    finder = CheapestOpFinder(CSV_FOLDER)
    node = finder.query("2692134123")
    logger.info(f"`{node.prefix}` {node.price}, {node.operator}")
