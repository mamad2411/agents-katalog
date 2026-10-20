---
name: bench-competitors
description: Research competitors and implement-to-production until the project beats them on every dimension
argument-hint: "[scope|report]"
related:
  - create-report-in-dot-devin
  - design-html-prototype
  - design-web-prototype
  - compare-competitors
  - deep-research
  - deep-review-codebase
  - deep-thinking
  - plan
  - create-plan-in-dot-devin
  - implement-to-production
  - report
  - idea
  - ask-me
  - suggest-next-action
  - ship
  - run-bench
---

## Goal

Research competitors with `/deep-research`, plan with `/create-plan-in-dot-devin`, then `/implement-to-production` until the project beats competitors in every dimension.

## Scope

Covers every dimension of the product: features, performance, UX/UI, architecture, DX, security, scalability, business — not just one.

- The features dimension is handled inline in this skill (merged from `bench-features`) — use `/deep-research` to collect competitor features, build a comparison matrix, and find gaps
- This skill implements for real through to production, not just planning — if you only want feature ideas → use `/idea-features`
- Unlike `/compare-competitors`, which only returns the comparison (matrix + gap list + ideas) without implementing, this skill compares and then implements
- UX/UI dimension — to match or beat a competitor visually: mock it fast with `/design-html-prototype`, build the real interactive prototype with `/design-web-prototype`, and design a CLI/TUI parity surface with `/design-cli-prototype` / `/design-tui-prototype` in chat — all before `/implement-to-production`

See also: /deep-review-codebase, /create-plan-in-dot-devin, /implement-to-production, /compare-competitors

## Execute

### Workflows

| Argument | Workflow |
|----------|----------|
| `report`, `report-comparison` | `## Merged Details → report-comparison` — matrix + gap list + re-bench delta → `.devin/temp/report/` |

1. If the argument is `report` → read `## Merged Details → report-comparison` and follow its flow — reuse the data already gathered, no new research
2. If not specified → run Steps 1-8 as usual, with Step 7 reading and executing the `report-comparison` workflow

### 1. Research Competitors

> Goal: Research relevant competitors with deep-research

1. Take `<scope>` from the argument or conversation context
2. Run `/deep-research` to identify direct and indirect competitors
3. Pick 3-5 competitors that are close to or better than the project
4. Analyze strengths, weaknesses, unique selling points, tech stack, UX patterns
5. If the scope is unclear → use `/ask-me` first; if the data can't be found → stop and report

### 2. Benchmark Features

> Goal: Compare the features dimension and find gaps

1. Run `/compare-competitors` with subject = project, alternatives = the competitors from Step 1, criteria = features (including the feature matrix and the pricing tiers tied to features) — the skill runs `/deep-research` on each competitor from official docs, changelogs, reviews, and user feedback, then returns a comparison matrix + gap list
2. Group the features in the matrix by category, e.g. core, advanced, integrations, automation
3. Save the result as `comparison-features.md` in `docs/project/`
4. Review the gap list from `/compare-competitors` — each gap must state the feature, the competitor that has it, impact, and effort
5. Identify the project's unique features that competitors lack, to preserve them
6. Build a prioritized feature list: Critical, High, Medium, Nice-to-have
7. If `/compare-competitors` can't find the data → stop and report

### 3. Benchmark Other Dimensions

> Goal: Compare the remaining dimensions beyond features

1. Run `/deep-review-codebase` to measure the project's current state for performance
2. Run `/deep-review-codebase` for UX/UI
3. Run `/compare-competitors` on each dimension that can be compared against competitors (performance benchmarks, UX patterns, architecture, DX, security, scalability, business)
4. Record the results in `docs/project.md`

### 4. Deep Plan Improvements

> Goal: Plan in depth with create-plan-in-dot-devin to improve beyond competitors

1. Run `/deep-thinking` to review priorities and impact
2. Run `/create-plan-in-dot-devin` in `chat-only` mode to build a detailed roadmap covering every dimension in chat — specify per-dimension actions, dependencies, sequencing, and success metrics comparable to competitors (chat-only — no plan file created)
3. Set priorities: Critical, High, Medium, Nice-to-have
4. If the scope is unclear → use `/ask-me` before planning

### 5. Implement To Production

> Goal: implement-to-production per the plan until production-ready with no gaps left

1. Run `/implement-to-production` following the in-chat roadmap from Step 4 — implement every gap as real production code end-to-end, leaving no TODO/MOCK/placeholder
2. Run `/run-check` after each implementation batch to check lint, typecheck, and scan
3. Run `/run-test all` to verify the features work and nothing existing breaks
4. Track progress consistently — close gaps one at a time in priority order Critical → Nice-to-have

### 6. Verify And Re-benchmark

> Goal: Confirm the project genuinely beats competitors in every dimension, not just that implementation finished

1. Run `/deep-review-codebase` for performance improvements
2. Run `/deep-review-codebase` for UX/UI improvements
3. Re-benchmark against competitors across all dimensions — update the status in the comparison table
4. If any dimension still isn't better than competitors → loop back to Step 4 for `/create-plan-in-dot-devin` + `/implement-to-production` on the remaining gaps only, until every dimension is better
5. Stop the loop when the project beats all competitors, or when the remaining gaps need data/decisions from the user → use `/ask-me`

### 7. Report Results

> Goal: Record the benchmark results and implementation outcomes as a report in .devin

1. Follow `## Merged Details → report-comparison` — matrix + gap list + re-bench delta → `.devin/temp/report/<workspace>/`
2. Run `/update-docs` to update `docs/project.md`
3. Report `REPORT_PATH` to the user

### 8. Ship

> Goal: Deliver once the project is better than competitors in every dimension

1. Run `/ship` to ship all improvements
2. After `/ship` finishes, delete `PLAN_PATH`
3. Run `/suggest-next-action`, recommending `/idea-features` if you want to extend the ideas further

## Rules

### 1. Focus On Actionable Insights

- Focus on metrics that are measurable and actionable
- Don't research deeper than necessary
- Keep reports concise, no more than 1 A4 page per competitor

### 2. Document Structure

- Main file `comparison.md` in `docs/project/`
- Child files `comparison-*.md` from sub-workflows are allowed, e.g. `comparison-features.md`
- Benchmark results must be saved as a report via `/create-report-in-dot-devin` in `.devin/temp/report/<workspace>/`
- 2-3 main sections are enough
- No detailed timeline needed

### 3. Multi-Dimension Focus

- Not just features — cover every dimension
- Measure with objective metrics
- Compare against relevant competitors

### 4. Features Evidence

- Always use `/deep-research` whenever competitor data is needed; never guess from memory
- Cite a source for each feature claim
- Every feature gap must have evidence from competitor docs or reviews
- Don't conclude the project is inferior without evidence
- Separate `fact` (the competitor really has it) from `assumption` (presumed to exist)
- Every gap must map to an implementable feature — don't report a broad gap without breaking it into smaller features
- Results must be ready to hand off to `/create-plan-in-dot-devin` (chat-only) or `/idea-features`

### 5. Implementation Discipline

- Always make the deep plan in chat via `/create-plan-in-dot-devin` `chat-only` mode before implementing — never create a plan file in `.devin/`
- Implement only with `/implement-to-production` — every gap must become real production code, no TODO/MOCK left
- Follow the plan until the project beats competitors — don't stop at research or plan
- Track progress consistently
- Re-benchmark after each improvement

### 6. Stop When Better

- Stop as soon as the project is better than competitors in every dimension
- No over-engineering or adding unnecessary features
- Move on to other work once the goal is achieved
- Use /run-bench if needed

## Merged Details

### report-comparison

##### Goal

Build the report for `/bench-competitors` — comparison matrix + gap list + post-implementation re-benchmark delta — a persistent artifact in `.devin/temp/report/`

##### Scope

- Use when `/bench-competitors` dispatches to `report` or when a report for one phase is needed
- Output: always a `/create-report-in-dot-devin` artifact (this report is the workflow's deliverable)

##### Execute

###### 1. Collect Evidence

> Goal: Gather data from the research/compare/bench phases

1. Collect the feature matrix + gap list from the `/compare-competitors` output
2. Collect benchmark numbers per dimension (perf, UX/UI, architecture, DX, security, scalability, business)
3. If post-implement → collect the re-bench delta (before vs after)
4. Every competitor claim must have a source citation

###### 2. Build Report Structure

> Goal: a report complete per the parent's contract

1. Matrix table: `No.`, `Dimension/Feature`, `Ours`, `Competitor A`, ..., `Gap`
2. Gap list ordered by priority with evidence
3. Re-bench delta table if this is the post-implement phase
4. Limit to ≤ 1 A4 page per competitor — merge into one summary if there are many

###### 3. Emit Artifact

> Goal: a permanent report that can be traced back

1. Run `/create-report-in-dot-devin` — name it following the `bench-competitors-<date>` convention
2. Clearly separate facts from assumptions in the report
3. End with a verdict: better/worse per dimension

##### Rules

- Every claim has a citation — no citation = tag it as an assumption
- Don't write long reports — density over prose
- The re-bench delta must use the same methodology as the baseline

##### Expected Outcome

- `.devin/temp/report/` artifact with matrix + gap list + verdict per dimension

## Expected Outcome

- Feature comparison matrix against 3-5 competitors with a prioritized gap list (impact + effort) and the unique features to preserve
- Deep plan roadmap covering every dimension shown in chat before implementing (chat-only — no plan file)
- Every gap turned into real production code via `/implement-to-production`, no TODO/MOCK left
- Report file in `.devin/temp/report/<workspace>/` from `/create-report-in-dot-devin`
- A `docs/project.md` file containing comparison tables for every dimension
- The project better than competitors in every dimension — verified by re-benchmark
- Benchmarking takes no more than 30 minutes
