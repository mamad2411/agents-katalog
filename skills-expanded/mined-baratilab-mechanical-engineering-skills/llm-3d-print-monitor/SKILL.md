---
name: llm-3d-print-monitor
description: Monitor and correct an FDM 3D print layer by layer through Klipper/Moonraker — pause after each layer, look at top and front camera images, diagnose defects (under-extrusion, stringing, blobs, poor adhesion), query the printer, and apply small safety-bounded G-code changes (flow, speed, temperature, retraction, pressure advance, Z offset) before resuming. Based on LLM-3D Print (Barati Farimani Lab). Use when a user wants an agent to watch a print, fix a print in progress, or set up camera-based print monitoring; includes a mock printer for rehearsal.
---

# LLM-3D Print monitor

Runs the closed loop from *LLM-3D Print: Large language models to monitor and control 3D
printing* (Jadhav, Pak & Barati Farimani, Additive Manufacturing 114 (2025) 105027;
code at github.com/BaratiLab/LLM-3D-Print-Large-Language-Models-To-Monitor-and-Control-3D-Printing).
Each layer:

1. The printer pauses and parks.
2. You inspect the images.
3. You gather information from the printer.
4. You plan a fix.
5. The fix is checked and sent.
6. The print resumes.

In the paper, a team of agents did this with GPT-4o. Here **you** are the vision model and
the planner. `scripts/printer.py` is the executor and the supervisor. It enforces stage order,
blocks unsafe G-code, and logs everything.

## Set up (once per printer)

1. Follow `references/klipper_setup.md`:
   - two webcams named `top` and `front`;
   - `[pause_resume]` and `[firmware_retraction]`;
   - the `LAYER_INSPECT` macro.
2. Insert the pauses into the sliced file:
   `python scripts/add_layer_pauses.py part.gcode part_mon.gcode [--every N]`.
3. Ask the user for the printer URL, the material, and a one-line description of the part.
   Knowing the part stops you from flagging intended features.
4. **Rehearse first** on the mock printer:
   `python scripts/mock_moonraker.py --port 7125 --fault underextrusion` (or `stringing` or
   `none`), with `MOONRAKER_URL=http://127.0.0.1:7125`.

## The loop

Use one session folder per job, set `MOONRAKER_URL`, and let `P = python scripts/printer.py --session runs/<job>`.

```
P wait                       # blocks until paused at the next layer (or reports the print done)
P snapshot                   # saves layer_N/top.jpg, front.jpg and occupancy
  -> Read both images. Write detect.json.          (format and guidance: references/stages.md)
P record detect detect.json
  if problems:
P query extruder gcode_move firmware_retraction   # pick objects that separate the causes
  -> Write plan.json: 1-2 levers from references/playbook.md, each with a why.
P record plan plan.json
P apply            # dry-run: shows the safety verdict for every line
P apply --live     # all-or-nothing; refused plans send nothing
P resume --live
```

Repeat until `wait` reports `complete`, then run `P report` for the markdown log. Every
detect, query, plan, verdict and resume for each layer is kept in `runs/<job>/session.json`.

## Rules

- **Dry-run first.** Without `--live`, nothing that changes the printer is sent. On a new
  printer, do the first few layers in dry-run, show the user `report`, and go live only once
  they agree.
- **Change little, then look.** Use one or two levers per layer, within the step sizes in
  the playbook. The next layer's image and its occupancy change tell you whether the fix
  worked. Say so in `previous_solution`. If the same lever has failed twice, stop pushing it.
  Name the probable hardware or material cause (clog, wet filament, worn nozzle) and tell
  the user.
- **Stop and tell the user** about layer shift, spaghetti, a detached part, anything
  mechanical, or a fault that keeps coming back. Do not resume a print you think is lost. Ask.
- `safety.py` is the authority on what is sendable (`references/safety.md`). Never work
  around a refusal by sending raw requests to Moonraker. If a bound is wrong for this
  material, ask the user to pass `--limits`.
- Occupancy (occupied pixels / total) is a number that supports your judgement. Your visual
  judgement decides.
- Respect the user's time. With `--every 1`, each layer waits for you. For long prints,
  suggest `--every 3` to `5` after the first layers look good.

## What the paper reported

- The VLM detected failures with accuracy comparable to 14 engineers, evaluated with a
  confusion matrix over common failure modes.
- Closed-loop corrections improved prints of the "CMU" letters and other parts across layers.
- Typical changes: speed to about 75% (`M220`), flow slightly above 100% (`M221`), pressure
  advance up to 0.1, retraction about +25%, a 220 °C nozzle for TPU, and small Z offsets.
- Unsafe classes (shutdown, restart, firmware) were excluded.
- Its logs also show what to avoid. Several changes per layer let speed ratchet down to 30%
  and retraction up to 7 mm. That is why this skill caps steps and cumulative drift.
