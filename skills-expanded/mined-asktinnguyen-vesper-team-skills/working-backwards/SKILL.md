---
name: working-backwards
description: "Plan PR/FAQ-style product bets from future customer success. Use when a feature needs future-state artifacts before build. Triggers on 'working backwards', 'PR/FAQ', or 'future press release'."
alwaysAllow: ["WebSearch", "WebFetch", "Task", "Read", "Glob", "Grep"]
lastReviewed: 2026-03-02
reviewCadence: quarterly
---

# Working Backwards: PR/FAQ-Inspired Product Bet Planning

Use this skill to define a product bet from future customer success backward, then hand it cleanly to execution.

This is a specialized planning method, not a general research workflow.

## When to Use

Trigger this skill when requests involve:
- Shaping a new product or feature bet with high ambiguity.
- Deciding whether a feature should be built at all.
- Producing future-state strategy artifacts before implementation.
- Aligning product, design, and engineering on a measurable success story.

## When NOT to Use

Do NOT use this skill when:
- The work is a bug fix or already-scoped implementation task.
- The user needs general planning without PR/FAQ-style deliverables.
- Execution has already started and the strategy question is settled.

## Deconfliction

- For general planning, discovery, and broad knowledge work, use `workflow-research`.
- Use `working-backwards` when the deliverable must include a future press release, FAQ, success scorecard, reverse roadmap, and execution handoff.
- Use canonical skill IDs such as `workflow-work`. Slash aliases are optional runner-specific shortcuts, not the source of truth.

## Routing Map

| Stage | Artifact or Skill | When to Use |
|-------|-------------------|-------------|
| Pre-work | `workflow-research` | Required for medium/high stakes unless equivalent research already exists |
| Core procedure | `workflows/working-backwards.md` | Main phase-by-phase workflow |
| Core artifacts | `references/*.md` | Open the relevant template only when entering that phase |
| Calibration | `references/example-*.md` | Optional when you need a quality bar for outputs |
| Review | `workflow-review` | Recommended before commitment; required in Deep mode |
| Execution | `workflow-work` | Turn the approved handoff into concrete tasks |
| Learnings | `workflow-compound` | Store reusable patterns after the decision |

## Quick Start

1. Open `workflows/working-backwards.md` and choose stakes + mode.
2. Complete preflight setup and `references/intake-template.md`.
3. Produce only the artifacts required by the chosen mode, in order. Put supporting detail in appendices, not the main body.
4. Finish with `references/execution-handoff-template.md` or an explicit no-go decision.

## Mode Discipline

| Mode | Default Shape | Output Budget | Main Body Requirement | Keep Out of the Main Body |
|------|---------------|---------------|-----------------------|---------------------------|
| Lite | Fast decision memo | ~600-1,000 words | Bet, concise press release, focused FAQ, lean scorecard, 3-stage roadmap, recommendation | Detailed assumption logs, full UX narratives, reviewer matrices |
| Standard | Decision-ready brief | ~1,200-2,000 words | Bet, concise press release, focused FAQ, lean scorecard, 3-stage roadmap, execution handoff, recommendation | Long tables, duplicated guardrails, exhaustive reviewer lists |
| Deep | Full decision dossier | 2,500+ words when needed | Full workflow artifacts with supporting detail inline | Only omit sections that are truly inapplicable |

Rules:
- Treat `Standard` as the default decision brief, not a full RFC.
- If a section does not change the decision, compress it to 1-3 bullets or move it to an appendix.
- Avoid repeating the same risk, condition, or kill criteria across multiple sections.

## Artifact Map

| Phase | Artifact | File | Exit Gate |
|-------|----------|------|-----------|
| Success inputs | Intake template | `references/intake-template.md` | Checklist passes; evidence + confidence recorded |
| Future narrative | Press release | `references/press-release-template.md` | Checklist passes |
| UX promise | Ultimate UX narrative | `references/ultimate-ux-template.md` | Checklist passes |
| Risk test | FAQ | `references/faq-template.md` | Checklist passes |
| Measurement | Success scorecard | `references/success-scorecard-template.md` | Checklist passes |
| Sequencing | Reverse roadmap | `references/reverse-roadmap-template.md` | Checklist passes |
| Execution bridge | Execution handoff | `references/execution-handoff-template.md` | Checklist passes |
| Final decision | Decision log | `references/decision-log-template.md` | Recommendation is explicit |
| Calibration | Worked examples | `references/example-press-release.md`, `references/example-faq.md`, `references/example-scorecard.md` | Optional |

## Operating Rules

- Default to the shortest artifact that preserves decision quality.
- Start with customer outcomes, not architecture.
- Record evidence sources and confidence levels for major assumptions.
- Complete the active template at the mode-appropriate depth and pass its checklist before moving forward.
- If blocked by missing input, use the recovery protocol in `workflows/working-backwards.md`.
- In `Standard`, only surface supporting tables when they materially change the decision.
- End with either an executable handoff or an explicit stop/conditions decision.

## Anti-Patterns to Avoid

- Writing feature notes instead of customer outcomes.
- Skipping the FAQ because momentum feels high.
- Treating high-stakes bets as if they are reversible.
- Producing strategy artifacts with no owner, evidence, or next action.
- Using this skill when `workflow-research` would be the better fit.

## Next Step

- When the plan is approved, run `workflow-work`.
- After the decision is made, run `workflow-compound` to store reusable learnings.
