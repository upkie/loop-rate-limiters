#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test asyncio rate limiter.
"""

import asyncio
import unittest

from loop_rate_limiters import AsyncRateLimiter


class TestAsyncRateLimiter(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """
        Initialize a rate with 1 ms period.
        """
        self.rate = AsyncRateLimiter(1000.0)

    async def test_init(self):
        """
        Constructor completed.
        """
        self.assertIsNotNone(self.rate)

    async def test_remaining(self):
        """
        After one period has expired, the "remaining" time becomes negative.
        """
        await self.rate.sleep()
        await asyncio.sleep(self.rate.period)
        remaining = await self.rate.remaining()
        self.assertLess(remaining, 0.0)

    async def test_slack(self):
        """
        Slack becomes negative as well after one period has expired.

        Notes:
            We wait slightly less than a period because Windows (windows-latest
            in the CI) has imprecise timers.
        """
        await self.rate.sleep()
        await asyncio.sleep(self.rate.period * 1.05)  # a tad extra
        await self.rate.sleep()  # computes slack of previous period
        self.assertLess(self.rate.slack, 0.0)

    async def test_sleep(self):
        await self.rate.sleep()
        await self.rate.sleep()  # presumably slack > 0.0
        await asyncio.sleep(self.rate.period)
        await self.rate.sleep()  # now for sure slack < 0.0
