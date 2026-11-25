---
name: crm-opportunity-summarizer
description: Use when a sales rep or RevOps lead needs a concise opportunity summary from Salesforce or HubSpot — pulling stage, amount, contacts, recent activity, and risks, then producing a deal brief and recommended next-best-action.
---

# CRM Opportunity Summarizer

## When to invoke
- "Summarize the Acme Corp deal."
- "Give me a brief on my top 5 open opps."
- "What's at risk in our Q2 pipeline?"

## Inputs needed
1. **CRM** — Salesforce or HubSpot.
2. **Filter** — opportunity ID(s), owner, stage, or close-date range.
3. **Context depth** — quick (just record fields) or deep (include emails, calls, notes).

## Workflow
1. **Resolve** — find the opportunity records via API or CSV.
2. **Aggregate** — pull stage, amount, contacts, owner, last activity, age in stage.
3. **Score risk** — flag stalled, no-MEDDIC, no-economic-buyer, slipped close date.
4. **Draft brief** — TL;DR, key facts, risks, recommended next-best-action.
5. **Hand off** — Markdown brief per opp, or a single roll-up table.

## Output format per opportunity
```
## <Account> — <Opportunity Name>
**Stage:** ... | **Amount:** $... | **Close:** YYYY-MM-DD | **Owner:** ...

**TL;DR:** <one line>

**Key contacts:** ...

**Recent activity:** <last 3 touches>

**Risks:**
- ...

**Next best action:** <specific, owned, dated>
```

## Guardrails
- Never invent contacts, amounts, or dates not in the source data.
- If MEDDIC/BANT fields are missing, state "missing" — do not infer.
- Mark records with no activity in 14+ days as "stalled".

## Reference code
`summarize.py` reads from Salesforce REST, HubSpot CRM API, or a CSV export and emits Markdown briefs.
