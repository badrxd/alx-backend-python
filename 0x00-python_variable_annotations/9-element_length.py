#!/usr/bin/env python3
"""Let's duck type an iterable object
"""
from typing import Sequence, List, Tuple, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Annotate the below function’s parameters and 
    return values with the appropriate types"""
    return [(i, len(lst)) for i in lst]
