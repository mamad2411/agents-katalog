---
name: esp32-usb-otg-serial-jtag
description: Use when selecting or debugging native USB device, USB host, USB-Serial-JTAG or OTG functionality on ESP32-family chips; especially when a design assumes every ESP32 has the same USB controller or boot/debug path.
license: MIT
---

# USB, OTG and Serial/JTAG capability

USB is not a uniform ESP32-family feature. The SoC, board routing, PHY, connector and boot configuration determine what is possible.

## Identify the actual USB block

- Record exact chip family, package, module, silicon revision and board schematic.
- Distinguish native USB OTG from USB-Serial-JTAG; they are different blocks with different capabilities.
- Confirm whether the target supports device mode, host mode, OTG role switching or only a debug/serial bridge.
- Check whether an external PHY is required and whether the board actually routes the relevant pins.
- Never infer USB capability from a connector shape or from another ESP32 family.
- Verify pins shared with strapping, JTAG or other peripherals before assigning them.

## Board and power design

- Check connector orientation, D+/D- routing, impedance guidance and ESD protection in the board design.
- Host mode must provide VBUS correctly; do not source 5 V from an ESP32 GPIO.
- Budget inrush current and current limiting for bus-powered devices.
- Define overcurrent and disconnect behavior for host applications.
- Use a suitable USB-C configuration network for the intended role; a USB-C receptacle alone does not negotiate role or power.
- Keep the USB return path and high-speed routing review separate from firmware review.

## Firmware architecture

- Select the ESP-IDF USB stack and component version supported by the target.
- Keep host/device role, endpoint configuration and descriptor ownership explicit.
- Handle enumeration, disconnect, suspend, resume and transfer errors as state transitions.
- Bound endpoint buffers and transfer queues; a host device can send malformed or unexpectedly large data.
- Do not perform filesystem writes, lengthy parsing or blocking logs inside transfer callbacks.
- For USB-Serial-JTAG, confirm boot ROM, console and debugger interactions before changing console routing.

## Debugging workflow

- Verify D+/D- continuity and ESD component placement before changing descriptors.
- Capture enumeration with a USB analyzer or host logs and record VID/PID, interface and endpoint descriptors.
- Compare behavior on a known-good cable and host; charge-only cables can mimic a firmware fault.
- Test repeated unplug/replug, suspend/resume and brownout during transfer.
- Preserve a recovery path if firmware reconfigures USB pins or console routing incorrectly.

## Security and robustness

- Treat host-provided descriptors and payload lengths as untrusted input.
- Validate every descriptor length and transfer result before indexing buffers.
- Do not expose a maintenance command interface over USB without authentication and an explicit service-mode policy.
- Disable unused debug interfaces in production only after validating factory recovery and RMA procedures.

## Acceptance criteria

- Capability claims cite the exact SoC datasheet and target documentation.
- The example compiles for one explicitly named USB-capable target.
- Tests cover descriptor parsing bounds and disconnect/reconnect state transitions.
- Hardware validation records board revision, connector role, cable, host OS and enumeration trace.

## References

- ESP-IDF USB Host: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/usb_host.html
- ESP-IDF USB Device: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/usb_device.html
- ESP-IDF USB Serial/JTAG: https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/usb-serial-jtag-console.html
- Espressif technical documents: https://www.espressif.com/en/support/documents/technical-documents
