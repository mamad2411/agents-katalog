---
name: logging-tradeoffs
description: Use when a deliberate shortcut is taken during a fix or feature, when investigating a bug that might already be logged, or when closing out an entry after a proper fix lands.
---

# Logging Tradeoffs

## Overview

A shortcut without a record is a landmine for whoever touches the code next — often future-you.
This skill defines one convention, `KNOWN_ISSUES.md`, kept at the root of each project, so
deliberate tradeoffs are findable instead of rediscovered the hard way.

**Core principle:** if you knowingly ship something imperfect, write down what, why, and when to
revisit it — in the same motion as writing the code, not as a follow-up you'll forget.

## Before creating a new entry

1. Check whether `KNOWN_ISSUES.md` already exists at the project root. If an equivalent file
   exists under a different name (`TODO.md`, `ISSUES.md`, `BACKLOG.md`), don't create a duplicate
   — ask the user whether to adopt the existing file for this convention instead.
2. If the project has `graphify-out/graph.json`, use the `graphify-recurring-bugs` skill's dedup
   check first — a new bug may be the same root cause as an existing open entry, not a new one.
3. **Ask before creating the file** if it doesn't exist yet. This is a new file the user didn't
   explicitly request — surface the proposed content, get a yes, then write it.

## Entry format

Append one block per issue, most recent first:

```
## <date> — <short title>
- What changed / what shortcut was taken:
- Ceiling (when this breaks):
- Upgrade trigger (what to do when it's hit):
- Status: open | resolved (<date>, <how>)
```

- **What changed**: the concrete simplification, with a `file:line` reference where relevant.
- **Ceiling**: the specific condition under which this stops being good enough — not vague, a
  testable fact ("more than 10k rows", "concurrent writers", "amounts with fractional cents").
- **Upgrade trigger**: what to actually do when the ceiling is hit — a real next step, not "fix
  it properly later."
- **Status**: flip to `resolved` with a date and one line on how, when addressed. Don't delete
  resolved entries — they're evidence the log is actually maintained, not decoration.

## When touching a file with an open entry

If `reviewer` or `coder` touches a file referenced by an open `KNOWN_ISSUES.md` entry, say
explicitly whether the current change resolves that entry, is unrelated to it, or makes it worse.
Silence here is how the same shortcut gets shipped around three times.
