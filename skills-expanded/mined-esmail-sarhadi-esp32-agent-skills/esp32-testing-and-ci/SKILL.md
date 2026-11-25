---
name: esp32-testing-and-ci
description: Use when setting up tests or CI for ESP32 firmware - nothing can be tested without hardware, the binary no longer fits, or a change breaks a target nobody built. Covers host tests, on-target tests and the checks that catch size regressions.
license: MIT
---

# Testing and CI for ESP32 firmware

Most firmware bugs do not need hardware to find. The trick is putting the logic
somewhere a host compiler can reach it.

## Three layers, three costs

| Layer | Runs on | Catches | Cost |
|---|---|---|---|
| Host tests | your CI machine, native | parsing, state machines, arithmetic, protocol framing | seconds |
| On-target tests | the board, via Unity | drivers, timing, peripheral configuration | minutes, one board per run |
| Hardware-in-the-loop | the board plus instruments | power, radio, real peripherals | slow, fragile, worth it for release |

A project with only the third layer tests rarely. A project with the first layer
tests on every push.

## Making logic testable

The single change that enables everything else: keep protocol and state-machine
code free of `#include <Arduino.h>` and of direct register access. Pass the
hardware in through a small interface. Then the same file compiles for the host.

If a function both decides and transmits, split it. The decision is testable; the
transmit is not.

## On-target tests

Unity ships with ESP-IDF and with the Arduino core. A `test` app that runs the
same assertions on the board catches the things the host cannot: a pin that does
not exist, a peripheral that needs a different clock, a driver that blocks.

## Size budgets

Firmware grows until it does not fit, usually on the day of a release. Record the
size on `main` and fail the build when a change grows it past a threshold:

```
pio run -t size          # PlatformIO
idf.py size              # ESP-IDF
```

A budget turns "it fits on my board" into a number in CI.

## Build matrix

Claiming support for three chips and building one is how a target breaks
silently. If the README lists `esp32`, `esp32s3` and `esp32c3`, CI builds all
three on every push - the compile is cheap next to the debugging session it
prevents.

## Rules for the agent

- New logic goes in a file the host can compile, with a test beside it.
- A bug fix without a test that fails before it is a fix that will regress.
- Never add a hardware test to CI without a timeout: a hung board blocks the queue.
