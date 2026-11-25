---
name: i2r-acceptance-mode
description: Gherkin G/W/T scenarios per FR + prose pass/fail mirror line; produces 06-acceptance.json
when_to_use: Preloaded into i2r-acceptance-author agent for Stage 6 (after 04-functional.json exists)
user-invocable: false
---

# i2r-acceptance-mode

Owned by: `i2r-acceptance-author` (opus). Input: `04-functional.json`. Output: `06-acceptance.json`.

## Purpose

Turn every functional requirement (FR) into:
1. **Internal layer** — one or more Gherkin Given/When/Then scenarios (machine-parseable, ISO 29148 verifiability).
2. **External layer** — one prose `"Passes when …"` line per scenario (GSD-native; lands verbatim in `PRD.md ## Acceptance Criteria`).

## Hard rules

- Every FR in `04-functional.json` MUST have **≥ 1 scenario**. Zero scenarios on any FR → BLOCKER.
- ID format: `AC-<FR_ID>-NN` (two-digit zero-padded). Example: `AC-AUTH-01-01`. See CONTRACT §5.
- `id` pattern: `^AC-[A-Z][A-Z0-9_]*-[0-9]{2,}-[0-9]{2,}$` (schema enforces).
- `given`, `when`, `then` are **arrays of strings** — never inline Gherkin text.
- One scenario = one observable behaviour. Spotted `and`/`or` inside a `then` → split.
- `prose` field = exactly ONE sentence starting with `"Passes when …"` or `"Passes when not …"`. No
  multi-sentence. No implementation detail (HOW). WHAT only.
- Verifiability backcheck (ISO 29148): every scenario must be checkable by an independent party with a
  known pass/fail outcome. Vague outcome → flag UNTESTABLE (BLOCKER) before writing.
- `placeholder_scan` applies to `prose` field (CONTRACT §9): reject `TBD`, `fast`, `secure`, `as needed`.

## References (depth lives here)

- `references/gherkin-rules.md` — Given/When/Then structure + one-scenario-one-behaviour rule
- `references/prose-pass-fail-projection.md` — how to project a scenario into a prose line
- `references/TEMPLATE.json` — single scenario object matching schema item shape
- `references/GOOD_EXAMPLE.json` — AC-ORDER-01-01 anchored on good-run
- `references/BAD_EXAMPLE.md` — anti-patterns + fixes

Sources: Gherkin/Cucumber; ISO 29148:2018 §5.2.6 verifiability; Spec Kit testability checklist;
product-on-purpose GOOD/BAD anchoring.

## Minimal execution flow

```
1. Read 04-functional.json → extract requirements[].id list
2. For each FR, draft ≥1 scenario (ISO 29148 verifiability backcheck per scenario)
3. Write prose mirror for each scenario ("Passes when …")
4. Assemble 06-acceptance.json with _meta block (CONTRACT §4)
5. Run: python scripts/i2r.py validate --stage 6
6. Schema-valid + all FRs covered → done; else fix and re-validate
```
