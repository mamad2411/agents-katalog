---
description: >
  Comprehensive QA arc -- the pre-stabilize audit ritual. A six-step procedural
  audit: forge-review on the dirty tree -> phase-wrap (banking commit) -> commit
  -> audit-code -> project-specific structural sweeps -> triage + conditional
  charter. Catches integration-boundary bugs unit tests and per-commit review
  can't see. Trigger on "qa arc", "run the qa arc", or "full audit before
  stabilize".
user-invocable: true
---

**MANDATORY FIRST OUTPUT -- say this before doing anything else, before any tool calls:**

> **Running /qa-arc...**
>
> *Six steps: forge-review -> wrap -> commit -> audit-code -> structural sweeps -> triage.
> Every step reports what it found, including nothing.*

# /qa-arc -- Comprehensive QA Arc

A six-step procedural audit. Designed for the moment when reactive bug-fixing reveals **integration-boundary bugs prior testing failed to catch** -- cross-component state, cross-screen lifecycle, cross-system invariants, stale phase-N TODOs, and similar. Catches the class of bugs unit tests can't, because they live where two individually-correct components meet.

This is the **pre-stabilize ritual**. Run it once or twice per project, typically before a formal stabilize/shelve phase opens. It's heavier than a normal phase: multiple subagent dispatches, several memory-satellite writes, at least one commit, and a multi-block charter that frames the entire stabilize phase.

---

## When to invoke

- After a substantial bug-fix wave has surfaced **structural** bugs (not just feature bugs) that prior testing missed.
- Before a formal stabilize phase opens and you want to be sure you're stabilizing on top of a known-good audit baseline.
- When reactive work has accumulated and a comprehensive sweep is overdue.
- When the operator directs: "run a comprehensive QA before we ship."

## When NOT to invoke

- For daily feature work. Use `/forge-review` (per-commit review) or `/audit-code` (full read-only audit) in isolation.
- Inside an active phase. Wait for the phase to wrap first -- the QA arc starts from a banked-commit baseline.
- For a trivial bug-fix pass. The arc's overhead (multiple subagent dispatches, multiple satellites) is wasted on a single-bug fix.
- If `/audit-code` alone would suffice. The structural-sweep layer (Step 5) is what differentiates this from a plain audit; if no integration-boundary classes are actually at risk, plain `/audit-code` is the right tool.

The ritual is heavy by design. Run `/audit-code` first as a lightweight check if you're unsure; promote to `/qa-arc` only if that audit finds enough to warrant the structural-sweep and triage layers on top.

**Interstitial invocation.** A QA arc doesn't have to slot cleanly into the project's phase-number sequence. If you're running it between two already-numbered phases (so a `phaseN-charter.md` would collide with a phase number already claimed), skip authoring a numbered charter at Step 6 and instead fold the triage findings into the next real kickoff's context read. The date-stamped gameplan and findings ledger from Step 0 still get written -- they're what the next kickoff reads. If the arc feeds directly into a named stabilize pass, prefer a short descriptive phase name over claiming the next number in sequence -- it avoids plan-file numbering collisions.

---

## The contract

Every run of this arc, regardless of project size, keeps to the same contract:

- Audit runs from a **banked-commit baseline** (dirty work committed first).
- **Arc-scoped artifacts**: a date-stamped gameplan satellite and findings ledger, created before any dispatch.
- **Sweep/lens selection recorded** with rationale, chosen against this project's actual integration boundaries.
- Every finding **cited to file:line**.
- **Adjudicated triage** -- FIX / DEFER / DISMISS / PROMOTE for every finding.
- **Charter and/or report outputs** consumed by the upcoming stabilize phase or next kickoff.
- A running **sweep-classes note** appended after the arc closes, so the next project's arc benefits from this one's choices.

For most projects, six sequential steps (below) are enough dispatch volume to cover this contract. Very large codebases can scale the same contract up (more sweep dispatches, more reviewers per sweep) without changing its shape -- the contract is what matters, not the exact dispatch count.

---

## Step 0: Setup

Before launching the arc, create the gameplan satellite and findings ledger.

**Two artifact lifecycles to keep separate:**

- **Arc-scoped artifacts** (gameplan + findings ledger) -- created at Step 0, consumed throughout Steps 1-6, no purpose after the arc closes. Date-stamp the filenames so multiple arcs across a project's lifetime don't collide.
- **Phase-scoped artifacts** (the phase-wrap satellite from Step 2, plus the conditional charter/execution-plan/task-tracker from Step 6) -- created by the arc but consumed by the **upcoming stabilize phase** for however many sessions that phase spans. These live flat in the project's memory folder alongside other phase satellites for normal discoverability. Don't bury them in an arc-scoped subfolder.

Setup:

1. **Project key:** drive letter lowercased + path with separators replaced by dashes (e.g. `e--myproject` for `E:\MyProject`).
2. **Gameplan satellite (arc-scoped):** `~/.claude/projects/<project-key>/memory/qa-arc-gameplan-<YYYY-MM-DD>.md`. Captures the per-arc scope (which sweep classes were chosen and why) plus a resume protocol if the arc pauses mid-execution.
3. **Findings ledger (arc-scoped):** a scratch file in the project (e.g. `.scratch/qa-findings-<YYYY-MM-DD>.md`, gitignored) that survives compaction. One section per step.
4. **Phase-scoped artifacts** are NOT created here -- they land in the memory folder at their respective steps (Step 2's phase-decisions satellite; Step 6's charter and supporting files).

Create the gameplan and findings ledger before Step 1 so subagents have a consistent place to write findings.

---

## Step 1: `/forge-review` on the dirty tree

**Scope:** all currently-modified files in the working tree. Standard forge-review, all four lenses.

**Why first:** if the dirty tree contains structural bugs you've already found and fixed by hand, forge-review catches the residual code smell and missed refactors before the phase-wrap commit.

**Action:** invoke `/forge-review` directly. It appends findings to its own tracking and applies FIX-category items per its own protocol. Categorize findings into FIX/DEFER/DISMISS/PROMOTE per forge-review's standard categorization.

**Append findings** to the date-stamped findings ledger under the Step 1 heading.

**Resume marker:** Step 1 is complete when all four forge-review lenses have returned, findings are in the ledger, and FIX items are applied. The tree may still be dirty.

---

## Step 2: `/phase-wrap` (banking commit)

**Naming:** this is a normal phase wrap, not the formal stabilize wrap. Give it a name that makes clear it's a bug-fix/audit-prep pass. The point is to **bank** the bug fixes and any forge-review fixes from Step 1 before the audit starts.

**Action:** invoke `/phase-wrap`. It produces the standard wrap deliverables: phase satellite, CLAUDE.md update, memory-index refresh, and a re-triage of prior deferrals whose target phase has now shipped.

**Resume marker:** Step 2 is complete when the CLAUDE.md/memory updates and phase satellite are written and presented to the operator.

---

## Step 3: Commit

Single commit covering source, tests, and memory changes. If the project keeps memory in a separate repository from the code, commit memory satellites separately so the project commit stays purely code.

**Append commit hashes** to the date-stamped findings ledger's Step 3 heading, along with any pre-commit hook output worth preserving.

**Resume marker:** Step 3 is complete when `git status` is clean (or, in a dual-repo setup, both repos are clean).

---

## Step 4: `/audit-code` on the committed tree

**Action:** invoke `/audit-code`. It runs its standard categories (architecture, style, project-health, testing, memory, skills sync) and produces a structured report. Read-only.

**Append a summary** of High/Critical findings to the date-stamped findings ledger's Step 4 heading. Audit-code deletes its own working scratch file at the end of its run; the QA arc's ledger preserves the High/Critical mirror for the triage step.

**Resume marker:** Step 4 is complete when the audit report is presented and the High/Critical mirror is in the findings ledger.

---

## Step 5: Project-specific structural sweeps

**This is the layer that makes `/qa-arc` more than just `/audit-code`.** A small set of focused subagent dispatches targeting integration-boundary bug classes specific to this project. Run two at a time.

### How to choose sweep classes

The sweeps are **templated, not enumerated**. Each project picks 3-7 sweep classes targeting the integration-boundary bugs **most likely to have been missed by prior testing in this specific project.**

To pick:
1. If a running sweep-classes note exists from prior arcs (this project's or an earlier one), read it for choices and rationale that might transfer.
2. Reflect on the recent bug-fix wave: which bugs were structural (cross-component) rather than feature-level? Each structural bug class is a candidate sweep.
3. Identify the project's actual integration boundaries -- rendering vs. logic, multi-tenant vs. single-tenant state, persistence vs. runtime state, whatever applies. Each boundary is a potential sweep class.
4. Cap at 7 sweeps. More than that and the arc loses focus.
5. **Append** the chosen sweep classes and rationale to a sweep-classes note (a plain markdown file kept alongside this skill, or in the project's memory folder) so future arcs -- this project's or another's -- benefit from the choice.

**Standing sweep worth including by default:** a **stale-deferred-ledger drift sweep** -- verify `deferred.md` entries against current disk state; intervening refactors silently resolve entries and invalidate the reasoning behind old dismissals. Skip it only with a stated reason in the gameplan.

### Example sweep set

For a hypothetical multi-user task-tracking application recovering from a bug-fix wave, a reasonable sweep set might look like:

| Sweep | Bug class it catches |
|-------|----------------------|
| Encoding / input audit | Non-ASCII or malformed input reaching a component that assumes a restricted character set |
| Tenant/scope isolation | A cross-tenant aggregate read where a per-tenant read was correct (or vice versa) |
| Lifecycle audit | Recursive component teardown invariants left partially applied (listeners not detached, state flags not reset) |
| Persistence round-trip | Serialization attributes or manual-state classes that silently drop fields on save/load |
| Stale TODO / phase-N comments | Deferred-work comments that quietly became load-bearing once the deferred phase shipped |

Pick sweeps that reflect *this* project's actual boundaries, not this table verbatim.

### Dispatch protocol

For each sweep:
1. Author a focused subagent prompt that:
   - Names the bug class explicitly and gives 1-2 concrete examples from the recent bug-fix wave.
   - Lists the codebase areas to check (specific files, patterns, or call sites).
   - Specifies the report format with file:line evidence per finding.
   - Mandates appending findings to the date-stamped findings ledger's Step 5 heading, under the sweep's own subheading.
   - **Instructs the subagent to read `deferred.md` and `patterns-promote.md` first.** As these ledgers grow across a multi-phase project, a sweep that skips them re-raises findings the project already triaged. Pass both files' current content in the dispatch prompt and instruct: "if a finding matches an existing entry, cite it and skip re-raising unless new evidence changes the disposition."
2. Run two sweeps in parallel. Wait for both to return before launching the next pair.
3. Compliance check: every finding must have a file:line citation. Sweeps reporting "no issues found" should be spot-checked against at least one site before being trusted.

**Resume marker:** Step 5 is complete when all chosen sweeps have returned and findings are in the ledger.

---

## Step 6: Triage + charter + (conditional) supporting satellites

**Read** the date-stamped findings ledger end-to-end. Categorize every finding:

- **FIX** -- apply now (small) or fold into the upcoming stabilize charter (larger)
- **DEFER** -- record in `deferred.md`; not blocking
- **DISMISS** -- record a one-line rationale in `deferred.md` so future audits don't re-raise
- **PROMOTE** -- pattern worth adding to a shared skill file (record in `patterns-promote.md`)

### Output artifacts -- conditional on scope

The number of FIX-category findings determines which satellites get written:

| Triage size | Satellites authored |
|-------------|---------------------|
| 0-1 FIX (clean audit) | One-line charter ("Stabilize phase: clean audit, plan-file scope only.") |
| 2-4 FIX (small triage) | Charter satellite only |
| 5+ FIX (substantial triage) | Charter + execution plan + task tracker (the full set) |

### The satellites (when the full set is warranted)

All land flat in the project's memory folder, alongside other phase satellites.

1. **Charter** -- WHAT to fix. Block A (high-priority structural), Block B (medium extractions), Block C (plan-file scope: performance, polish, packaging), Block D (cross-cutting cosmetic). Deferrals/dismissals/promotions are documented separately in `deferred.md`/`patterns-promote.md`, not repeated here.
2. **Execution plan** -- WHAT ORDER to fix in. Dependency graph, per-step blocked-by lists, risk callouts, explicit anti-patterns to avoid (e.g. "don't interleave this fix with smaller ones already in flight"). Saves the next session from redoing work or breaking a fix in progress.
3. **Task tracker** -- a file-based persistent to-do list with a simple status legend (not-started / in-progress / done / blocked / skipped). Grouped by sub-phase. Includes a resume protocol if the phase pauses mid-execution. Update as tasks complete; don't delete finished entries -- they're the audit trail.

### Sub-split recommendation

If the FIX count is large enough that the charter would produce an unwieldy single phase, the charter should recommend splitting into labeled sub-phases (e.g. `a`/`b`/`c` suffixes on the phase name). The operator may split further at the sub-phase kickoff.

**Resume marker:** Step 6 is complete when the charter (and supporting satellites, if warranted) is presented to the operator for sign-off. The operator then decides whether to start the stabilize phase immediately or pause.

---

## Sub-skill invocation discipline

`/qa-arc` orchestrates -- it does NOT reimplement.

- **Step 1** invokes `/forge-review` directly. Its findings, categorization, and FIX-application protocol carry through unchanged.
- **Step 2** invokes `/phase-wrap` directly. Its CLAUDE.md/memory/phase-satellite discipline carries through.
- **Step 4** invokes `/audit-code` directly. Its category protocol and report shape carry through.

The QA arc adds three layers on top: the six-step orchestration shape itself, Step 5's structural sweeps, and Step 6's conditional satellite outputs.

If a sub-skill's protocol changes, the QA arc inherits the change automatically. Don't duplicate sub-skill doctrine in this file.

---

## Compliance and receipts

At each step, surface a brief receipt to the operator:

- **Step 1:** N forge-review findings; X FIX applied; Y DEFER; Z DISMISS; tests still passing?
- **Step 2:** wrap satellite path; wrap result.
- **Step 3:** commit hash(es); clean-tree confirmation.
- **Step 4:** audit-code summary -- High/Critical count by category; report location.
- **Step 5:** sweep-by-sweep finding count; any high-severity hits.
- **Step 6:** charter scope (block sizes); which satellites were authored.

Receipts go to user-facing text. Detail lives in the date-stamped findings ledger and the satellites.

---

## Resume protocol if the arc pauses mid-execution

If the operator pauses between steps:

1. Read the date-stamped gameplan satellite for the current arc.
2. Read the date-stamped findings ledger to see what's already recorded.
3. Identify the most recently completed step's resume marker; resume the next step.
4. Continue dispatching subagents and updating the ledger until Step 6 completes.

The operator may interrupt at any step to redirect. Default behavior on resume: continue the arc unless told otherwise.

---

## Cleanup

After Step 6 completes and the operator signs off on the stabilize phase:
- **Arc-scoped artifacts** (date-stamped): keep the findings ledger and gameplan satellite until the stabilize phase wraps -- they're useful as the resume artifact if that phase pauses. Delete/archive them at the stabilize wrap.
- **Phase-scoped artifacts** (flat in the memory folder): the Step 2 wrap satellite and the conditional Step 6 set (charter, execution plan, task tracker) are preserved as the stabilize phase's reference artifacts, closed by that phase's own wrap -- not by the arc.

Date-stamped naming on arc-scoped files means multiple QA arcs across a project's lifetime accumulate side-by-side without collision.

---

## Cross-references

- `/forge-review` -- Step 1 sub-skill.
- `/phase-wrap` -- Step 2 sub-skill.
- `/audit-code` -- Step 4 sub-skill.
