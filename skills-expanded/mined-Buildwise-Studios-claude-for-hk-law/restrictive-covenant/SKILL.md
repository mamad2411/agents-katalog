---
name: restrictive-covenant
description: >
  Review non-compete, non-solicitation, non-dealing, and non-poaching clauses
  in Hong Kong employment contracts and settlement agreements. Assesses
  enforceability under HK common law (legitimate business interest,
  reasonableness in scope/geography/duration, public policy, blue pencil
  test).
argument-hint: "[paste or attach the restrictive covenant clause(s) and context]"
---

# /employment-legal:restrictive-covenant

1. Load `CLAUDE.md` for the HK common law framework on restrictive covenants.
2. Gather the clause(s) and context: employee's role, seniority, market access, confidential information, customer relationships.
3. Walk the assessment framework below.
4. Produce an enforceability report with recommendations.

## HK Common Law Framework

### General Principle

Restrictive covenants are **prima facie void** as a restraint of trade. They are enforceable only if the employer can establish ALL THREE elements:

1. **Legitimate business interest** — something the employer is entitled to protect
2. **Reasonableness** — the covenant goes no further than necessary to protect that interest (scope, geography, duration)
3. **Not contrary to public interest** — the covenant does not harm the public

### Legitimate Business Interests

| Interest | Typical protection | Examples |
|---|---|---|
| Trade secrets / confidential information | Non-compete, non-dealing | Proprietary formulas, client lists, business strategies |
| Customer connections | Non-solicit | Long-term client relationships, key accounts managed by the employee |
| Employee relationships / team stability | Non-poach | Key personnel the employee has recruited or managed |
| Goodwill of business | Non-compete | Professional services, partnerships |

**Note:** General skill and experience acquired during employment is NOT a legitimate business interest.

### Reasonableness Test

| Factor | What to check |
|---|---|
| **Duration** | Typically 3–6 months for most junior/senior employees; 12 months for senior executives with deep client relationships; anything beyond 12 months faces heavy scrutiny |
| **Geographic scope** | Must be tied to the employer's actual business footprint — "Hong Kong" is typical; "worldwide" is rarely enforceable unless truly global business |
| **Activity scope** | Must match the employee's actual role — "any business" is too broad; "same or similar business as employer" may be acceptable if narrowly defined |
| **Party-specific factors** | Employee's seniority, access to confidential information, client relationships, remuneration |

### Blue Pencil Test

HK courts apply the **blue pencil test**: if the offending part of a covenant can be struck out without rewriting the clause (i.e., by deleting specific words), the remainder may be enforceable. The court will NOT add words or rewrite the clause.

- ✅ Severable: "in Hong Kong and Macau" → strike "and Macau" → "in Hong Kong" (single geographical block)
- ❌ Not severable: "any business in the technology sector" → court cannot redefine "any" to "some"

### Case Law Principles (HK)

- HK courts follow English common law on restraint of trade, adapted to HK commercial reality.
- **Burden of proof:** Employer bears the burden of establishing enforceability.
- **Consideration:** A post-employment restrictive covenant in an existing employment contract may require fresh consideration to be enforceable (e.g., promotion, pay rise, or a specific sum for signing).
- **Garden leave:** An alternative to restrictive covenants — employee serves notice period at home on full pay. Courts will enforce genuine garden leave but not extend it unreasonably.

## Assessment Checklist

| Factor | Check | Risk |
|---|---|---|
| Duration > 12 months | [ ] | 🔴 High |
| Duration 6–12 months | [ ] | 🟠 Medium |
| Duration 3–6 months | [ ] | 🟡 Medium |
| Duration < 3 months | [ ] | 🟢 Low |
| Global/regional scope where business is HK-only | [ ] | 🔴 High |
| Covers broader activities than employee's role | [ ] | 🔴 High |
| Employee has genuine client relationships | [ ] | 🟢 Favourable |
| Employee has access to trade secrets | [ ] | 🟢 Favourable |
| Consideration provided for post-employment covenant | [ ] | 🔴 High if missing |
| Blue pencil severable | [ ] | 🟢 Favourable |
| Clause uses "reasonable" language | [ ] | 🟢 Favourable |

## Output

| Element | Assessment | Tags |
|---|---|---|
| Legitimate business interest | [Exists / Unclear / Absent] | `[review]` |
| Duration | [Reasonable / Excessive] | |
| Scope | [Reasonable / Excessive] | |
| Geography | [Reasonable / Excessive] | |
| Blue pencil | [Severable / Not severable] | `[review]` |
| Consideration | [Adequate / Missing] | `[review]` |
| **Overall enforceability** | **[Likely / Unlikely / Depends]** | |

**Recommendation:** Redline suggestions (narrow scope, reduce duration, add garden leave as alternative, add fresh consideration).

**Append:** `⚠️ Restrictive covenant enforceability is highly fact-dependent. Review this assessment with a licensed HK solicitor or barrister before relying on the covenant.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
