---
name: loudcheck
version: 0.3.2
description: >
  Loudness compliance verdicts against formal published standards — EBU
  R 128, ATSC A/85, or BS.1770 measure-only. Use it when audio or video has
  to pass a delivery gate: "is this file broadcast-legal?", "will this mix
  get rejected?", "how far off target is it and what's the exact fix?",
  batch-checking a delivery folder, or verifying a fix landed. One
  ffmpeg-based engine; verdict, exact deltas, and remediation — not raw
  meter output.
---

# loudcheck — the loudness gate with the fix attached

Measures integrated loudness, true peak, and LRA, then verdicts against the
standard you name. A fail always includes the exact delta and a copy-paste
remediation. Deterministic per file + standard + ffmpeg build.

## Three things to remember

1. **Formal standards only, never platform folklore.** EBU_R128, ATSC_A85,
   BS_1770 — published documents the verdict can cite. "YouTube wants -14"
   is not a standard and not in this tool, on purpose.
2. **The remediation is part of the verdict.** A fail tells you the exact
   gain or loudnorm invocation to apply — relay it, apply it, re-check.
3. **BS_1770 is measure-only.** It defines measurement, not limits: you get
   numbers, not pass/fail. Picking it because R128 "failed" is gaming the
   gate.

## Exit codes

`0` = pass, complies with the standard · `1` = fail, remediation included ·
`2` = error (missing file, no audio stream, ffmpeg absent, unknown
standard). Note: exit 2 here is an error lane, not the D&D trio's honest
refusal — this tool's refusals are explicit in output.

## Invocation

```bash
loudcheck program.wav                          # EBU R128 (default)
loudcheck spot.mov --standard ATSC_A85 --json
loudcheck delivery/ --all-streams              # batch a folder, every stream
loudcheck mix.wav --detailed                   # + max momentary / short-term (extra pass)
loudcheck --schema                             # machine-readable tool definition
loudcheck-mcp                                  # MCP server (stdio)
```

## Worked example

```bash
loudcheck tone.wav --json
```

```json
{
  "verdict": "fail",
  "standard": "EBU_R128",
  "citation": "EBU R 128 (https://tech.ebu.ch/docs/r/r128.pdf)",
  "metrics": {
    "integrated": {"measured": -27.75, "unit": "LUFS", "target": -23.0,
                   "tolerance": 0.5, "delta": -4.75, "pass": false},
    "true_peak":  {"measured": -24.06, "unit": "dBTP", "max": -1.0, "pass": true},
    "lra":        {"measured": 0.0, "unit": "LU", "pass": true, "informational": true}
  },
  "failures": ["integrated loudness -27.8 LUFS is 4.8 LU under target -23.0"],
  "remediation": ["apply +4.8 LU gain to reach -23.0 LUFS (e.g. ffmpeg -af volume=4.8dB, or loudnorm I=-23)"]
}
```

Exit 1. Apply the remediation, run again, expect exit 0 — the demo GIF in
the README is exactly that loop.

## MUST / MUST NOT

- MUST name the standard the delivery spec actually cites; default is
  EBU_R128 only because Europe's is the common gate.
- MUST re-check after applying a remediation — a fix is a claim until the
  exit code confirms it.
- MUST use `--all-streams` for containers with multiple audio streams; a
  pass on stream 0 says nothing about stream 1.
- MUST report the measured values and deltas, not just pass/fail, when a
  human will decide what to do.
- MUST NOT verdict against platform upload targets (YouTube/Spotify/etc.) —
  out of jurisdiction by design; say so and point at the formal standards.
- MUST NOT eyeball-adjust gain from memory; the remediation string is the
  computed fix.
- MUST NOT treat `--detailed` momentary/short-term numbers as R128 limits
  unless the delivery spec invokes them (EBU Tech 3341 context applies).

## Validation checkpoints (self-audit before reporting)

standard matches the delivery spec · stream(s) covered stated · exit code
read · deltas and remediation relayed on fail · re-check performed after
any fix.

## Cross-skill workflows (check family)

- **Delivery QC:** loudcheck is the audio lane of a delivery gate; pair
  with container/format checks before greenlighting a file.
- **Fix loop:** fail → apply the emitted ffmpeg remediation → re-run →
  attach both verdicts (before/after) as the evidentiary record.

Family contract: [FAMILY.md](https://github.com/chaoz23/srdcheck/blob/main/FAMILY.md).
Note this tool's exit-2 divergence from the D&D trio, recorded there.

## Changelog / stale-knowledge deltas

- Measurement context (ffmpeg version, stream index) is stamped into every
  JSON verdict — cite it when two machines disagree; the meter is part of
  the measurement.
- Standards list is closed: EBU_R128, ATSC_A85, BS_1770. Requests for
  platform templates are refused by design, not by omission.

Verdicts are advisory to the delivery decision; the delivery owner signs.
