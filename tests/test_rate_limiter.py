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
Test rate limiter.
"""

import time
import unittest

from loop_rate_limiters import RateLimiter


class TestRate(unittest.TestCase):
    def setUp(self):
        """
        Initialize a rate with 1 ms period.
        """
        self.rate = RateLimiter(frequency=1000.0)

    def test_init(self):
        """
        Constructor completed.
        """
        self.assertIsNotNone(self.rate)

    def test_remaining(self):
        """
        After one period has expired, the "remaining" time becomes negative.
        """
        self.rate.sleep()
        time.sleep(self.rate.period)
        remaining = self.rate.remaining()
        self.assertLess(remaining, 0.0)

    def test_slack(self):
        """
        Slack becomes negative as well after one period has expired.
        """
        self.rate.sleep()
        time.sleep(self.rate.period)
        self.rate.sleep()  # computes slack of previous period
        self.assertLess(self.rate.slack, 0.0)

    def test_sleep(self):
        self.rate.sleep()
        self.rate.sleep()  # presumably slack > 0.0
        time.sleep(self.rate.period)
        self.rate.sleep()  # now for sure slack < 0.0
