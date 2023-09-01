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

"""Non-blocking loop frequency limiter for asyncio.

Note that there is a difference between a (non-blocking) rate limiter and a
(blocking) synchronous clock, which lies in the behavior when skipping cycles.
A rate limiter does nothing if there is no time left, as the caller's rate does
not need to be limited. On the contrary, a synchronous clock waits for the next
tick, which is by definition in the future, so it always waits for a non-zero
duration.
"""

import asyncio
import logging


class AsyncRateLimiter:
    """Loop frequency regulator.

    Calls to :func:`sleep` are non-blocking most of the time but become
    blocking close to the next clock tick to get more reliable loop
    frequencies.

    This rate limiter is in essence the same as in the one from pymanoid_. It
    relies on the event loop time never jumping backwards nor forwards, so that
    it does not handle such cases contrary to e.g. rospy.Rate_.

    .. _pymanoid:
        https://github.com/stephane-caron/pymanoid/blob/d3e2098e40656943f2639f90a1ec4269cf730157/pymanoid/sim.py#L140

    .. _rospy.Rate:
        https://github.com/ros/ros_comm/blob/noetic-devel/clients/rospy/src/rospy/timer.py

    Attributes:
        name: Human-readable name used for logging.
        warn: If set (default), warn when the time between two calls
            exceeded the rate clock.
    """

    __last_loop_time: float
    __loop: asyncio.AbstractEventLoop
    __measured_period: float
    __next_tick: float
    __period: float
    __slack: float
    name: str
    warn: bool

    def __init__(
        self, frequency: float, name: str = "rate limiter", warn: bool = True
    ):
        """Initialize rate limiter.

        Args:
            frequency: Desired loop frequency in hertz.
            name: Human-readable name used for logging.
            warn: If set (default), warn when the time between two calls
                exceeded the rate clock.
        """
        loop = asyncio.get_event_loop()
        period = 1.0 / frequency
        assert loop.is_running()
        self.__last_loop_time = loop.time()
        self.__loop = loop
        self.__measured_period = 0.0
        self.__next_tick = loop.time() + period
        self.__period = period
        self.__slack = 0.0
        self.name = name
        self.warn = warn

    @property
    def dt(self) -> float:
        """Desired period between two calls to :func:`sleep`, in seconds."""
        return self.__period

    @property
    def measured_period(self) -> float:
        """Period measured at the end of the last call to :func:`sleep`.

        This duration is in seconds.
        """
        return self.__measured_period

    @property
    def next_tick(self) -> float:
        """Time of next clock tick."""
        return self.__next_tick

    @property
    def period(self) -> float:
        """Desired period between two calls to :func:`sleep`, in seconds."""
        return self.__period

    @property
    def slack(self) -> float:
        """Slack duration computed at the last call to :func:`sleep`.

        This duration is in seconds.
        """
        return self.__slack

    async def remaining(self) -> float:
        """Get the time remaining until the next expected clock tick.

        Returns:
            Time remaining, in seconds, until the next expected clock tick.
        """
        return self.__next_tick - self.__loop.time()

    async def sleep(self, block_duration: float = 5e-4):
        """Sleep the duration required to regulate the loop frequency.

        This function is meant to be called once per loop cycle.

        Args:
            block_duration: the coroutine blocks the event loop for this
                duration (in seconds) before the next tick. It is non-blocking
                before that.

        Note:
            A call to this function will be non-blocking *except* for the last
            ``block_duration`` seconds of the limiter period.

        The block duration helps trim period overshoots and brings the measured
        period much closer to the desired one (< 2% average error vs. 8-12%
        average error with a single asyncio.sleep). Empirically a block
        duration of 0.5 ms gives good behavior at 400 Hz or lower.
        """
        self.__slack = self.__next_tick - self.__loop.time()
        if self.__slack > 0.0:
            block_time = self.__next_tick - block_duration
            while self.__loop.time() < self.__next_tick:
                if self.__loop.time() < block_time:
                    await asyncio.sleep(1e-5)  # non-zero sleep duration
        elif self.__slack < -0.1 * self.__period and self.warn:
            logging.warning(
                "%s is late by %f [ms]",
                self.name,
                round(1e3 * self.__slack, 1),
            )
        loop_time = self.__loop.time()
        self.__measured_period = loop_time - self.__last_loop_time
        self.__last_loop_time = loop_time
        self.__next_tick = loop_time + self.__period
