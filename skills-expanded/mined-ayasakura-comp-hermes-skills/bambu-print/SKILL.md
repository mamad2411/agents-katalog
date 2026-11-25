---
name: bambu-print
description: Turn a 3D model (STL/OBJ/3MF/GLB, Pixal3D output, or a parametric part you script) into a sliced Bambu .gcode.3mf with the official Bambu Studio CLI and print it on the local Bambu Lab P2S over LAN (MQTT+FTPS); also printer status, AMS, camera, pause/stop. Use for 3D 列印、印出來、切片、Bambu/拓竹、P2S、送印、印表機狀態.
---

# Bambu print (model → slice → LAN print)

Everything lives in `scripts/` (run with absolute paths; they use `~/opt/bambu/venv`).

| Piece | Path |
|---|---|
| Bambu Studio 02.09.01.70 AppImage (extracted, CLI) | `~/opt/bambu/squashfs-root/AppRun` |
| Python venv (trimesh, paho, bambulabs_api, manifold3d, scikit-image) | `~/opt/bambu/venv` |
| Printer config (secret, 0600) | `~/.config/bambu-print/printer.json` |

Known printer: **P2S** (model code N7) on the home LAN. Get its IP and serial from `scripts/printer.py discover` (SSDP) — they are deliberately not written here (this repo is public). IP is DHCP — re-run `discover` if it stops answering.

## 0. One-time setup
1. On the printer: Settings → Network → enable **LAN Only Mode** + **Developer Mode** (needed for third-party MQTT print commands under Bambu's authorization firmware; cloud/Handy app stops working while LAN-only). Read the 8-char **Access Code** from the same screen.
2. `scripts/printer.py setup --ip <IP from discover> --serial <SN from discover> --access-code <CODE> --model P2S --nozzle 0.4 --bed-type textured_plate`
   Never echo the access code back to the user / chat.
3. Verify: `scripts/printer.py status` (read-only).

## 1. Get a model
- User file: STL/OBJ/3MF/GLB path.
- Image → 3D: follow the `image-to-3d` skill (Pixal3D) → `model.stl`/`model.glb`.
- Text → 3D: `create-image` / `qwen-image` (single object, plain background, full body) → `image-to-3d`.
- Functional/geometric parts (brackets, boxes, holders): write a small trimesh/manifold3d Python script with real dimensions (venv has both) and export STL. Prefer this over AI mesh for anything that must fit.

## 2. Check / repair / scale (always for AI meshes)
```bash
scripts/mesh_check.py in.stl                                   # report only
scripts/mesh_check.py in.glb --repair --size-mm 80 --out fixed.stl
```
Repair = decimate to ≤400k faces → scale → drop loose fragments → fix normals/holes → if still not watertight, voxel remesh (`--voxel-mm 0.25`, ~20 s, watertight solid). Orthographic fill may close deep enclosed cavities. Report bbox, watertight, volume, `fits_bed` (P2S 256³).

## 3. Slice (headless, ~seconds–1 min)
```bash
scripts/slice.py fixed.stl --out /tmp/job --name penguin \
  --process "0.20mm Standard" --filament "Bambu PLA Basic" --support auto [--infill 15] [--walls 3] [--brim auto] [--orient] [--scale 1.0]
scripts/slice.py x --out x --list        # list P2S presets (process/filament/machine)
```
Uses flattened official system presets (`<preset> @BBL P2S`), outputs `<name>.gcode.3mf` + JSON (`time_hms`, `weight` g). Patches `printer_model_id` (N7) like the GUI. Figurines/overhangs → `--support auto`; flat functional parts usually `off`. No thumbnail is rendered headless (no GL) — use `image-to-3d/scripts/render_stl_gif.py` for a preview.

## 4. Print — ALWAYS confirm first
Before `send`: run `printer.py status`, show the user model preview, size, time, grams, filament/AMS slot, plate type; ask explicitly 「要開印嗎？」. Only after a clear yes:
```bash
scripts/printer.py send /tmp/job/penguin.gcode.3mf --yes --ams-map 0      # AMS slot 0-based (ams*4+tray); --no-ams / --ams-map -1 for external spool
```
Options: `--plate N`, `--no-level`, `--timelapse`, `--upload-only`. Refuses if printer is RUNNING/PAUSE/PREPARE. Match `ams_trays[].type/color` from status to the filament.

## 5. Monitor / control
```bash
scripts/printer.py status [--json|--raw]   # gcode_state, mc_percent, mc_remaining_time(min), temps, hms errors, AMS
scripts/printer.py snapshot --out /tmp/cam.jpg   # then [[image: /tmp/cam.jpg]]
scripts/printer.py pause|resume|stop --yes        # confirm with user first
scripts/printer.py light on|off
```

## Safety
- Hot, moving machine: never send/stop/pause without explicit user consent in this turn; never use print as a "test".
- Do not claim AI meshes are printable until mesh_check says watertight and slicing succeeded.
- Keep the access code only in `~/.config/bambu-print/printer.json`.
