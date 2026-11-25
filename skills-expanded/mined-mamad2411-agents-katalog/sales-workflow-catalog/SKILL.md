---
name: sales-workflow-catalog
description: A catalog of 100 named n8n sales-funnel workflows, organised into the 10 funnel stages they cover (prospecting, outreach, qualification, deal execution, CS handoff, account growth, inbound/demand capture, seller enablement, ops hygiene, reporting/meta) — each with a one-line job, a node-sequence sketch, and a build-priority tier. Use when the user asks "what should I automate in sales/RevOps", wants to look up or build one named workflow from the catalog, or is deciding what to build first across a sales funnel. Complements `gtm-outbound-engine` (the top-of-funnel data layers in depth) and `ai-automation-blueprints` (8 fully detailed cross-functional automations); this skill is breadth across the whole funnel, not depth on any one workflow until you ask for it.
---

# Sales Workflow Catalog (100 workflows · 10 stages)

Source: uploaded infographic "The Complete Claude + n8n Sales System — 100
workflows for the entire sales funnel." **[Certain]** all 100 names and
their grid position are transcribed from the image. **[Guessing]** the
one-line job, node sketch and tier for each: the source graphic gives
names only, no descriptions — everything past the name is built here to
make the catalog usable, not copied from anywhere.

This is a lead-magnet graphic ("Comment 'SALES' for free access") — you
have the table of contents, not a vendor's build. Nothing here should be
treated as tested or benchmarked until you build and run it.

## How to use this

1. Find the workflow by name or number below.
2. Run `/sales-workflow [number or name]` for a build sheet (trigger, node map, credentials, prompt if it needs one, and what it hands off to).
3. Workflows marked **[data]** need a real export (CRM, ad platform, calendar) — never let the model invent that data.
4. Workflows marked **[send]** touch a customer or prospect directly — route through a human-approval gate (`outbound-campaign-brief`, or gate G1 in `governed-marketing-team`) before going live.

## Build order (by stage, not by number)

Build stages in this order. A later stage automated on top of a broken earlier one just automates the chaos faster (same rule as `operational-excellence-layers`).

1. **09 — Ops hygiene** (81–90): if your CRM data is dirty, everything downstream lies to you.
2. **02 — Outreach** (11–20) and **03 — Qualification** (21–30): where most solo/small teams actually bleed time.
3. **04 — Deal execution** (31–40) and **10 — Reporting** (91–100): visibility before you scale volume.
4. **01 — Prospecting** (01–10): only once outreach/qualification can absorb more volume.
5. **05–08**: CS handoff, account growth, inbound, enablement — once the core funnel runs clean.

## The 10 stages

### 01 · Prospecting & research (01–10)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 01 | Lead Scraper **[data]** | Pull raw prospect lists from a source (Apollo/Apify/LinkedIn export) | Schedule → Scraper API → dedupe → CRM staging |
| 02 | Enrich Leads **[data]** | Waterfall-enrich raw leads to verified contact + firmographic data | CRM staging → enrichment API(s) → merge → CRM |
| 03 | ICP Research | Score/derive ICP fit from closed-won patterns | CRM export → LLM scoring (see `gtm-outbound-engine` rubric) → tag |
| 04 | Signal Monitor | Watch for hiring/funding/tech-change triggers | Schedule → signal API/RSS → filter → notify |
| 05 | Company Intel | One-page account brief before outreach | Trigger → web/news search → LLM summarise → CRM note |
| 06 | Buyer Persona | Draft a persona from won-deal patterns | CRM export → LLM → persona doc |
| 07 | Email Finder **[data]** | Resolve verified email from name + domain | Contact row → finder API → validate → CRM |
| 08 | LinkedIn Outreach **[send]** | Connection request + first message sequence | Prospect list → LinkedIn API/Expandi → human approval → send |
| 09 | Personalise Emails **[send]** | Insert one real, sourced personal line per email | Contact + signal → LLM (cite the signal) → draft |
| 10 | Multi-Channel Sequencer **[send]** | Coordinate email + LinkedIn + call touches on one timeline | Sequence config → branch by channel → log to CRM |

### 02 · Outreach execution (11–20)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 11 | Follow-Up Automation **[send]** | Auto-advance sequence steps on no-reply | Timer → check reply status → send next step or stop |
| 12 | Reply Triage | Classify inbound replies (interested/OOO/not-now/negative) | Inbox webhook → LLM classify → route |
| 13 | Lead Scoring **[data]** | Score inbound/outbound leads against ICP + engagement | CRM trigger → scoring rules/LLM → update field |
| 14 | Qualification Flow | Route a scored lead to the right next step | Score → branch → book meeting / nurture / disqualify |
| 15 | Discovery Prep | Auto-build a discovery-call brief | Meeting booked → CRM + web pull → LLM brief → send to rep |
| 16 | Meeting Booker | Self-serve scheduling with routing rules | Link/form → calendar API (round-robin) → confirm |
| 17 | Meeting Reminders **[send]** | Reminder sequence pre-meeting | Calendar event → timer → email/SMS |
| 18 | Call Notes Summary | Turn a call recording/transcript into structured notes | Recording webhook (tl;dv-style) → LLM summarise → CRM |
| 19 | BANT Scoring | Score a call against Budget/Authority/Need/Timeline | Call notes → LLM extract → score → CRM field |
| 20 | MEDDIC Analysis | Score a deal against MEDDIC (see `sales-enablement`) | Deal notes → LLM extract → gap list → CRM |

### 03 · Qualification & deal-building (21–30)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 21 | Research Account | Deeper account research once qualified | Deal opened → web/news/10-K pull → LLM brief |
| 22 | Stakeholder Mapping | Map buying-committee roles from CRM contacts | Contacts on deal → LLM classify role → org chart doc |
| 23 | Pain Point Finder | Extract stated pains from notes/transcripts | Notes → LLM extract → tag on deal |
| 24 | Value Prop Generator | Draft a value prop mapped to the stated pain | Pains + offer spec (`claude-marketing-jobs`) → LLM draft |
| 25 | Objection Handler | Draft responses to logged objections | Objection text → LLM (grounded in proof.md) → response |
| 26 | Competitor Intel | Pull what's known about the competitor on this deal | Deal field → web search → LLM brief |
| 27 | Case Study Finder | Match the best case study to this account's profile | Account profile → case-study index → LLM match |
| 28 | ROI Calculator | Build a numeric ROI case from account inputs | Account numbers (real, not invented) → calc → doc |
| 29 | Proposal Drafter | Draft a proposal from deal + template | Deal data + template → LLM/`insight-to-deck-flow` → draft |
| 30 | Quote Generator **[data]** | Generate a priced quote from a pricing table | Deal config → pricing rules → PDF/doc |

### 04 · Deal execution & forecasting (31–40)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 31 | Proposal Follow-up **[send]** | Nudge sequence after a proposal is sent | Proposal sent → timer → email if no view/reply |
| 32 | Redline Summary | Summarise contract redlines for the rep | Redlined doc → LLM diff-summarise → CRM note |
| 33 | Contract Tracker | Track contract status through approval | Doc status webhook → CRM stage update |
| 34 | E-Signature Flow | Trigger and track e-signature | Approved contract → DocuSign/Adobe Sign API → track |
| 35 | Deal Stage Updates | Keep CRM stage in sync with real activity | Activity trigger → rule → CRM stage |
| 36 | Pipeline Alerts | Notify on stage stalls / risk flags | Schedule → CRM query → Slack/email alert |
| 37 | Stalled Deal Finder **[data]** | List deals with no activity past a threshold | CRM query → filter by last-activity date → report |
| 38 | Win/Loss Analysis **[data]** | Structured win/loss reasons from closed deals | Closed deals → LLM extract reason categories → report |
| 39 | Forecasting **[data]** | Roll up weighted pipeline into a forecast | CRM export → weight by stage → aggregate → report |
| 40 | Revenue Reporting **[data]** | Standard revenue report for leadership | CRM/finance export → aggregate → `business-intelligence-report` |

### 05 · CS handoff & onboarding (41–50)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 41 | Handoff to CS | Structured handoff packet on close-won | Deal closed → compile notes/context → CS tool/CRM |
| 42 | Onboarding Tasks | Auto-create the onboarding checklist | Handoff → template → task tool (`clickup`/Notion) |
| 43 | Customer Welcome **[send]** | Welcome sequence to the new customer | Close-won → email/CRM sequence |
| 44 | Kickoff Scheduler | Book the kickoff call | Onboarding start → calendar API |
| 45 | Onboarding Tracker | Track onboarding milestone completion | Task tool webhook → CRM/dashboard update |
| 46 | Usage Monitoring **[data]** | Pull product-usage data per account | Product analytics API → CRM field |
| 47 | Renewal Reminders **[send]** | Reminder sequence before renewal date | Contract end date → timer → email/task |
| 48 | Expansion Opportunities **[data]** | Flag accounts showing expansion signals | Usage + CRM data → rule/LLM → flag |
| 49 | Churn Risk Detection **[data]** | Flag accounts showing churn signals | Usage + support data → rule/LLM → flag → alert CS |
| 50 | NPS Collection **[send]** | Send and collect NPS surveys | Trigger (time/event) → survey tool → CRM |

### 06 · Account growth & retention (51–60)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 51 | Review Analysis **[data]** | Theme customer reviews/tickets | Review export → LLM cluster → report (`customer-feedback-themes`) |
| 52 | Feature Requests | Log and tag feature requests | Support/CS input → LLM tag → product backlog tool |
| 53 | Upsell Triggers **[data]** | Flag accounts matching upsell criteria | Usage/CRM rule → flag → notify AE |
| 54 | Account Health Score **[data]** | Composite health score per account | Usage + support + NPS → weighted score → CRM |
| 55 | QBR Preparation | Auto-build a QBR deck | Account data → `insight-to-deck-flow` |
| 56 | Executive Summary | One-page exec summary per account | Account data → LLM → doc |
| 57 | Customer Check-Ins **[send]** | Scheduled check-in outreach | Timer → email/task → CRM log |
| 58 | Renewal Sequence **[send]** | Multi-touch renewal campaign | Renewal date → sequence → CRM |
| 59 | Feedback Analysis **[data]** | Aggregate feedback across sources | Multi-source export → LLM synthesise → report |
| 60 | Referral Requests **[send]** | Ask happy customers for referrals | NPS/health trigger → email → track |

### 07 · Inbound & demand capture (61–70)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 61 | Lead Ads Sync | Sync ad-platform leads into CRM | Meta/LinkedIn lead ads webhook → CRM |
| 62 | Form Handler | Route website form submissions | Form webhook → validate → CRM/router |
| 63 | Webinar Follow-Up **[send]** | Post-webinar sequence by attendance | Webinar platform export → branch → email |
| 64 | Event Leads | Import and route trade-show/event leads | CSV/scan import → enrich → CRM |
| 65 | Partner Leads | Route partner-referred leads | Partner form/API → CRM with source tag |
| 66 | Inbound Routing | Route inbound leads to the right rep/queue | Lead data → rules (territory/size) → assign |
| 67 | Demo Request Flow | Handle a demo request end to end | Form → qualify → calendar → confirm |
| 68 | Intent Detection **[data]** | Flag accounts showing buying intent (visits, content, search) | Intent data API (see `gtm-outbound-engine` signal layer) → flag |
| 69 | Lead Nurture **[send]** | Drip sequence for not-yet-ready leads | Lead status → nurture track → email |
| 70 | Re-Engagement **[send]** | Win back stalled/cold leads | Timer on inactivity → email sequence |

### 08 · Seller enablement & performance (71–80)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 71 | Sales Content Gen | Draft sales assets (one-pagers, decks) | Request → `sales-enablement` skill → draft |
| 72 | Battlecard Builder | Build a competitor battlecard | Competitor intel → template → doc |
| 73 | Competitor Monitor | Watch competitor moves | Schedule → web/news search → digest |
| 74 | Market News Alerts | Alert reps to relevant market news per account | News feed → filter by account list → notify |
| 75 | Training Updates | Push new enablement content to reps | New asset → notify (Slack) |
| 76 | Coaching Feedback | Summarise call coaching notes | Call recording/notes → LLM → feedback doc |
| 77 | Activity Tracker **[data]** | Roll up rep activity metrics | CRM export → aggregate → dashboard |
| 78 | Quota Tracking **[data]** | Track attainment vs quota | CRM/finance export → calc → dashboard |
| 79 | Leaderboards **[data]** | Rep leaderboard by chosen metric | Activity data → rank → post (Slack) |
| 80 | Weekly Reports **[data]** | Standard weekly sales report | CRM export → aggregate → `business-intelligence-report` |

### 09 · Ops hygiene (81–90)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 81 | Slack Notifications | Route key events to Slack | Any trigger → format → Slack webhook |
| 82 | Gmail Integration | Sync email activity to CRM | Gmail webhook → parse → CRM log |
| 83 | Calendar Management | Sync/manage rep calendars | Calendar API → rules → update |
| 84 | Task Creation | Auto-create follow-up tasks from triggers | Event → rule → task tool |
| 85 | Data Cleanup | Standardise and clean CRM fields | Schedule → `clean_leads.py`-style rules → CRM update |
| 86 | Duplicate Finder | Find and flag/merge duplicate records | CRM export → fuzzy match → flag/merge |
| 87 | Error Handling | Central error-catch and alert for other workflows | Workflow error trigger → log → alert |
| 88 | Auto Tagging | Tag records by rule or LLM classification | Record trigger → rule/LLM → tag field |
| 89 | Data Enrichment **[data]** | General-purpose enrichment step reused across flows | Record → enrichment API → merge |
| 90 | Google Sheets Sync | Two-way sync between CRM and a working sheet | CRM/Sheets trigger → map fields → sync |

### 10 · Reporting, monitoring & meta (91–100)
| # | Workflow | Job | Node sketch |
|---|---|---|---|
| 91 | Workflow Monitor | Watch that other workflows are actually running | Schedule → check last-run timestamps → alert on silence |
| 92 | Run Reports | Scheduled report generation and delivery | Schedule → aggregate → email/Slack |
| 93 | Alert on Issues | Central alerting for anomalies across workflows | Any workflow → threshold check → alert |
| 94 | Usage Analytics **[data]** | Track usage of the automation stack itself | Logs → aggregate → dashboard |
| 95 | System Backup | Back up workflow configs/CRM exports | Schedule → export → storage |
| 96 | Template Builder | Turn a proven workflow into a reusable template | Workflow → parameterise → save as template |
| 97 | API Connector | Generic connector for a new tool | Auth config → test call → register |
| 98 | Webhook Handler | Generic inbound webhook router | Webhook → parse → route by type |
| 99 | Custom Logic | Catch-all code step for one-off logic | Code node (JS/Python) → whatever the flow needs |
| 100 | Scale & Optimise | Review and tighten the whole stack | Audit trigger → `operational-excellence-layers` review |

## Honest limits
- 100 items is a menu. Most solo operators need 5–8 of these; most small teams need 15–20. Building all 100 before proving stage 1 (ops hygiene) works is how automation projects die.
- Every **[send]** workflow needs the same GDPR/deliverability gates as `gtm-outbound-engine`.
- The source gives no evidence this is "the complete" system — treat the name as marketing, not a claim.

## Related
`gtm-outbound-engine`, `ai-automation-blueprints`, `n8n-agent-builder`, `sales-enablement`, `customer-success-claude`, `outreach-execution`, `operational-excellence-layers`.
