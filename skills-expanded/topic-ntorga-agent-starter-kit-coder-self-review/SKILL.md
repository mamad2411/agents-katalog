---
name: coder-self-review
description: Deterministic self-evaluation rubric for Coder — scored every run using the GRASP framework.
usedBy: [coder]
version: 0.2.0
lastUpdated: 2026-09-12
---

## Purpose

Before delivering a handoff, the Coder evaluates its own output against the GRASP rubric. Each letter is scored 0, 1, or 2 with evidence quoted from the rubric and cited from actual work. The total determines whether to deliver, rewrite, or abort.

## Procedure

1. **Gather evidence.** Honest self-review makes verification efficient. Accurate scorecards confirm fast; dishonest ones fail and re-run, wasting time and compute. Before scoring, run verification commands to gather proof. The examples below show common patterns — choose what provides the best evidence for your specific work.

   Examples:
   - Incomplete markers: `rg -n 'TODO|FIXME|HACK|stub|placeholder' <changed-files>` — zero results supports higher scores
   - Test suite: run the project's test command — all passing supports higher scores
   - Lint suppressions: `rg -n 'nolint|eslint-disable|@ts-ignore|# noqa|disable-line' <changed-files>` — zero results or justified suppressions support higher scores
   - Secrets: `rg -n 'password|secret|api_key|token|PRIVATE.KEY' <changed-files>` — zero results in source supports higher scores
   - Attack surface: identify every endpoint/handler accepting external input — verify each has explicit auth and input sanitization
   - Run the project's linter if one exists.

   These are examples, not mandates. Choose commands that provide the strongest proof for your work.

2. **Score each criterion.** Read the GRASP rubric below. For each letter, assign a score of 0, 1, or 2. You must:
   - Quote the specific criterion level (0, 1, or 2) that your work matches.
   - Cite evidence from your actual work — file paths read, commands run, test output, patterns checked. Generic claims like "I followed all guidelines" are not evidence and score 0.

3. **Output the Scorecard.** Fill in the scorecard below. This is not internal reasoning — this is your deliverable checkpoint.

4. **Apply the hard-fail rule.** If any letter scores 0, do not deliver — go to step 5 immediately.

5. **Determine action by total score:**
   - **9 – 10** — **DELIVER** — Implementation meets all criteria. Deliver to user.
   - **7 – 8** — **FIX the scored < 2 criteria.**
     a. Identify which letters scored below 2.
     b. Fix those gaps automatically (do NOT consult the user).
     c. Re-score, then deliver if 9-10.
     d. If still below 9, retry once more.
     e. After 2 failed fix attempts, yield with the current state, rubric scores, and blocking letters.
   - **0 – 6** — **RESTART** — The implementation is fundamentally broken. Rewrite from scratch with corrected understanding, or yield to the user with an explanation of what went wrong.

## Scorecard

Complete this before delivering. Each letter requires the matched criterion quote and specific evidence from your work.

- **G — GUIDELINES** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [files read, commands run, test results]
- **R — REASONING** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [error paths verified, tests run, boundaries checked]
- **A — ARCHITECTURE** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [files checked, dependency directions verified]
- **S — STYLE** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [neighboring files read, linter results]
- **P — PROTECTION** — Score: [0/1/2] — Matched: [quote the 0, 1, or 2 description] — Evidence: [attack surface analysis, rg results]

**Total: X/10** → Action: [DELIVER/FIX/RESTART]

## GRASP Rubric

### G — GUIDELINES

_Did I follow the playbook end-to-end with no scope creep?_

- **0** — Skipped todo creation or management. Did not review context files or FEATURE-MAP before touching code. Tests do not pass or were not run. Handoff format is wrong, missing sections, or absent. Scope expanded beyond the plan/brief.
- **1** — Todo managed and context reviewed, but one or more procedural gaps: did not load relevant skills before implementing, did not update `.context.md`/`FEATURE-MAP.md` when file changes warranted it, or handoff has minor omissions (missing Decisions section when deviations occurred, or Incomplete section not populated for unfinished items).
- **2** — All playbook steps followed: todo checked or created, plan type determined, context files reviewed, sibling files read for style, relevant skills loaded, tests written first and failed before implementation, all tests pass, `.context.md` and `FEATURE-MAP.md` updated where warranted, acceptance criteria verified, handoff delivered in exact format. Yield conditions evaluated honestly.

### R — REASONING

_Will this code survive real-world input and error paths?_

- **0** — Logic does not match the task brief's acceptance criteria. Error paths silently swallowed. Boundary conditions (nil, empty, zero, off-by-one) not handled. Resource leaks in error paths (unclosed connections, file handles, channels). Incomplete work markers present (TODO, FIXME, stub returns, skipped tests without justification).
- **1** — Logic is sound and tests pass, but one or more edge cases are uncertain: retry logic missing backoff, external calls lack timeouts, backward compatibility of API changes not verified, or one error path logs but does not propagate.
- **2** — All error paths handled or explicitly logged. Boundary conditions tested. No resource leaks. All external calls have timeouts. No incomplete markers. Backward compatibility verified or breaking changes documented in handoff Decisions. Tests cover Good, Bad, and Ugly lenses per the plan.

### A — ARCHITECTURE

_Does this code respect the project's architectural boundaries?_

- **0** — Change violates layer boundaries (outer layer depends on inner, or vice versa). New dependency flows against the project's dependency direction. Duplicated logic where extraction exists, or premature abstraction where a simple function would do.
- **1** — Boundaries respected, but one concern is unclear: a new cross-cutting dependency might create a cycle at scale, or an abstraction's necessity is questionable (not obviously wrong, but not obviously needed either).
- **2** — Layer boundaries respected per `.context.md` definitions. All dependencies flow in the correct direction. No duplication — existing utilities reused where applicable. No premature abstractions — code is as simple as the problem requires. Structural coherence check passes.

### S — STYLE

_Does this code look like it belongs in this codebase?_

- **0** — Code does not match the local style of surrounding files (different naming conventions, structure, or patterns). MUST-level rule violations present. Cryptic one-liners or clever patterns that need comments to understand. Unjustified lint/type suppression markers added.
- **1** — Style mostly matches, but one or two naming or formatting inconsistencies exist against the surrounding code. SHOULD-level deviations present without visible justification. One lint suppression added without an adjacent comment explaining why (a comment earned under `rules/code/general.md` § Comments — the tool contract is the external constraint).
- **2** — Read two neighboring files before writing and matched their style exactly. All naming follows project conventions. Code is readable without comments — the structure explains itself. No new lint suppressions, or each has a clear adjacent justification. All rules checked and followed. MUST rules respected, SHOULD deviations justified.

### P — PROTECTION

_Did I map and secure every point where untrusted data enters?_

- **0** — Change introduces an endpoint, handler, or data flow accepting external input. Auth not enforced on mutating operations. Secrets visible in source or config. No sanitization on data reaching SQL, templates, file paths, or command sinks.
- **1** — Attack surface identified and basic sanitization present, but one area is uncertain: auth enforcement relies on middleware ordering convention rather than explicit attachment, error messages may leak internals, or rate limiting missing on auth-adjacent endpoints.
- **2** — No new attack surface (score 2). If surface exists: trace every untrusted data flow to its sink, use parameterized queries, attach auth to each endpoint, keep secrets out of source, keep TLS validation intact, use modern crypto with adequate key lengths.

## Guardrails

- Never deliver if any letter scores 0 — regardless of total. A zero is a hard fail.
- Never skip scoring any letter — all 5 must be evaluated every run.
- A letter without a specific evidence citation scores 0. "I followed all guidelines" is not evidence — cite what you did or did not do.
- Every evidence citation must reference a specific action, file path, command output, or test result. Generic justifications are rejected.
- The scorecard is not internal reasoning — it is a deliverable checkpoint. Output it.
- The rubric is fixed — do not add or remove criteria. If a criterion proves inadequate, file a framework change request.
- When fixing gaps (score 7-8 range), only address the letters that scored below 2. Do not rework letters that already scored 2. Fix automatically — do NOT stop to consult the user.
- After 2 failed fix attempts, yield — do not keep looping. Present the current state, rubric scores, and blocking letters to the user.
- The "restart" action (score 0-6) means: do not deliver the current output. Rewrite the implementation from scratch with corrected understanding, or yield to the user with a clear explanation of the failure mode.
