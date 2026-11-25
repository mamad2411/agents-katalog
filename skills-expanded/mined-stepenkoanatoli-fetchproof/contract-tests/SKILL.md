---
name: contract-tests
description: Turns the verified claims in a Fetchproof brief - response shapes, field names, limits, error codes, quoted behaviour - into tests and fixtures, so the code is checked against the research rather than against the builder's memory of it. Use while building from research/BRIEF.md, when writing tests for an integration with an external API or platform, or when the user asks to test against the docs or the brief.
---

# Contract tests

The brief says what the outside world does. A test that encodes it makes the brief
executable: when the code drifts from the research, a test goes red.

## Steps

1. From the brief's **What we verified** table, pick each claim the code depends on.
2. Write one test per claim, named for it and citing its row:
   `test('E-07: a 429 carries Retry-After in seconds', ...)`.
3. Build fixtures from the claim's evidence: the field names and types the capture
   shows, the limit it states, the error body it quotes. Quote, do not paraphrase - a
   `[quote: ...]` in the evidence row is the exact text to hold the code to.
4. Show each test fails without the code it guards (remove the guard, run, see red),
   then passes with it. A test that stays green with its guard removed proves nothing.

## Rules

- Never invent a field, code or limit for a fixture. If the brief does not state it, it
  is a `fact-request`.
- A known unknown gets no contract test - its first task is `day-one-tasks`.
- Do not call the live service in the suite unless the project already does; the claims
  are the contract, the fixtures carry them.
