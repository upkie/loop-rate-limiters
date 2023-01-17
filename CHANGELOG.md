# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

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
