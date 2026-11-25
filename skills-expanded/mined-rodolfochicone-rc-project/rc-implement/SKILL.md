---
name: rc-implement
description: "Implements tickets in dependency order — least code, tests, then the gate. Use to build a ticket. Do not use to author one (rc-tickets)."
argument-hint: "[slug-or-ticket]"
model: sonnet
effort: high
---

# Implement

Build what a ticket describes, verify it for real, and record what it taught. One ticket or a whole
slug's worth in dependency order — the same cycle either way, so there is one skill rather than one per
orchestration style.

Read `$CLAUDE_PLUGIN_ROOT/skills/promoted/rc/references/conventions.md` first — the `.rc` resolution,
Serena navigation, the root-cause rule, the verification-evidence bar and the project-memory contract.

## 1 — Ground

Read the ticket, then the spec it comes from (`_techspec.md`, `_tasks.md`) and the ADRs under
`adrs/`. Consult project memory for the ticket's terms and load the confirmed lessons
(`rc-memory` section B) — they are design constraints for this scope, not suggestions.

**If the ticket, the spec and an ADR contradict each other, stop and report the conflict.** Do not
guess which one wins. Then reconcile the current working tree before editing: know what is already
changed and why.

## 2 — Build the checklist

Extract every deliverable, acceptance criterion and explicit `Validation` / `Test Plan` / `Testing`
item into one numbered checklist, and **print it before implementing** so it is visible and trackable.
Capture the concrete pre-change signal that proves the work is not done yet — the failing test, the
missing endpoint, the wrong output. If you cannot reproduce it directly, capture the strongest
available baseline and state the limitation.

The checklist is a gate: mark each item as its evidence appears, and do not enter verification until
every item is addressed.

## 3 — Write the least code that works

You understood the task in steps 1–2. Now write the *minimum* that satisfies it, stopping at the first
rung that holds:

1. **Does this need to exist?** Speculative, or beyond the ticket's contract → record it as a
   follow-up note, do not build it.
2. **Already in this codebase?** Reuse the helper, type or pattern that already lives here — find it
   with `find_symbol` / `find_referencing_symbols` first. Re-implementing what sits a few files over is
   the most common kind of slop.
3. **Standard library does it?** Use it before hand-rolling.
4. **An already-installed dependency solves it?** Use it. Never add a dependency for what a few lines
   cover.
5. **Only then** write the minimum idiomatic code, mirroring the ticket's `Patterns to Mirror`.

**Never simplify away** input validation at trust boundaries, error handling that prevents data loss,
security, correct concurrency, accessibility basics, or anything the ticket explicitly requests. The
ladder shortens the *solution*, never the comprehension in steps 1–2 — the smallest change in the wrong
place is not lazy, it is a second bug.

Keep scope tight to the ticket. Record meaningful out-of-scope work as a follow-up note instead of
silently expanding. Mark a deliberate shortcut with a `ponytail:` comment naming its ceiling and the
upgrade path.

## 4 — Test

Drive the test side through `rc-tdd`: it owns what a good test is, where the seams are, and the
anti-patterns. Tests must encode **why** the behaviour matters — a test that cannot fail when the
business logic regresses is not adequate.

## 5 — Verify, in a bounded loop

Run every command the ticket lists **plus** the project's own gate — not one or the other. The gate is
this loop's until-condition and is mandatory regardless of commit mode.

Green on the first pass → self-review, resolve anything blocking it surfaces, continue. Red → iterate
**gather evidence → fix root cause → re-verify**, up to **3 cycles**. Diagnose before each fix; route a
stubborn failure through `rc-diagnose` rather than attempting a fourth blind fix.

**Never mark a ticket complete on a red gate.** Still red after the third cycle → stop, leave the
status unchanged, and report it **blocked** with the failing output and what was tried. Premature
success is the one outcome worse than a blocked ticket.

## 6 — Close out

In this order — the sequence matters, because status is the last thing to move:

1. Record durable project facts via `rc-memory`, and any lesson the verification signals taught
   (`--signal ac_gap | gate_fail | spec_deviation`). Only what is not already obvious from the repo or
   the spec.
2. Tick the ticket's checkboxes — only where implementation *and* evidence are complete.
3. Set the ticket status.
4. Update `_tasks.md`.
5. Commit, if and only if commit mode is enabled.

`references/tracking-checklist.md` holds the exact rules for status, checklist and commit updates.
**Never push.** A commit is local; anything outward-facing is the user's call.

## Running a set

For several tickets, resolve the dependency order from each ticket's `dependencies` and run this cycle
per ticket, sequentially. Sequential is the default on purpose: the tickets share one working tree, and
parallel writers over a shared tree is how a run corrupts itself.

Delegate the *read-only* parts freely — recon, library lookups, a second opinion on a diagnosis — to
parallel subagents. Fan out **writers** only when the tickets are genuinely independent and each owns a
distinct folder, with per-agent worktree isolation. When in doubt, stay sequential.

A ticket that comes back blocked stops the set. Do not continue into tickets that depend on it; report
what is blocked and what remains reachable.

## Unattended mode

Walking a roadmap without a human gate per step is **earned, not default**. Ordinary feature work stays
human-gated. Before starting, answer the five readiness questions in `references/loop-readiness.md`
with the user — **any "no" stops it**. A loop does not fix a weak harness; it compounds its errors, and
the effort is better spent on the harness.

When it does run: for each phase, load lessons → decompose with `rc-tickets` → run this cycle per
ticket → verify → record lessons → flip the phase checkbox **only on green**. Stop on a reliable stop
condition: the roadmap is exhausted, a phase cannot reach green, or a decision comes up that the loop
cannot assume.

**Never autonomous, in any mode:** pushing, opening a PR, writing to a tracker, or anything else
outward-facing. Those stop and ask, always.

## Error handling

- Tracking files missing → stop and report the path before claiming completion.
- A step that can only be satisfied by a workaround, or that would introduce a pattern harmful to this
  codebase, is a defect in the ticket. Surface it instead of implementing it.
