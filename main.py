from __future__ import annotations
from typing import TypedDict
import csv


class DigitNode:
    next_digit = TypedDict("next_digit", {"digit_node": "DigitNode"})
    cheapest_operator: str = None
    cheapest_price: float = None

    def __init__(self, digit) -> None:
        self.digit = digit

    def __hash__(self) -> int:
        return self.digit

    # def insert(self, )


if __name__ == "__main__":
    a = DigitNode(9)
    print(a)
    first_digit = TypedDict("first_digit", {"digit_node": "DigitNode"})
    first_digit[5] = DigitNode(5)
    

    with open('opa.csv', newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='|')
        operator_pricing = [row for row in reader]

    for prefix, price in operator_pricing:
        assert prefix and price, "prefix or price cannot be empty"
        current_node = prefix[0]
        for digit in prefix[1:]:
            if digit in current_node["next_digit"]:
                
