---
name: turnstile-evidence
description: Publish or inspect turnstile evidence bundles — the correlated proof that a task's gate state was earned (green gate, plan approval, reviewer ensemble) — via opencode-turnstile evidence. Use when the user asks to publish, inspect, or validate evidence for a task, or wants a pre-landing self-check.
---

# Turnstile evidence

Evidence bundles correlate a task's journaled gate state into a shareable
artifact: the green gate, the plan approval, the reviewer ensemble, and the
journal integrity anchor. A bundle is **a correlated claim, not proof — say
so wherever it is posted**.

## When to use

- Publishing earned state for a task (PR description, sticky comment).
- Inspecting what the journal recorded for a task handle.
- A pre-landing self-check that the ensemble bar was actually met.

## Reading a bundle

- Task handle: `t-<8 hex>` (the journal's task identity).
- `green: true` marks the earned green-gate flag.
- The plan/tests/review sections carry the journaled counts: the reviewer
  ensemble must show 2 unwaived reviewer approvals under the default
  `reviewEnsemble: enforce`, plus the waiver/block/dispatch counts.
- `journal.head` is the sha integrity anchor for the task's session-scoped
  journal tail — the tail the bundle was built from.

## Publishing

Detect context: inside the turnstile repo use `node bin/cli.mjs evidence`;
elsewhere `npx opencode-turnstile evidence`.

- `--format markdown` renders the shareable bundle.
- `--out <name>` writes the `.json` bundle plus a sibling `.md`.
- `--validate` re-checks an existing bundle without writing anything.

If the user names any other options, forward them to the CLI invocation
verbatim. If the CLI rejects an option, surface the usage error verbatim;
never retry blind, never drop the flag.

## Refresh before every PR push

The journal is per-machine, so CI can post a committed artifact but never
refresh it: the badge is whatever `.turnstile/evidence.json` and the sibling
`.md` said when they were last committed. Before opening a PR — and before
every push that adds commits to one — re-emit and commit both files:

1. Run the emitter: `evidence --task latest --out .turnstile/evidence.json`
   (this writes the sibling `.md` too).
2. `git add .turnstile/evidence.json .turnstile/evidence.md` and include them
   in the commit you push.

CI now flags the stale case for you: when the committed evidence predates the
latest non-evidence commit (the head, or its parent when the head commit only
touches `.turnstile/`), the posted badge carries an amber "Stale" notice
instead of reading as current. A normal re-emit → commit → push cycle is never
flagged. Treat a stale notice the same way as a red gate — re-emit and push
the refreshed pair.
