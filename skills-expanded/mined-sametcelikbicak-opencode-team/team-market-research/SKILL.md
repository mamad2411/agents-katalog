---
name: team-market-research
description: Market, competitor and user research methodology. Source verification, competitor table, niche analysis and risk assessment. The playbook of the analyst role.
---

# Market and User Research

## 1. Frame the problem

Answer these four questions; if you cannot answer them, the research has not started yet:

| Question | Answer |
|---|---|
| Who is in pain? | A concrete role ("a freelance graphic designer issuing 5-10 invoices a month") |
| What is the pain? | An observable behavior ("waiting weeks for payment, sending 3 reminders") |
| How do they solve it today? | The existing alternative (spreadsheet + email + WhatsApp) |
| Why now? | A timing rationale (a regulation change, a cost drop, a channel maturing) |

The "why now" answer is the hardest one. If it cannot be answered, write it up as a risk.

## 2. Source hierarchy

**Verify competitor names and prices with `websearch`.** Do not write made-up competitor names, made-up prices or made-up market sizes. Mark a competitor you could not verify as "unverifiable", or do not write it at all.

From strongest to weakest:

1. **Primary data**: your own sales/measurement data, support records, user interview notes, survey responses.
2. **The competitor's own material**: the competitor's pricing page, documentation, changelog, status page, support forum.
3. **Competitor user reviews**: G2/Capterra/Product Hunt/Reddit/HN — real expressions of pain live here.
4. **General search volume trend** (Google Trends) — the direction of demand.
5. **Secondary articles** — context only, never as the primary source.

Write the source next to every claim. A claim without a source is marked as an "estimate".

## 3. Competitor table

Do not compare prices only. The dimensions to compare:

| Dimension | Question |
|---|---|
| Price | Who it is for, which tier, what is included |
| Target segment | Who they target, who they do not |
| Main flow | What the user does in the first 5 minutes |
| Gap | What they **do not do** (a missing feature = an opportunity) |
| Bad experience | Where users struggle (the most valuable column) |
| Trust signals | SOC2, GDPR, data location, pricing model |

**The most valuable column is "bad experience".** Go where the competitor is in pain and be better there.

At most 6 competitors. More than that is noise.

## 4. Niche analysis

Think in combinations, not in a single dimension:

`[small segment] × [widespread problem] × [specific solution]`

Is the niche good? Apply this test:

- **Is it wide enough?** Are there 1000+ potential users?
- **Is it narrow enough?** Can you say something specific to them?
- **Is it reachable?** Which channel are they on, and what does it cost?
- **Is there a network effect** (user → user)? If so, growth happens on its own.

## 5. Risks

| Risk | How it is detected | Early test |
|---|---|---|
| No problem (artificial demand) | Nobody is paying money / wasting time right now | Payment intent test (pre-order form, "would you pay for this?") |
| Wrong segment | You are talking in general terms and nobody says "this is not for me" | Talk to 5 users, ask "how would this solve your problem?" |
| Competitive pressure | The competitor already has this feature | Look at the competitor's changelog, read their 12-month roadmap |
| No distribution channel | No access to the channel or it is too expensive | Test reaching 100 target users |
| Regulatory | GDPR/data tax/payment regulation | Sector scan |

## 6. Decision table

Research is not a document, it produces a **decision**. End with this table:

| Question | Answer | Evidence | Confidence |
|---|---|---|---|
| Is the problem real? | yes/no/unclear | source | high/medium/low |
| Is the segment right? | ... | ... | ... |
| Will the niche work? | ... | ... | ... |
| The biggest risk | ... | ... | ... |

Leave unclear answers as "unclear". Deciding nothing and then marking everything as "yes" is the most expensive mistake.

## Output format

Markdown. At most 3 pages. Sections: Problem and users / Market context / Competitor table / Opportunity and niche / Risks and open questions / Decision table.

In the user's language (Turkish or English).
