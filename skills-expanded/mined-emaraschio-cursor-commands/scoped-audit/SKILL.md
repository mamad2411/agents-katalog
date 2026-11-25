---
name: scoped-audit
description: >-
  Scoped, plan-first workflow for large "check-N-things" tasks (audits,
  inventories, catalogs, large migrations, cross-checks). Decomposes the
  surface, fans out capped parallel subagents, verifies findings before
  reporting, and gates any change behind explicit approval. Use for "audit
  X for Y", "find all", "catalog every", "inventory", "migrate across", or
  any repeatable workflow that has quietly become "check 400 things".
user-invocable: false
---
# Scoped audit

## Role

You orchestrate a large, repetitive task as a scoped workflow. The goal is a trustworthy catalog of verified findings (and, only when asked and approved, a set of changes derived from them). Big surfaces are where agents hallucinate and burn tokens; this contract exists to prevent both.

## When to use

Use this skill when the task is "do one thing" repeated across a large surface: audit every flag, catalog every call site, inventory every config, cross-check every doc, or migrate a pattern repo-wide. For a single requirement or a single-file change, use `requirement-to-implementation` instead.

## Workflow

Run phases in order. Do not make changes until Phase 3 (approval) passes. Do not report a finding until Phase 6 (verification) confirms it.

### Phase 0: Scope

1. Restate the target surface and the question being asked in one sentence.
2. Bound the surface: which directories, repos, file globs, or datasets are in and out of scope.
3. Define what a single "finding" is and the exact pass/fail condition for it.
4. If the surface or success condition is ambiguous, ask one focused question before proceeding (use `AskQuestion` when available).

### Phase 1: Plan (show before running)

Present the plan to the user and wait. The plan must show, explicitly:

1. **Stages**: the ordered steps of the workflow.
2. **Subagent responsibilities**: what each parallel subagent will inspect, and how the surface is partitioned across them.
3. **Verification method**: how each finding will be confirmed against the source before it is reported.
4. **Files and commands to touch**: read paths for the audit; for any proposed change, the write paths and commands.
5. **Smallest safe first pass**: the scoped sample you will run before fanning out across the whole surface.

### Phase 2: Scoped sample (first pass)

1. Run the workflow against the **scoped sample** only, never the full surface first.
2. Confirm the finding shape, the partition strategy, and the verification method actually work.
3. Report sample results and the projected cost/scale of the full run. Surface the token-burn risk: parallel fan-out across a large surface compounds quickly.

### Phase 3: Approval gate (hard stop)

1. Do not expand beyond the scoped sample, and do not make any change, until the user gives **approval** for the full plan.
2. If the scoped sample revealed the plan was wrong, return to Phase 1 and re-plan rather than pushing forward.

### Phase 4: Parallel fan-out (capped)

1. Partition the approved surface into independent slices.
2. Launch parallel subagents (Cursor `explore` for read-only discovery, `generalPurpose` for analysis), one slice each. **Cap concurrency at ≤ 6** to bound token burn and keep results reviewable. Batch additional slices in waves.
3. Each subagent returns structured findings for its slice only; it does not make changes.

### Phase 5: Aggregate

1. Merge subagent results into a single catalog, de-duplicated by a stable key.
2. Normalize the finding records so every row has the same fields.

### Phase 6: Verify (before reporting)

1. **Verify findings before reporting** them: re-check each candidate finding against the actual source (re-read the file, re-run the query) rather than trusting a subagent's summary.
2. Drop or flag any finding that cannot be confirmed. Never report an unverified finding as fact.
3. Note coverage gaps: slices that failed, timed out, or were skipped.

### Phase 7: Report

1. Present the verified catalog (table or list) plus a short summary: total found, verified, unverified, and coverage gaps.
2. If the user asked for changes (e.g. a migration), present them as a **separate proposed change set** with the affected files and commands, and return to an approval gate before editing anything.

## Output template

```markdown
# Scoped audit: <surface> (<question>)

## Scope
- In: <paths/globs/datasets>  | Out: <excluded>
- Finding = <definition>; condition = <pass/fail rule>

## Coverage
| Slices | Completed | Failed/skipped |

## Findings (verified)
| # | Location | Value / detail | Verified | Notes |

## Unverified / needs review
| # | Location | Why unconfirmed |

## Proposed changes (only if requested, requires approval)
| File | Change | Command |
```

## Safety

- Make no changes (no edits, migrations, or destructive commands) until the plan is approved.
- Never log or echo secrets, tokens, credentials, PII, or PHI encountered while scanning the surface; redact them in findings.
- Respect the concurrency cap; do not spawn unbounded subagents.
- Prefer reporting a coverage gap over fabricating a complete-looking result.

## Distinction from other commands

- **`requirement-to-implementation`**: one requirement → build it. This skill is many repeated checks across a large surface, audit-first.
- **`security-audit`**, **`seo-audit`**, **`accessibility-audit`**: single-domain audits with domain rubrics. This skill is domain-agnostic orchestration. Use it to drive a large cataloging pass, and lean on the domain skill for what counts as a finding when relevant.
- This skill **catalogs and proposes**; it does not edit until a separate approval gate, even when the surface is read with write tools available.

## Guardrails

- Run a scoped sample first; never sweep the full surface before the approach is validated.
- Verify findings before reporting them; never report an unverified finding as fact.
- Make no changes until the plan has explicit approval; respect the subagent concurrency cap and redact secrets in findings.
