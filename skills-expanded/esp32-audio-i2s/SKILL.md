---
name: esp32-audio-i2s
description: Use when ESP32 plays or records audio - clicks and pops, wrong pitch, buffer underruns, a microphone that returns silence, or a codec that will not lock. Covers I2S clocking, DMA buffers and master/slave roles.
license: MIT
---

# I2S audio on ESP32

Audio problems are timing problems. The data is almost always correct; the clock
is not.

## Who is the master

One side generates BCLK and WS (and often MCLK); the other follows. Get this
wrong and you get silence or noise, never an error.

- A MEMS microphone module (INMP441 and similar) is usually a **slave**: the ESP32
  must generate the clocks.
- A codec (MAX98357, PCM5102, ES8388) may be either; read its datasheet.

## MCLK

Some codecs need a master clock at 256x the sample rate and will not lock without
it. If the codec stays silent and everything else looks right, check whether MCLK
is wired at all.

## Buffers

DMA is described by a buffer count and a buffer length. Too few buffers and any
scheduling hiccup becomes an audible gap; too many and latency grows. Four to
eight buffers of a few milliseconds each is the usual starting point.

An underrun is a click, not an error code. If clicks appear only when Wi-Fi is
active, the DMA starved - raise the buffer count before touching the sample rate.

## Sample rate accuracy

The default clock source divides the peripheral clock, which gives a small error.
A 44.1 kHz stream from a divided 80 MHz clock is not exactly 44.1 kHz, and over a
long recording the drift is measurable. The audio PLL exists for this; use it when
the rate must be exact.

## Symptom to cause

| Symptom | Usually |
|---|---|
| total silence | wrong master/slave role, or MCLK missing |
| pitch shifted | sample rate mismatch between the two sides |
| periodic clicks | DMA underrun, too few buffers |
| noise only when Wi-Fi is on | buffer starvation or a shared power rail |
