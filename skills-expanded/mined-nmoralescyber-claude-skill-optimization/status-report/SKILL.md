---
name: status-report
description: Generate a multi-audience status report (exec, board, team, investor) with green/yellow/red status criteria, named risks, decisions needed, and a 5-minute scannable layout. Use this skill when the user says write a weekly/monthly/quarterly status report, summarize project or program health for leadership, build a board update, draft an investor update, produce a cross-functional status, turn tracker activity into a narrative, or asks for a "state of the program" summary. Specializes in cybersecurity-startup status reporting (security incidents, compliance program status, customer-trust events) and bilingual (Spanish/English) Puerto Rico stakeholder context. Do NOT use for product-specific stakeholder updates (use product-management:stakeholder-update), legal-meeting briefings (use legal:meeting-briefing), personal daily recap or morning brief (use personal-assistant), runbook procedures (use operations:runbook), or compliance program tracking dashboards (use operations:compliance-tracking).
argument-hint: "[weekly | monthly | quarterly | board | investor] [audience: exec | board | team | investor] [project or program]"
---

# Status Report

Produces a status report calibrated to audience and cadence, with explicit green/yellow/red criteria, named risks, and surfaced decisions. Optimized so a busy reader can grasp state in 5 minutes or less.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Weekly/monthly/quarterly cross-functional or program status | Product-launch or feature-progress update for one product → `product-management:stakeholder-update` |
| Board update, investor update, exec roll-up | Daily personal recap, morning briefing, end-of-day → `personal-assistant` |
| Security-incident summary for board, customer-trust event report | Templated outbound legal reply (DSAR, hold notice) → `legal:legal-response` |
| Compliance program health for execs (SOC 2 status, audit readiness) | Operational evidence-collection tracking, control-by-control → `operations:compliance-tracking` |
| Pre-meeting status briefing for stakeholders | Legal meeting prep with case context and action tracking → `legal:meeting-briefing` |
| Procedure-execution log for an on-call task | Documenting the procedure itself → `operations:runbook` |

If the request is genuinely product-only ("update on Feature X launch") delegate to `product-management:stakeholder-update`. If it spans security + compliance + customer + roadmap, this skill is correct.

## Core principles

1. **Headline first, detail later.** Top 3 lines must convey: overall status color, the one thing on fire, the one decision needed. If a board member reads only the headline they should still make the right call.

2. **Green/yellow/red has criteria, not vibes.** Every status color must reference a measurable threshold. "Yellow because we slipped one milestone" is OK. "Yellow because it feels off" is not.

3. **Audience-calibrated.** Same underlying facts, different framing for exec vs. board vs. team vs. investor. This skill produces the right framing per audience — never one report shoehorned into all four.

4. **Risks named with owners and dates.** A risk without an owner is a wish. A risk without a mitigation date is theater.

5. **Decisions surfaced, not buried.** If the reader needs to decide something, it goes in its own section with: context, options, recommendation, deadline.

6. **5-minute scannable.** Total length: 1 page for weekly, 2 pages for monthly, 3 pages for quarterly/board. If it's longer, it's a memo, not a status report.

## Status color criteria (apply consistently)

| Color | Meaning | Trigger |
|---|---|---|
| Green | On track | All key metrics within target band; no unmitigated high-severity risks; milestones on schedule |
| Yellow | At risk | At least one metric off-target but recoverable; OR one milestone slipped <2 weeks; OR one medium-severity risk lacks mitigation owner |
| Red | Off track | Multiple metrics off-target; OR milestone slipped >2 weeks with no recovery plan; OR open high/critical-severity risk; OR a customer-trust event in flight |

State the trigger in the report. "Yellow — Q2 ARR pacing 8% under plan, recovery plan due May 5" is useful. "Yellow" alone is not.

## Audience variants

The same underlying facts get reframed per audience. Always ask which audience(s) are needed; produce multiple variants in one call if requested.

### Exec (CEO, leadership team — weekly default)
- Length: 1 page
- Tone: direct, candid, decision-oriented
- Includes: headline color, top 3 wins, top 3 risks with owners, decisions needed THIS WEEK, top 3 next-period priorities
- Omits: granular task lists, internal team gossip

### Board (quarterly default; ad hoc for security incidents)
- Length: 2-3 pages + appendix
- Tone: strategic, governance-oriented, fiduciary-aware
- Includes: company-level KPIs vs. plan, material risks, regulatory/legal status, security/compliance posture, capital/runway, asks of the board
- Cybersec board content (the operator's context):
  - Security incidents (any P1/P2 in period; near-misses worth flagging)
  - Compliance program status (SOC 2 readiness %, ISO 27001 progress, PR-specific: DACO/OCIF posture)
  - Customer-trust events (notable customer security questionnaires, audit findings, breach exposure)
  - Insurance posture (cyber policy renewal, coverage limits)

### Team (weekly default)
- Length: 1 page
- Tone: collaborative, action-oriented, shoutout-friendly
- Includes: team-level wins, blockers needing peer help, next-week commitments, kudos
- Omits: financial detail, board-only content

### Investor (monthly default)
- Length: 2 pages
- Tone: confident but candid; metrics-driven; no surprises
- Includes: top funnel and revenue metrics, runway, asks (intros, hires, customer warm leads), product highlights, security/trust differentiator
- Cybersec startup investor content (the operator's context):
  - Security-specific KPIs: customers passing security review on first attempt, time-to-SOC-2, mean time to remediate (MTTR) for vulns, security incidents in period
  - Customer-trust as growth lever: enterprise deals unblocked by SOC 2, security-questionnaire turnaround time
  - Threat landscape commentary if material to product/market

## Standard output anatomy

```markdown
# Status Report: [Program/Team] — [Period]
**Author:** [Name] | **Date:** [Date] | **Audience:** [Exec | Board | Team | Investor]

## Headline
**Status: [Green | Yellow | Red]** — [one-sentence reason citing the trigger criterion]
**The one thing on fire:** [what + owner + by-when]
**The one decision needed:** [what + by-when]

## Key Metrics
| Metric | Target | Actual | Trend | Status | Why |
|---|---|---|---|---|---|
| [KPI] | [Target] | [Actual] | [up/down/flat vs. last period] | G/Y/R | [1-line rationale] |

## Wins This Period (max 5)
- [Win — with measurable impact, not "we shipped a thing"]

## Risks (named, owned, dated)
| Risk | Severity | Owner | Mitigation | Mitigation due |
|---|---|---|---|---|
| [Specific risk] | Critical/High/Med/Low | [Person] | [Action being taken] | [Date] |

## Decisions Needed
| Decision | Context | Options | Recommendation | Decide by |
|---|---|---|---|---|
| [Question] | [Why it matters now] | [A vs. B vs. C] | [What I'd choose + why] | [Date] |

## Next Period Priorities (max 3)
1. [Priority — with owner and success criterion]
2. ...
3. ...

## Appendix (board/investor only — link or attach, don't inline)
- Detailed metrics tables
- Incident reports
- Compliance evidence summaries
- Financial detail
```

Audience-specific sections (apply per variant):

- **Board:** add `## Compliance & Security Posture`, `## Material Legal/Regulatory`, `## Capital & Runway`, `## Asks of the Board`.
- **Investor:** add `## Funnel & Revenue`, `## Runway & Burn`, `## Asks` (intros, hires, customer leads).
- **Team:** add `## Blockers Needing Peer Help`, `## Kudos`.

## Cybersecurity-specific content modules (the operator's context)

When the program is a cybersec startup, security org, or compliance program, include these modules where relevant:

### Security incident summary (always include in board update if any P1/P2 in period)
```
**Incidents this period:** [count by severity]
- [Date] [Severity] [1-line description] — [Status: contained/recovering/closed] — [Owner]

**MTTR (mean time to remediate):** [hours/days] — [trend vs. last period]
**Mean time to detect (MTTD):** [hours/days] — [trend]
**Notification triggered:** [Yes/No — to whom: customers, regulators (DACO/OCIF/state AG/GDPR), insurers]
```

### Compliance program status
```
| Framework | Stage | Readiness % | Audit date | Owner | Status |
|---|---|---|---|---|---|
| SOC 2 Type II | Evidence collection | 78% | 2026-08-15 | [name] | G |
| ISO 27001 | Stage 1 audit prep | 55% | 2026-Q4 | [name] | Y |
| PR DACO (consumer data) | Notification process documented | 100% | N/A | [name] | G |
| PR OCIF (financial customer data) | Procedure under review | 60% | TBD | [name] | Y |
```

### Customer-trust events
```
- Security questionnaires received: [#] | Avg turnaround: [days] | Win rate: [%]
- Notable customer audits: [list with outcome]
- Enterprise deals unblocked by compliance: [list]
```

### Bilingual considerations (PR market)
- If status report is for a PR-customer-facing audience or includes external comms drafts, produce a Spanish-language version of the headline + key facts in addition to English. Cybersec incident notifications to PR consumers should be bilingual by default.

## Brevity discipline

Hard caps to enforce:
- Weekly exec/team: 400 words max
- Monthly: 800 words max
- Quarterly/board: 1500 words max body + appendices
- Investor monthly: 800 words max

If draft exceeds caps, cut from these sections in order: appendix detail → in-progress task list → wins narrative (keep bullets) → next-period priorities (cap at 3).

A status report that needs more than 5 minutes to read failed at being a status report. It became a memo.

## Connector use (if available)

If project tracker is connected:
- Pull completed/in-progress/blocked items for the period
- Identify slippage automatically and flag for yellow/red rationale

If chat (Slack) is connected:
- Scan for decisions reached, blockers raised, customer escalations
- Offer to post the finished report to a channel after user approval

If calendar is connected:
- Reference key meetings and decisions reached
- Note upcoming decision deadlines

If GRC/compliance tool is connected:
- Pull live SOC 2/ISO control completion %
- Pull open audit findings

If incident-management tool (PagerDuty, Incident.io) is connected:
- Pull incident counts by severity, MTTR/MTTD for security section

## Anti-patterns

- **Status colors without criteria.** "Yellow because gut feel" — write the criterion or use green.
- **Risks without owners.** Every risk row must name a person. "TBD" is not a person.
- **Decisions buried in narrative.** If a decision is needed, it goes in the Decisions table, full stop.
- **Same report for all audiences.** Board doesn't need team-kudos; team doesn't need runway. Re-frame per audience.
- **Encyclopedic length.** A 4-page weekly is a confession that you don't know what matters.
- **Hidden bad news.** Surfacing risks early builds trust. Hiding them and getting found out destroys it.
- **Generic "going well" wins.** "Improved performance" is gesture. "p95 latency dropped from 800ms to 240ms" is a win.

## Validation cadence

- Re-read the prior period's status report before drafting the new one. Verify last period's predicted priorities actually got done — if not, that's a yellow signal.
- Re-validate G/Y/R criteria quarterly: are the thresholds still meaningful as the company has scaled?
- Board updates: have a peer (CFO, COO, or board observer) read before sending.

## Output checklist

Before delivering a status report, verify:
- [ ] Headline conveys color, fire, decision in 3 lines
- [ ] Every status color has a stated trigger criterion
- [ ] Every risk has owner + mitigation + date
- [ ] Every decision has options + recommendation + deadline
- [ ] Audience variant matches the requested audience (exec/board/team/investor)
- [ ] Word count under cap for cadence
- [ ] If cybersec: incident, compliance, and customer-trust modules included where applicable
- [ ] If PR-customer-facing: Spanish version of headline + key facts attached
