---
name: adversarial-review
description: >-
  Use when the user asks for an adversarial review, opposing-model review,
  hostile review, red-team review, or extra critical review of a plan, branch,
  implementation, or large diff.
schedule: "After cook sessions that produce large diffs (200+ lines), implement plan phases, or complete a planning session"
---

# Adversarial Review

Spawn independent subagents to challenge work from distinct lenses grounded in the bundled review lens definitions. The deliverable is a synthesized verdict; do not make changes.

**Hard constraint:** Use the current environment's native subagent tools for reviewers. Same-model subagents are supported; independence comes from separate review contexts and assigned lenses. Do not launch reviewer model CLIs (`codex exec`, `claude -p`, or equivalents).

## Step 1 — Load Review Lenses

Read `references/reviewer-lenses.md`. These bundled lens definitions govern reviewer judgments and are the only required local reference material for this skill.

## Step 2 — Determine Scope and Intent

Identify what to review from context (recent diffs, referenced plans, user message).

Determine the **intent** — what the author is trying to achieve. This is critical: reviewers challenge whether the work *achieves the intent well*, not whether the intent is correct.
State the intent explicitly before proceeding.

Assess change size:

| Size | Threshold | Reviewers |
|------|-----------|-----------|
| Small | < 50 lines, 1–2 files | 1 (Skeptic) |
| Medium | 50–200 lines, 3–5 files | 2 (Skeptic + Architect) |
| Large | 200+ lines or 5+ files | 3 (Skeptic + Architect + Minimalist) |

## Step 3 — Spawn Independent Reviewers

Use the native delegation tools exposed by the current environment (for example, Codex `spawn_agent` or Claude Code's Agent tool). Use the current environment's default subagent model unless the user specifies a supported model; no opposite-model selection is required.

Create one fresh subagent per selected lens. Give each reviewer the same review scope and intent plus its own lens, without the lead's conclusions or other reviewers' findings. Prefer an isolated context when supported (for example, `fork_turns: "none"` on Codex). Reviewers inspect the work read-only and return findings directly; they must not edit files or delegate further.

Dispatch reviewers in parallel within available concurrency limits. If capacity is limited, run the remaining lenses in subsequent batches without dropping any. Track each subagent ID, assigned lens, completion status, and returned findings. Separate output files are not required.

If native delegation is unavailable, report that the adversarial review is incomplete. Do not substitute a CLI reviewer or present a lead-only review as a completed independent review.

### Reviewer prompt template

Each reviewer gets a single prompt containing:

1. The stated intent (from Step 2)
2. Their assigned lens (full text from references/reviewer-lenses.md)
3. The code or diff to review, or exact accessible workspace paths and base/head references; include enough context to inspect the same scope independently
4. Instructions: "You are an adversarial reviewer. Your job is to find real problems, not validate the work. Be specific — cite files, lines, and concrete failure scenarios.
   Rate each finding: high (blocks ship), medium (should fix), low (worth noting).
   Return findings as a numbered markdown list in your final response, or explicitly state that you found no issues. Do not edit files or spawn further reviewers."

Wait for every selected reviewer to complete before synthesis.

## Step 4 — Verify and Synthesize Verdict

Verify each selected lens has a completed subagent result. A completed response explicitly stating no findings is valid; a missing, empty, failed, or timed-out response is not a clean review. Retry a failed reviewer when possible and record any unresolved failure by lens.

Read every completed result and deduplicate overlapping findings. Include reviewer coverage (lens, subagent ID, and status) in the report. If any selected lens remains unresolved, label the verdict **INCOMPLETE**, present available findings as partial, and do not issue PASS.

Produce a single verdict:

```text
## Intent
<what the author is trying to achieve>

## Verdict: PASS | CONTESTED | REJECT | INCOMPLETE
<one-line summary>

## Findings
<numbered list, ordered by severity (high → medium → low)>

For each finding:

- **[severity]** Description with file:line references
- Lens: which reviewer raised it
- Lens principle: which bundled review lens principle it maps to
- Recommendation: concrete action, not vague advice

## What Went Well
<1–3 things the reviewers found no issue with — acknowledge good work>
```

**Verdict logic:**

- **INCOMPLETE** — a selected reviewer did not return a usable result; this takes precedence over the other verdicts
- **PASS** — all selected reviewers completed and there are no high-severity findings
- **CONTESTED** — high-severity findings but reviewers disagree on them
- **REJECT** — high-severity findings with reviewer consensus

## Step 5 — Render Judgment

After synthesizing the reviewers, apply your own judgment. Using the stated intent and bundled review lenses as your frame, state which findings you would accept and which you would reject and why. Reviewers are adversarial by design; not every finding warrants action. Call out false positives, overreach, and findings that mistake style for substance.

Append to the verdict:

```text
## Lead Judgment
<for each finding: accept or reject with a one-line rationale>
```
