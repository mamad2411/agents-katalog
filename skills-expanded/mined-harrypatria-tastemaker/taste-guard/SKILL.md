---
name: taste-guard
description: Quality gate and fix loop of the Tastemaker suite. Runs the slop scanner, the state matrix, an accessibility trace and a compile trace on generated UI, then fixes findings until clean (max 3 cycles). Use after generating or editing any frontend code, before saying "done", when a hook reports slop findings, or when the user says "check", "verify", "lint the UI", "is this production ready".
---

# Taste Guard: nothing ships with slop

Run after every BUILD step of the Taste Loop and on every hook report. Findings use catalog IDs from `tastemaker/references/slop-catalog.md`.

## Pass 1: Slop scan (automated)

```bash
node <skill-dir>/scripts/slop-scan.mjs <changed paths or src>      # human report
node <skill-dir>/scripts/slop-scan.mjs src --json                  # machine report
node <skill-dir>/scripts/slop-scan.mjs . --project                 # adds stack checks (E11-E13)
```
No shell (chat platforms): apply the catalog's Auto rules by reading the code, top to bottom, and list findings in the same `ID file:line` format.

Fix every **error**. Fix every **warn** or keep it with an `taste-ignore <ID> <reason>` comment the user can see. **Info** is optional polish.

## Pass 2: State matrix (review)

For each view and each async organism, confirm it renders: loading (skeleton at final size), empty (teaches next action), filtered-empty, error (cause + retry, input kept), success, permission-denied; for each control: hover, focus-visible, active, disabled, loading. Missing state = U10 error. Show the matrix only if asked.

## Pass 3: Accessibility trace (review)

Keyboard path through the critical flow (Tab order, Enter/Space, Esc returns focus); landmarks and heading order; names for every control; error association; contrast of any new color pair (`taste-tokens/scripts/contrast.mjs`); reduced motion; 320px reflow; color-only meaning (U15).

## Pass 4: Compile trace (review, or run)

Imports resolve, props and types match, handlers wired, `'use client'` only on interactive leaves, no unused code, keys stable. File-system environments: run the project's typecheck, lint and build and read the real output.

## Fix loop

```
scan -> fix errors -> re-scan touched files
stop when: 0 errors on two consecutive passes, or 3 cycles done
after 3 cycles: report remaining findings honestly with IDs; never claim clean
```
Fix the cause, not the symptom: a V08 raw hex is fixed by adding or using a token, not by moving the hex into a variable inside the component.

## Report line

`Taste: <errors> errors · <warnings> warnings · score <0-100> · BASIC <n>/10 · build: passed|failed|not run`

## Claude Code hook

The plugin's PostToolUse hook runs the scanner on every edited UI file and returns error findings to you as feedback. Treat them as part of this loop. Control with `TASTEMAKER_HOOK=off|warn|block` (default `block`: errors returned as feedback; `warn`: printed only).
