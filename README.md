# Loop rate limiters

[![Build](https://img.shields.io/github/actions/workflow/status/tasts-robots/loop-rate-limiters/main.yml?branch=main)](https://github.com/tasts-robots/loop-rate-limiters/actions)
[![Coverage](https://coveralls.io/repos/github/tasts-robots/loop-rate-limiters/badge.svg?branch=main)](https://coveralls.io/github/tasts-robots/loop-rate-limiters?branch=main)

Simple loop frequency regulators in Python with an API similar to ``rospy.Rate``:

```python
from loop_rate_limiters import RateLimiter
from time import perf_counter

rate = RateLimiter(frequency=400.0)
while True:
    print(f"Hello from loop at {perf_counter():.3f} s")
    rate.sleep()
```

A similar ``AsyncRateLimiter`` class is available for [asynchronous code](#asynchronous-io).

## Installation

### PyPI

[![PyPI version](https://img.shields.io/pypi/v/loop-rate-limiters)](https://pypi.org/project/loop-rate-limiters/)
[![PyPI downloads](https://static.pepy.tech/badge/loop-rate-limiters)](https://pepy.tech/project/loop-rate-limiters)

```console
$ pip install loop-rate-limiters
```

### Conda

[![Conda version](https://anaconda.org/conda-forge/loop-rate-limiters/badges/version.svg)](https://anaconda.org/conda-forge/loop-rate-limiters)
[![Conda downloads](https://anaconda.org/conda-forge/loop-rate-limiters/badges/downloads.svg)](https://anaconda.org/conda-forge/loop-rate-limiters)

```console
$ conda install loop-rate-limiters -c conda-forge
```

## Asynchronous I/O

The ``AsyncRateLimiter`` class provides a loop frequency limiter for [asyncio](https://docs.python.org/3/library/asyncio.html):

```python
import asyncio
from loop_rate_limiters import AsyncRateLimiter

async def main():
    rate = AsyncRateLimiter(frequency=400.0)
    while True:
        loop_time = asyncio.get_event_loop().time()
        print(f"Hello from loop at {loop_time:.3f} s")
        await rate.sleep()

if __name__ == "__main__":
    asyncio.run(main())
```
