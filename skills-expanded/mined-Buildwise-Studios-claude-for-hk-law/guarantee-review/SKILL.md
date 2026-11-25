---
name: guarantee-review
description: >
  Review guarantee and indemnity under HK common law — distinction, execution
  formalities, demand, discharge, limitation.
---

# Guarantee & Indemnity Review (HK Common Law)

Review guarantees and indemnities under Hong Kong common law.

## Guarantee vs Indemnity

| Aspect | Guarantee | Indemnity |
|--------|-----------|-----------|
| **Nature** | Secondary liability (surety promises to answer for principal debtor's default) | Primary liability (indemnifier's own obligation to hold harmless) |
| **Statute of Frauds** | Must be in writing and signed (s 5 Cap 26 Statute of Frauds) | No formal writing requirement (though prudent to document) |
| **Default condition** | Principal debtor must default first | Indemnifier liable immediately |
| **Limitation** | Runs from principal debtor's default | Runs from indemnifier's breach |

## Key Sections — Statute of Frauds (Cap 26)

- **s 5** — promise to answer for another's debt must be evidenced in writing and signed
- **s 4** — special promise not affected (guarantees caught)

## Execution Formalities

- Guarantee must be **signed** by the guarantor (or authorised agent)
- **Consideration** is required — past consideration is sufficient for guarantees (unusual exception)
- Companies: check directors' authority — ultra vires risk (s 117 Cap 622)
- Personal guarantors: separate legal advice recommended (Chiu Man v Standard Chartered)

## Demand

- Guarantee typically requires a **written demand** before enforcement
- Demand must be **clear and unambiguous**
- Misstatement of amount does not necessarily invalidate demand if debtor can ascertain correct sum
- Time for compliance: "forthwith" = reasonable time

## Discharge of Guarantor

| Event | Effect |
|-------|--------|
| Variation of principal contract (material) without consent | Automatic discharge |
| Release of principal debtor by creditor | Guarantor discharged |
| Part payment + reservation of rights against surety | Guarantor not discharged if rights preserved |
| Lapse of time (no demand) | Not automatic; check limitation |
| Death / mental incapacity | Revocable guarantee — may continue or not depending on terms |
| Creditor's breach of duty (e.g., failure to disclose material facts) | May discharge in good faith / Uberrimae fidei cases |

## Limitation

- Guarantee: 6 years from date of demand / default (Cap 347, s 4)
- Indemnity: 6 years from breach
- Running of time: each default gives fresh cause of action (continuing guarantees)

## Review Checklist

- [ ] Guarantee or indemnity? Check operative language ("default", "answer for", "hold harmless")
- [ ] s 5 Cap 26 compliance — written, signed?
- [ ] Consideration identified?
- [ ] Is demand clause clear?
- [ ] Continuing or specific guarantee?
- [ ] Charge over assets (if secured)?
- [ ] Joint and several liability (if multiple guarantors)?
- [ ] Governing law and exclusive jurisdiction


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
