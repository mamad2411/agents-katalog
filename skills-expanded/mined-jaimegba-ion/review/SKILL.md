---
name: review
description: Deep review of a knowledge area — find gaps, contradictions, staleness, and suggest improvements
---

# Review — Deep Knowledge Review

Conduct a thorough review of a specific knowledge area.

## Usage

The partner specifies an area: `/review strategy`, `/review goals`, `/review characters`, etc. The valid areas depend on the chosen mode (see `ion/state.md`).

If no area is specified, ask which area to review.

## Process

1. Dispatch the **Librarian** sub-agent to scan the area for structural issues, contradictions, and staleness
2. Dispatch the **Strategist** sub-agent if the area involves planning, positioning, or external context (e.g., strategy, intelligence, goals, plot) — for deeper analytical review
3. Read ALL files in the specified `knowledge/` subdirectory
4. Read `ion/state.md` for current context
5. Cross-reference with adjacent knowledge areas that might reveal inconsistencies

## Analysis

For each file in the area, evaluate:
- **Currency**: Is the information still accurate? Are dates outdated?
- **Completeness**: Are there obvious gaps or unanswered questions?
- **Consistency**: Does anything contradict other files in the knowledge base?
- **Actionability**: Is the knowledge driving decisions, or just sitting there?
- **Depth**: Is the level of detail appropriate for the partner's current situation?

## Output

```
# Review: [Area] — [Date]

## Overall Health: [Strong / Adequate / Needs Attention / Critical Gaps]

## What's Solid
[Well-documented, current, useful knowledge]

## Gaps
[What's missing or too thin]

## Stale
[What needs updating — with specific suggestions]

## Contradictions
[What conflicts with other knowledge — cite both sources]

## Recommendations
[Prioritized actions, from most to least impactful]
```

## After Review

- Save the review to `ops/reviews/YYYY-MM-DD-review-[area].md`
- Offer to make recommended updates immediately (following the three-tier model)
- Add deferred fixes to `ops/action-items.md`
