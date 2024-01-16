#!/usr/bin/env python3
'''Run time for four parallel comprehensions'''
import asyncio
from typing import List
import time
async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    ''' Run time for four parallel comprehensions'''
    start = time.time()
    await asyncio.gather(*[async_comprehension() for i in range(4)])
    return time.time() - start
