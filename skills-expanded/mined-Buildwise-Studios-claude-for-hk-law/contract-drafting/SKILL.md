---
name: contract-drafting
description: >
  Draft commercial contracts under HK law — offer, acceptance, consideration,
  intention, terms, breach, remedies. References common law contract principles.
---

# Contract Drafting (HK Common Law)

Draft and review commercial contracts under Hong Kong common law. Focus on
formation, essential terms, breach provisions, and remedial clauses.

## Core Formation Elements

1. **Offer** — clear, definite, communicated to offeree
2. **Acceptance** — unconditional, communicated; silence generally insufficient
3. **Consideration** — each party must give, suffer, or promise something of value
4. **Intention to create legal relations** — presumed in commercial contexts
5. **Capacity** — natural persons, companies (s 34 Cap 32, directors' authority)

## Drafting Checklist

- [ ] Identify parties correctly (registered name, BR number for HK companies)
- [ ] Recitals (background, commercial purpose)
- [ ] Definitions & interpretation clause
- [ ] Obligations — clear, measurable, time-bound
- [ ] Consideration / price clause
- [ ] Term & termination (fixed, notice period, for cause)
- [ ] Representations & warranties
- [ ] Limitation of liability / exclusion clauses (see Cap 71)
- [ ] Governing law & jurisdiction (HK law, HK courts / arbitration)
- [ ] Boilerplate: entire agreement, variation, waiver, notices, assignment, force majeure

## Common Pitfalls

- **Vague acceptance window** — specify time for acceptance or set an expiry
- **Illusory consideration** — ensure each party actually promises something
- **Inconsistent definitions** — use defined terms consistently throughout
- **Missing execution block** — execute under Cap 622 (Companies Ordinance) for company contracts

## References

- HK common law contract principles
- Cap 26 Sale of Goods Ordinance (for goods)
- Cap 71 Control of Exemption Clauses Ordinance
- Cap 622 Companies Ordinance (execution formalities)


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
