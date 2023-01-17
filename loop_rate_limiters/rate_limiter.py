#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
# Copyright 2023 Inria
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

"""Basic rate limiter."""

from time import perf_counter, sleep


class RateLimiter:
    """Regulate the frequency between calls to the same instruction.

    This rate limniter is meant to be used in e.g. a loop or callback function.
    It is, in essence, the same as rospy.Rate_. It assumes Python's performance
    counter never jumps backward nor forward, so that it does not handle such
    cases contrary to rospy.Rate_.

    .. _rospy.Rate:
        https://github.com/ros/ros_comm/blob/noetic-devel/clients/rospy/src/rospy/timer.py
    """

    __period: float
    __slack: float
    __next_tick: float

    def __init__(self, frequency: float):
        """Initialize rate limiter.

        Args:
            frequency: Desired frequency in hertz.
        """
        period = 1.0 / frequency
        self.__next_tick = perf_counter() + period
        self.__period = period

    @property
    def dt(self) -> float:
        """Desired period between two calls to :func:`sleep`, in seconds."""
        return self.__period

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

    def remaining(self) -> float:
        """Get the time remaining until the next expected clock tick.

        Returns:
            Time remaining, in seconds, until the next expected clock tick.
        """
        return self.__next_tick - perf_counter()

    def sleep(self):
        """Sleep for the duration required to regulate inter-call frequency."""
        self.__slack = self.__next_tick - perf_counter()
        if self.__slack > 0.0:
            sleep(self.__slack)
        self.__next_tick = perf_counter() + self.__period
