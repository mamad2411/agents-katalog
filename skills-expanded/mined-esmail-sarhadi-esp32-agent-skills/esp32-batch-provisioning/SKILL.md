---
name: esp32-batch-provisioning
description: Use when more than a handful of ESP32s need Wi-Fi credentials - each unit is typed in by hand, provisioning fails on Android but works on iOS, the QR payload is rejected, or a batch needs the same settings. Covers SoftAP, BLE and QR provisioning plus batch flashing.
license: MIT
---

# Provisioning a batch

One device is a settings screen. A hundred devices is a process, and the process
has to work for someone who did not write the firmware.

## Three mechanisms, three trade-offs

| Method | Good for | Fails when |
|---|---|---|
| SoftAP + captive portal | phones, no app needed | Android drops a network with no internet - the portal never opens |
| BLE provisioning (`wifi_prov_mgr`) | reliable on both platforms | needs an app, and the phone must stay in range |
| QR code with the payload | fastest for a batch | the payload format is not what the app expects |

The IDF's `wifi_prov_mgr` supports both transports behind one API and handles the
proof-of-possession. Use it rather than writing the portal yourself; the edge
cases (Android's network validation, iOS captive sheet) are the whole difficulty.

## The QR payload

The common format is a small JSON or a `WIFI:` string. Whichever you choose:

- Keep it under 100 characters or the code gets dense and phones struggle.
- Include a per-device proof-of-possession or a shared secret, not just the SSID.
- Test with the actual scanner app on both platforms. A payload that only your
  own app can read is not a QR code, it is a private format.

## Batch flashing

`esptool.py write_flash` one unit at a time does not scale past twenty. Options
that work:

- **Multi-port**: `esptool` can run against several ports in parallel from a
  script; a 8-port hub with a scripted loop does 8 units per cycle.
- **Same image, unique identity**: flash one image, then write the serial into
  NVS with a second command (`nvs_partition_gen.py` produces a per-unit binary).
- **Provisioning at first boot**: leave credentials empty and let the installer
  provision. This is the only approach that scales to a technician in the field.

Never bake the site's Wi-Fi password into the image: one leaked binary is the
whole fleet's password.

## After provisioning

The device should report what it got, and the installer should see it:

- Confirm the connection on the device (LED, or a short beep).
- Publish a "provisioned" message to the backend with the serial.
- Keep the AP/portal reachable for a few minutes in case the credentials were
  wrong, then close it.

## Symptom table

| Symptom | Usually |
|---|---|
| portal never opens on Android | no internet on the AP, and the phone refuses the network |
| works on iOS only | captive portal detection differences; use BLE |
| provisioning succeeds, no connection | 5 GHz SSID, or WPA3-only |
| credentials lost after power cut | written to RAM or to a file without commit |
| a batch has the same serial | identity flashed into the image, not per unit |
