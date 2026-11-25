---
name: exclusion-clause
description: >
  Review exclusion clauses under Cap 71 (Control of Exemption Clauses
  Ordinance) — reasonableness test, non-contractual notices.
---

# Exclusion Clause Review (Cap 71)

Review exclusion and limitation clauses under the Control of Exemption Clauses
Ordinance (Cap 71).

## Scope of Cap 71

- Applies to **business liability** (s 2)
- Covers **contract terms** and **non-contractual notices** (s 7–8)
- Some exclusions **void altogether** (e.g., death / personal injury — s 7)
- Others subject to **reasonableness test**

## Void Terms (Unenforceable)

| Type | Section |
|------|---------|
| Death / personal injury from negligence | s 7 |
| Implied terms in sale of goods (title excluded) — vs consumer | s 11(1) |
| Implied terms in hire-purchase — vs consumer | s 11(2) |

## Reasonableness Test (s 3)

Guidelines in **Schedule 2**:

1. **Bargaining strength** of parties
2. **Inducement** to accept (e.g., discount for agreeing to exclusion)
3. **Custom** — whether the customer knew or ought to have known of the term
4. **Insurance** — which party could insure against the risk
5. **Practical possibility** of meeting the condition

For limitation clauses: consider **financial resources** of the party relying on it and **availability of insurance**.

## Key Factors (Case Law)

| Factor | Weight |
|--------|--------|
| Equal bargaining power | Favours clause |
| Clause in standard form (no negotiation) | Against clause |
| Customer had legal advice | Favours clause |
| Limitation = actual loss covered by insurance | May be reasonable |
| Total exclusion (zero liability) | Hard to justify |
| Clause hidden / small print | Against clause |

## Non-Contractual Notices (s 8)

- Notices excluding or restricting negligence liability
- Must satisfy reasonableness test
- "Negligence" includes breach of common law duty of care

## Review Checklist

- [ ] Does Cap 71 apply? (business liability?)
- [ ] Is the clause a **total exclusion** or a **limitation**?
- [ ] Is it **void per se**? (death / personal injury? consumer sale?)
- [ ] Apply Schedule 2 reasonableness guidelines
- [ ] Is the clause incorporated by signature, notice, or course of dealing?
- [ ] Does contra proferentem narrow interpretation against the drafter?


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
