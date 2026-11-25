---
name: gbb-pulse
description: Draft signals for the weekly AI GBB Pulse. Use when asked to write a pulse signal, customer win/loss, escalation, compete signal, product signal, IP initiative, or skills/people signal.
---

# GBB Pulse Signal Drafter

Draft structured signals for the weekly AI GBB Pulse — field insights (patterns, trends, competitive intelligence) fed back to product groups and go-to-market teams. Signals feed into MSR and MTR reviews.

## Workflow

1. Gather input from the user about their customer engagement or market observation
2. Use WorkIQ to enrich context from recent M365 emails, Teams, meetings, documents
3. Classify into one of the signal types below
4. Draft using the matching template, ask if any required fields are missing
5. Save to `output/pulse-signals/YYYY-MM-DD-<signal-name>.md`

## Guidelines

- Always use WorkIQ to gather context before drafting
- Ask clarifying questions when input is incomplete — never fabricate
- Keep signals concise and actionable
- One signal per draft

---

## Signal Templates

### Customer Win

- **Customer Names**: _e.g. Contoso Inc_
- **Deal Size / Microsoft Impact**: _ACR, MACC, deal size_
- **Technology**: _AI Services, M&M, Database, 3P/OSS_
- **Compete**: _AWS, GCP, etc. if applicable_
- **IP Used**: _any IP leveraged_
- **Use Cases**: _list use cases_
- **Industry**: _industry name_
- **Description**: _3-4 sentences: customer situation, approach, technical solution, compete details_
- **Business Impact**: _quantify: ROI, cost reduction, UX improvement_
- **Additional Info**: _architecture, pricing, compete pricing_

### Customer Loss

- **Customer Names**: _e.g. Contoso Inc_
- **Type**: _Loss / Blocked / Challenged_
- **Deal Size / Microsoft Impact**: _ACR lost/blocked, MACC, deal size_
- **Technology**: _AI Services, M&M, Database, 3P/OSS_
- **Use Cases**: _list use cases_
- **Industry**: _industry name_
- **Compete**: _AWS, GCP, etc._
- **Description**: _3-4 sentences: situation, why we lost/blocked, tech blockers, execution challenges, compete details_
- **Learnings**: _what peers can use for future opportunities_
- **Additional Info**: _IP, architecture, pricing details_

### Customer Escalation

> Top 2-3 largest escalations SLT needs to know about. Not for UAT/tech blockers.

- **Customer Name**: _name or business impact_
- **Impact to MS**: _quantify in $$: ACR loss, deal at risk, compete risk_
- **MS Exec Sponsor**: _e.g. Zia, Judson, Area LT_
- **Compete Involved**: _competitor name if applicable_
- **Description**: _customer situation, context, how we got here_
- **Impact if Not Resolved**: _$$ impact, deadline_
- **Ask**: _ideal resolution or recommendation_

### Compete Signal

- **Competitor Name**: _name_
- **Signal Type**: _New Entry / Pricing Change / Feature Difference / Strategy Shift / Customer Feedback_
- **Description**: _what was observed and why it's significant, single or multiple customers_
- **Customer/Market Segment**: _names or segment (Digital Native, Industry)_
- **Potential Impact / Action**: _impact to customers or Microsoft, who should act_
- **Additional Info / Recommendation**: _details_

### Product Signal

- **Product/Service**: _technology, product, or service name_
- **Signal Type**: _Feature Request / Bug / Performance Issue / Integration / Other_
- **Source**: _Customer Feedback / Partner / Internal Testing / Market Research_
- **Description**: _context, details of feedback/observation_
- **Use Cases**: _where this is observed_
- **Competitor Comparison**: _if relevant, why competitor is better/worse_
- **Customer Examples**: _names where observed_
- **Customer/Microsoft Impact**: _how this affects customers or Microsoft_
- **Additional Details / Recommendation**: _details_

### IP / Initiative / Best Practice

- **Title**: _short title_
- **Type**: _IP / Initiative / Program / Best Practice_
- **Description**: _objectives, key activities, learnings, success metrics_
- **Customer/Segment Impacted**: _names or segments_
- **Status**: _Planning / In Progress / Completed / Paused_
- **Next Steps**: _what's next_
- **Area/OU**: _where this is observed_
- **Additional Details**: _recommendations_

### Skills / People Signal

- **Team/Area**: _team or area name_
- **Signal Type**: _Hiring Need / Skill Gap / Training Requirement / Resource Request_
- **Description**: _recurring asks, lack of awareness, IP/asset needs_
- **Impact**: _delivery, customer satisfaction, GBB time_
- **Proposed Solution**: _recommended approach_
- **Timeline**: _Immediate / This Quarter / Next Quarter / Long-term_
