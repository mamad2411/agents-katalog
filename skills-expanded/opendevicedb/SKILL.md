---
name: opendevicedb
description: Use before and after reverse engineering any hardware device (drone, camera, router, smart plug, robot, wearable, BLE/USB/Wi-Fi gadget). Always call the OpenDeviceDB lookup_device tool before starting, so you do not redo work that already exists or that someone else is doing, and call publish_findings when you finish.
license: CC0-1.0
---

# OpenDeviceDB: check before you reverse engineer, publish when done

OpenDeviceDB is an open directory of devices whose protocols or firmware have already been
reverse engineered, with live "claims" saying who is working on what. It is reached through
the `opendevicedb` MCP server (tools `lookup_device`, `search_devices`, `claim_device`,
`publish_findings`, `request_device`, `list_sources`).

## Before any reverse-engineering work

1. Collect identifiers first: FCC ID from the label, USB `vid:pid` (`lsusb`), BLE advertised
   name, Zigbee model id, vendor and exact model.
2. Call `lookup_device` with them. Read `recommendation` and act on it:
   - **open-firmware / controllable**: use the listed firmware, SDK or library. Do not start
     reverse engineering unless the user's goal is something they do not cover.
   - **partial-protocol**: build on the documented interfaces and projects; work only on the
     missing part.
   - **live claim by someone else**: tell the user who holds it, its scope and expiry, and
     the contact. Do not duplicate it; pick another scope or coordinate.
   - **found: false / nothing public known**: go on. If the user does not want to reverse
     engineer it themselves, give them the `request.url` (to add a 👍 to the existing request)
     or the `request_url` (a pre-filled public GitHub issue they review and submit), or call
     `request_device`. Never submit a request yourself.
3. If the user wants to **install** open firmware or software on it, read the record's
   `install` routes (official `guide`, `installer`, `difficulty`, `tools`, safety flags).
   Walk them through the easiest route that fits, with the project's own guide: check
   `firmware_constraints` against their firmware version, have them back up first, and say
   plainly the `brick_risk`, whether it is `reversible` (and the `revert` guide), and whether
   it `opens_device`. Never guide step by step a route that opens a `mains_powered` device:
   give the official link and a mains-voltage warning. Nothing is flashed from OpenDeviceDB.
   Each project's `freedom` says what stays proprietary (`nonfree`) and whether the vendor
   `cloud` is still needed (none, setup-only, optional, required); absent means unknown.
4. If you are going to work on it, call `claim_device` (who = the user, contact, a precise
   scope, days ≤ 90) and give the user the git / `gh pr create` command from the result so
   the claim becomes visible.

If the tools are unavailable, say so to the user instead of silently skipping this step.

## While working

Never work on anything whose purpose is to defeat a safety or compliance function (drone
Remote ID, geofencing / no-fly zones, radio power limits, emissions, medical interlocks),
and never copy firmware images, vendor code, keys or credentials into what you publish.

## When you finish (or stop, even with partial results)

Call `publish_findings` with the device `id` and a `patch`:

- `summary`: one plain paragraph of what is now known;
- `status`: only if it moved forward (`partial-protocol`, `controllable`, `open-firmware`);
- `interfaces`: one per transport, with `status`, honest `confidence` (untested AI work is
  `low` or `medium`) and `spec` = URL of the protocol write-up;
- `projects`: your code or docs, hosted elsewhere under an open license;
- `install`: install routes you used or confirmed (project, method, official guide URL,
  difficulty, safety flags); merged by method + guide;
- `verification`: `hardware-replay` only if a replayable test ran on the real device (give
  the firmware version);
- `provenance`: `ai_assisted: true` and the tools used;
- `release_claim_of`: the `who` of your claim.

If it returns errors, fix the patch and retry; nothing is written until it validates. Then
give the user the git / `gh pr create` command from the result (you may run it if they
agree).

---
This skill file is dedicated to the public domain under CC0-1.0, so any tool may embed it.
