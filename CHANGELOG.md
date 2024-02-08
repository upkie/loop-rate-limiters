# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.0] - 2024-02-08

### Added

- Documentation

## [0.6.1] - 2023-10-17

### Fixed

- RateLimiter: Initialization of slack attribute

## [0.6.0] - 2023-09-01

### Added

- AsyncRateLimiter: `dt` property

### Changed

- AsyncRateLimiter: `measured_period` is now a property
- AsyncRateLimiter: `next_tick` is now a property
- AsyncRateLimiter: `period` is now a property
- AsyncRateLimiter: `slack` is now a property

## [0.5.0] - 2023-07-25

### Added

- AsyncRateLimiter: ``warn`` constructor argument
- RateLimiter: ``warn`` constructor argument

## [0.4.0] - 2023-04-13

### Added

- RateLimiter: warn when the limiter is running late

## [0.3.0] - 2023-01-20

### Added

- Installation from conda-forge
- RateLimiter: ``dt`` property
- RateLimiter: ``next_tick`` property

### Changed

- Attributes are now read-only
- RateLimiter: ``period`` becomes read-only
- RateLimiter: ``slack`` becomes read-only

## [0.2.0] - 2022/12/5

### Added

- Loop rate limiter for asyncio

## [0.1.0] - 2022/12/2

- Loop rate limiter based on ``time.perf_counter``

[unreleased]: https://github.com/upkie/loop-rate-limiters/compare/1.0.0...HEAD
[1.0.0]: https://github.com/upkie/loop-rate-limiters/compare/0.6.1...v1.0.0
[0.6.1]: https://github.com/upkie/loop-rate-limiters/compare/0.6.0...v0.6.1
[0.6.0]: https://github.com/upkie/loop-rate-limiters/compare/0.5.0...v0.6.0
[0.5.0]: https://github.com/upkie/loop-rate-limiters/compare/0.4.0...v0.5.0
[0.4.0]: https://github.com/upkie/loop-rate-limiters/compare/0.3.0...v0.4.0
[0.3.0]: https://github.com/upkie/loop-rate-limiters/compare/0.2.0...v0.3.0
[0.2.0]: https://github.com/upkie/loop-rate-limiters/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/upkie/loop-rate-limiters/releases/tag/v0.1.0
