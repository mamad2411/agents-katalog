---
name: fable5-outbound-5-stage-map
description: Map of the "50+ sales skills inside Fable 5" outbound folder tree (01-prospecting, 02-research, 03-outreach, 04-conversations, 05-pipeline; about 10+ skills each) to the 17-skill chain already installed as /fable5-outbound-17skills, with the 15 skill files named on the slide and what each does. Use when the user asks for that folder structure, wants the "50+ skills" system, or needs to know which outbound skills exist here. Source "50+ Sales Skills Inside Fable 5" (Batch 102).
---

# "50+ sales skills" outbound tree vs what exists here

The slide shows `~/fable5-outbound/` with five stage folders and "10+ skills" each, but it names only three files per folder (15 in all). The other 35+ files are not visible, so they are **not** reproduced here and none are invented. The slide ends with a "Comment SEND to get it now" offer, i.e. the files sit behind a social-media gate; nothing was downloaded.

| Slide folder | Named skill file | Purpose on slide | Installed equivalent |
|---|---|---|---|
| 01-prospecting | icp-definition.md | define your ideal customer | step 01 of `/fable5-outbound-17skills` (ICP Definition) |
| | target-accounts.md | find target accounts | step 02/03 (ICP Research, Account Research); `abm-gtm-layers` |
| | decision-makers.md | locate and verify decision-makers | step 05 (Contact Enrichment) |
| 02-research | account-research.md | research accounts and prospects | step 03 (Account Research); `/sales-research 1` |
| | buying-signals.md | detect buying signals | step 04 (Buying Signals); `/sales-research 9` |
| | personalization-angles.md | find relevant pain points | step 07 (Personalization); `/sales-research 4` |
| 03-outreach | cold-email.md | write high-converting emails | step 08 (Cold Email); `cold-email` skill |
| | linkedin-messages.md | create LinkedIn outreach | step 10 (LinkedIn Outreach) |
| | follow-up-sequences.md | personalised follow-ups | step 11 (Follow-Up Sequences) |
| 04-conversations | reply-classifier.md | classify and analyse replies | step 12 (Reply Classification) |
| | objection-handler.md | identify and handle objections | not in the 17; use `/objection` |
| | next-steps.md | recommend next steps | step 13-14 (Qualification, Meetings) |
| 05-pipeline | conversation-analysis.md | find where leads drop off | step 15 (Sales Pipeline) |
| | pipeline-review.md | review pipeline quality | step 16 (Weekly Report) |
| | improvement-plan.md | figure out what needs fixing | step 17 (Pipeline Optimization) |

Terminal shown on the slide: "Claude Code v2.1.90 / Fable 5.0 (high effort)" and `claude run --all-skills`. That command is not a documented Claude Code command; do not run it expecting an effect. To run the chain here use `/fable5-outbound-17skills` or `/outbound-pipeline`.

Gaps worth filling, if you want them (each would be written from scratch, not from the slide): an `objection-handler` command is covered by `/objection`; a `conversation-analysis` step needs your real reply data, which this repo does not hold.
