---
name: esp32-camera-pipeline
description: Use when an ESP32 camera does not initialise, reboots when the flash fires, produces green or torn frames, or streams too slowly. Covers OV2640 limits, PSRAM framebuffers and the power budget that the camera hides.
license: MIT
---

# Camera pipeline on ESP32

The camera is the most demanding peripheral on the chip: a parallel bus, a clock
it generates, and a current draw that arrives in bursts.

## Resolution and memory

The OV2640 is a 2 MP sensor. JPEG at UXGA (1600x1200) needs a framebuffer in
PSRAM - without PSRAM the driver falls back to smaller modes or fails to init.
Two framebuffers are what makes streaming possible; one means capture and send
cannot overlap.

## Initialisation happens once

`esp_camera_init()` can be called once per boot and there is no matching
de-initialisation. Calling it again - on a sensor event, on a reconnect - faults.
If a design needs to re-configure the camera, it either reconfigures the sensor
registers or restarts the board deliberately.

## Power

The camera plus Wi-Fi transmit is the classic brownout recipe:

- the camera draws current continuously while streaming, not only per frame
- the Wi-Fi transmit burst adds a spike on top
- a USB-serial adapter's 3.3 V pin often cannot supply both

Symptom: a reboot with `Brownout detector was triggered` a few seconds into
streaming. The fix is a supply that can deliver the peak, a bulk capacitor at the
module, and never powering the camera from a programmer's 3.3 V pin.

## Pin conflicts

The camera uses a fixed set of pins on most ESP32-CAM boards, and several of them
are also used by the SD card. Enabling both without checking the schematic gives
a board that boots and then cannot mount the card.

## Throughput

MJPEG over HTTP is the cheap path and it is what most examples use. It is not a
video stream: every frame is a separate JPEG. Clients that expect a real stream
protocol (RTSP, RTMP) need a client library, not the Arduino web server.

## Symptom to cause

| Symptom | Usually |
|---|---|
| init fails with no detail | no PSRAM, or the wrong pin map for the board |
| reboots mid-stream | supply cannot deliver camera + Wi-Fi peak |
| green or torn frames | XCLK too high for the wiring, or one framebuffer |
| works once, then dead | `esp_camera_init()` called a second time |
