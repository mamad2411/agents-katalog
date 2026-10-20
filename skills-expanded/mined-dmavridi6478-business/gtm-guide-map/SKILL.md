---
name: gtm-guide-map
description: Index and run-order for "The GTM Guide to Claude, Fully Mapped" - 3 chapters and 40 files (37 skills + 3 templates) from who you go after (ICP, lists, signals, intent), through personalisation, qualification and discovery, to the pipeline, CRM and send layer with a weekly read. Use when the user does outbound or go-to-market work and wants the right skill for ICP-from-closed-won, list quality, signal finding, opener writing, call prep, pipeline diagnosis, reply classification or a weekly GTM report. Source @your.aimentor tree diagram (Batch 99): only the file names and one-line purposes were visible, not the skill bodies.
---

# GTM guide to Claude - mapped

The diagram shows a `gtm-guide/` folder with 3 chapters of skills that "your agent reads". Only the names and one-line purposes appear in the image; the instructions inside each skill were NOT in the upload, so this file maps and sequences them and links to what already exists here. It does not pretend to be the original skills. Closing line on the diagram: *targeting decides who. verification decides whether. the weekly read decides what changes.*

## Chapter 1 - icp-lists-signals-intent: who you go after, and who you skip

| Skill | Purpose on the diagram |
|---|---|
| icp-from-closed-won | Real buyers, not the stated ICP |
| persona-builder | The person, not the segment |
| voice-of-customer | Their words, quoted exactly |
| disqualifier-writer | Who this is not for |
| list-builder | Where the rows come from |
| icp-filter-pass | Cheapest model, every row |
| list-quality-scorecard | A to F, below B rebuild |
| account-tiering | Tiers, and the effort each gets |
| engager-scorer | Who engaged, and how warm |
| signal-finder | Dated triggers, or NONE |
| job-post-trigger | They are hiring for the pain |
| funding-trigger | New money, new budget |
| intent-scorer | Fit times intent times urgency |

## Chapter 2 - personalisation-qualification-discovery: where interest becomes a deal

| Skill | Purpose on the diagram |
|---|---|
| opener-writer | One ask, under 300 characters |
| merge-prompt-writer | Personalised at send time |
| voice-note-scripter | Spoken, not read aloud |
| message-self-check | Five of seven must pass |
| methodology-implementer | The framework, applied the same way |
| disqualification-check | Reasons to kill it, actively sought |
| committee-mapper | Everyone who can say no |
| call-prep | Prep pulled from the record |
| question-designer | Topics, never a script |
| pain-quantifier | Their arithmetic, not yours |
| objection-handler | Agree, add one fact, ask |
| next-step-closer | A date, not a follow-up |

## Chapter 3 - pipeline-crm-send-layer: which of the six is broken

| Skill | Purpose on the diagram |
|---|---|
| pipeline-diagnostic | Which stage is actually broken |
| acceptance-diagnostic | The note, or the list |
| reply-diagnostic | The message, not the list |
| win-loss-analysis | What they chose instead, and why |
| crm-hygiene | Fields that survive a handover |
| lead-source-tagger | Campaign and signal, never channel |
| follow-up-sequencer | Four touches, each a new angle |
| warm-signal-tracker | Cold rows that went warm |
| send-budget-splitter | One ceiling, split across campaigns |
| sequence-builder | Node by node, inside the cap |
| reply-classifier | Seven categories, escalates when unsure |
| account-health-check | Capped, parked, or fine |
| icp-template | The file every skill reads |
| sequence-template | The shape, before the words |
| weekly-report-template | Every metric paired with an action |

## Use what exists here

| Need | Already installed |
|---|---|
| ICP, personas, lists | `icp` command, `lead-intelligence`, `prospecting`, `niche-prospecting`, `client-research` |
| Signals and intent | `gtm-strategy`, `event-prospecting`, `linkedin-signal-outreach` |
| Openers, DMs, sequences | `cold-email`, `colddm`, `outreach-planning`, `outreach-execution`, `gtm-outbound-engine` |
| Qualification and call prep | `os-qualify` (new), `objection` command, `sales-enablement` |
| Pipeline and weekly read | `revops`, `kpi-dashboard-framework`, `os-business-analyst` |

## Guardrails (from the diagram's own rules, plus this repo's)

- Dated trigger or `NONE`; never invent a signal.
- Respect the cap: one send ceiling split across campaigns; outbound goes through the OS approval gate and consent registry (`docs/ai-os/rules/compliance-rules.md`).
- Under GDPR and PECR, cold outreach to people needs a lawful basis; B2B email rules differ by country. Check before building a list.
