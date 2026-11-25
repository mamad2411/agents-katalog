---
name: writing-acceptance-criteria
description: Given/When/Then acceptance-criteria authoring conventions for user stories and implementation tasks. Use when writing acceptance criteria for a PRD user story, a GitHub issue, or verifying an implementation against stated criteria.
---

# Writing Acceptance Criteria

One convention, two granularities. `planning-artifacts` uses it at story level (a PRD's `As a/I want/So that` user stories); `program-manager` uses it at task level (one GitHub issue = one implementable unit). Same shape either way — this skill is the single place that defines the shape, so neither has to relearn it.

## What Makes a Criterion Testable

- **Given** the starting context/state, **when** a specific action happens, **then** a specific, observable outcome follows.
- One behavior per criterion. A criterion with "and" hiding a second behavior should be split into two.
- State the outcome, not the implementation. "Then the page shows an error message" is testable; "then the code catches the exception" is not — a reviewer can't verify implementation detail from the outside, only observable behavior.
- Avoid vague outcomes. "Works correctly," "handles it properly," and "behaves as expected" aren't verifiable — a reviewer checking this criterion has nothing to check against. State the actual expected value, message, status code, or state transition.
- A story or issue with acceptance criteria that can't fail isn't done — if you can't picture the input that would make a criterion false, it isn't actually testing anything.

## Granularity: Story vs. Task

| Level | Owner | Scope | Example |
|-------|-------|-------|---------|
| Story | `planning-artifacts` (PRD) | Feature/requirement — may span several implementable units | Given a signed-in user with items in their cart, when they click checkout, then they see an order confirmation with the correct total |
| Task | `program-manager` (GitHub issue) | One ~200-400 LOC / 15-45 min implementable unit | Given a `CollectibleView` request for an unrecognized `collectible_type`, when the view resolves, then it returns HTTP 404 |

A single story's acceptance criteria commonly expand into several tasks' worth of narrower criteria during `/program-manager`'s decomposition — that's expected, not duplication. The task-level criteria should still trace back to the story they came from (via the plan/PRD backlink), not restate it verbatim.

## Good vs. Bad Examples

**Bad**: "Given the form, when submitted, then it works." — no context, no specific outcome, unfalsifiable.
**Good**: "Given a signup form with an empty email field, when the user submits, then the field shows 'Email is required' and the form does not submit."

**Bad**: "Given invalid input, when processed, then an exception is caught and logged." — describes implementation (exception handling), not observable behavior.
**Good**: "Given a duration string that doesn't match `\d+h\d+m`, when `parse_duration` is called, then it returns `None` rather than raising."

**Bad**: "Given the API, when called with bad auth, then it handles it correctly." — "correctly" isn't a value.
**Good**: "Given a request with an expired token, when it hits any authenticated endpoint, then the response is HTTP 401 with body `{\"error\": \"token_expired\"}`."

## Verification

When reviewing an implementation against stated criteria (`/swarm-review`, or `/land-the-plane` before closing an issue): check each Given/When/Then individually, not the criteria as a group. A diff can satisfy most criteria in a set and still fail one — general "looks good" review misses that; per-criterion verification doesn't.
