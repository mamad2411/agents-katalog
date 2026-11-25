---
name: customer-research
description: Multi-source research on a specific EXISTING customer question, account, or topic — pulling from internal sources (tickets, CRM, email, Slack, prior call transcripts, docs, product analytics) and external (web, news, social, filings) with full source attribution and confidence levels. Use when the user says research [customer/account], look up [customer name], find what we know about [account], background on [customer], dig up context on [issue], check if we've seen this before, what did we tell [customer] about X, who at [customer] cares about Y, has this bug been reported, is this customer at churn risk, prep me on [existing customer] before [meeting/response/escalation], or describes wanting consolidated research with citations before drafting a response, escalation, or decision. Specializes in cybersec-customer research patterns: security-incident-related research (extra scrutiny path), compliance/SOC2 questionnaire customers, customers with cybersec teams (technical-sophistication signaling). Do NOT use for cold prospect intel (use sales:account-research), competitive intelligence on competitors (use sales:competitive-intelligence), pre-sales call prep on a prospect (use sales:call-prep), legal-relevant meeting prep with action-tracking (use legal:meeting-briefing), generic web search without customer context (just web search), or running an analysis on customer data in aggregate (use data:analyze). Defining characteristic: "research about an EXISTING customer relationship or a topic in their context, with source attribution and confidence levels, feeding a downstream action."
---

# Customer Research

Multi-source research with source attribution and confidence levels for existing customer questions. Designed to feed a downstream action: a drafted response, an escalation package, or a decision.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Researching an EXISTING customer | Researching a cold prospect → `sales:account-research` |
| Question is operational/support context | Competitive intel about a competitor → `sales:competitive-intelligence` |
| Need source attribution + confidence levels | Pre-call prep for a sales call with a prospect → `sales:call-prep` |
| Pulling from internal + external sources | Legal-relevant meeting prep + action tracking → `legal:meeting-briefing` |
| Research feeds a draft/escalation/decision | Generic web research with no customer → just use web search |
| Research is about ONE account / a few named contacts | Aggregate analysis across many customers → `data:analyze` |
| Customer-related compliance question (SOC 2 evidence request, security questionnaire) | Tracking the compliance program over time → `operations:compliance-tracking` |

If the user is about to draft a customer reply or escalate, this skill runs FIRST and chains into `customer-support:draft-response` or `customer-support:customer-escalation`. If they're triaging a brand-new ticket, `customer-support:ticket-triage` runs first and may chain INTO this skill.

## Decision tree — pick a path before starting

```
Is the question a security-incident / breach / forensics / CVE-exposure issue?
  YES → Path A (extra scrutiny — see "Cybersec-customer specializations" below)
  NO  ↓

Is the question a SOC 2 / DPA / questionnaire / compliance evidence request?
  YES → Path B (compliance routing)
  NO  ↓

Has this customer ever shown technical sophistication (CISO, security team, red team)?
  YES → Path C (use technical depth; pull transcripts not summaries)
  NO  → Standard path
```

## Research depth tiers — match effort to decision stakes

| Tier | Time budget | When | Output |
|---|---|---|---|
| **Quick lookup** | <5 min | Single fact, low-stakes ("what plan are they on?") | 1-3 bullets, sources only — no full template |
| **Standard** | 15-30 min | Drafting a response, prepping for a routine call | Full template, internal sources, light external |
| **Deep package** | 1-2 hr | Escalation to leadership, churn intervention, security incident | Full template + cross-checks + external + Path A/B/C steps |

Pick the tier explicitly at the top of the output. Over-researching simple questions is the most common failure mode after under-attribution.

## Research scope — internal sources (priority order)

Walk top-down. Stop when the question is answered with sufficient confidence; note what you skipped.

1. **Open and recent tickets** for this customer (Zendesk/Intercom/Freshdesk) — last 90 days default; expand if pattern suggests longer history
2. **CRM record** (HubSpot/Salesforce) — account history, contract status, ARR, health score, named contacts, recent owner notes
3. **Email correspondence** (Gmail/Outlook) — last 60 days threads with @customer-domain; older if topic-specific
4. **Slack/internal chat** — `#cs-<customer>` channels, mentions of customer name in last 30 days
5. **Doc storage** (Box/Drive/SharePoint) — case studies, signed contracts, custom integrations, security questionnaires they sent
6. **Engineering tickets** (Linear/Jira/GitHub) — known bugs labeled with their account, feature requests filed on their behalf
7. **Product analytics** (Amplitude/Pendo/Mixpanel) — usage patterns, feature adoption, error rates, login frequency trend
8. **Prior call recordings/transcripts** (Gong/Fireflies/Chorus) — what they actually said in past calls, with timestamps
9. **KB articles** — content created from their issues (sometimes the answer to "have we seen this before" is an article)
10. **Status page incident history** — outages that affected their region/feature

### Recency rules (default staleness thresholds)

| Source | Stale after | Override when... |
|---|---|---|
| Tickets | 90 days | Pattern recurs → pull full history |
| CRM health/ARR | 30 days | Renewal in <90 days → pull current snapshot regardless |
| Email | 60 days | Specific commitment search → no time limit |
| Slack | 30 days | Incident context → expand to whenever incident started |
| Product analytics | 14 days | Trend question → 90-day rolling |
| Call transcripts | No limit (search by topic) | Always include relevant matches |

If a source is stale beyond threshold and you cite it anyway, label it `[STALE: source from YYYY-MM-DD, X days old]`.

## Research scope — external sources

1. Their public website (changes, recent posts, careers page if org-change question)
2. Recent news mentions (acquisitions, leadership changes, funding, layoffs, breach disclosures)
3. Social signals (LinkedIn posts from named contacts; X/Mastodon if cybersec audience)
4. Public filings (10-K/10-Q, S-1) — only if public company AND material to question
5. Industry/regulatory context (SEC filings of breach, FTC actions, sector-specific rules — NIS2, DORA, HIPAA changes, etc.)
6. Threat intel feeds (only for security-incident research path — see below)

External research is ADDITIONAL to internal, not a substitute. If internal already answers it, don't add external noise — just note "no external check needed because [reason]."

## Attribution standards

Every fact gets a source citation AND a confidence level.

**Confidence levels:**
- `[Confirmed]` — sourced from authoritative internal record (ticket, signed contract, CRM-of-record field)
- `[Likely]` — sourced from a reasonable secondary source (email summary, Slack mention, prior call transcript paraphrase) — facts that are probably true but worth verifying before acting
- `[Unconfirmed]` — sourced from external/social/inferred — useful context, not actionable on its own

**Format:**
```
The customer reported login failures on 2026-04-22. [Confirmed]
[Source: Zendesk ticket #4521, opened 2026-04-22 14:30 UTC]

They are renewing in Q3 at $X ARR. [Confirmed]
[Source: HubSpot opportunity #98765, last updated 2026-04-15]

Their CISO appears to be transitioning out — replacement search underway. [Unconfirmed]
[Source: LinkedIn post by Jane Doe, 2026-04-19; their careers page lists "VP Security" as of 2026-04-20]

The customer was told in March that the SSO bug fix would ship in Q2. [Likely]
[Source: Fireflies transcript 2026-03-12 — paraphrase, not verbatim quote]
```

No floating claims. No "the customer probably..." without `[Unconfirmed]` and a source. If sources conflict, surface both with a `[CONFLICTING SOURCES]` flag and recommend who to ask to resolve.

## Output structure

```markdown
# Research: [Customer Name] — [Question/Topic]

## Question
[Restate the question being researched, with the downstream action it feeds]

## TL;DR (3-5 bullets, ranked by impact on the next action)
Each bullet: [finding] [Confidence] [Source] — and ★ marks the finding that most changes the recommended next action.
- ★ [Highest-impact finding for the decision] [Confirmed] [Source: ...]
- [Next finding] [Confidence] [Source: ...]
- ...

## Customer snapshot
- Account size: [ARR, contract end date]
- Tier / segment: [Enterprise / Mid-Market / SMB / Strategic]
- Health: [score / R-Y-G / churn risk indicators]
- Named contacts: [primary + role + last contact date + tenure]
- Technical sophistication: [High / Medium / Low — based on past interactions; CISO/security team present?]
- Sensitivity flags: [PII handler? Regulated industry? Active security incident? Prior breach disclosure?]

## Findings (organized by question facet)

### [Facet 1]
- [Finding] [Confidence] [Source]
- [Finding] [Confidence] [Source]

### [Facet 2]
- ...

## Open questions / gaps
- [Things research couldn't answer]
- [Recommended owner to ask or data to pull]

## Conflicting sources (if any)
- [Source A says X; Source B says Y; recommend [resolution path]]

## Suggested next action
[Specific next step with skill chain — e.g., "Draft response (chain → customer-support:draft-response)" or "Escalate to AE (chain → customer-support:customer-escalation)"]

## Sources consulted (full list with timestamps)
- [Source 1: type, ID, retrieved YYYY-MM-DD HH:MM]
- [Source 2: ...]
- [Sources skipped and why: ...]
```

## Cybersec-customer specializations

### Path A: Security-incident-related research (EXTRA SCRUTINY)

Trigger: customer reports a suspected breach, asks about exposure to a known CVE in your product, sends a forensics request, or filed a security ticket marked sensitive.

Extra steps:
1. **Confirm scope of disclosure first** — what has the customer ALREADY been told vs. what's still internal-only? Cross-check with legal/IR lead before assembling research package.
2. **PII/log handling** — if research involves customer log data, redact or reference IDs only; do not paste raw logs into the research output.
3. **Chain of custody note** — for any artifact you reference (log line, email, ticket), include exact source ID + timestamp so the artifact can be re-pulled in evidence-grade form later.
4. **Sibling skill chain** — research feeds `operations:runbook` (incident response procedure) AND `legal:legal-response` (templated breach comms) AND `customer-support:customer-escalation`. Don't try to draft the comms here.
5. **Confidence bar is higher** — only `[Confirmed]` facts go into the TL;DR for security-incident research. `[Likely]` and `[Unconfirmed]` go in a separate "investigative leads" section.

### Path B: Compliance / questionnaire customer (SOC 2 / ISO / PR Ley 111-2005 / HIPAA BAA / DORA)

Trigger: customer sent a security questionnaire, asked for SOC 2 report, requested DPA, asked about Puerto Rico breach notification timing, or wants evidence for their own audit.

Steps:
1. Pull prior questionnaire responses for this customer (or similar customers — note differences).
2. Check `operations:compliance-tracking` for current state of relevant controls before answering.
3. Flag any question that requires a NEW commitment (vs. restating existing posture) — those need legal/security review, not just research.
4. Sibling chain: research → `legal:legal-response` (if templated) OR `operations:compliance-tracking` (if program update needed).

### Path C: Cybersec-team customer (technical sophistication HIGH)

If past interactions show the customer has a CISO/security team/red team:
- Note technical sophistication = High in snapshot
- Findings can use technical terminology without translation
- Past calls likely contain technical depth — pull transcripts, not just summaries
- Their questions often have a "we already tried X" subtext — search for prior interactions on the same topic

## Common research scenarios

### "Has this bug been reported before?"
- Zendesk/Intercom: similar ticket search across all customers (not just this one)
- Linear/Jira: known bugs + status
- Slack engineering channels for discussion
- Status page history
- KB for known-issue article

### "What's the relationship history with this account?"
- CRM timeline (deals, renewals, expansions, churn signals)
- Email correspondence summary by quarter
- Past escalations and their resolution
- Past commitments (features promised, SLAs given) — flag these as `[Confirmed if from contract], [Likely if from email/call]`

### "What was previously told to this customer about [topic]?"
- Email search for the topic
- Past ticket responses (especially escalations)
- Prior call notes/transcripts
- Account notes in CRM
- Contract/SOW for explicit commitments
- Surface VERBATIM quote when possible; flag paraphrases as `[Likely]`

### "Is this customer at churn risk?"
- Health score trend (last 90 days)
- Recent ticket volume + sentiment
- Login frequency / usage decline
- Known org changes (sponsor leaving — LinkedIn check)
- Renewal timing
- Competitive mentions in tickets/calls

### "Who at this customer cares about [topic/feature]?"
- Email correspondence on the topic
- Past meeting attendees who raised it
- LinkedIn role-search at the company
- CRM contact list filtered by interest tag

### "What's their current security posture / what did they ask in the questionnaire?"
- Pull last questionnaire from doc storage
- Pull DPA + any side letters
- Cross-reference with current product state
- Note gaps vs. their stated requirements

## Anti-patterns

- **Research without attribution** — claims become rumors
- **Research without confidence levels** — "the customer is at churn risk" with no signal-strength indicator misleads decisions
- **Internal-only when external context matters** — missing news (acquisition, breach, layoffs) shapes the response
- **External-only when internal exists** — ignoring tickets that already answered the question
- **Speculation framed as finding** — "they're probably going to churn" needs evidence or `[Unconfirmed]` label
- **Stopping at first answer** — the first source may be incomplete; cross-check at least one other for high-stakes findings
- **Over-researching simple questions** — match depth to decision stakes (a routine "what plan are they on" doesn't need 10 sources)
- **Pasting raw PII/logs into output** — reference IDs, redact when in doubt, especially for security-incident path
- **Skipping the downstream chain** — research that doesn't end with a recommended next action and skill chain leaves the user stranded
- **Treating cybersec-team customers like generalists** — under-technical answers waste their time and signal you don't get them

## Output

Produces:
1. Structured research above with full attribution + confidence levels
2. Suggested next action with skill chain (almost always `customer-support:draft-response`, `customer-support:customer-escalation`, `legal:legal-response`, or `operations:runbook` for IR)
3. Open questions / gaps with recommended owner
4. Conflicting-sources flag if encountered
5. Sources consulted with retrieval timestamps
6. For security-incident research: separate "investigative leads" section keeping `[Likely]`/`[Unconfirmed]` items out of TL;DR
