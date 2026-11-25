---
name: xiao-webcam-ap
description: >
  Build and flash the XIAO ESP32S3 Sense camera web apps in STANDALONE AP
  (hotspot) mode: a Teachable-Machine-style dataset collector page and a live
  inference viewer page served by the board itself at http://192.168.4.1.
  Use this skill whenever the user wants the camera web app WITHOUT a router —
  classroom/education deployments, demos with no WiFi, per-student boards, or
  says "AP 모드", "핫스팟", "공유기 없이". For router (STA) mode use the
  xiao-webcam-sta skill instead.
---

# XIAO ESP32S3 camera web apps — AP (hotspot) mode

The board becomes its own WiFi hotspot. Clients join the board's SSID and the
page is ALWAYS at **http://192.168.4.1**. No router, no internet needed.
Best for classrooms: one board per student/team, isolated networks.

Read the `xiao-esp32s3` skill (same repo) first for base workflow and pitfalls
(especially: PSRAM flag mandatory, DTR reset-stuck recovery, no serial reads
while a demo must keep running).

## Step 1 — ALWAYS ask the user first

Never invent credentials. Ask the user for:

1. **AP 이름(SSID)** — e.g. `XIAO_01`. For classroom fleets suggest numbered
   names (`XIAO_01`..`XIAO_20`).
2. **AP 비밀번호** — 8+ chars (WPA2 minimum). If the user wants an open AP,
   confirm explicitly.
3. **채널** (optional, default 1) — for MULTIPLE boards in one room, spread
   across 1 / 6 / 11 (board N → channel `[1,6,11][N % 3]`); 20 boards all on
   channel 1 will jam each other.
4. Which app: collector, inference viewer, or both.

## Step 2 — generate the sketch from the template

Templates in `assets/` are verified working code — do not rewrite them:

- `assets/web_collect.ino.tpl` — dataset collector (gallery + delete + ZIP download)
- `assets/web_infer.ino.tpl` — live inference viewer (needs the
  `<project>_inferencing` Edge Impulse library installed in the sketchbook)

Copy the template to `<workspace>\<NN>_<name>\<NN>_<name>.ino` (folder = ino
name), then replace the placeholders literally:

| Placeholder | Meaning | Example |
|---|---|---|
| `__AP_SSID__` | hotspot name | `XIAO_01` |
| `__AP_PASS__` | hotspot password (8+ chars) | `class1234` |
| `__AP_CHANNEL__` | WiFi channel (bare number, no quotes) | `6` |

## Step 3 — compile, upload

```powershell
arduino-cli compile --fqbn esp32:esp32:XIAO_ESP32S3 --board-options PSRAM=opi <SKETCH_DIR>
arduino-cli upload -p COM4 --fqbn esp32:esp32:XIAO_ESP32S3 --board-options PSRAM=opi <SKETCH_DIR>
```

`PSRAM=opi` is mandatory (camera + model need PSRAM). The inference build
needs `--clean` if the Edge Impulse library was just swapped.

## Step 4 — verify WITHOUT breaking the demo

Do NOT open the serial port after flashing (it can leave the board held in
reset — pitfall 8 of xiao-esp32s3). Instead verify from the network side:

```powershell
# the AP should appear in a WiFi scan within ~15 s of flashing
netsh wlan show networks | Select-String "<AP_SSID>"
```

(netsh caches scans — retry after 20 s before concluding failure.)
Full check: connect a device to the AP and open http://192.168.4.1 —
tell the user connecting from THEIR phone/PC will drop that device's
internet while connected; that is expected in AP mode.

## Notes

- Collector page: captures go to an in-browser gallery (label badges, per-shot
  delete, "전체 ZIP 다운로드" produces `label.N.jpg` files ready for Edge
  Impulse). Refreshing the page clears the gallery — download the ZIP first.
- Inference page: whole-frame colored box + top label + per-class confidence
  bars (classification model — per-object location boxes need a FOMO model).
- The camera renders rotated 90°; the inference template already compensates
  (CW feature rotation, verified empirically).
