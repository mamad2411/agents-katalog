# Subagents — Design Spec

Status of everything in this file: proposed and now being implemented per Task 3 below.

For the reasoning on *why* these are subagents rather than in-thread skills, see the
2026-07-01 "Skills vs. Subagents" entry in `DECISIONS.md`. Short version: these are all
bounded, isolated tasks where we want a result back, not a process to watch.

---

## 1. `pipeline-reviewer`

**Purpose:** Read-only review of any change touching `pipeline/*.py` or
`prompts/scoring.txt` before it gets committed. Specifically flags if scoring thresholds,
verdict logic, or the qualification prompt changed — since those are joint
business/engineering decisions per `CLAUDE.md`, not pure refactors either of us should wave
through alone.

**Why a subagent and not a skill:** We don't need to watch it reason through every line of a
diff — we just want a clear pass/flag verdict back. Its intermediate file reads would clutter
the main session for no benefit.

**Trigger:** Manually ("review this diff before I commit") to start. Once trusted, could be
wired to run automatically before any commit touching `pipeline/` or `prompts/` via a hook —
that's a later step, not part of this build.

**Tools:** `Read`, `Grep`, `Glob` only. Deliberately no `Write`/`Edit` — this agent reports,
it never changes anything.

---

## 2. `docs-sync`

**Purpose:** After a code change that affects pipeline behavior or configuration, checks
whether `docs/*.md` or `CLAUDE.md` are now out of date and updates them to match.

**Why a subagent and not a skill:** This is repetitive housekeeping — we want it done
correctly, not narrated step by step. Isolating it also means a docs-sync pass can't
accidentally touch pipeline code itself.

**Trigger:** Manually after a commit touching `pipeline/*.py` or `railway.toml`, e.g. "sync
the docs with what we just changed." Could later be wired to fire automatically post-commit
via a hook.

**Tools:** `Read`, `Grep`, `Glob`, `Edit` — write access, but should be scoped to `docs/` and
`CLAUDE.md` only (not the pipeline code itself).

---

## 3. `lead-researcher`

**Purpose:** Given a specific lead (shop name + its Supabase row), does supplementary
research beyond what `scorer.py` captures — social media activity, nearby competitor
density, recency of Google posts — to give Matthew richer context before recording a Loom or
making a call.

**Why a subagent and not a skill:** Research work involves many searches and page reads that
would flood the main session with content neither of us needs to reread. We want the
synthesized findings, not the process.

**Trigger:** Manual — "research [shop name] before I record the Loom," typically run right
before `cold-caller` generates the call script, so its findings can feed into that skill's
context.

**Tools:** Web search/fetch tools, plus `Read` (to pull the lead's existing Supabase-derived
context if passed in, e.g. from `scraped_content`).

---

## Build order

1. `pipeline-reviewer` first — lowest risk (read-only), highest immediate value given active
   pipeline changes.
2. `docs-sync` second — pairs naturally with `pipeline-reviewer` once code changes are
   flagged/approved.
3. `lead-researcher` last — most valuable once outreach is flowing regularly.
