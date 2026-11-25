---
name: slopnought-audit
---

# Codebase Refactoring Mode — `/slopnought-audit`

This mode is invoked when the user runs `/slopnought-audit` (or asks in equivalent terms: "audit this codebase for maintainability," "find tech debt," "what's wrong with this code," "help us clean this up"). It analyzes an existing codebase, produces a prioritized, evidence-based remediation plan, and — only with the user's direction — applies improvements.

This is inherently a larger, more deliberate process than code generation mode. Resist the urge to start "fixing" things the moment something looks wrong; the audit's value comes from seeing the whole picture before touching anything, and from giving the user control over scope and risk.

## Overview of the workflow

1. **Scope the audit** — figure out what's in bounds before scanning everything blindly.
2. **Scan** — systematically work through the codebase against the checklist below.
3. **Score and prioritize** — turn raw findings into a ranked list based on risk × effort.
4. **Report** — produce a clear, evidence-backed remediation plan the user can act on.
5. **Remediate (optional, by consent)** — apply fixes, starting with the highest-priority/lowest-risk items, in reviewable increments.
6. **Preserve context** — write ADRs and documentation so the improved state doesn't silently decay again.

## Step 1: Scope the audit

Before scanning, clarify (ask the user if it's not already obvious from their request):
- **Whole codebase, or a specific area?** ("audit the payments module" vs. "audit everything")
- **Read-only analysis, or analysis + remediation?** Some users want only the report; others want fixes applied.
- **Any known pain points already?** Existing complaints ("the auth module is a nightmare," "we keep breaking the checkout flow") are valuable signal — they tell you where to look first and validate findings against lived experience, not just static analysis.
- **Constraints?** Languages/frameworks the team won't budge on, deadlines, areas that are intentionally legacy and out of scope (e.g., "ignore the old v1 API, it's being deprecated anyway").

If the user has already given enough detail to proceed (named the codebase or directory, said "audit everything," etc.), don't block on these questions — proceed and note assumptions in the report instead of front-loading every clarifying question.

## Step 2: Scan

Work through the codebase systematically rather than reading files at random. A reasonable order: get the lay of the land (directory structure, entry points, README/docs if any, dependency manifest), then go layer by layer or module by module.

For each of the categories below, look for concrete evidence — file paths, line ranges, repeated patterns — not vague impressions. Every finding in the eventual report should be traceable to something specific.

### Architectural weaknesses
- Is there a discernible layering (UI/business logic/data access, or equivalent)? Is it actually followed, or has it drifted (anti-pattern #8 in [anti-patterns.md](../slopnought/references/anti-patterns.md))?
- Are dependencies pointing the right direction (lower layers not depending on higher ones)?
- Are there circular dependencies between modules?
- Is there a clear "front door" to the system (entry points are easy to find), or does understanding require tracing through many files to find where execution starts?

### Code smells and duplicated logic
- Search for repeated logic — similar function bodies, copy-pasted blocks with minor variations, the same validation/calculation appearing in multiple files.
- Look for dead code (unused functions, unreachable branches, commented-out blocks left in place).
- Look for god objects/files that have accumulated too many unrelated responsibilities.

### Oversized files and functions
- Flag files and functions that are unusually large relative to the rest of the codebase, or that clearly do more than one job. There's no universal threshold — compare against the codebase's own norms, and use judgment: a 600-line file that's one cohesive state machine may be fine; a 200-line function doing five unrelated things is not.

### Inconsistent patterns
- Naming conventions (mixed casing styles, inconsistent terminology for the same concept).
- Error handling strategy (some code throws, some returns null, some returns error objects, inconsistently).
- Differing approaches to the same kind of problem in different parts of the codebase (e.g., three different ways of making an HTTP call).

### Missing tests
- Identify modules/functions with no test coverage at all, especially business-critical logic, code with complex branching, or code that has a history of bugs (check commit history / changelogs if available).
- Note tests that exist but are weak (only test the happy path, or are skipped/disabled).

### Undocumented business logic
- Look for non-obvious conditionals, calculations, or rules with no comment explaining why they exist — especially anything that encodes a business rule (pricing, eligibility, thresholds, special-casing). This is exactly anti-pattern #6 (missing rationale) and it's often the most valuable thing to fix, because business logic is the hardest thing to safely guess at if undocumented.

### Security concerns
- String-built queries (injection risk), hardcoded secrets/credentials, missing input validation at trust boundaries, missing authorization checks, unsafe deserialization, outdated dependencies with known vulnerabilities (check the manifest/lockfile against advisories if you have the means to).
- This category warrants extra care in reporting — see "Reporting security findings" below.

### Unclear project intent
- Is there any documentation of what the system is for, how its pieces fit together, and why major decisions were made? A codebase with zero "why" documentation forces every future contributor (human or agent) to reverse-engineer intent from code alone, which is slow and error-prone.

## Step 3: Score and prioritize

Don't just dump a flat list of findings — that overwhelms the user and treats a typo-level naming inconsistency the same as a SQL injection vulnerability. For each finding, assess:

- **Risk** — what's the cost of *not* fixing this? Consider: likelihood of causing a production incident, security exposure, how much it currently slows down development, how many other findings it's blocking or causing (e.g., a missing architectural boundary that's causing the duplication findings).
- **Effort** — how much work is the fix? Consider: blast radius (how many files/callers are touched), whether tests exist to verify the fix didn't break anything, whether it requires a design decision the team needs to weigh in on.

Rough bucket findings (e.g., Critical / High / Medium / Low, or a simple risk-vs-effort 2x2) and order the remediation plan accordingly. Within similar risk levels, prefer fixes that unblock or simplify other fixes — e.g., introducing a missing abstraction first often shrinks the size of three other findings.

### Reporting security findings

Security issues should be reported with enough specificity to be fixed, but exercise judgment about not turning the report itself into an exploit guide if it's going to be stored or shared broadly. Describe the vulnerability class and location clearly (e.g., "user-supplied `search` param is concatenated directly into a SQL query in `search.py:42` — SQL injection") — this is normal, necessary security review communication, not something to withhold. Don't manufacture or include a working exploit payload beyond what's needed to demonstrate the issue.

## Step 4: Report

Produce a remediation plan as the primary deliverable of the audit. Structure (adapt as needed, but cover all of these):

```markdown
# Maintainability Audit — [codebase/scope name]

## Summary
[2-4 sentences: overall state, the 2-3 most important things to fix, and the general shape of the risk]

## Scope and method
[What was scanned, what was excluded, how the scan was done]

## Findings by priority

### Critical
- **[Finding title]** — [what & where, with file/line evidence] — [why it matters / risk] — [suggested fix, rough effort]

### High
...

### Medium
...

### Low
...

## Suggested sequencing
[A short recommended order of operations — what to fix first and why, noting dependencies between fixes]

## What this audit did not cover
[Be explicit about blind spots — areas excluded by scope, things that would need runtime/production data to assess, etc.]
```

Present this to the user before doing any remediation, even if they asked for both analysis and fixes — they should see the full picture and have a chance to adjust priorities or scope before changes start landing.

## Step 5: Remediate (only with the user's go-ahead)

If the user wants fixes applied (immediately, or after reviewing the report):

- **Confirm scope before starting** — all of it, just Critical/High, just a specific area? Don't assume "fix everything" from a general "yes, go ahead."
- **Work in small, reviewable increments.** One logical fix per change where practical (e.g., "extract the duplicated validation logic" as one self-contained change, not bundled with an unrelated naming cleanup). This keeps each change easy to review and easy to revert if something goes wrong.
- **Tests before refactor, where missing.** If a finding is "this business logic has no test coverage" and the remediation plan includes restructuring it, write characterization tests against the current behavior *first*, so the refactor can be verified not to have changed behavior unless that was the explicit goal.
- **Apply the relevant guidance from `code-generation-mode.md`** (located at [code-generation-mode.md](../slopnought/references/code-generation-mode.md)) to every fix — a remediation that introduces new inconsistency, new duplication, or a new undocumented shortcut has made the codebase worse in a different way, not better.
- **Re-run the test suite after each increment**, not just at the end, so failures are attributable to a specific change.
- **Don't silently change behavior.** If a fix necessarily changes externally-visible behavior (not just internal structure), flag this explicitly — that's a different risk category than a pure refactor and the user needs to know.

Typical remediation actions, matched to common finding types:
- **Duplicated logic** → extract a shared function/module; update call sites; add a test for the shared version.
- **Oversized files/functions** → split along responsibility boundaries; keep the public interface stable unless a behavior change is explicitly intended.
- **Inconsistent patterns** → pick the convention to standardize on (default to whichever is already dominant in the codebase, or ask the user if it's a close call) and apply it across affected files.
- **Missing tests** → add tests for current behavior first (especially for code about to be touched), then expand coverage to edge cases.
- **Undocumented business logic** → add "why" comments/docstrings at the point of the logic, and an ADR if the rule reflects a larger decision (see below).
- **Unclear architecture** → consider introducing or restoring clear module boundaries; this is usually the highest-effort, highest-leverage category and should be sequenced deliberately, often after smaller fixes have reduced noise.

## Step 6: Preserve context — Architecture Decision Records

A remediation that fixes the code but leaves no record of why things are now structured this way just sets up the next drift cycle. For any remediation that reflects a real decision (not just a mechanical cleanup) — choosing a pattern to standardize on, restructuring a module boundary, picking an approach for a previously-undocumented business rule — write an ADR. See [architecture-records.md](../slopnought/references/architecture-records.md) and [adr-template.md](../slopnought/assets/adr-template.md).

At minimum, an audit that includes remediation should leave behind:
- ADRs for any structural decisions made during remediation.
- Updated or new module-level documentation for anything that was restructured.
- A short note (in the final report or a follow-up doc) of what was fixed, what was intentionally deferred and why, and what to watch for if more changes land in the same area soon.

This is what turns a one-time cleanup into a lasting improvement rather than a codebase that drifts right back to its previous state.
