---
name: ats-mini-radio
description: Control an ATS-Mini Pro SI4732 receiver (tune, seek, mode/band/volume/bandwidth, memories, all device settings) over its network API via the ats-mini MCP server. Use when the user wants to listen to, tune, scan, or configure the physical radio.
---

# ATS-Mini radio control

Drive a physical ATS-Mini Pro receiver through the **ats-mini MCP server**, which wraps the
receiver's HTTP control API. Every tool returns the receiver's status JSON (or an `{"error": …}`
object) so you can confirm the result.

## Before you start

- Call **`get_status`** first. It returns the current `frequency`, `frequencyDisplay`, `mode`,
  `band`, `bandMin`/`bandMax`, `volume`, `rssi`, `snr`, `stationName`, and settings
  (`step`, `bandwidth`, `squelch`, `brightness`, `agc`, `theme`).
- The receiver must be on WiFi and reachable. Connection is configured by the server's
  `ATS_MINI_HOST` env var — if tools return a "cannot reach receiver" error, tell the user to
  enable WiFi on the radio (Menu → Settings → WiFi) and check the host/IP (Menu → Settings →
  About shows the IP).

## Frequency units (important)

`tune(freq)` and the `frequency` field use **band units**, not Hz:
- **FM**: 10 kHz units → `9600` = 96.00 MHz, `10130` = 101.30 MHz.
- **AM / SSB**: kHz → `7150` = 7150 kHz.

Always tune within `bandMin..bandMax` from `get_status` (out-of-range returns an error).
To change band first, use `set_band`.

## Tools

- `get_status()` — read everything.
- `tune(freq)` — jump to an absolute frequency (band units, see above).
- `seek(direction)` — `'next'`/`'prev'` to the next station (not in SSB; can take a while).
- `set_mode(direction)` — `'up'`/`'down'` cycles FM/AM/LSB/USB.
- `set_band(direction=…, index=…)` — `'up'`/`'down'`, or an absolute band `index`.
- `set_volume(direction=…, level=…)` — `'up'`/`'down'`, or absolute `level` 0–63.
- `set_bandwidth(direction)` — `'up'`/`'down'`.
- `set_setting(name, direction)` — adjust any setting by one step (`'up'`/`'down'`). Names:
  `step, squelch, agc, avc, softmute, brightness, calibration, rds, utc, fmregion, theme, ui,
  sleep, sleepmode, zoom, scroll, bandwidth, volume, mode, band`.
- `memory_list()` — non-empty slots (`slot`, `freq` in Hz, `band`, `mode`, `name`).
- `memory_recall(slot)` / `memory_save(slot, name="")` / `memory_clear(slot)` — slots 0–98.
- `autoscan(clear=False)` — sweep the current band and store every station found into memory
  (`clear=True` empties all slots first). Returns `{"found": N}`. Not in SSB; blocks a while.

## Recipes

- **"Tune to 101.3 FM"** → check `get_status`; if `mode` isn't FM / band isn't the FM band,
  `set_band`/`set_mode` first, then `tune(10130)`.
- **"Find a station"** → `seek('next')`, then report `frequencyDisplay` + `stationName`.
- **"Save this as slot 5 named BBC"** → `memory_save(5, "BBC")`.
- **"Scan the band and store every station"** → `autoscan(clear=True)`, then `memory_list()`
  to report what was found.
- **"Louder"** → `set_volume(direction='up')` (or `level=N` for a specific level).
- **"Quieter background hiss"** → raise `set_setting('squelch','up')` or narrow
  `set_bandwidth('down')`.
- **"Dim the screen"** → `set_setting('brightness','down')`.

## Cautions

- Relative settings (`set_setting`, and the directional forms) move one step per call; loop and
  re-read `get_status` to reach a target value.
- Do not try to change WiFi/BLE/USB connection modes — they are intentionally not exposed
  (switching them would drop the link you're using).
- `seek` can block; don't call it repeatedly in a tight loop.
