---
name: setup-walkthrough
description: "Use when the owner must do a setup by hand: walk them through it one step at a time, never a wall."
version: 1.1.0
author: "coder role of hermes-fleet-apps (adapted from davidondrej/skills setup-help, MIT, Copyright (c) 2026 David Ondrej)"
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [setup, onboarding, installation, configuration, teaching]
    related_skills: [build-method, wizard]
---

# Setup Walkthrough

Use when the owner has to do something themselves in a UI, a dashboard, an installer, or
a config file — and specifically when they must type a key, token, or password,
which the coder never handles.

Assume the owner is busy and not a developer. A 20-step wall makes them close the
window. One step at a time, with the end always in sight, does not.

**Not this skill when the walk is repeatable.** If the owner will do this same setup
again — on another machine, or after a rebuild — build a script with the `wizard`
skill instead of walking it by hand a second time.

## Response format — every single response, no exceptions

```
  <CURRENT STEP>
  One coherent step. 1-4 short lines. Every value they need, spelled out.
  Group fields from the same screen or form together - do not split one
  form into four micro-steps.
  ----
  STILL REMAINING
  1. <headline>
  2. <headline>
  3. <headline>
```

Remaining items are **headlines only** — a few words each. No commands, no URLs,
no values, no explanation. That detail appears only when the item becomes the
current step.

## Rules

- Build the full checklist **before** the first step: from the owner's outline, the
  repo, the docs, the screen they are on, and any prerequisite you discover.
  Keep it internally; never show the whole thing.
- **Never more than 8 items in STILL REMAINING.** More is a wall. If more than 8
  remain, show the nearest steps individually and merge the later ones into
  phase-level headlines. Never drop a step from internal tracking to fit.
- Split only at a real decision, a verification point, or a screen change.
- Discover a new required step mid-setup? Insert it in the right position
  immediately.
- Re-audit the list against the internal checklist before every reply. Fix it
  before sending, not after.
- Never jump ahead. Only the current step gets instructions.
- When a step is done, promote the next one and reprint the format.
- When nothing remains: say setup is complete. Drop the list.

## Secrets

When a step involves a key, token, password, or seed phrase:

- Name the exact file and the exact variable name.
- Tell the owner to type it themselves.
- Do not read it back, echo it, or verify it by printing it.
- Verify by *effect* instead — "run this, you should see a 200".

## Verification

End each step that can be checked with a concrete check and its expected
output: "you should see `ok` printed", not "it should work now". Nobody can
debug a vague success.
