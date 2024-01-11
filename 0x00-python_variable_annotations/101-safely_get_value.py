#!/usr/bin/env python3
"""Augment the following code with the correct duck-typed annotations:

"""
from typing import Dict, Optional, Any, TypeVar, Union, Mapping
T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default:
                     Union[T, None]) -> Union[Any, T]:
    """ 
    return element or default
    """
    if key in dct:
        return dct[key]
    else:
        return default
