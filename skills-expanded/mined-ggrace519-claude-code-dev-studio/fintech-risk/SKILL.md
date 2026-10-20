---
name: fintech-risk
description: Risk modeling specialist. Owns credit, fraud, and exposure models, feature pipelines, decisioning thresholds, and model monitoring. Auto-invoked for credit decisioning, fraud scoring, chargeback prediction, or risk-limit code.
---

# Fintech Risk

Risk models make money-moving decisions in milliseconds, and a silently drifted
model is a silent, compounding loss. The engineering problem is less the model
than everything around it: features, thresholds, rollout, and monitoring.

## When to reach for this

- Building credit decisioning, fraud scoring, or chargeback prediction
- Designing feature pipelines that must match between training and serving
- Setting decision thresholds, risk limits, or velocity rules
- Rolling out a new model or investigating drift in a live one

## Principles

1. **Shadow before live.** Run the challenger in shadow on production traffic
   long enough to cover a full behavioral cycle (for most consumer portfolios,
   2–4 weeks minimum) and compare decision-level outcomes — not just AUC —
   before it gates a single dollar.
2. **Point-in-time features only.** Every training feature must be computable
   from data available *at decision time*; backfilled or current-state features
   leak the future and inflate offline metrics that evaporate in production.
3. **Policy outranks the model.** Hard rules — exposure limits, sanctions
   blocks, velocity caps — live in a reviewable policy layer outside the model.
   A model score must never be the only thing standing between an attacker and
   an unlimited limit.
4. **Monitor inputs and decision rates, not just accuracy.** Labels arrive
   weeks late (fraud) or months late (credit); feature-distribution drift
   (PSI > 0.25 = act, 0.1–0.25 = investigate) and approval/decline-rate shifts
   are the alarms that fire in time.
5. **Explainability is a legal requirement, not a nice-to-have.** For US credit
   decisions, adverse-action reasons (ECOA/FCRA) must be reconstructable per
   decision — persist the score, top reason codes, feature values, and model
   version at decision time.
6. **Champion/challenger with an exit criterion.** Define the promotion metric,
   the comparison window, and the rollback trigger before the experiment
   starts; an open-ended challenger is just a second unowned model.

## Model rollout checklist

- [ ] Decision policy written: thresholds, hard rules, override authority, and who signs off on threshold changes
- [ ] Training/serving feature parity verified (same code path or a parity test on sampled live traffic)
- [ ] Shadow mode: scores + would-be decisions logged for ≥ 2 weeks, divergence from champion reviewed
- [ ] Per-decision record persisted: model version, features, score, reason codes, applied policy rules
- [ ] Drift monitors live before launch: PSI per top feature, score distribution, approval/alert rate, with paged thresholds
- [ ] Bias/fair-lending analysis run on the challenger across protected-class proxies
- [ ] Rollback is one config change back to champion — no deploy required
- [ ] Threshold and policy changes logged immutably (they change outcomes as much as model swaps)

## Pitfalls

- Validating on a random split instead of out-of-time — time-based holdout or the metrics lie
- Features that proxy the label (e.g. "account closed" predicting default) discovered after launch
- Thresholds tuned once at launch, then frozen while the applicant mix shifts
- Fraud-rule changes evaluated only on caught fraud, ignoring insult rate on good customers
- Retraining on outcomes filtered by the previous model's approvals (selection bias compounding each cycle — design reject inference deliberately)
- Decision records too thin to generate an adverse-action notice after the fact

---
*Related: `fintech-compliance` (rule-based controls and EDD triggers),
`fintech-ledger` (exposure derives from balances), `fintech-audit-trail`
(immutable decision records) · domain agent: `fintech-architect` (risk posture
and model-governance topology) · output/ADR format: `playbook-conventions`*
