---
name: sog-review
description: >
  Sale of goods contract review under Cap 26 (Sale of Goods Ordinance) —
  implied terms, passing of property, acceptance, remedies.
---

# Sale of Goods Review (Cap 26)

Review goods contracts under the Sale of Goods Ordinance (Cap 26).

## Key Implied Terms

| Term | Section | Nature |
|------|---------|--------|
| Title | s 14 | Condition |
| Description | s 15 | Condition |
| Satisfactory quality | s 16(2) | Condition (if sale in course of business) |
| Fitness for purpose | s 16(3) | Condition (if buyer relies on seller's skill) |
| Sample | s 17 | Condition (bulk must match sample) |

## Passing of Property

- **s 19** — specific/ascertained goods pass at parties' intention
- **s 20** — rules for unascertained goods (unconditional appropriation)
- **s 22** — reservation of right of disposal
- **s 21** — nemo dat rule; **s 24**(seller in possession) / **s 25**(buyer in possession) exceptions

## Acceptance

- **s 35** — acceptance by: (a) intimation, (b) act inconsistent with seller's ownership, (c) retention beyond reasonable time without rejection
- **s 36** — buyer not bound to return rejected goods
- **s 37** — buyer's duty to reject within reasonable time if not already accepted

## Remedies

### Seller's Remedies
- Action for price (s 49)
- Damages for non-acceptance (s 50)
- Lien (s 41)
- Stoppage in transit (s 44)

### Buyer's Remedies
- Damages for non-delivery (s 51)
- Specific performance (s 52)
- Damages for breach of warranty (s 53)
- Rejection + damages for condition breach

## Review Steps

1. Identify goods, price, delivery terms
2. Check whether seller acts "in course of business"
3. Identify any express exclusion of implied terms
4. Review acceptance / rejection timelines
5. Assess available remedies


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
