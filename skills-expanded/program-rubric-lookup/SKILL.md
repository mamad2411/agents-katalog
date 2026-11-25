---
name: program-rubric-lookup
audience: specialist
description: Use when you have a candidate finding and must map it to the bounty program's own accepted vulnerability classes, severity language, payout tiers, and submission requirements — confirm the asset is in scope, cite the exact governing policy clause for each claimed impact, and score conservatively where program rules override generic scoring.
---

# Program Rubric Lookup

Map a finding to the target program's accepted vulnerability classes, severity language, payout rubric, and submission requirements.

## Inputs

- The exact program policy or ruleset, with retrieval date and provenance.
- A concise finding statement, affected asset, impact, and prerequisites.
- Any explicit exclusions, safe-harbor conditions, or severity overrides.

## Method

1. Confirm the asset and vulnerability class are in scope before scoring.
2. Extract the program's controlling severity rubric and any class-specific caps.
3. Map each claimed impact to one quoted or precisely cited rubric clause.
4. Record exclusions, prerequisites, and ambiguity separately from the score.
5. Produce a conservative classification and identify what evidence would raise or lower it.

## Acceptance

- Every classification cites the governing policy text and retrieval date.
- Scope, severity, payout eligibility, and submission requirements are distinct fields.
- Unsupported impact is marked unproven rather than inferred.
- Conflicts between generic scoring and program-specific rules resolve in favor of the program rules.
- **The evidence contract is an output, not an assumption.** Record, as separate fields: the
  program type and payout model; the authoritative target and what makes it authoritative
  (repo@commit, deployed address, host or build, binary hash); the PoC forms the program's own text
  accepts; and the forms it explicitly forbids, each tied to the clause that says so.
- **Where the program is silent, write "not stated" — never infer a restriction.** A generic or
  internal grading heuristic is not a program rule. Do not conclude from one that a live-chain
  transaction, a particular tool, or a production crash is required when the program's published
  text asks only for a working proof of concept. Inferring such a requirement has already sent a
  campaign chasing evidence nobody asked for.

## Payout topology (AUD-11)

There is **no universal severity-to-dollar table** — rewards are program-specific. Record, alongside
the rubric:

```
payout_model: fixed_per_severity | range_per_severity | critical_only | contest_pool | unknown
payout_source: exact program clause + retrieval date
marginal_reward_notes: duplicate handling, pool dilution/uniqueness rules, PoC eligibility conditions
```

**Payout topology is an operator SELECTION fact, never a pre-hunt kill list.** It informs which
program to enter; it never prunes what may be hunted, chained, or banked inside one.

### `critical_only` programs — the disqualifier checklist (AUD-12)

On a `critical_only` program the grader closes a genuine sub-Critical finding as *Informative*, not
out-of-scope, when “the trigger is not attacker-controlled, impact is off-chain/liveness/MEV, PoC
exercises out-of-scope contracts, or the finding requires developer error as proximate cause.”
Produce this checklist at Phase 1, so the hunt aims at the step function rather than discovering it at
submission time. The finding must survive all four:

- **Attacker-controlled trigger** — not a privileged, accidental, or operator-only one.
- **Direct user fund loss or permanent lock** — not liveness, not MEV, not off-chain, and not a
  protocol-insolvency abstraction.
- **In-scope-only PoC surface** — the PoC exercises no out-of-scope contract.
- **No dependence on an assumed developer or configuration error** as proximate cause.

This is `impact-validator`'s G1 applied with the program's own words. It sets what a hunt aims at; it
is not a fifth exclusion ground and it never removes a banked primitive.
