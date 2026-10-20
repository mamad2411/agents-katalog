---
name: differential-privacy-basics
description: >
  Differential privacy (DP) basics for analytics and data releases: epsilon/delta privacy
  budgets, Laplace/Gaussian mechanisms, composition, privacy units, local vs central DP,
  and safe reporting of aggregates on owned datasets. Use when differential privacy, epsilon
  budget, DP-SGD awareness, private aggregates, noise addition for releases, or privacy
  engineering for internal metrics — not a substitute for legal counsel or de-identification
  certifications alone.
---

# Differential Privacy Basics

## Scope And Authorization

- **In scope:** Datasets and release pipelines you own; internal privacy engineering with policy approval.
- **Out of scope:** Claiming DP guarantees without budget accounting; re-identifying people; publishing microdata as “DP” without mechanism design.
- Prefer central DP on trusted aggregators when policy allows; document residual risk.
- Redact raw unit-level data from tickets; treat privacy budgets as production config.
- Pair with `device-fingerprint-ethics` for tracking ethics, `ai-ml-security` for ML training leakage, and `code-quality-standards`.

## When To Use

- Publishing dashboards, cohort metrics, or research tables from sensitive user data.
- Setting an ε (epsilon) / δ (delta) policy for product analytics.
- Reviewing whether “we added noise” is actually DP with composition tracked.
- Awareness of DP-SGD and private learning claims.
- Choosing between suppression, k-anonymity-style methods, and formal DP.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Fingerprint/tracking ethics | `device-fingerprint-ethics` |
| Secrets management | `secrets-management-hygiene` |
| ML supply chain / model theft | `ai-ml-security` |
| Access control on data lakes | data platform IAM skills |
| Legal interpretation of GDPR | counsel / privacy legal process |
| Code quality baseline | `code-quality-standards` |

## Core concepts

| Term | Meaning |
| --- | --- |
| Privacy unit | Who is protected (user, event, household)—must be explicit |
| Neighboring datasets | Differ by one unit’s data |
| ε (epsilon) | Privacy loss bound; smaller = stronger privacy, more noise |
| δ (delta) | Small failure probability (often with Gaussian mechanism) |
| Sensitivity | Max change in query output when one unit is added/removed |
| Mechanism | Algorithm that adds calibrated noise (Laplace, Gaussian, etc.) |
| Composition | Multiple queries consume budget; total ε grows (basic/advanced) |
| Central DP | Trusted curator holds raw data, releases noisy answers |
| Local DP | Noise on device before send; stronger trust model, more noise |

**Important:** DP protects against *relative* presence of a unit under a threat model; it does not encrypt data or replace access control.

## Workflow

### 1. Confirm scope and success criteria

1. Dataset class, privacy unit (usually user-id), release audience (public / partners / internal).
2. Policy: max ε per release window (day/month), δ if used, and whether interactive queries allowed.
3. Success: documented budget ledger; releases use calibrated mechanisms; no raw exports via side channel.

### 2. Define queries and sensitivity

| Query type | Typical sensitivity approach |
| --- | --- |
| Count of users | Sensitivity 1 if unit is user |
| Sum of bounded metric | Clip contribution per user then sensitivity = clip bound |
| Mean | Noisy sum / noisy count carefully; or clamp |
| Histogram | Per-bin counts with contribution limits |
| Distinct / graph stats | Often high sensitivity—redesign query |

1. **Clip** per-user contributions before aggregating.
2. Reject unbounded SUM without clipping—noise cannot be calibrated.

### 3. Choose mechanism and parameters

```text
# Laplace for pure ε-DP on numeric query with sensitivity Δ
# noise ~ Lap(Δ / ε)
# Gaussian for (ε,δ)-DP (use standard calibration formulas / library)
```

```python
# Illustrative only — use audited libraries in production
import numpy as np

def laplace_count(true_count: int, epsilon: float) -> float:
    # sensitivity 1 for user-level count
    scale = 1.0 / epsilon
    return true_count + np.random.laplace(0.0, scale)
```

1. Prefer maintained libraries (e.g. OpenDP, Google DP library, Tumult Analytics, PyTorch Opacus for DP-SGD) over hand-rolled crypto-adjacent math for production.
2. Record: ε, δ, mechanism, clipping, date, query id.

### 4. Budget accounting (composition)

1. Maintain a **ledger**: every release deducts from remaining budget for that population/window.
2. Basic composition: sum of ε; advanced/RDP composition for tighter bounds when library supports.
3. Parallel composition: disjoint partitions can share budget carefully—only if partitions guaranteed disjoint.
4. Stop releasing when budget exhausted; do not “just use the same ε again” silently.

### 5. Engineering the pipeline

```text
raw events → enforce ACL → per-user clip → aggregate → DP mechanism → publish
                              ↘ never publish side channel (logs, debug CSV)
```

1. Separate roles: who can run unlimited raw SQL vs DP interface only.
2. Rate-limit interactive analytics; prefer batch releases.
3. Post-process carefully: some floating clamps can break guarantees—follow library guidance.

### 6. DP-SGD / ML awareness (basics)

1. DP-SGD clips per-example gradients and adds noise; privacy cost depends on steps, batch sampling, noise multiplier.
2. Published ε must match **training configuration**; do not copy ε from a paper with different params.
3. Model outputs and memorization still need evaluation (`ai-ml-security` / membership inference awareness).

### 7. Verify and hand off

1. Review: sensitivity proofs/docs, budget ledger samples, no raw microdata in publish path.
2. Utility check: noise vs decision quality; if unusable, redesign query—not zero noise.
3. Document user-facing privacy language accurately (no overclaim).
4. Schedule parameter review when product usage changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Unit | Explicit user-level | Undefined “row” when users have many rows |
| Clip | Bound contributions | Unbounded revenue sum + tiny noise |
| Budget | Ledger with composition | Fresh ε every dashboard refresh |
| Library | Audited DP tooling | Mystery noise in spreadsheet |
| Access | ACL + DP | DP on public S3 of raw logs still open |
| Claims | “ε=1 user-level weekly” | “Fully anonymous forever” |

## Output Checklist

- [ ] Privacy unit, audience, and policy ε/δ documented
- [ ] Queries listed with sensitivity/clipping
- [ ] Mechanism and library chosen
- [ ] Budget ledger and composition method defined
- [ ] Pipeline enforces ACL and no side-channel raw export
- [ ] Interactive query limits considered
- [ ] Utility vs privacy tradeoff accepted by owners
- [ ] ML training claims (if any) parameterized correctly
- [ ] Public language reviewed for overclaim
- [ ] Review date and owners set

## Rules

- No sensitivity, no DP—noise alone is not enough.
- Track composition; budgets are real resources.
- DP complements access control, encryption, and purpose limitation—it does not replace them.
- Prefer libraries and peer review for production privacy guarantees.
- Owned data and authorized releases only; not legal advice.
