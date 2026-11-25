---
name: bspdn-pdn-sufficiency-evaluator
description: Evaluate whether the current BSPDN PDN contract is strong enough under `BPR reserved for PDN`, separating PDN sufficiency from signal-mixing questions.
---

# BSPDN PDN Sufficiency Evaluator

Use this skill when the question is "is the current PDN contract strong enough?" rather than "did backside signal routing help?"

## When to use

Use this skill when:
1. the project needs to decide whether `BPR + current backside PDN` is sufficient,
2. PDN weakness may be confounding backside-signal conclusions,
3. `Strict-BPR`, `PDN-boost`, or `Stress-check` comparisons need a dedicated evaluator,
4. PDN stability must be judged without letting signal use `BPR`.

## Scope boundary

This skill owns:
- PDN sufficiency judgments under the current BSPDN contract,
- separating PDN strength questions from signal-routing benefit questions,
- deciding whether the issue is likely `PDN under-strength` vs `topology invalidity` vs `case unsuitability`.

It does not own:
- redefining the physical contract itself without `bspdn-physical-contract-auditor`,
- benefit attribution across `front-only / CTS-backside-only / partial-signal-backside`,
- general execution orchestration.

## Core experiment family

Use this family by default:
1. `Strict-BPR`
2. `PDN-boost`
3. `Stress-check`

## Expected outputs

1. `*.results.tsv`
2. `*.conclusion.md`
3. optional `*.experience_delta.md`

## Hard rules

1. Never answer "PDN is weak" by letting signal use `BPR`; that changes the question.
2. Keep `BPR-reserved-for-PDN` intact unless the physical contract is separately overturned.
3. Distinguish:
- PDN connectivity/stability evidence
- timing side effects
- congestion side effects
4. A better `PDN-boost` result implies "strengthen PDN", not "relax the signal contract".

## Operational references

1. Load `references/background-knowledge-links.md` for the current summarized PDN-sufficiency knowledge contract.
2. Load `references/update-mechanism.md` when deciding whether the evaluator's assumptions or pass/fail criteria need refresh.
