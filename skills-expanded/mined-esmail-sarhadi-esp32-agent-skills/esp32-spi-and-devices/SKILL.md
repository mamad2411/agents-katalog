---
name: esp32-spi-and-devices
description: Use when an ESP32 talks to SPI peripherals - the second device on the bus fails, the bus is initialised twice, transfers are slow or corrupted, or the clock rate is a guess. Covers bus versus device, DMA and chip select.
license: MIT
---

# SPI on ESP32

ESP32 SPI has a strict two-level model and most bugs come from mixing the levels.

## Bus, then device

```c
spi_bus_initialize(host, &bus_cfg, SPI_DMA_CH_AUTO);   // once per host
spi_bus_add_device(host, &dev_cfg, &handle);            // once per device
```

Calling `spi_bus_initialize()` twice on the same host returns
`ESP_ERR_INVALID_STATE`. Every device on a host shares the clock, the mode and the
DMA channel; only the chip-select and the clock speed are per device.

## Which hosts are free

On the classic ESP32, SPI0 and SPI1 belong to the flash. HSPI and VSPI are
available to the application. The S3 and C3 have a different count and different
default pins - read the target's datasheet rather than assuming the classic map.

## Clock

Start low. 1 MHz gets a device talking; raise it afterwards and re-test. Long
wires, breadboards and 3.3 V logic at 40 MHz are a combination that works on the
bench and fails in the enclosure. If a device works at 1 MHz and not at 20 MHz,
the answer is wiring, not the driver.

## Chip select

Either let the driver drive CS (`spics_io_num` in the device config), or drive it
manually and hold it across the whole transaction. Half-and-half - driver-driven
CS plus manual toggling - produces frames that are shifted by one byte and look
like a protocol error.

## DMA

A DMA-capable buffer on the classic ESP32 must be in internal RAM. A buffer
allocated in PSRAM transfers garbage or fails outright. See `esp32-memory-and-heap`.

## Symptom to cause

| Symptom | Usually |
|---|---|
| second device returns 0xFF | CS not driven, or the bus was initialised twice |
| data shifted by one bit | wrong SPI mode (CPOL/CPHA) |
| works at low clock only | wiring, missing ground, or no decoupling at the device |
| intermittent corruption under Wi-Fi load | shared DMA channel or too-short CS hold |
