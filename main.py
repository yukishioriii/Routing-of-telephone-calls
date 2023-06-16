from __future__ import annotations
import csv
from os import listdir
from os.path import isfile, join
from pprint import pprint
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

    # def insert(self, )


def query(first_digit, phone_number):
    assert phone_number
    node = first_digit[int(phone_number[0])]
    for digit in phone_number[1:]:
        digit = int(digit)
        if digit in node.next_digit:
            node = node.next_digit[digit]
        else:
            return node.cheapest_operator, node.cheapest_price, node.digit


if __name__ == "__main__":
    minimum_price_dict = dict()
    files = [join(CSV_FOLDER, f) for f in listdir(CSV_FOLDER)
             if isfile(join(CSV_FOLDER, f))]

    for i, file in enumerate(files):
        with open(file, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for prefix, price in reader:
                if prefix in minimum_price_dict:
                    if price < minimum_price_dict[prefix]["price"]:
                        minimum_price_dict[prefix]["price"] = price
                        minimum_price_dict[prefix]["operator"] = file
                else:
                    minimum_price_dict[prefix] = {
                        "price": price,
                        "operator": file
                    }
    pprint(minimum_price_dict)

    first_digit = {}
    for i in range(10):
        first_digit[i] = DigitNode(i)

    for prefix in minimum_price_dict.keys():
        price = minimum_price_dict[prefix]["price"]
        operator = minimum_price_dict[prefix]["operator"]

        assert prefix and price and operator
        current_node = first_digit[int(prefix[0])]

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

    print(query(first_digit, "144234123423"))
