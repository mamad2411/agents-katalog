---
name: ki-stack-verify
description: |
  Verify KiCad changes with render-after-edit workflows, DRC/ERC, and evidence-first
  reporting. Use when a change has been made and the agent needs to prove the result
  instead of merely describing it.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ki-stack-verify

## Purpose

This skill teaches the agent how to prove that a KiCad change actually worked.

It is the canonical `ki-stack` skill for:

- render-after-edit verification
- PCB DRC
- schematic ERC when relevant
- export/check loops
- evidence-first reporting

## When to use it

Use this skill after:

- a live IPC edit
- an offline `kiutils-rs` transform
- a manual KiCad file change that needs proof
- any task where visual and structural correctness matters

## Shared assumptions

- A change is not done until there is evidence.
- Prefer deterministic exports over subjective descriptions.
- Prefer CLI checks when available.
- Report exact outputs, not just impressions.

## Phase 1: Orient

1. Determine the artifact type that changed:

- board
- schematic
- symbol
- footprint
- project metadata only

2. Confirm KiCad CLI availability:

   ```bash
   skills/ki-stack/bin/kicad-cli-path
   skills/ki-stack/bin/kicad-version
   ```

3. Decide which evidence applies:

- visual render
- DRC
- ERC
- file re-inspection
- a combination of the above

## Phase 2: Render evidence

If the change affects anything visual, render it.

Examples:

### Board before/after

```bash
skills/ki-stack/bin/kicad-render pcb-svg board.kicad_pcb before_dir --layers F.Cu,F.SilkS,Edge.Cuts --mode-single
skills/ki-stack/bin/kicad-render pcb-svg board.kicad_pcb after_dir --layers F.Cu,F.SilkS,Edge.Cuts --mode-single
```

### Board 3D proof

```bash
skills/ki-stack/bin/kicad-render pcb-render board.kicad_pcb board.png --width 1800 --height 1200 --side top
```

### Schematic proof

```bash
skills/ki-stack/bin/kicad-render schematic-svg design.kicad_sch out_dir
```

### Symbol or footprint proof

```bash
skills/ki-stack/bin/kicad-render symbol-svg library.kicad_sym out_dir --symbol Device:R
skills/ki-stack/bin/kicad-render footprint-svg my.pretty out_dir --footprint SOIC-8_3.9x4.9mm_P1.27mm
```

## Phase 3: Run machine checks

### PCB DRC

Preferred command:

```bash
skills/ki-stack/bin/kicad-drc-json board.kicad_pcb drc.json
```

Interpretation rules:

- zero violations is strong evidence
- nonzero violations must be reported explicitly
- if the task intentionally leaves existing violations untouched, say so clearly

### Schematic ERC

Preferred command:

```bash
skills/ki-stack/bin/kicad-erc-json design.kicad_sch erc.json
```

If JSON output is unavailable or unsupported by the local version, capture plain CLI output and say that the evidence format is version-limited.

### File re-inspection

For offline file edits, re-inspect the output with `kiutils-inspect` where useful:

```bash
skills/ki-stack/bin/kiutils-inspect output.kicad_pcb --show-unknown --show-diagnostics
```

## Phase 4: Assess

Verification should answer these questions explicitly:

1. Did the output artifact get generated?
2. Does the artifact represent the intended object?
3. Did machine checks pass?
4. If checks failed, are the failures new or pre-existing?
5. Is the result fully verified or only partially verified?

## Phase 5: Report

Always report:

- what was verified
- which commands were run
- artifact paths
- check outputs and whether they passed
- any known limitations in the verification method

Preferred report shape:

```text
VERIFY REPORT
Target: <board|schematic|symbol|footprint>
Visual evidence: <paths>
Checks: <DRC/ERC/inspect outputs>
Result: <DONE|DONE_WITH_CONCERNS|BLOCKED>
Notes: <anything version-specific or unresolved>
```

## Helper assets

References:

- `skills/ki-stack/references/render-recipes.md`
- `skills/ki-stack/references/version-matrix.md`

Helpers:

- `skills/ki-stack/bin/kicad-render`
- `skills/ki-stack/bin/kicad-drc-json`
- `skills/ki-stack/bin/kicad-erc-json`
- `skills/ki-stack/bin/kiutils-inspect`

## Guardrails

- Do not say "looks good" without artifact paths or check output.
- If a check fails, report the failure instead of narrating around it.
- If the local KiCad version limits the available evidence format, say so explicitly.
- If the task changed something visual, render it.
- If the task changed something electrical, run the relevant checks.

## Completion states

- `DONE`: render/check evidence supports the claimed result
- `DONE_WITH_CONCERNS`: evidence exists but is partial, version-limited, or affected by pre-existing violations
- `BLOCKED`: verification command failed irrecoverably or required tooling is unavailable
- `NEEDS_CONTEXT`: the changed target or desired evidence format is unclear
