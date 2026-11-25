# Skill: Private and early-stage investing

Domain guidance for angel, seed and other private-company decisions. It tells you what
competent analysis looks like, not what to conclude.

## What a serious answer must contain

- **Explicit power-law framing.** Expected value in this asset class comes from a small
  number of extreme outcomes. An analysis that reasons about the median outcome is
  answering the wrong question. State the outcome distribution you are assuming.
- **Ownership at exit, not ownership today.** Model dilution across the plausible
  financing path. An entry percentage without a dilution path is meaningless.
- **Illiquidity priced explicitly.** Capital is locked for years with no secondary market
  assumption unless one is evidenced. State the holding period.
- **The specific reason this deal is available.** If the round is accessible to the user,
  say why better-informed capital is not taking it. Adverse selection is the default
  hypothesis and must be argued against, not ignored.

## Standard alternatives to consider

Do nothing; a smaller check; waiting for the next round with information rights; an
index or public-market equivalent for the same capital; and deploying across several
smaller positions instead of one.

## Source hierarchy for this domain

1. Primary deal documents: term sheet, SAFE or note, cap table, articles.
2. Direct company data: audited or management accounts, cohort and retention data,
   customer contracts.
3. Reference calls with customers and former employees, recorded with date and role.
4. Sector benchmarks from named datasets (with vintage and sample size stated).
5. Press coverage, founder-authored posts, pitch material. Directional only; treat all
   founder-supplied projections as claims, never as evidence.

Founder statements and the deck derived from them are **one** source. Group them.

## Domain-specific traps

- **Narrative substituting for traction.** A compelling story about a large market is not
  evidence of demand. Look for revenue, retention, or paid conversion.
- **TAM inflation.** Top-down market sizing is almost always wrong. Prefer bottom-up.
- **Reference bias.** Founder-supplied references are selected. Weight unsolicited
  references far higher and say which kind you obtained.
- **Round-price anchoring.** The last round's valuation is a negotiation artifact, not a
  measurement.
- **Ignoring graveyard risk.** Most seed companies return zero. State the probability of
  total loss explicitly and keep it as an outcome probability.

## Quantitative expectations

Model at minimum: total loss, a modest exit, and a power-law outcome, with an explicit
probability on each and the resulting expected multiple. Sensitivity must include
dilution and the probability of total loss. Numbers come from executed code under
`analysis/`.
