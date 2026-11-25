---
name: exploratory-charter
description: >-
  Formats a feature and risk hypothesis into an exploratory testing charter and
  findings template. Use when the user says "exploratory charter", "charter for",
  or "explore X for risks", before ad-hoc exploratory sessions, or when turning a
  feature + risk into a structured session plan. Format only — does not prescribe
  heuristics or exploration strategy.
disable-model-invocation: true
---

# Exploratory Charter

Format-only scaffold for exploratory testing. The thinking is human; this skill keeps the output structure consistent. Do not prescribe heuristics, risk analysis, or exploration strategy — fill templates from the user's feature and risk inputs.

## When to use

- User provides (or you elicit) a feature and a risk
- Triggers: "exploratory charter", "charter for", "explore X for risks"
- Before ad-hoc exploratory testing sessions
- When turning a feature + risk hypothesis into a structured session plan

## When NOT to use

- Coverage discovery without a risk hypothesis → use explore-and-generate
- Jira ticket with acceptance criteria → use jira-ticket-to-gherkin
- Writing or running Playwright specs → delegate to test-writer

## Steps

1. **Collect inputs** — Feature (what to explore) and risk (why / what could go wrong). Ask if either is missing.
2. **Derive focus areas from the risk** — Human judgment; list 3–6 probe areas as bullets under Charter. Do not invent a testing methodology.
3. **Output both templates** — Charter first, then an empty Findings template ready for session notes.
4. **Keep it brief** — One page per template. No essays.

## Charter template

Fill from feature + risk. Copy and populate:

```markdown
# Exploratory Charter

## Feature under test
<what to explore>

## Risk / concern
<why this session — what could go wrong>

## Mission
<one sentence — what you aim to learn or disprove>

## Scope
**In:** <areas, flows, states>
**Out:** <explicit exclusions>

## Time box
<duration, e.g. 45 min>

## Charter — areas to probe
- <test idea derived from risk>
- <test idea derived from risk>
- <…>

## Oracles / signals
<what would indicate a problem — error messages, bad data persisted, wrong UI state, etc.>

## Session setup
- **Environment:** <URL, build, account>
- **Data:** <fixtures, starting records>
- **Starting point:** <navigation / preconditions>

## Session notes (during exploration)
| Time | Action | Observation |
|------|--------|-------------|
|      |        |             |
```

## Findings template

Output alongside the charter — empty, ready to fill after the session:

```markdown
# Exploratory Findings

## Session metadata
| Field | Value |
|-------|-------|
| Date | |
| Feature | |
| Risk | |
| Duration | |
| Tester | |

## Observations
<what was seen — facts, not verdicts>

## Questions
<open items, ambiguities, needs product/dev input>

## Issues found
| # | Severity | Summary | Steps | Expected | Actual |
|---|----------|---------|-------|----------|--------|
|   |          |         |       |          |        |

## Coverage notes
**Touched:** <flows, inputs, states explored>
**Not touched:** <deferred areas, time-box cuts>

## Follow-ups
- **Automation candidates:** <flows worth scripting>
- **Bugs to file:** <ticket drafts or links>
- **Deeper dives:** <future charters or spikes>
```

## Example

Inputs: Feature = Program name validation · Risk = special characters bypass client-side checks

### Charter (filled)

```markdown
# Exploratory Charter

## Feature under test
Program name validation on create-program flow

## Risk / concern
Special characters may bypass client-side checks and persist invalid names

## Mission
Determine whether disallowed characters are blocked consistently in UI and API.

## Scope
**In:** Create-program modal, name field, submit, list refresh
**Out:** Edit-program rename, bulk import, i18n locales

## Time box
45 min

## Charter — areas to probe
- Paste strings with `<`, `>`, `&`, quotes, slashes, emoji
- Leading/trailing whitespace and null bytes
- Max-length boundary (255 vs 256 chars)
- Submit via Enter vs button; double-submit
- Inspect network payload vs displayed value after save

## Oracles / signals
- Inline validation error before submit
- Submit disabled or request rejected (4xx)
- Saved name matches input or is safely normalized — never corrupted/truncated silently

## Session setup
- **Environment:** Didaxis Studio staging, authenticated author
- **Data:** fresh session, no conflicting program names
- **Starting point:** Programs list → Create program

## Session notes (during exploration)
| Time | Action | Observation |
|------|--------|-------------|
|      |        |             |
```

### Findings (filled briefly)

```markdown
# Exploratory Findings

## Session metadata
| Field | Value |
|-------|-------|
| Date | 2026-08-14 |
| Feature | Program name validation |
| Risk | Special chars bypass client checks |
| Duration | 40 min |
| Tester | |

## Observations
- `<script>` blocked inline; `&` accepted and displayed encoded in list
- Double-submit created duplicate programs with same name

## Questions
- Is `&` intentionally allowed or a normalization gap?

## Issues found
| # | Severity | Summary | Steps | Expected | Actual |
|---|----------|---------|-------|----------|--------|
| 1 | Medium | Double-submit duplicates | Rapid double-click Create | Single program | Two rows same name |

## Coverage notes
**Touched:** create modal, 12 char variants, network inspect
**Not touched:** edit rename, API direct POST

## Follow-ups
- **Automation candidates:** double-submit guard (DS-3 adjacent)
- **Bugs to file:** duplicate on double-submit if not known
- **Deeper dives:** edit-flow rename with same char set
```

## Guardrails

- Format only — no heuristics lecture, no SFDPOT/RCRC lists unless the user asks
- Do not run the session or write Playwright specs in this skill
- Do not weaken or replace formal test plans when a ticket exists
