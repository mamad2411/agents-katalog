---
name: limitation-checker
description: >
  Check limitation periods for civil claims under the Limitation Ordinance
  (Cap 347) and other relevant HK legislation. Determines whether a claim
  is in time or time-barred, and identifies any special rules (extension,
  late knowledge, disability, fraud, concealment, or mistake).
argument-hint: "[describe the claim type, cause of action, dates of relevant events, and any special circumstances]"
---

# /litigation-legal:limitation-checker

1. Load `CLAUDE.md` for the limitation framework (Cap 347).
2. Gather facts: claim type, cause of action, dates, any special circumstances (disability, fraud, concealment, mistake).
3. Walk the checklist below.
4. Produce a limitation assessment report.

## Standard Limitation Periods (Cap 347)

| Claim type | Section | Period | From when |
|---|---|---|---|
| Simple contract | s.4(1)(a) | 6 years | Cause of action accrued |
| Contract under seal (deed) | s.4(3) | 12 years | Cause of action accrued |
| Tort (general) | s.4(1)(a) | 6 years | Cause of action accrued |
| Tort (personal injury) | s.27(3) | 3 years | Date of injury OR knowledge (whichever later) |
| Tort (defamation) | s.27(2) | 6 years | Cause of action accrued |
| Land recovery | s.7(1) | 12 years | Right of action accrued |
| Rent recovery | s.18 | 6 years | Rent due |
| Enforcement of judgment | s.4(4) | 6 years | Judgment date |
| Contribution between tortfeasors | s.26 | 2 years | Right accrued |
| Fatal accident claim | s.27(3) | 3 years | Date of death or knowledge |
| Arbitration award | s.4(1)(c) | 6 years | Breach of award |
| Recovery of sums due under statute | s.4(1)(d) | 6 years | Cause of action accrued |

### Custom Periods Under Specific Ordinances

| Claim type | Ordinance | Period |
|---|---|---|
| Contract of carriage (carriage by sea) | Carriage of Goods by Sea Ordinance (Cap 462) | 1 year |
| Employment claim (Labour Tribunal) | Labour Tribunal Ordinance (Cap 25, s.9) | 12 months |
| Discrimination claim | Cap 480, 487, 527, 602 — various sections | 24 months |
| Employees' compensation | Cap 282, s.14 | 24 months |
| Defamation (newspaper) | Cap 347, s.27(2) | 6 years (but limitation shorter under some provisions) |

## Assessment Checklist

### 1. Identify the Claim Type

| Factor | Detail |
|---|---|
| Nature of claim | [Contract / Tort / Land / Other] |
| Specific category | [Simple contract / PI / Defamation / Land / etc.] |
| Relevant statute | [Cap 347 / other — specify] |
| Applicable period | [N years] |

### 2. Calculate Accrual Date

**When does the cause of action accrue?**

- **Contract:** Date of breach (not when loss is suffered).
- **Tort:** Date damage occurs (not necessarily the date of the wrongful act).
- **Personal injury:** Date of injury OR date of knowledge (if later).
- **Negligence (latent damage):** Cap 347, s.32 — where facts relevant to the cause of action are not known at the time of accrual, time runs from the earliest date the plaintiff knew or ought to have known the relevant facts.
- **Continuing breach:** Each breach gives rise to a fresh cause of action; limitation runs separately for each.

### 3. Check for Extensions

| Circumstance | Rule |
|---|---|
| **Disability (s.22)** | If plaintiff was under a disability (minors, mental incapacity) at the time the cause of action accrued, the limitation period does not start until the disability ends (or death, if earlier). |
| **Fraud / Concealment (s.26A)** | Where the defendant fraudulently concealed the right of action, time does not run until the plaintiff discovered (or could with reasonable diligence have discovered) the fraud. |
| **Mistake (s.26B)** | In claims for relief from the consequences of mistake, time runs from when the plaintiff discovered or could have discovered the mistake. |
| **Personal injury — late knowledge (s.30)** | Court may override the 3-year limit if it is equitable to do so, having regard to prejudice to the defendant. |
| **Acknowledgement / Part payment (s.23)** | For debts and land claims: acknowledgement of the claim or part payment resets the limitation clock. |
| **Agreement to extend time** | Parties may agree to extend limitation by contract (subject to certain limits). |
| **Stay of proceedings** | Limitation is not suspended by a stay of proceedings. |

### 4. Check for Ouster

**Is the claim ousted by a specific limitation defence?**

- [ ] Claim filed within limitation period → presumptively in time
- [ ] Claim prima facie out of time → check for extension grounds
- [ ] Personal injury / fatal accident → check s.30 discretion
- [ ] Latent damage → check s.32 knowledge date
- [ ] Continuing tort → limitation runs from each event

### 5. Is Limitation Pleaded?

- **Limitation is an affirmative defence** — must be pleaded by the defendant (O.18, r.8).
- **Court will not raise limitation of its own motion.**
- **If limitation is not pleaded, the claim may proceed even if theoretically time-barred.**

## Output

| Item | Assessment |
|---|---|
| Claim type | [E.g., Simple contract] |
| Limitation period | [6 years] |
| Cause of action accrued | [DD/MM/YYYY] |
| Limitation expiry | [DD/MM/YYYY] |
| Current date | [DD/MM/YYYY] |
| **In time?** | **✅ Yes / 🔴 No / ⚠️ Potentially — needs extension** |
| Extension grounds | [Disability / Fraud / Concealment / Mistake / Late knowledge / None] |
| Action needed by | [DD/MM/YYYY — if extension] |

### Recommended Actions

- [ ] If in time: proceed with claim; confirm filing before deadline.
- [ ] If expired: advise on alternative claims or extension grounds.
- [ ] If borderline: investigate extension grounds; obtain full factual history.
- [ ] Always verify dates against original documents, not oral statements.
- [ ] If limitation is contestable, advise on protective issue of proceedings.

**Append:** `⚠️ This analysis is based on the information provided and the general provisions of the Limitation Ordinance (Cap 347). Specific claims may be subject to special limitation periods under other ordinances, case law, or contractual provisions. Review with a licensed HK solicitor or barrister before relying on this assessment.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
