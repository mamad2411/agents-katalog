---
name: draft-response
description: Drafts professional customer-facing replies to inbound support tickets, escalations, billing issues, feature requests, security-incident updates, and bad-news communications (delays, won't-fix, outages, RCA follow-ups). Use whenever the user says "reply to this ticket", "draft a response to [customer]", "write back to [account]", "handle this escalation", "send the RCA to [customer]", or describes a customer-facing message tied to a specific support situation. Adapts tone to relationship (new vs. multi-year), severity (P1 outage vs. minor question), channel (email, in-app, status page), and language (English/Spanish for PR/LATAM customers). Defers to marketing:draft-content for broad-audience marketing, sales:draft-outreach for prospect outbound, product-management:stakeholder-update for internal updates, legal:legal-response for contractual/regulatory inquiries (subpoenas, DSARs, SOC 2 evidence packages, security questionnaires that touch contractual reps), and customer-support:customer-escalation for packaging an issue that needs eng/leadership before any customer reply goes out. The defining characteristic is "the recipient is an existing customer with a specific issue and we are sending the actual reply now."
---

# Draft Response

Drafts customer-facing replies tailored to relationship, severity, channel, and language. Built for a cybersecurity product where security-incident communications carry extra scrutiny.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Replying to a specific customer about a specific issue | Drafting marketing content for a broad audience -> `marketing:draft-content` |
| The recipient is an existing customer | The recipient is a sales prospect (not yet a customer) -> `sales:draft-outreach` |
| Tone needs apology/empathy/resolution framing | Audience is internal (board, eng, exec team) -> `product-management:stakeholder-update` |
| Operational matter (bug, billing, feature request, outage, security incident notification) | Contracts, NDAs, subpoenas, DSARs, SOC 2 evidence packages, security questionnaires with contractual reps -> `legal:legal-response` |
| You already have triage + facts and just need the reply | You still need to investigate before replying -> `customer-support:customer-research` |
| The reply can ship without engineering/leadership signoff | Issue needs eng or leadership packaging first -> `customer-support:customer-escalation` (this skill drafts the customer-facing message AFTER escalation lands) |

Hand-off chain: `ticket-triage` -> (`customer-research` if needed) -> (`customer-escalation` if needed) -> `draft-response`. If the upstream skill produced a brief, quote its facts verbatim — do not re-investigate.

### Edge-case decisions (transfer tests)

- **Security questionnaire from a customer's procurement team**: if it is a checkbox/spreadsheet exercise with no contractual reps, this skill drafts. If it asks for sub-processor lists, breach-notification SLAs, or DPA amendments -> `legal:legal-response`.
- **RCA write-up after a handled outage**: this skill drafts; cite the engineering postmortem verbatim, do not re-derive timeline.
- **Customer asks for a feature on a sales call follow-up thread**: still this skill (existing customer); flag the AE in CC.
- **Renewal-at-risk message triggered by a support thread**: this skill drafts the support-side reply; tag CSM/AE for the commercial conversation, do NOT negotiate pricing here.
- **A prospect who has a free-trial account complaining about a bug**: existing user -> this skill (not `sales:draft-outreach`).

## Tone calibration matrix

| Severity / Relationship | New (<3 mo) | Established (3 mo–2 yr) | Strategic (multi-year, regulated industry, $$$$) |
|---|---|---|---|
| **P1 outage / data loss / security incident** | Direct, action-led, named owner, status page link | Direct, action-led, exec named, dedicated channel offered, RCA promised within 5 business days | Exec call within 1 hr, written follow-up same day, RCA within 3 business days, legal:legal-response in CC if breach notification obligations may apply |
| **P2 broken workflow** | Acknowledge + ETA + workaround | Acknowledge + ETA + workaround + cadence | Same + named eng owner + Slack/Teams channel offer |
| **P3 question / how-to** | Friendly, link to docs, offer call | Direct answer, light docs link | Friendly + proactive next-step suggestion |
| **P4 feature request** | Thank + log + honest expectation | Thank + log + roadmap context + alternative | Thank + log + PM intro + roadmap-influence offer |
| **Bad news (delay, won't fix, deprecation)** | Direct, alternative offered, no over-apology | Direct, context, alternative, named accountability | Pre-call before written, exec involvement, retention angle |

### Language / locale

- Default to the language the customer wrote in. For Puerto Rico and LATAM accounts that previously corresponded in Spanish, draft in Spanish first and offer English mirror in the same thread.
- For bilingual incident comms (status page, breach notification), produce both EN and ES side-by-side; flag the ES version as "draft — confirm with native reviewer" if the stakes are legal-grade.
- Keep technical terms (SOC 2, MFA, EDR) in English even in Spanish drafts — that is industry convention.

## Structure for high-stakes responses

Use this exact frame for P1, P2, bad news, strategic accounts, and any security-incident comms:

1. **Acknowledgment** (1 sentence) — what happened, that you see it, that it matters.
2. **What we know now** (2-4 sentences) — facts only, no speculation. Include scope/blast radius if security-related.
3. **What we are doing** (bullet list with named owners and times) — not "the team is working on it."
4. **What we need from you** (if anything) — explicit ask or "nothing — we have it."
5. **When you will hear next** — specific date/time, not "soon."
6. **Apology if warranted** — direct, not over-blown. "This shouldn't have happened. We are sorry it did."

### Security-incident addendum (when category = Security or P1 with data exposure risk)

Add these elements before sending and route a copy to legal:legal-response for review:

- **Scope statement**: what data/systems were/were-not affected, with timestamps.
- **Customer-required action**: rotate keys / reset MFA / re-attest, etc. — be unambiguous.
- **Forensics status**: "investigation ongoing" vs. "contained" vs. "remediated" — pick one.
- **Notification posture**: whether this triggers contractual or regulatory notification (HIPAA, GLBA, state breach laws, GDPR) — if yes, do NOT send without legal:legal-response signoff.
- **Evidence preservation note** (internal): logs frozen, chain-of-custody owner.

For routine P3/P4: skip the frame, just answer clearly.

## Anti-patterns to avoid

- **"We apologize for any inconvenience"** — every customer hears this 50x/month. Either apologize specifically or skip it.
- **"As you know..."** — patronizing. Just say the thing.
- **"Per our last conversation..."** — defensive. If they need a recap, give one.
- **Passive voice for failures** — "An issue was experienced" -> "We had a database outage."
- **Over-promising on resolution time** — under-commit by 30%, communicate proactively if you beat it.
- **Defending the product** — when something broke, the customer doesn't want a tour of mitigating factors.
- **Speculating during an active security incident** — say "investigation ongoing" rather than guess at cause; wrong attributions become contractual problems.
- **Confirming a breach in writing before legal review** — use neutral language ("security event under investigation") until scope is confirmed.

## Output

Always produce:
1. The draft response (ready to send) — in the customer's language; bilingual side-by-side if incident-class.
2. Suggested CC list — eng manager for P1, AE for strategic accounts, legal for security/compliance, CISO if breach notification on the table.
3. Suggested follow-up cadence — next message timing.
4. Internal note (1-3 lines) — what to log in CRM/ticketing.
5. Pre-send checklist — for security/legal-touching drafts: "legal reviewed? scope confirmed? notification clock started?" (do NOT mark as ready-to-send until checked).
