---
name: esp32-lvgl-and-displays
description: Use when an ESP32 drives a display - the panel stays white, the image tears, refresh is too slow, colours are swapped, or LVGL runs out of memory. Covers SPI and RGB panels, DMA buffers, PSRAM and the flush callback.
license: MIT
---

# Displays and LVGL on ESP32

A display is a memory bandwidth problem wearing a UI library. Get the buffer and
the bus right and LVGL behaves; get them wrong and every symptom looks like a
library bug.

## The bus decides everything

| Panel | Bus | Reality |
|---|---|---|
| ST7735, ST7789, ILI9341 | SPI | 40 MHz is the practical ceiling on a short ribbon; a full 320x240 frame is 150 kB, so partial updates only |
| RGB parallel (ESP32-S3) | 16 pins + PCLK | fast, but the pins are fixed and PSRAM bandwidth becomes the limit |
| I2C OLED (SSD1306) | I2C | 128x64 monochrome at 400 kHz is ~20 fps of full redraw; fine for text, not for animation |

## DMA is not optional above 20 MHz

Without DMA the CPU copies every byte and the rest of the firmware starves.
`spi_bus_config` with `max_transfer_sz` large enough for one buffer, then
`spi_device_queue_trans` from the flush callback. Two buffers (double buffering)
remove the visible seam.

## The flush callback is where tearing comes from

LVGL hands you a rectangle and expects you to say when it is done. Sending it
synchronously blocks the LVGL task; sending it asynchronously without
`lv_disp_flush_ready()` freezes the UI. The rule: queue the transfer, call
`lv_disp_flush_ready()` from the transfer-done callback.

## Colours are swapped, inverted, or both

Three independent settings get confused: RGB vs BGR order, inverted vs normal,
and the byte order of 16-bit colour. A red screen that should be blue is one of
them. Fix it in the panel init sequence, not with a colour transform in code.

## PSRAM and framebuffers

A full framebuffer for a 480x320 panel is 300 kB at 16 bpp - more than the
internal RAM left after Wi-Fi. Options, in order of preference:

- Partial buffers in internal RAM (10 to 20 % of the screen), LVGL redraws dirty
  areas only.
- Full framebuffer in PSRAM, but then the flush reads PSRAM over the same bus as
  the panel and the frame rate drops.
- Never put the LVGL draw buffer in PSRAM and the flush in internal RAM: the copy
  costs more than it saves.

## Slow UI that is not the display

| Symptom | Usually |
|---|---|
| white screen, backlight on | init sequence never ran, or reset pin not toggled |
| tearing on scroll | single buffer, or `flush_ready` called before the transfer finished |
| 5 fps with a simple screen | redrawing the whole screen per frame (`lv_obj_invalidate` everywhere) |
| crash after a few minutes | LVGL heap exhausted - `lv_mem_monitor` shows fragmentation |
| colours wrong only on photos | byte order, not the palette |
