# Routing-of-telephone-calls
![Python versions](https://img.shields.io/badge/python-3.10-blue)

alaTest / ValueChecker (ICSS) challenge 2023 for An Đỗ [anmana000@gmail.com]


Some telephone operators have submitted their price lists including price per minute for different phone number prefixes. The price lists look like this:

```
Operator A:
1	 0.9
268	 5.1
46	 0.17
4620	 0.0
468	 0.15
4631	 0.15
4673	 0.9
46732	 1.1

Operator B:
1	 0.92
44	 0.5
46	 0.2
467	 1.0
48	 1.2
```

And so on...

The left column represents the telephone prefix (country + area code) and the right column represents the operator's price per minute for a number starting with that prefix. When several prefixes match the same number, the longest one should be used. If you, for example, dial +46-73-212345 you will have to pay \$1.1/min with Operator A and \$1.0/min with Operator B.

If a price list does not include a certain prefix you cannot use that operator to dial numbers starting with that prefix. For example it is not possible to dial +44 numbers with operator A but it is possible with Operator B.

# The Goal

The goal with this exercise is to write a program that can handle any number of price lists (operators) and then can calculate which operator that is cheapest for a certain number. You can assume that each price list can have thousands of entries but they will all fit together in memory.

Telephone numbers should be inputted in the same format as in price lists, for example “68123456789”. The challenge is to find the cheapest operator for that number.

# Instructions

Use your favorite language to solve the exercise.
Put your focus on code design and readability.
Do not use a database or create a GUI.
Plus is given to efficient solutions.
The code should have unit test(s).
Deliver to us via online repository (give access to erik.ohlzon@alatest.com). If your repo username does not indicate your name somehow, please make a note of whom the solution belongs to.
Please include (in the repo) a current CV listing any recent or relevant code examples.

# Checklist

- [x] Algorithm
- [x] Logging
- [x] Testing
- [x] CI CD github
- [x] Functions documentation
- [x] Restrict python version
---
## Testing
- [x] Logic
- [x] Stress Test
