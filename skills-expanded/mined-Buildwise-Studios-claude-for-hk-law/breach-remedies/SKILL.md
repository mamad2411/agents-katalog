---
name: breach-remedies
description: >
  Breach of contract remedies under HK common law — damages (expectation,
  reliance), specific performance, injunctions, rescission, limitation periods.
---

# Breach Remedies (HK Common Law)

Remedies for breach of contract under Hong Kong common law.

## Primary Remedies

### 1. Damages

| Type | Measure | Notes |
|------|---------|-------|
| **Expectation** | Put claimant in position as if contract performed | Default measure |
| **Reliance** | Restore wasted expenditure | Used when expectation is speculative |
| **Consequential** | Losses flowing naturally from breach (Hadley v Baxendale) | Limb 1: direct; Limb 2: in contemplation |
| **Liquidated** | Agreed sum in contract | Must be genuine pre-estimate (not a penalty) |

**Limiting principles:**
- Causation
- Remoteness (Hadley v Baxendale)
- Mitigation (duty to take reasonable steps)
- Contributory negligence (rare in contract)

### 2. Specific Performance

- Equitable remedy
- Not available for personal services
- Not granted if damages adequate
- Subject to laches, unclean hands, hardship

### 3. Injunction

- Prohibitory — restrain breach of negative covenant
- Mandatory — compel act (rare, stricter)
- Quia timet — prevent anticipated breach

### 4. Rescission

- Restore parties to pre-contract position
- Available for: misrepresentation, duress, undue influence, mistake
- Lost if: affirmation, lapse of time, third-party rights acquired

### 5. Action for an Agreed Sum

- Debt claim for price / payment due
- No mitigation requirement

## Limitation Periods

| Claim | Period | Trigger |
|-------|--------|---------|
| Simple contract | 6 years | Cause of action accrues |
| Deed / specialty | 12 years | Cause of action accrues |
| Latent damage | 6 years (or 3 from discoverability) | s 32 Limitation Ordinance |

**Key rules:**
- s 4 Limitation Ordinance (Cap 347)
- Part payment or written acknowledgment restarts limitation (s 23)
- Claims for contribution between wrongdoers: 2 years (s 6 Law Reform Ord)

## Checklist

- [ ] Identify breach and when it occurred
- [ ] Expectation vs reliance — which is appropriate?
- [ ] Check liquidated damages clause (penalty rule)
- [ ] Are losses remote under Hadley v Baxendale?
- [ ] Did claimant mitigate?
- [ ] Specific performance — is damages inadequate?
- [ ] Limitation period check (6 years / 12 years)
- [ ] Any limitation or exclusion clause (Cap 71)?


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
