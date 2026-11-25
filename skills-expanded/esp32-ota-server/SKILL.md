---
name: esp32-ota-server
description: Use when firmware updates are served to devices - an update downloads and does not boot, a bad release bricks a batch, devices update in a loop, or the rollback never happens. Covers versioning, staged rollout and the server side.
license: MIT
---

# The server side of OTA

The device code is the easy half. The hard half is deciding who gets which
binary, and what happens when that binary is wrong.

## Version comparison is a protocol

Compare versions as numbers, not strings: `1.10.0` is newer than `1.9.0` and
older than `1.10.1`, and a string comparison gets both wrong. Send a monotonic
build number as well - it is the only thing that survives a human typing the
version wrong.

The device should also report its hardware revision. A binary built for rev B on
a rev A board is a bricked unit that passed every check.

## Never serve a binary that has not booted

The pipeline, in order:

1. Build, run the host tests.
2. Flash one device on the bench, boot it, run a smoke test over the network.
3. Mark the release as "canary" and give it to 1 to 5 % of the fleet.
4. Watch the failure signal for 24 hours.
5. Promote, or pull.

The failure signal must be something the device reports, not something a human
notices: boot count, uptime after update, panic count, reconnect count.

## Rollback needs a trigger

`esp_ota_mark_app_valid_cancel_rollback()` is what makes an image permanent. If
the new firmware never calls it, the next reset rolls back - which is a safe
default and a confusing bug when you forget it. If it calls it immediately at
boot, rollback never happens even when the device is broken.

The pattern that works: mark valid only after the device has connected to the
network and served one successful request, with a timeout. A device that cannot
connect rolls back by itself.

## Update loops

| Symptom | Usually |
|---|---|
| updates, reboots, updates again | version reported is the old one - NVS not updated, or the app reads the file version |
| update succeeds, device offline | new firmware has wrong credentials or a new partition layout |
| half the fleet never updates | server returns 200 with an HTML error page; the device checks size, not content |
| update stalls at 90 % | chunked transfer with no `Content-Length`, or a proxy timeout |
| device bricks after power loss mid-update | single OTA slot; the running image was overwritten |

## Serving the file

- HTTPS with a certificate the device trusts (cert bundle, not pinned to one CA).
- `Content-Length` set, and a stable ETag so a resumed download is possible.
- Range requests if you want resumable updates over flaky links.
- The binary behind a signed URL, and the signature checked on the device if the
  fleet is worth attacking.

## What to log on the device

Report, per attempt: version before, version after, bytes, duration, result, and
the reason for failure. Without that, "some devices did not update" is a
diagnosis you cannot make.
