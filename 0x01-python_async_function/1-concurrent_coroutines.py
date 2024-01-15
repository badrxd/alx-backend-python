#!/usr/bin/env python3
"""Let's execute multiple coroutines at the
same time with async
"""
import asyncio
from typing import List

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """function execute multiple coroutines at the same time
    with async"""
    li: List[float] = []
    while len(li) < n:
        li.append(await wait_random(max_delay))
    return sorted(li)
