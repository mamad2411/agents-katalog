---
name: verify
description: "Verify final deliverables against commitments before marking work complete. Use after capture/compose to check video proofs, screenshots, or QA reports. Examples: \"verify this demo\", \"check the deliverable\", \"did we meet all commitments\", \"qa validation\""
---
# Verify

The orchestrator routed you here. This atom checks the final deliverable against the commitments made at the start of the workflow.

## Inputs

You receive:

1. **Commitments** from the command's parse step -- the promises made about what the deliverable would contain
2. **Compose outputs** -- the finished artifact(s) and their metadata, including
   the `handoff` path to the JSON artefact that carries `target_resolution`

## Video deliverables

### Technical checks

Run `ffprobe` on the final .mp4:

```bash
ffprobe -v quiet -print_format json -show_format -show_streams <video>
```

| Check | Pass condition |
|---|---|
| Exists and plays | ffprobe exits 0, duration > 0 |
| Resolution | Matches `target_resolution` from the compose handoff artefact. When that file or field is absent, matches the target the effective fidelity and props produce: each explicit `width`/`height` is kept, each missing dimension falls back separately to the fidelity default (`inspect` => 2560x1440, `compact`/`standard` => 1920x1080) |
| Pixel format | yuv420p |
| File size | Under 5 MB for GitHub embeds (25 MB hard limit) |
| Duration | Must fall within the compose pacing table's target range for this demo type: **30-45s** (single feature), **45-75s** (side-by-side comparison), **60-120s** (multi-phase). Below the minimum is a **failure** — re-compose with a lower speed factor or re-capture with more steps. |
| Filename | Includes PR number or meaningful identifier |

### Commitment checks

Walk through each commitment from the parse step:

| Commitment | How to verify |
|---|---|
| Title card | Video starts with a static frame showing PR info (check first 5s) |
| Side-by-side layout | Video shows two panels with a divider |
| Showcase polish | Resolution matches the target from Step 0, window chrome and rounded corners visible |
| Keystroke overlay | Pill overlays appear at interaction points |
| Effects | Effects matching the committed tier are present (utilitarian: zoom/keystroke; full: spotlight, zoom, callout, keystroke) |
| Speed note | Title card mentions playback speed |

### Content checks

- Every claim from the "what to prove" analysis has visible evidence in the video
- Both states (before/after, input/result) appear on screen
- No dead time longer than 3 seconds without visible activity

## Screenshot/snapshot deliverables

### For proofs

| Check | Pass condition |
|---|---|
| Evidence exists | Screenshots/snapshots at every claimed proof point |
| Environment stated | Driver, terminal/browser, OS identified |
| Conclusion present | Evidence explicitly supports or refutes the claim |
| Before/after paired | If comparison, both branches shown at same capture points |

### For QA reports

| Check | Pass condition |
|---|---|
| Step coverage | Every defined test step has a result (PASS/FAIL) |
| Evidence attached | Screenshots/snapshots at every step |
| Failures documented | Failed steps have evidence and description |
| Report structured | Markdown report follows the QA template |

## Step 0 — run the sidecar for video deliverables

Before manual checks, run the technical checks:

```bash
./scripts/check-video.sh <video.mp4> --type single
```

Use `single`, `side-by-side` or `multi` for `--type` (pick one value — the
`a|b|c` notation is documentation, not a command).

The sidecar defaults to 1920x1080 for every type, so pass `--resolution` with
the **target** size you asked the renderer for.

1. **Prefer the compose handoff artefact.** Compose writes
   `<deliverable>.handoff.json` (or whatever path it reports as `handoff`), and
   it already carries the renderer-resolved target:

   ```bash
   jq -r .target_resolution /tmp/demo-pr-11621.handoff.json
   ```

   That value comes from the same `resolve_target_dimensions` /
   `resolve_fidelity` code the render path uses
   (`scripts/render-showcase-helper.py`, reached from
   `scripts/render-showcase.sh` via `--handoff`), per-axis fill included. Use it
   verbatim: it is the renderer's target, not a measurement, so it is safe as a
   pass condition. Do not re-derive it.
2. **Fallback — only when the field or the file is absent** (older handoffs).
   Resolve the target exactly the way the renderer does —
   `scripts/render-showcase-helper.py:9-24` (`resolve_fidelity`) and the
   per-axis fill in `resolve_target_dimensions`:
   
   a. **Resolve the effective fidelity first.** A `--fidelity` flag on the
      `render-showcase.sh` command line wins, unless it is `auto`. Otherwise a
      `fidelity` set in the props wins, unless it is `auto`. Only when both are
      absent or `auto` does the layout decide: `side-by-side` => `inspect`,
      anything else => `standard`. An omitted `fidelity` behaves like `auto`, so
      a side-by-side render with no `fidelity` in the props and no `--fidelity`
      flag is still `inspect`.
   b. **Fill each dimension separately, from that effective fidelity.** Width
      and height are resolved one at a time: an explicitly given `width` or
      `height` is kept as-is, and each missing (absent or `null`) dimension is
      filled from the effective fidelity's default — `inspect` => 2560x1440;
      `compact` or `standard` => 1920x1080. So `fidelity: inspect` with only
      `width: 1920` renders **1920x1440** (width kept, height from the inspect
      default): check it with `--resolution 1920x1440`. Likewise
      `fidelity: inspect` with `width: 1920, height: 1080` really renders
      1920x1080 — do not reject either of these against the 2560x1440 profile
      default.

   Rather than doing this by hand, run the helper on the props:
   `PROPS_JSON="$(cat showcase-props.json)" python3 scripts/render-showcase-helper.py handoff /tmp/handoff.json auto props.json`.

Never take the expected size from the **measured** fields of the compose
handoff (`resolution`, duration), the render log, or an existing
`verification.json`: those carry the measured size of the render. Feeding that
back in makes the check compare the render against itself and approves a
1920x1080 output that was asked for at 2560x1440. The sidecar treats
`--resolution` as the pass condition, so a measured/target mismatch is a hard
failure — that is the check working, not a false alarm.

Example — handoff present:

```bash
TARGET=$(jq -r .target_resolution /tmp/demo-pr-11621.handoff.json)
./scripts/check-video.sh /tmp/demo-pr-11621.mp4 --type side-by-side --resolution "$TARGET"
```

Example — no handoff (fallback), side-by-side with `"fidelity": "inspect"` and
no explicit dimensions:

```bash
./scripts/check-video.sh <video.mp4> --type side-by-side --resolution 2560x1440
```

It validates plays, resolution against that target, pixel format (yuv420p),
size (5MB comfort / 25MB hard), and the duration window for the demo type.
JSON output, non-zero exit on hard failure. Fix what it flags before spending
time on commitment/content review — a wrong resolution never passes.

## Chaining into showcase

Verify is not the end of the line — it feeds `compose`/`showcase`.
After all checks pass, write `verification.json` next to the deliverable:

```json
{
  "video": "<path>",
  "type": "single | side-by-side | multi",
  "resolution": "1920x1080",
  "duration_s": 42,
  "commitments_met": ["title card", "side-by-side layout"],
  "sidecar": { "ok": true, "checked_at": "<ts>" }
}
```

Copy the technical fields from the sidecar JSON — `resolution` there is the
**measured** size, which is safe to record only because Step 0 already failed
the run when it differed from the target. Consumers trust this file instead of
re-probing, so never hand-write it and never paste a target into `resolution`
that the measured check did not confirm. `compose`/`showcase`
consume this file instead of re-probing the video. If any check fails,
chain backwards instead: report the failed stage (capture or compose)
and re-verify after the fix — never forward a failing deliverable.

## Failure handling

If any check fails:

1. Identify which stage produced the problem (capture or compose)
2. Report the specific failure: "Side-by-side layout was committed but the output is a single panel"
3. Go back to the failed stage and fix it
4. Re-verify after the fix

Do not report a deliverable as complete until every commitment is met.

## Output

```
## Verification

### Technical
- Resolution: 1920x1080 ✓
- Duration: 42s ✓
- Size: 3.2 MB ✓
- Format: yuv420p ✓

### Commitments
- [x] Title card with PR info
- [x] Side-by-side comparison layout
- [x] Showcase hero preset applied
- [x] Keystroke overlay visible

### Content
- [x] Fork creates independent session (visible at 0:18)
- [x] History diverges after fork (visible at 0:32)

All commitments met. Deliverable ready.
```
