---
name: woostack-address-comments
description: Use when addressing the unresolved review threads on a pull request — fix or push back on each finding, reply, resolve, and push. Never merges.
---

# woostack-address-comments

## Overview

Addresses the unresolved review threads on a PR. For each thread it verifies the concern
against the code and recommends **FIX** / **ACCEPT** (push back, with reasoning) /
**CLARIFY**. By **default** it presents the batched recommendations — including the
one-line fix plan for each FIX, so you see *how* it will fix before approving — for your
approval (or per-thread override) before applying anything; with `--auto` it skips the
gate and acts autonomously. After the approved verdicts are applied it replies without performative
language, resolves, records accept-by-design learnings as scoped memory notes when
available, pushes, and offers a re-review. **Never merges.**

## Workflow

When the user invokes `/woostack-address-comments [PR#]`, address the unresolved review
threads on that PR. If no PR number is given, use the current branch's open PR.

This flow is **local only** — it commits, pushes, resolves GitHub threads, and may write
memory. It never merges.

**Lifecycle (A0→A7):**

0. **Resolve skill path** — set `WOO_ADDRESS_ACTION_PATH` to the directory containing this
   `SKILL.md`. All address-comments prompts and scripts live inside this skill directory.
1. **Prefetch** — resolve the PR# (explicit arg, else the current branch's open PR), then
   `bash "$WOO_ADDRESS_ACTION_PATH/scripts/prefetch.sh"` writes every unresolved thread
   (any author) to `$OUTDIR/address-threads.json`, writes changed paths to
   `$OUTDIR/address-changed-paths.txt`, and composes `$OUTDIR/memory.md`. When the repo has
   a `.woostack/memory/` store, memory is scope-routed to the PR's changed files via
   `recall.sh`; otherwise flat `.woostack/memory.md` is used when present.
2. **Precondition** — the working tree must be clean **and** the current branch must be the
   PR head. Otherwise abort before any edit; tell the user to checkout the PR head on a
   clean tree.
3. **Reception loop (analysis only)** — per thread, follow `prompts/address.md`: read →
   understand → verify → evaluate → **recommend** `FIX` / `ACCEPT` / `CLARIFY`. The loop
   makes **no** working-tree edits, **no** replies, **no** resolves, and **no** memory writes;
   it stages a recommended verdict + reasoning + (for a FIX) a one-line fix plan per thread.
   Hosts with subagent support may
   fan out independent threads or file groups to fast workers, but workers only return
   recommendation records and reply/fix drafts. The parent orchestrator validates worker
   output, fills gaps itself or escalates complex threads, and remains the only actor that
   owns the verdict gate, edits, commit, push, replies, resolution, and memory writes.
4. **Verdict gate** — default: the user approves the batch — seeing the planned fix for
   each FIX — or overrides specific threads before anything is applied; `--auto` skips the
   gate; a non-interactive host with no `--auto` aborts rather than acting unapproved. The
   **final** verdict per thread is the override where given, else the recommendation. See
   `prompts/address.md` § Phase 2 for the gate mechanics, including the override→FIX plan
   confirm.
5. **Commit + push** — apply all final `FIX` edits to the working tree → one commit
   referencing the threads → push to the PR head → capture `<sha>` before any reply, so
   "Fixed in `<sha>`" is real. Never force-push.
6. **Reply + resolve + memory** — per handled thread, `scripts/resolve-thread.sh` posts the
   reply then resolves. CLARIFY threads use `RESOLVE=0`: reply only, left open. Only a
   **final** `ACCEPT` writes memory via `scripts/memory-record.sh`.
7. **Report** — summary table: thread → recommended → final → action → memory-written?

Only a **final ACCEPT** (accept-by-design — an ACCEPT the user kept in the default flow, or
one the skill produced itself under `--auto`) writes memory, deduplicated and phrased as a
reusable pattern — never a log of every fix. When `.woostack/memory/` exists, the write is a
scoped note and `MEMORY.md` is rebuilt; otherwise the script appends to flat
`.woostack/memory.md`. Memory is read back as context on the next review run, keeping
re-reviews quiet.

## Hard constraints

- **No merge.** Branch protection and the merge decision stay with the user.
- **No performative replies.** Reply with the technical reasoning or the fix itself.
