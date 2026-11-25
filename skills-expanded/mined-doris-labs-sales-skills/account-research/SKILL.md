---
name: account-research
description: "Build a sharp, one-page account brief before a call — firmographics, recent triggers, the likely buying committee, mapped pains, and hypotheses to test. Use before a discovery call, an outbound push, or any first touch with a new account. Triggers on: research this account, company research, account brief, who are they, account profile."
---

# Account Research

## Purpose
Walk into the call already knowing who they are, what changed recently, who's likely
in the room, and what you'll bet is hurting them — so the call is spent testing
hypotheses, not gathering facts you could have found beforehand.

## Inputs
- Company name and/or domain
- Any prior relationship (past deals, contacts, meetings) if it exists
- Your product and the pains it removes (so research maps to value)
- The call type and goal (first outbound, inbound demo, expansion)

## Method
Work the five blocks below, then collapse them into the one-page brief. Skip nothing —
a missing block is a blind spot you'll discover live on the call.

**1. Firmographics (the baseline).**
- Industry / sub-vertical, what they actually sell, and to whom
- Headcount + growth trend (flat, hiring hard, RIF'd recently)
- Revenue band / funding stage, ownership (PE, VC, public, bootstrapped)
- HQ + key locations, and whether they're multi-entity
- Tech stack signals relevant to you (e.g. CRM, CI, comms tools)

**2. Recent triggers (the "why now").** Hunt for events in the last ~6 months:
- Funding round, M&A, or new market entry → budget + change appetite
- Leadership change (new VP/C-level in your buyer function) → new mandate, fresh eval
- Aggressive hiring in the function you sell to → scaling pain
- Product launch, repricing, or strategy pivot → operational strain
- Press, earnings commentary, layoffs, or regulatory pressure → priorities shifting
Each trigger becomes a line you can open the call with.

**3. Org structure & likely buying committee.** Map the roles, not just names:
| Role | Who (name/title) | Likely stance |
|------|------------------|---------------|
| Economic buyer | | owns the budget |
| Champion | | feels the pain, will sell internally |
| Technical/eval | | judges fit |
| Blocker | | status-quo or competing priority |
| Coach | | gives you inside info |
Flag the gaps — an unknown economic buyer is the single highest-value thing to learn.

**4. Map likely pains to your product.** For each plausible pain, name the evidence
and the bridge to your value:
```
Pain hypothesis → Trigger/evidence that suggests it → Your capability that removes it → Proof point
```
Three strong mapped pains beats ten generic ones.

**5. Hypotheses to test on the call.** Turn research into questions, not assertions:
- "You raised a Series B in March — I'd guess the team's scaling faster than your
  current process. Is that landing on <buyer function>?"
- "Saw you hired three <role>s last quarter — usually that means <pain>. True here?"
Each hypothesis is falsifiable and earns you a discovery answer either way.

**One-page account brief output format:**
```
ACCOUNT: <name> (<domain>)
Snapshot: <industry> · <headcount> · <funding/ownership> · <HQ>

WHY NOW (triggers):
- <trigger> → <implication>
- <trigger> → <implication>

LIKELY BUYING COMMITTEE:
- Economic buyer: <name/title or UNKNOWN>
- Champion: <name/title or UNKNOWN>
- Other: <names/roles>

MAPPED PAINS → VALUE:
- <pain> → <your capability> (<proof point>)
- <pain> → <your capability> (<proof point>)

HYPOTHESES TO TEST:
1. <falsifiable question>
2. <falsifiable question>

OPEN QUESTIONS / GAPS:
- <the most important unknown to close on the call>

PRIOR RELATIONSHIP:
- <past deals / contacts / meetings, or "net new">
```

## Tool binding
This skill works from a company name alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration, when there's prior history.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected and the account already exists in
your world, pull its real history instead of starting cold:
- `ontology_resolve("account", id, expand=["deals","contacts","meetings","activity","sentiment"])`
  — `deals` gives prior/open deals and outcomes, `contacts` seeds the buying-committee
  map with people you already know, `meetings` surfaces what's been discussed,
  `activity` shows the recent timeline (the real "why now"), and `sentiment` tells you
  whether the relationship is warm or cooling.
- `ontology_search` / `ontology_list` to find the account by name or domain and list
  accounts in the same segment for pattern reference.
- `search_transcripts(...)` to quote what people at this account have actually said in
  prior calls — gold for hypothesis framing.
Prefer Doris-derived contacts, meetings, and sentiment over re-deriving from public
data — they reflect what's true in *your* relationship, not just the open web.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the account + contact records, open/past
  opportunities, and owner/activity history.
- Apollo / LinkedIn (or a data-enrichment MCP) → firmographics, headcount/growth,
  and the org chart for the buying-committee map.
- Web search MCP → recent triggers (funding, hiring, leadership change, news,
  product launches).
- CI MCP (Gong/Chorus/Fireflies) or an email MCP → any prior conversation content.

### With nothing connected
Fully manual path — needs only a company name or domain and the user's notes:
1. Ask the user for the company name/domain, their product, and the call goal.
2. Use web search (or have the user paste): the company website/about page, LinkedIn
   company page (headcount + recent hires), Crunchbase/PitchBook (funding/ownership),
   recent news/press, and the leadership/team page for the org map.
3. Work the five Method blocks from that public info plus anything the user already
   knows about the account.
4. Output the one-page brief, marking every unverified field as a hypothesis and every
   missing role as `UNKNOWN` so the gaps are explicit going into the call.

## Works without Doris
Fully functional from a company name and public sources — Doris only removes the
manual gathering and adds your real relationship history (prior deals, known contacts,
past-call quotes, and sentiment) that the open web can't give you.

## Common mistakes
- A brief that's all firmographics and no "why now" — facts without a reason to call.
- Listing names without mapping them to buying-committee roles and stances.
- Generic pains not tied to a trigger or to your specific capability.
- Hypotheses written as assertions you'll defend instead of questions you'll test.
- Ignoring prior relationship — pitching an account you've already lost or are already
  working as if it were net new.
