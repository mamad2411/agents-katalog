---
name: signal-detection
description: >
  Detect and prioritize buying-intent signals (funding, hiring, tech changes, job changes, news)
  and map each to a concrete ColdIQ marketplace endpoint. Use when deciding which intent signals
  to track for a client, sourcing funding/hiring/acquisition/job-change signals, scoring accounts
  by signal strength, deciding outreach timing from signal freshness, or stacking signals.
  Triggers on "intent signals", "buying signals", "trigger events", "funding signal", "hiring
  signal", "job change", "tech stack change", "signal detection", "when to reach out", "signal
  stacking". Do NOT use for writing the copy that references the signal (see crawford-method /
  cold-email-copy), list scoring math (see tam-scoring), or generic search (see coldiq-search-enrich).
---

# Signal Detection

30 sales triggers across 6 categories, tiered by reliability, each mapped to the ColdIQ endpoint
that surfaces it. Blend ≥2 independent signals before high-effort plays.

Where a signal is detectable, this skill routes it to a ColdIQ marketplace endpoint; the rest stay
as research guidance.

## ColdIQ Marketplace Endpoints

| Signal | Method | Path | Credits | Endpoint ID | Notes |
|--------|--------|------|---------|-------------|-------|
| Funding events | GET | `/v1/signalbase/funding-signals` | unknown | `signalbase.funding_signals` | Series A+ / rounds |
| Acquisition / M&A | GET | `/v1/signalbase/acquisition-signals` | unknown | `signalbase.acquisition_signals` | |
| Job changes (champion moves) | GET | `/v1/signalbase/job-change-signals` | unknown | `signalbase.job_change_signals` | Role-aware |
| Hiring surge | GET | `/v1/signalbase/hiring-signals` | unknown | `signalbase.hiring_signals` | Open postings |
| Company jobs (one company) | POST | `/v1/limadata/jobs` | 2 | `limadata.jobs` | LinkedIn jobs for a page |
| Financing events (alt source) | GET | `/v1/predictleads/discover/financing_events` | 0.18 | `predictleads.discover.financing_events` | |
| Job openings (alt source) | GET | `/v1/predictleads/discover/job_openings` | 0.18 | `predictleads.discover.job_openings` | By O*NET / location |
| News events | GET | `/v1/predictleads/discover/news_events` | 0.18 | `predictleads.discover.news_events` | |
| Tech adoption / removal | GET | `/v1/predictleads/companies/{companyIdOrDomain}/technology_detections` | 0.18 | `predictleads.company.technology_detections` | |
| Buying intent (job + tech) | POST | `/v1/theirstack/companies/buying_intents` | 3 | `theirstack.companies.buying_intents` | |
| LinkedIn post engagement | POST | `/v1/limadata/posts/reactions` | 2 | `limadata.posts.reactions` | Warm-engager lists |
| News / ads (general) | POST | `/v1/serper/news` | unknown | `serper.news` | Cheap catch-all |

## Reliability tiers

- **Tier 1 — highest intent (same-day):** Series A+ funding, expansion into new market, leadership
  change in the buyer's department. Budget approved or imminent.
  → **GET** `/v1/signalbase/funding-signals` · ? cr · `signalbase.funding_signals` (unverified)
- **Tier 2 — strong (30–90d):** competitor tech adoption, partnership/acquisition, hiring surge (5+).
  → **GET** `/v1/signalbase/hiring-signals` · ? cr · `signalbase.hiring_signals` (unverified)
- **Tier 3 — moderate (nurture):** 1–3 job postings, award/recognition, product launch.
  → **GET** `/v1/predictleads/discover/job_openings` · 0.18 cr · `predictleads.discover.job_openings`
- **Tier 4 — weak (context only):** social activity, traffic spikes, general news.
  → **POST** `/v1/serper/news` · ? cr · `serper.news` (unverified)

## The 30 triggers → where to source them

- **Funding & financial:** Series A+ (`signalbase.funding_signals`), M&A
  (`signalbase.acquisition_signals`), financing events (`predictleads.discover.financing_events`).
- **Hiring & team:** new exec / champion move (`signalbase.job_change_signals`), hiring surge
  (`signalbase.hiring_signals`), SDR/BDR or dept expansion (`limadata.jobs`, `predictleads.discover.job_openings`).
- **Technology & digital:** new tech adoption / stack removal (`predictleads.company.technology_detections`),
  buying intent (`theirstack.companies.buying_intents`), running ads / launches (`serper.news`).
- **Competitive & vendor:** competitor reviews / contract expiry / comparison shopping — no native
  endpoint; use `serper.news` / `predictleads.discover.news_events` as proxies.
- **Product & business events:** geographic expansion, new office, partnership, regulatory change
  (`predictleads.discover.news_events`, `serper.news`).
- **Marketing & reputation:** LinkedIn post engagement (`limadata.posts.reactions`), PR/media mention
  (`serper.news`).

## Freshness windows (outreach timing)

Funding 90d (weeks 2–8) · Series C deployment 180d (weeks 5–12) · LinkedIn posts 30d (0–7d) ·
hiring 60d (14–30d) · new exec 90d (days 14–30) · tech change 60d (0–30d) · champion job change
30d (0–14d, fastest decay) · event attendance 21d (±7d).

## Multi-signal stacking

- **T1 + T1 = white-glove (immediate):** funding + hiring surge; new exec + tech removal;
  champion job change + ICP fit.
- **T2 + T2 = priority sequence:** hiring (1–3) + LinkedIn engagement; competitor review + your
  pricing-page visit; industry-news impact + geographic expansion.
- **T3 = templated nurture.**

## "So what?" test for copy

Every signal you reference must be: recent, connected to your offer, something they'd care that
you noticed, tied to a specific pain. Go deeper than the obvious — "hiring SDRs but no rev-ops
lead yet" beats "you're hiring SDRs". Hand off to [crawford-method](../crawford-method/SKILL.md)
for the actual opener.

## Tips

- Automate Tier 1 with same-day triggers (`/v1/limadata/watch`); batch Tier 3–4 weekly.
- Cheapest source first: `serper.news` / `predictleads.*` (0.18) before 3-credit intent calls.
- Track signal→meeting conversion, not detection volume.
