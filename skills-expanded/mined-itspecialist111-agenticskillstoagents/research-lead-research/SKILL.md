# research/lead-research — skill payload

> Machine-readable contract: [`../lead-research.manifest.json`](../lead-research.manifest.json).

## What this skill does

Builds a structured sales-lead dossier from a company name (and
optionally a contact). Aggregates:

- Public company profile: HQ, size, sector.
- Funding history (rounds, lead investors, amounts).
- Recent news (last 90 days).
- Technology fingerprint (visible stack signals).
- Decision-maker pointers (named contact's role, LinkedIn URL).

Every field is sourced; the dossier carries citations so a sales rep can
verify before reaching out.

## When to use it

- A rep is preparing for a discovery call and needs context fast.
- An SDR wants to prioritise a list of leads by recent funding or news.

## When **not** to use it

- The target is a private individual (consumer) — out of scope; privacy
  risk.
- The data is going into automated outreach without human review —
  combine with a human send-step or do not use.

## Determinism and risk

Determinism: **low** — depends on what the web returns today. Risk:
**medium** — wrong dossier means a bad-fit pitch. Citations are the
mitigation.

## How it composes

Often paired with `research/competitive-ads-extract` (what messaging is
the competitor running?) and `comms/meeting-insights` (post-call notes
back into CRM).
