---
name: review
description: "Parallel three-perspective code review via sub-agent orchestration. Dispatches Test Review, Code Review, and Impact Review sub-agents in parallel — each independently re-reads all shared context. Merges reports, highlights contradictions for human adjudication. Use after task completion, before merge, or before release. Trigger words: review, check, 把关, 发布前, 完成开发, 验收, code review."
---

# Review: Parallel Three-Perspective Review

🥷 Complete all finish work before merge or release.

Dispatches three independent review sub-agents in parallel — Test Review, Code Review, Impact Review — each re-reading all shared context from scratch. Merges their reports into a single comprehensive review. Issue sync and release follow-through require current-turn explicit authorization.

## Outcome Contract

- **Outcome**: Merged three-perspective review report — test quality, implementation quality, and impact analysis — with contradictions highlighted for human adjudication
- **Done when**: All three sub-agent reports produced, merged report presented, local file updates completed or listed as follow-up, remote actions completed only if explicitly authorized
- **Evidence**: Test/lint/typecheck/build output, code diff analysis, updated files
- **Output**: Structured merged report with per-perspective sections, contradiction block (if any), and unified recommendation

## Prerequisites

- Code is complete (by `tdd`, `implement`, or manual)
- Reviewable changes exist — uncommitted (staged or unstaged) **or** already committed on the current branch (e.g., per-seam commits from `/implement`)

## Runtime Note

"Sub-agent" is a logical concept — see [Sub-Agent Runtime Semantics](../rules/sub-agent-runtime.md). Independence comes from re-reading shared context from disk, not from execution timing.

## Process Summary

**Step 1 — Collect context**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read the diff — staged + unstaged if the working tree is dirty, otherwise the branch range since the default branch (or the PR diff) when the work is already committed (see [REFERENCE.md Chapter 1](REFERENCE.md)). Read README, package.json, Makefile, CI configs. If the diff contains an Issue reference, read the PRD path from the Issue body's `Meta → PRD` field and load it. Gather available shared context paths (PRD, Story, Issues, CONTEXT.md, ADRs). **PRD quality check:** if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete — review acceptance criteria coverage with extra care.

**Step 2 — Dispatch three parallel review sub-agents**: Dispatch all three (see [Runtime Note](#runtime-note) and [Three Sub-Agents](#three-sub-agents) below).

**Step 3 — Merge reports**: Concatenate the three reports. Do not auto-resolve contradictions — flag them explicitly for human adjudication. See [Report Merge Rules](#report-merge-rules).

**Step 4 — Present merged report**: Show the full merged report to the user with per-perspective sections, verification status, contradiction block, and unified recommendation.

**Step 5 — Authorization gate**: Present the report and ask **one** question — approve the recommendation, or request changes. Merge/release and other actions are not part of the approval: they are requested (and authorized) separately per Chapter 6. Local doc updates are allowed when necessary; remote actions require current-turn explicit authorization.

**Step 6 — Execute authorized actions**: Perform only actions the user explicitly requested in the current turn — local file updates, issue sync, release follow-through. If the review passes and the Issue belongs to a PRD's `Sliced into` list, update the Issue's status there to `— Done`. If all entries in `Sliced into` are `— Done`, update the PRD Status to `Done`. See [Authorization Boundaries](#authorization-boundaries).

See [REFERENCE.md](REFERENCE.md) for detailed sub-agent instructions, checklists, and report templates.

## Three Sub-Agents

Each sub-agent is an independent review perspective. They run in parallel, each re-reading all shared context from scratch (PRD, Story, Issues, CONTEXT.md, ADRs, diff). No sub-agent sees another sub-agent's output until the merge step.

| Sub-Agent | Focus Area |
|---|---|
| **Test Review** | Test quality, boundary coverage, test design reasonableness, naming, isolation, mock usage |
| **Code Review** | Implementation quality, security, performance, code conventions, error handling, readability, engineering principles local to the diff ([rules/engineering-principles.md](../rules/engineering-principles.md)) |
| **Impact Review** | Change scope, regression risk, compatibility, architecture health (local to this change), principles with cross-module consequence (DIP, OCP, new coupling), tech debt introduced, release strategy (feature flags, canary, rollback plan). Suggests `/improve-architecture` for global architecture concerns |

### Sub-Agent Independence

Sub-agents are independent (anti-patterns [#34, #35](../rules/anti-patterns.md)); the shared re-read checklist is in [REFERENCE.md Sub-Agent Common](REFERENCE.md), plus each chapter's role-specific addition.

## Report Merge Rules

Concatenate the three sub-agent reports as distinct sections. If two or more reach conflicting conclusions on the same item, extract them into a `Contradictions` block — present both sides, **never auto-resolve** (the human adjudicates). Derive a single recommendation; if sub-agents disagree, the recommendation is "Request Changes" and the disagreement goes in Contradictions. See [REFERENCE.md Chapter 5](REFERENCE.md) for the merge steps, contradiction format, and merged-report template.

## Authorization Boundaries

Default review is local inspection only. Local doc/PRD/CONTEXT/ADR updates are allowed **only when the review verified the underlying change**. Issue close/status/label changes and all release actions require explicit user authorization **in the current turn**. See [REFERENCE.md Chapter 6](REFERENCE.md) for the full boundary table.

## Hard Rules

- **Security first**: Block immediately on any security issue. Code Review Sub-Agent runs the full Security Checklist in REFERENCE.md before approving any diff. Security-sensitive changes must include rollback path, audit trail, and regression test (anti-pattern #18).
- **Test coverage**: New code must have tests. Test Review Sub-Agent verifies this independently.
- **Evidence first**: Every conclusion needs evidence. Run actual commands — never say "should work" (anti-pattern #6).
- **Verify the artifact, not just the source**: "tests pass, code looks right" is not done. Report each layer's status separately — source tests, build/package, CI, runtime — a missing layer is an explicit gap, not passing evidence (anti-pattern #17).

## Integration Review

When all vertical slices of a PRD are complete, perform extra checks beyond single-slice review (cross-slice data flow, shared state consistency, full PRD acceptance criteria coverage, integration test coverage, dependency order). See [REFERENCE.md](REFERENCE.md) for details. State explicitly: "Integration Review — checking <N> slices for PRD <name>."

## Gotchas

| What happened | Rule |
|---|---|
| Sub-agent reused context from another sub-agent | Independence rule: each sub-agent re-reads all shared context from scratch (anti-pattern #35) |
| Contradictions silently resolved in merge | Report Merge Rules: extract to Contradictions block, present both sides |
| Said "should work" without verification | Hard Rules: run verification commands |
| Assumed project commands | Step 1: extract from config |
| Didn't check security issues | Hard Rules: Security first — Code Review Sub-Agent runs Security Checklist |
| Impact Review drifts into global architecture review | Impact Review scope: local impact only. Suggest `/improve-architecture` for global concerns |
| Sub-agents run sequentially when parallel is possible | Runtime Note: dispatch in parallel if runtime supports it; sequential is acceptable fallback |
| PRD not updated after review | Step 6: update local files when authorized |
| Issues closed without authorization | Authorization Boundaries: close/status/label requires current-turn authorization |
| Sub-agent skipped re-reading shared context | Independence rule: never cache file reads from previous skill or sub-agent (anti-pattern #34, #35) |
| Principle violation reported as a blocker, or with no stated consequence | Ch3 Engineering Principles gates: name the concrete consequence or drop the finding; severity defaults to `minor`, and a principle tag never creates a blocker |

## Output

```
Review complete.

── Test Review ──      <Test Review Sub-Agent report>
── Code Review ──      <Code Review Sub-Agent report>
── Impact Review ──    <Impact Review Sub-Agent report>
── Contradictions ──   <both sides, or "No contradictions">
── Verification ──     Tests / Lint / Typecheck / Build: <pass/fail>
── Findings ──         new terms, new decisions, updated files, synced issues
Recommendation: Approve / Request Changes / Comments

Next: User decides — merge/release, or fix issues and re-review.
```

The full merged-report template (with all fields and next-step branches) is in [REFERENCE.md Chapter 5](REFERENCE.md).
