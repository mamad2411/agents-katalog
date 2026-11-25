---
name: esp32-time-and-rtc
description: Use when ESP32 time is wrong, certificates fail to validate, schedules fire at the wrong hour, or the clock drifts across deep sleep. Covers SNTP, time zones, the RTC across sleep, and why time must be checked before it is trusted.
license: MIT
---

# Time on ESP32

The ESP32 has no battery-backed clock by default. Time comes from the network,
and until it does, `time()` returns 1970.

## SNTP is asynchronous

`configTime()` and `esp_sntp_init()` return immediately. Reading the clock on the
next line gives a 1970 timestamp, and anything that depends on a plausible date -
TLS certificate validation most of all - fails for a reason that looks unrelated.

Wait for a sane value with a timeout:

```c
time_t now = 0;
for (int i = 0; i < 50 && now < 1600000000; i++) { delay(100); time(&now); }
```

## Time zones

`TZ` is a POSIX string, not an offset. `CET-1CEST,M3.5.0,M10.5.0/3` carries the
DST rules; `UTC+3:30` does not and will be an hour wrong twice a year. Set it once
at boot and call `tzset()`.

## Across deep sleep

- The RTC keeps counting during deep sleep only if a 32 kHz crystal is fitted.
  Without one, the internal RC oscillator drifts by percent, which is minutes per
  day - fine for a wake timer, useless as a clock.
- `RTC_DATA_ATTR` variables survive sleep; normal RAM does not. If you store an
  offset, store it there.

## Certificates depend on this

A TLS handshake with a clock in 1970 fails with "certificate is not yet valid",
which reads like a certificate problem. If HTTPS works on the bench and fails
after a power cut, check the clock before the CA bundle.

## Schedules

A schedule that must survive a reboot needs an absolute time, not "in 8 hours".
Store the next due timestamp, and on boot compare against network time once it is
available. An interval counter reset by a power cut fires at the wrong time
forever after.

## Rules for the agent

- Never trust `time()` without a floor check.
- Never compute a time zone offset by hand - use a TZ string with DST rules.
- If the product schedules anything, state what happens when the network is down.
