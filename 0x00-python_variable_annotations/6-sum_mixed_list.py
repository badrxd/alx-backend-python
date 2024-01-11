#!/usr/bin/env python3
"""Complex types - mixed list"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """function sum_list which takes a list input_list of
    floats as argument and returns their sum as a float.
    """
    total = 0
    for i in range(len(mxd_lst)):
        total += mxd_lst[i]
    return total
