---
name: godot-verify
description: Run a Godot project headlessly and prove a change actually works before reporting it as done. Use this after writing or editing any GDScript, scene, or resource — and always before telling the user something is finished, fixed, or working. Covers headless import, parse checking, GdUnit4/GUT test runs, and reading exit codes honestly. If you changed Godot code and have not run this, you do not know whether it works.
category: engineering
---

# Godot Verify

This is the skill that makes every other Godot skill worth having. Without a way to run the
project, generating GDScript is guessing with syntax highlighting.

This skill owns the **rule**. When the Randroids-Dojo `godot` skill is installed, it owns the
**machinery** — GdUnit4 wiring, PlayGodot E2E automation, `run_tests.py`, `validate_project.py`.
Prefer those over anything hand-rolled. Everything below is the fallback.

## The core rule

Never write "this should work", "this now works", or "fixed" about code you have not executed.
Either run the verification and report what it said, or state plainly that you could not run it
and why. Those are the only two honest options.

A `Stop` hook in this pack enforces this: if `.gd`, `.tscn`, or `.tres` files changed and
nothing was verified, the turn is blocked. Do not work around it by making a claim vaguer.

## Level 0: import the assets

A fresh clone has no `.godot/` cache. **Running the project does not import** — importing is an
editor pass. Skip this and you get missing-asset failures that look like code bugs:

```bash
godot --headless --path . --import
```

Once per checkout, and after adding assets. On builds without `--import`, use
`godot --headless --path . --editor --quit`.

## Level 1: does the project still load?

The cheapest check, and the one that catches broken scene files:

```bash
godot --headless --path . --quit ; echo "exit: $?"
```

## Level 2: does the script parse?

```bash
godot --headless --path . --check-only --script res://scripts/player.gd
```

Fast, catches syntax errors and unknown identifiers without running anything. Good on each file
you touched before moving to tests.

## Level 3: do the tests pass?

If the project uses **GdUnit4** (look for `addons/gdUnit4/`):

```bash
godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://test
```

`-a` points at a test directory or a single file. GdUnit4 also ships `runtest.sh` / `runtest.cmd`
wrappers at the addon root which handle some environment setup — prefer them if present.

If the project uses **GUT** (look for `addons/gut/`):

```bash
godot --headless --path . -s res://addons/gut/gut_cmdln.gd -gdir=res://test -gexit
```

`-gexit` is required or the runner will not exit and your command will hang.

If the project has **no test framework**, say so rather than silently skipping verification.
Offer to add GdUnit4 — it supports scene tests and input simulation, which matters for gameplay
code a pure unit test cannot reach.

## Level 4: does it actually play?

Unit tests do not catch "the player falls through the floor". Use a tool built for it rather
than hand-rolling a `SceneTree` script — driving physics frames and awaiting correctly from a
bare main loop is fiddly and easy to get subtly wrong:

- **GdUnit4's scene runner** — instantiate a scene, simulate input, advance a known number of
  frames, assert on the result. See the Randroids skill's `references/scene-runner.md`.
- **PlayGodot** — Playwright-for-games over Godot's debugger protocol: node control, method
  calls, property inspection, input simulation, screenshots. See `references/playgodot.md`.

Both give you a real frame loop and real assertions. If neither is installed, say that the
gameplay behaviour is unverified rather than substituting a script you also have not run.

## Reading the output honestly

Godot prints a lot on stderr that is not failure — shader cache messages, import notices, audio
and driver warnings, first-run cache chatter. Plenty of those lines literally start with
`ERROR:`. Matching bare `ERROR:` produces false failures; match the patterns that mean something:

```
SCRIPT ERROR | Parse Error | Failed to load | Cannot open file | Resource file not found
```

Conversely, Godot will sometimes print a real error and still exit 0. Read both.

What counts as a pass:

- Exit code 0, **and**
- no lines matching the patterns above, **and**
- if tests ran, the runner's own summary shows zero failures

If any of those is not true, the change is not done. Report the actual error text rather than
paraphrasing it — the exact message is what the user will search for.

## The bundled runner

`scripts/verify.sh [project-dir] [test-dir]` runs Levels 0–3, detects GdUnit4 or GUT, applies
the error patterns above, and writes `<project>/.godot/verify-stamp` so the `Stop` hook knows
verification happened. Set `GODOT_BIN` if the binary is not on `PATH`.

## If Godot is not on PATH

Ask the user for the binary path rather than fabricating a result. Common locations:
`/usr/bin/godot`, `/Applications/Godot.app/Contents/MacOS/Godot`, or a versioned name like
`godot4`. Once known, export `GODOT_BIN` and use it for the whole session.

## The loop

When a check fails: read the actual error, form one hypothesis, make the smallest change that
tests it, re-run. Do not stack three speculative fixes and re-run once — when it passes you will
not know which one mattered, and when it fails you will not know which one broke it.
