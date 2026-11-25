---
name: appeal-routes
description: >
  Determine the correct appeal route, leave requirements, and time limits
  from any Hong Kong court or tribunal decision. Covers the Court of Final
  Appeal, Court of Appeal, Court of First Instance, District Court, Labour
  Tribunal, Small Claims Tribunal, and Lands Tribunal.
argument-hint: "[describe the court/tribunal decision — originating court, type of order, amount in issue]"
---

# /litigation-legal:appeal-routes

1. Load `CLAUDE.md` for the appeal framework and court hierarchy.
2. Gather the decision details: originating court, type of order (final/interlocutory), amount in issue, and date of decision.
3. Walk the appeal route decision tree below.
4. Produce a route map with leave requirements, time limits, and procedural steps.

## Appeal Route Decision Tree

### Step 1: Identify the Originating Court or Tribunal

| Originating body | Appeal goes to |
|---|---|
| Master of the CFI | Judge in Chambers (CFI) |
| CFI Judge (final order) | Court of Appeal |
| CFI Judge (interlocutory) | Court of Appeal (leave usually required) |
| District Court Judge | Court of Appeal |
| Registrar of DC | Judge in Chambers (DC) |
| Labour Tribunal | CFI (point of law only — leave required) |
| Small Claims Tribunal | CFI (point of law or jurisdiction — leave required) |
| Lands Tribunal | CA (final order) / CFI (interlocutory) |
| Court of Appeal | Court of Final Appeal |

### Step 2: Determine Leave Requirements

| Route | Leave required? | Who grants leave? |
|---|---|---|
| Master → Judge (Chambers) | No (unless interlocutory matters under specific rules) | — |
| DC → CA (amount < HK$1M) | Yes | CA (single judge) |
| DC → CA (amount ≥ HK$1M) | Usually no, but CA may require | — |
| CFI → CA (final order) | No (as of right) | — |
| CFI → CA (interlocutory) | Yes | CA |
| Labour Tribunal → CFI | Yes | CFI (on point of law only) |
| Small Claims → CFI | Yes | CFI (on point of law/jurisdiction) |
| CA → CFA (value ≥ HK$1M) | No (appeal as of right) | — |
| CA → CFA (value < HK$1M) | Yes | CFA Appeal Committee |
| CA → CFA (criminal) | Yes | CFA Appeal Committee |

### Step 3: Calculate Time Limits

| Route | Time limit | From when |
|---|---|---|
| Master → Judge (Chambers) | 14 days | Date of order (unless otherwise directed) |
| DC → CA | 14–28 days | Date of judgment/order |
| CFI → CA | 28 days (final) / 14 days (interlocutory) | Date of order |
| Labour Tribunal → CFI | 7 days | Date of LT order |
| Small Claims → CFI | 7 days | Date of order |
| Lands Tribunal → CA | 28 days | Date of order |
| CA → CFA (Notice of Motion) | 28 days | Date of CA order/judgment |

### Step 4: Procedural Requirements

#### Appeal to Court of Appeal (RHC O.59)

| Step | Timing | Document |
|---|---|---|
| Notice of Appeal | Within time limit (above) | Form — must specify order, grounds, and relief |
| Respondent's Notice | 21 days after Notice of Appeal served | If respondent varies order |
| Skeleton argument (appellant) | 14 days before hearing | Concise, numbered, with authorities |
| Skeleton argument (respondent) | 7 days before hearing | |
| Appeal bundle | 7 days before hearing | Indexed, paginated |

#### Appeal to Court of Final Appeal (Cap 484A)

| Step | Timing | Document |
|---|---|---|
| Notice of Motion (leave) | 28 days of CA order | Form CFA 1 |
| Appeal Committee | Screened in chambers (3 judges) | Written submissions |
| Full hearing (if leave granted) | Set by the Registrar | Fresh notice of appeal required |

### Step 5: Special Considerations

#### Stays Pending Appeal

- **Automatic stay:** None — a party must apply for a stay of execution pending appeal.
- **Stay conditions:** Security for costs, payment into court, or undertakings.

#### Security for Costs on Appeal

- Appellant ordinarily resident outside HK: security for costs may be required.
- In CA, the respondent may apply for security (O.59, r.10).

#### Intervener

- The Secretary for Justice may intervene on constitutional questions (CFA Rules).
- Amicus curiae: CFA and CA may invite.

## Output

```
Appeal Route Map
═════════════════
Originating court: [Labour Tribunal]
Type of decision: [Final order — breach of employment contract]
Amount in issue: [HK$150,000]
───────────────────────────────────────────
Step 1:      Labour Tribunal
Step 2:      └─ Appeal to CFI (leave required – point of law)
                  │
                  ├─ Leave granted? → Appeal on point of law
                  │   Time limit: 7 days from LT order
                  │
                  └─ Leave refused? → No further appeal
                  │   (Judicial review possible but exceptional)
                  │
Step 3:      CFI decision
             └─ Appeal to CA (if final order, as of right)
                  Time limit: 28 days
Step 4:      CA decision
             └─ Appeal to CFA
                  │ Amount ≥ HK$1M: as of right
                  │ Amount < HK$1M: leave required
                  Time limit: 28 days
───────────────────────────────────────────
Key documents required:
• Notice of Appeal (CFI or CA)
• Skeleton arguments
• Appeal bundle
```

**Append:** `⚠️ Appeal routes, leave requirements, and time limits are subject to the court's specific rules and directions. Verify against the current RHC, RDC, or CFA Rules. This is not a substitute for legal advice.`


## HK primary sources (run before citing)

Run from the **cloned `claude-for-hk-law` repo root** (see `references/hk-primary-sources-setup.md`). Before citing a Cap, rule, or case, run scripts **in this session** and tag: `[HK e-Legislation / DOJ open data]`, `[HKLII search]`, `[Judiciary site search]`, or `[model knowledge — verify]`. No HKLII/CLIC MCP is shipped.

```bash
python3 scripts/download_legislation_list.py --cap <cap>
python3 scripts/download_legislation_text.py <cap>
python3 scripts/hklii_search.py "<query>" --cases --limit 10
python3 scripts/judiciary_search.py "<query>" --limit 10
```
