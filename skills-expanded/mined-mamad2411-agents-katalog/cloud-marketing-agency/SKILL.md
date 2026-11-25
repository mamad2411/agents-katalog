---
name: cloud-marketing-agency
description: Run an end-to-end sovereign marketing campaign through the 92-unit MCCO fleet (Strategy, Creative, Planning, Distribution, Measurement, Audit & Legal). Delivers Campaign Charter, research brief, positioning thesis, 30-day calendar, ~40 atoms, QA report, audit, legal temper, publish manifest, and KPI plan in one response. Use when the user has a campaign objective and wants the full agency output in 24–48 hours.
---

# Cloud Marketing Agency Skill

Operate the Coastal Key Cloud Marketing Agency — a fully-automated, sovereign-governed marketing operation running inside the Cloudflare + Airtable + Claude stack. Replaces ~19 FTE traditional agency with 92 AI units under MCCO command. Coastal Key does not hire an agency. Coastal Key operates one.

## When to Invoke

User provides a campaign request with any combination of:
- Objective (lead-gen / authority / reactivation / listing acquisition)
- Target audience segment
- Pillar asset or topic
- Budget envelope (optional)
- Launch window

If any required input is missing, request **once** with a numbered list. Do not assume.

## Operating Standards

Fortune 500 production · Red Bull Racing optimization · SpaceX engineering · Ferrari precision · IQVIA research · UiPath automation · DeviQA testing · AECON planning · Siemens engineering · David Yurman + LVMH creative · Alphabet/Deloitte/PwC/EY/KPMG audit · Alphabet risk · Cooley/Gibson Dunn/Latham & Watkins legal tempering · Coastal Key Sovereign Governance voice.

## Six Operating Divisions

**Div 1 — Strategy & Research (IQVIA).** Agents: MCCO-001 Psyche Decoder, MCCO-002 Authority Forge, MCCO-007 War Room Intel, IO-BRAVO. Endpoints: `POST /v1/mcco/audience-profile` · `POST /v1/mcco/positioning`.

**Div 2 — Creative & Production (David Yurman + LVMH).** Agents: MCCO-005 Scroll Breaker, MCCO-011 Narrative Forge, MKT copy squad (12), MKT visual squad (10). Endpoints: `POST /v1/mcco/post` · `POST /v1/social/draft` · `POST /v1/visuals/social-brief`.

**Div 3 — Planning & Orchestration (AECON).** Agents: MCCO-004 Calendar Command, MCCO-008 Campaign Blitz, MCCO-013 Timing Strike. Endpoints: `POST /v1/mcco/content-calendar` · `POST /v1/mcco/directive`.

**Div 4 — Distribution & Automation (UiPath + Siemens).** Agents: MKT paid squad (8), 20 Email AI Agents, Publish Tracker. Endpoints: `POST /v1/campaign/*` · `POST /v1/email/*` · Buffer.

**Div 5 — Measurement & Intelligence (Red Bull + Ferrari).** Agents: MCCO-012 Performance Command, IO Squad ECHO. Endpoints: `GET /api/standup` · `GET /api/dashboard`.

**Div 6 — Audit, Risk & Legal (Big Four + AmLaw 100).** Agents: MCCO-014 Quality Shield, MCCO-010 Trust Engine, IO Squad CHARLIE.

## Execution — Nine Phases (run in sequence, no pauses)

1. **Brief Intake** → Campaign Charter (≤150 words)
2. **Deep Research (IQVIA)** → Audience Brief + Competitive Gap + Decision Trigger
3. **Strategy** → Positioning Thesis (≤80 words)
4. **Planning (AECON)** → 30-day critical-path calendar
5. **Creative Production** → ~40 atoms per pillar with visual direction (invokes `content-maxxing` skill)
6. **AI Testing (DeviQA)** → QA Report per atom
7. **Audit & Legal** → Four-control audit + Temper Notes
8. **Distribution (UiPath)** → Publish Manifest (JSON) + Cron Schedule
9. **Measurement** → KPI Dashboard + Standup Input

**Total brief-to-live: 24–48 hours** (vs. 3–6 weeks traditional).

## Deliverable Format (single response)

- Campaign Charter
- Research Brief
- Positioning Thesis
- 30-day Calendar (table)
- Atomic Inventory + Final Copy (per atom)
- QA Report
- Audit + Legal Temper
- Publish Manifest (JSON)
- KPI Targets + Measurement Plan
- Risk Register
- Execution Command

## Four-Control Audit Framework

Every artifact passes before release:

1. **Factual Control** — claim traceable to repo doc or cited source
2. **Brand Control** — voice, visual, positioning compliance
3. **Legal Control** — disclosure, disclaimer, jurisdictional tempering
4. **Performance Control** — KPI defined and instrumented before publish

## Risk Register (every campaign)

- **Reputational** — MCCO-010 Trust Engine
- **Legal / regulatory** — Division 6
- **Competitive** — MCCO-007 War Room Intel
- **Operational** — IO Squad ECHO
- **Data / privacy** — IO Squad CHARLIE

Each risk: likelihood · impact · mitigation · owner · trigger · rollback.

## Legal Tempering Categories

Investment return claims · client-facing financial projections · franchise disclosure-adjacent content · securities-adjacent communications · comparative competitor claims · real estate licensure claims (Florida-specific) · any "guarantee" language.

Standard pattern: *"Projections are based on [dataset] and are not guarantees of future performance. Past results do not ensure future outcomes. Not legal, financial, or tax advice. Specific to [jurisdiction]. Consult licensed counsel."*

## Cost Comparison

| Model | Monthly Cost | Turnaround | Scale |
|---|---|---|---|
| Traditional agency retainer | $40K–$150K | 3–6 weeks | Agency headcount |
| Fractional / freelance stack | $12K–$35K | 2–4 weeks | Coordination overhead |
| In-house (19 FTE) | $180K–$250K loaded | 1–3 weeks | Headcount ceiling |
| **Coastal Key Cloud Agency** | **~$2.5K–$6K** | **24–48 hrs** | **Elastic** |

## Composition With Sister Skills

- **claude-secrets** — governs every prompt used by every agent in the fleet
- **content-maxxing** — runs inside Division 2 (Creative & Production); invoke for pillar atomization

Pattern: **Claude Secrets produces the prompt → Content Maxxing atomizes the pillar → Cloud Marketing Agency orchestrates the campaign.**

## Reference

Full architecture: `CK-CLOUD-MARKETING-AGENCY.md` (repo root).
Reference reel: Instagram DWVD4R1iFRb by @theaisurfer.
Commander: MCCO-008 Campaign Blitz.
Fleet: 92 units (15 MCCO + 47 MKT + 20 Email + 10 IO-ECHO).
