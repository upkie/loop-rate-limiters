# Loop rate limiters

[![Build](https://img.shields.io/github/actions/workflow/status/stephane-caron/loop-rate-limiters/main.yml?branch=main)](https://github.com/stephane-caron/loop-rate-limiters/actions)
[![Coverage](https://coveralls.io/repos/github/stephane-caron/loop-rate-limiters/badge.svg?branch=main)](https://coveralls.io/github/stephane-caron/loop-rate-limiters?branch=main)
[![Conda version](https://img.shields.io/conda/vn/conda-forge/loop-rate-limiters.svg)](https://anaconda.org/conda-forge/loop-rate-limiters)
[![PyPI version](https://img.shields.io/pypi/v/loop-rate-limiters)](https://pypi.org/project/loop-rate-limiters/)

Simple loop frequency regulators in Python with an API similar to [``rospy.Rate``](https://wiki.ros.org/rospy/Overview/Time#Sleeping_and_Rates).

## Installation

From conda-forge:

```sh
conda install loop-rate-limiters -c conda-forge
```

From PyPI:

```sh
pip install loop-rate-limiters
```

## Usage

The ``RateLimiter`` class provides a loop frequency limiter:

```python
from loop_rate_limiters import RateLimiter
from time import perf_counter

rate = RateLimiter(frequency=400.0)
while True:
    print(f"Hello from loop at {perf_counter():.3f} s")
    rate.sleep()
```

### asyncio

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
