---
name: evidence-and-validation
description: Validation discipline that turns a candidate signal into a confirmed, rejected, or inconclusive verdict using category-specific oracles, baselines, and negative controls. Use whenever any scanner, browser, source, fuzzing, or manual step produces a possible vulnerability, before creating or verifying a finding. This is the guard against false positives.
metadata:
  domain: offensive-security
  tier: spine
---

# evidence and validation

every incoming item is a *candidate* until an oracle confirms it. the goal is to
never report a false positive: unvalidated findings cost more to triage than they
are worth, and low-quality automated reports are actively rejected by real
programs.

bind each candidate to its hypothesis, the exact request surface, the identity
used, and the saved evidence (`campaign_test`, `evidence_save`).

## the evidence ladder

farai records evidence strength as a ladder. know which rung a candidate is on and
what the next rung requires:

```text
signal → differential_observed → reproduced → impact_demonstrated → independently_verified
```

- `signal`: a single suggestive observation (a scanner hit, an anomaly). never
  reportable alone.
- `differential_observed`: the payload response differs from a baseline in a way a
  negative control does not explain. the minimum bar for blind/boolean classes.
- `reproduced`: the effect repeats deterministically across runs.
- `impact_demonstrated`: a concrete security effect is shown (data crossed a
  boundary, code executed, state changed).
- `independently_verified`: a *different session* reproduced it (`campaign_verify`
  cross-session gate).

## verdict rule

choose the category oracle *before* the final probe. require:

1. a **baseline** (the operation without the mutation), and
2. a **negative control** that would *falsify* the hypothesis if the signal were
   coincidental (caching, timing, eventual consistency, shared state, WAF, or a
   status-code artifact).

return exactly one of `confirmed`, `rejected`, or `inconclusive`. emit
"control passed" only from an observed artifact, never from confidence. a
`confirmed` result with a clean negative control may create a primitive for impact
and chaining; `rejected` / `inconclusive` records failure knowledge and continues
other hypotheses — it never becomes a global "target is safe" conclusion.

## category oracles (summary)

distinguish *data presence* from *authorization success*, and *reflection* from
*execution*. each class has its own discriminating test and minimum evidence
level — load `resources/oracles.md` for the full checklist:

- **xss** — fire in a real browser (`browser_*`); require an observed dom/js
  side-effect (dialog, exfil, node injected), not reflected markup.
  `impact_demonstrated`.
- **ssrf / blind injection / oob** — a `callback_oast` token unique to *this*
  attempt must be received; correlate it to rule out cached or coincidental
  callbacks. `impact_demonstrated`.
- **open redirect** — follow the `Location` header and diff the destination host.
- **sqli (blind)** — boolean/time differential against a baseline, repeated.
  `differential_observed`+.
- **access control (idor/bola)** — cross-identity server-side readback: another
  identity's exact resource returned or mutated, proven by state, not `200` vs
  `403`.
- **business logic** — server-side readback of the invariant violation, with
  rollback of any durable effect.

## routing

- record the verdict and evidence with `campaign_test` (status + evidence level)
  and `evidence_save`.
- create the candidate with `report_add_finding`, then promote with
  `campaign_verify` once impact or independent verification is met.
- for independent verification, hand off to a fresh `verify` lane (`agent_spawn`)
  so the confirmer is a different session than the finder.

resource: `resources/oracles.md` — per-category discriminating tests and required evidence.
