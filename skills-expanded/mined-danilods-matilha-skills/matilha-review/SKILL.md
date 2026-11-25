---
name: matilha-review
description: Use when user wants a quality review of a completed wave — will dispatch 6 parallel review agents (code-quality, UX, security, architecture, performance, docs) once Wave 3c ships.
category: matilha
version: "1.0.0"
optional_companions: ["superpowers:dispatching-parallel-agents"]
---

## When this fires

After `/matilha-gather` completes a wave, user says "review this wave" or "is this good quality". Wave 3c ship will automate the 6-agent review; until then this skill runs a simplified sequential review.

## Preconditions

- `docs/matilha/waves/wave-NN-status.md` shows `status: completed`.
- `review_report: null` (or user wants a re-review).

## Execution Workflow

1. Read wave-status via Read tool.
2. Confirm all SPs merged and regression passed.
3. If `superpowers:dispatching-parallel-agents` available, invoke via Skill tool with 6 review roles (code-quality, UX, security, architecture, performance, docs). Otherwise, run each review role sequentially via Task tool.
4. Synthesize outputs into `docs/matilha/reviews/<date>-wave-NN-review.md`.
5. Update wave-status: `review_report: <path>`.

## Rules: Do

- Preserve reviewer independence (don't synthesize until all reviews return).
- Cite specific commits + files in findings.
- Surface blockers distinctly from nice-to-haves.

## Rules: Don't

- Fix issues yourself (reviewer surfaces, humans fix).
- Synthesize before all reviews complete.
- Mark wave as reviewed without the review_report link.

## Expected Behavior

User gets a structured markdown with one section per reviewer + a synthesis. Wave 3c will automate; until then this skill is the manual fallback.

## Quality Gates

- `review_report` exists.
- `wave-NN-status.md:review_report` updated.

## Companion Integration

- If **superpowers:dispatching-parallel-agents** is available: dispatch 6 review agents in parallel via Skill tool.
- Otherwise: run each review role sequentially (slower; same output quality).

## Output Artifacts

- `docs/matilha/reviews/<date>-wave-NN-review.md`.
- Updated `wave-NN-status.md`.

## Example Constraint Language

- Use "must" for: all 6 review roles produce output.
- Use "should" for: dispatch parallel via superpowers when available.
- Use "may" for: skip review for trivial waves (user decision).

## Troubleshooting

- **"wave not completed"**: Finish `/matilha-gather` first.
- **"review_report already exists"**: Inspect existing; don't overwrite.

## CLI shortcut (optional)

> Wave 3c will ship `matilha review <slug>`. Until then, no CLI equivalent exists.
