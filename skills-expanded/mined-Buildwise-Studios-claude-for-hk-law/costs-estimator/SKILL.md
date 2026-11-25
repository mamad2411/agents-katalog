---
name: costs-estimator
description: >
  Estimate litigation costs on a party-party or indemnity basis under the
  Rules of the High Court (Cap 4A, O.62) and Rules of the District Court
  (Cap 336H, O.62). Estimates costs for each phase of litigation
  (pleadings, discovery, trial, appeal) and compares likely recovery on
  party-party vs indemnity assessment. Includes HK costs-shifting analysis.
argument-hint: "[describe the case type, estimated duration, likely outcome, and budget]"
---

# /litigation-legal:costs-estimator

1. Load `CLAUDE.md` for the costs framework (RHC O.62 / RDC O.62).
2. Gather case context: court, case complexity, estimated hearing days, number of witnesses, discovery scope.
3. Estimate phase-by-phase costs.
4. Apply basis of assessment (party-party vs indemnity).
5. Produce a costs estimate with recovery analysis.

## Costs Framework

### Basis of Assessment (O.62)

| Basis | Test | Approximate recovery |
|---|---|---|
| **Party and party (standard)** | Costs "necessary and proper" for the attainment of justice — Interlocutory Chambers costs Taxing Master scale | ~60–70% of actual |
| **Indemnity basis** | All costs except those unreasonably incurred or of an unreasonable amount — more generous; all doubts resolved in favour of the receiving party | ~80–90% of actual |
| **Common fund** | Applies to legal aid; more generous | |

### Scale of Costs (O.62, Appendix — prescribed scales)

HK courts have prescribed scales for certain items (e.g., solicitor's fees for interlocutory applications, brief fees per day). The Taxing Master applies these scales unless the court orders otherwise.

- **Scale A:** Lower value claims, simpler work
- **Scale B:** Standard matters
- **Scale C:** Complex/higher value claims

## Phase-by-Phase Cost Estimate

### 1. Pre-Action Phase

| Item | Estimated cost (HK$) | Party-party recoverable |
|---|---|---|
| Correspondence and negotiations | [amount] | ~60% |
| Pre-action protocol compliance | [amount] | ~60% |
| Advice on merits | [amount] | ~60% |
| Letter before action | [amount] | ~60% |

### 2. Pleadings Phase

| Item | Estimated cost | Party-party recoverable |
|---|---|---|
| Drafting SoC / Defence | [amount] | ~65% |
| Pleading amendments | [amount] | ~60% |
| Reply / Counterclaim | [amount] | ~60% |
| Striking out application | [amount] | ~50% |

### 3. Discovery Phase

| Item | Estimated cost | Party-party recoverable |
|---|---|---|
| Document collection & review | [amount] | ~60% |
| Affidavit of documents | [amount] | ~65% |
| Specific discovery application | [amount] | ~50% |
| Privilege review | [amount] | ~60% |

### 4. Interlocutory Applications

| Item | Estimated cost | Party-party recoverable |
|---|---|---|
| Summons for directions | [amount] | ~65% |
| Summary judgment | [amount] | ~60% |
| Security for costs | [amount] | ~50% |
| Injunction / freezing order | [amount] | ~50% |
| ADR / mediation | [amount] | ~60% |

### 5. Trial Preparation

| Item | Estimated cost | Party-party recoverable |
|---|---|---|
| Brief fee (counsel) | [amount] | Scale B/C |
| Witness preparation | [amount] | ~60% |
| Expert report(s) | [amount] | ~60% |
| Trial bundle preparation | [amount] | ~65% |
| Skeleton argument | [amount] | ~65% |

### 6. Trial

| Item | Estimated cost | Party-party recoverable |
|---|---|---|
| Brief fee (per day) | [amount] | Scale |
| Instructing solicitor (per day) | [amount] | Scale |
| Counsel's refreshers | [amount] | Scale |
| Travel, subsistence | [amount] | — |

### 7. Appeal

| Item | Estimated cost | Party-party recoverable |
|---|---|---|
| Notice of Appeal | [amount] | ~60% |
| Skeleton argument | [amount] | ~65% |
| Appeal hearing (per day) | [amount] | Scale |
| CFA leave application | [amount] | ~50% |

## Summary Cost Calculation

| Category | Estimated actual | Party-party recovery | Indemnity recovery |
|---|---|---|---|
| Pre-action | HK$ [N] | HK$ [N] | HK$ [N] |
| Pleadings | HK$ [N] | HK$ [N] | HK$ [N] |
| Discovery | HK$ [N] | HK$ [N] | HK$ [N] |
| Interlocutory | HK$ [N] | HK$ [N] | HK$ [N] |
| Trial prep | HK$ [N] | HK$ [N] | HK$ [N] |
| Trial | HK$ [N] | HK$ [N] | HK$ [N] |
| Appeal (if any) | HK$ [N] | HK$ [N] | HK$ [N] |
| **Total** | **HK$ [N]** | **HK$ [N]** | **HK$ [N]** |

### Key Assumptions

- [ ] Case type: [simple / moderate / complex]
- [ ] Estimated hearing days: [N]
- [ ] Number of witnesses: [N fact / N expert]
- [ ] Discovery documents: [small / moderate / large]
- [ ] Interlocutory applications anticipated: [N]

## Output

- [x] Phase-by-phase cost estimate
- [x] Party-party vs indemnity comparison
- [x] Costs-shifting analysis (loser pays)
- [x] Part 22 offer strategy recommendation
- [x] Security for costs assessment (if applicable)

**Append:** `⚠️ Cost estimates are indicative only. Actual costs depend on the complexity of the case, the court's directions, and the outcome of individual applications. Taxing Master's scale rates should be verified against current scales. Review with a practising HK costs specialist for a formal estimate.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
