---
name: groom-backlog
description: Review backlog items into ready — clarify stories, add acceptance criteria + estimate, split oversized items, flag blockers; not ranking (prioritize) or epic story-mapping (decompose-epic).
---

# groom-backlog

> Grooming makes items *ready*, not *ordered*. Walk each item until a team could pick it up without a meeting.

## When to use

- A backlog has vague, oversized, or under-specified items that aren't ready to pull.
- Prepping items before sprint/iteration planning ("backlog refinement").
- A workflow invokes `polymath-product:groom-backlog`.

This refines *individual items* against a Definition of Ready. It does not rank them (`polymath-planning:prioritize`), slice an epic into a story map (`polymath-product:decompose-epic`), or estimate a whole initiative (`polymath-planning:estimate`).

## Definition of Ready (the bar each item must clear)

- Clear, outcome-phrased title and a one-line "why".
- Acceptance criteria (Given/When/Then or a checklist) — testable.
- Small enough to finish in one iteration; if not, split.
- Dependencies and blockers named.
- A rough estimate or size, with confidence.

## Procedure

1. For each item, assess it against the DoR above.
2. **Clarify** the story and outcome; rewrite vague titles.
3. **Add acceptance criteria** if missing (lean on `polymath-product:acceptance-criteria` for the form).
4. **Split** anything too big to finish in one iteration into independently shippable items.
5. **Flag blockers/dependencies** and the question that must be answered before it's pullable.
6. **Size** each with a rough estimate + confidence; mark guesses.
7. Output the groomed items, each marked ready / not-ready with the reason.

## Output

```text
Backlog grooming — N items

READY
  [ ] <item>   AC: <testable criteria> · size: S · deps: none
NOT READY
  [!] <item>   gap: <DoR item missing, e.g. no acceptance criteria>
               question to unblock: <the one answer needed>
               split proposal: <child items if oversized>
```

## Quality bar

- Every item ends marked ready or not-ready, with the specific gap if not.
- No item left larger than one iteration without a split proposal.
- Acceptance criteria are testable; "works correctly" is not acceptance criteria.
- Does not reorder or prioritize the backlog — readiness only.
