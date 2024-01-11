#!/usr/bin/env python3
"""DComplex types - list of floats"""
from typing import List


def sum_list(sum_list: List[float]) -> float:
    """function sum_list which takes a list input_list of
    floats as argument and returns their sum as a float.
    """
    total = 0
    for i in range(len(sum_list)):
        total += sum_list[i]
    return total
