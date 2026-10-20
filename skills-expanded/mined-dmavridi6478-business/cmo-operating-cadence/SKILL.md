---
name: cmo-operating-cadence
description: A 12-routine operating rhythm for a CMO or marketing lead adapted from "The CMO's ChatGPT Playbook" (The ChatGPT Marketer) to Claude — daily inbox drafts, industry roundup and priorities; weekly report, delegation board and plan reviewer; monthly review, strategy reset and budget-vs-actuals; ad hoc brief writer, competitor scan and exec update. Gives each routine a ready prompt, the connectors it needs and its safety rule. Use when setting up a marketing leader's week, building scheduled tasks or skills for a CMO. Run via /cmo-cadence.
---

# The CMO operating cadence (12 routines)

Source: infographic "The CMO's ChatGPT Playbook" by The ChatGPT Marketer (thechatgptmarketer.com). Written for ChatGPT; the structure below is translated to Claude and its connectors. Time budgets are the author's claims (10 min daily, 30 min weekly, 1 h monthly), not measured.

## Cadence

| # | Rhythm | Routine | Type | Connectors | Safety rule |
|---|--------|---------|------|------------|-------------|
| 01 | Daily · 10 min | Inbox drafts | scheduled task | Gmail | Drafts only. Never send. |
| 02 | Daily | Industry roundup | scheduled task | web search | Cite every story with its URL |
| 03 | Daily | Daily priorities | prompt | Calendar, tasks | Max 3 priorities; name what to delegate or drop |
| 04 | Weekly · 30 min (Mon) | Weekly report | dashboard + schedule | Drive / analytics | Label data as of date; no invented numbers |
| 05 | Weekly | Delegation board | dashboard | pasted team updates | Mark "unknown owner" instead of guessing |
| 06 | Weekly | Plan reviewer | skill | none | Must list risks, gaps and three questions |
| 07 | Monthly · 1 h | Monthly review | skill | data in Drive | Plain English, one page |
| 08 | Monthly | Strategy reset | prompt | last month's results | Rank 5 experiments by impact and effort |
| 09 | Monthly | Budget vs actuals | dashboard | uploaded budget | Forecast must show its method |
| 10 | Ad hoc | Brief writer | skill | none | Goal, audience, message, deliverables, budget, deadline |
| 11 | Ad hoc | Competitor scan | prompt | web search | Facts vs inference separated |
| 12 | Ad hoc | Exec update | prompt | pasted updates | Five lines: progress, risks, asks |

## Using the cadence
- Build the three skills (06, 07, 10) once; run the rest as prompts. Prompts are in `docs/batch-99-prompts.md`.
- Scheduled tasks (01, 02, 04) cost tokens on every run — start with one, read its output for a week, then decide whether to keep it (see `claude-token-rules-22`, rule 12).
- Anything that sends, posts or spends goes through a human. This skill never sends.
