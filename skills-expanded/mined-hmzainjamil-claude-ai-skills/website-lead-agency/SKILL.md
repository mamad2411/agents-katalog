---
name: website-lead-agency
description: "Master revenue engine: website-builder + lead-gen-ai + HMZ daily sweeps. Find clients via 4 automated daily sweeps → build demo sites → close. 10-actor pipeline + 4 scheduled sweeps running autonomously."
allowed-tools: Read, Bash, Write, Agent
---

# Website + Lead Agency — Master Revenue Engine

## Triggers
"website lead agency" / "build and find clients" / "agency automation" / "full agency stack" / "website agency pipeline" / "lead gen website agency" / "digital agency engine" / "automated agency" / "hmz agency pipeline" / "sweep and build"

---

## WHAT THIS ORCHESTRATES

Two revenue streams + four autonomous daily pipelines:

```
STREAM 1 — Website Builder ($1,500–$8,000/site)
  One prompt → Next.js + Tailwind + Framer Motion → Vercel

STREAM 2 — Lead Generation ($500–$2,000/list)
  One prompt → 20-100 qualified leads → Excel + outreach

AUTOMATION — 4 Scheduled Daily Sweeps (running 24/7)
  hmz-daily-leads      → 7 AM PKT  → 10 elite B2B leads (score ≥80)
  hmz-bdm-morning      → 9 AM PKT  → 10-platform job sweep (score ≥65)
  hmz-bdm-evening      → 9 PM PKT  → 10-platform job sweep + Reddit drafts
  hmz-indeed-mcp       → on-demand → Indeed MCP structured job search
```

---

## PHASE 1 — FIND CLIENTS (4 Lead Gen Sources)

### Source A — Automated Daily Sweeps (already running)

| Sweep | Time | Lead Type | Threshold |
|---|---|---|---|
| `hmz-daily-leads` | 7 AM PKT | B2B ad buyers (Apollo + Vibe + Apify + WebSearch) | ≥80 score |
| `hmz-bdm-morning-sweep` | 9 AM PKT | Job board leads (10 platforms) | ≥65 score |
| `hmz-bdm-evening-sweep` | 9 PM PKT | Job board leads + Reddit signals | ≥65 score |
| `hmz-indeed-mcp-sweep` | on-demand | Indeed MCP structured search | ≥65 score |

All leads land in: `~/Downloads/Leads/HMZ-Leads-Daily.xlsx` (appended daily, never wiped)

State tracking: `python3 /Users/mc/.claude/bin/hmz-bdm-state-update [sweep-name]`

### Source B — Vibe Prospecting MCP (on-demand for any niche)

```
Actor 1 — Brief Generator (Kimi 8K)       → extract niche + location + fields
Actor 2 — Vibe Prospecting (MCP)           → fetch-entities + fetch-businesses-events + enrich-prospects
Actor 3 — Apollo Enricher (MCP)            → companies search + people match + contacts search
Actor 4 — Data Formatter (Python/openpyxl) → ~/Downloads/prospects.xlsx
```

### Source C — Job Posting Intelligence (convert postings into client pitches)

Companies posting PPC/paid media roles they haven't filled = confirmed budget, open to freelance:
```
WebSearch: site:linkedin.com/jobs "google ads specialist" OR "paid media" remote past-month
WebSearch: site:indeed.com "meta ads" OR "google ads" remote past-30-days
→ Extract company name → pitch directly as freelancer (NOT applying to job)
```

### Source D — Meta Ad Library Spy (active ad spenders = confirmed budget)
```
WebSearch: "facebook ad library" ecommerce active ads USA 2025
→ Extract brand names → enrich via Apollo/Vibe → pitch with audit offer
```

---

## PHASE 2 — QUALIFY & SCORE

Gate system (same as hmz-daily-leads):
| Gate | Condition |
|---|---|
| GATE 1 | Real + active business |
| GATE 2 | Spending on ads (or clear need to) |
| GATE 3 | Problem that Zulqarnain/agency solves |
| GATE 4 | Can pay ($5k+ ad spend signal) |
| GATE 5 | Can hire globally / remote |

Score ≥80 → Website demo or cold pitch
Score 65-79 → Direct outreach only (no demo)
Score <65 → Discard

---

## PHASE 3 — DEMO SITE BUILD (website-builder pipeline)

For top-scored leads → build a demo site in their niche/city in ~10 min:

```
Actor 5 — Brief Extractor (Kimi 8K)        → parse prospect's business type + vibe from their site
Actor 6 — Design Director (UI/UX Pro Max)  → design spec matched to their industry
Actor 7 — Component Selector (21st.dev)    → assemble Hero, Features, CTA, Footer
Actor 8 — Site Builder (Claude Code)       → Next.js + Tailwind + Framer Motion build
```

One-prompt format:
```
"Build a demo website for a [BUSINESS TYPE] called [NAME] in [CITY].
Vibe: [pull from their existing brand]. Sections: Hero, Services, Testimonials, CTA, Footer.
Framer Motion animations. Deploy preview only (not prod)."
```

---

## PHASE 4 — OUTREACH + CLOSE

```
Actor 9  — Outreach Generator (Kimi K2.5)
  Per lead:
  - Cold email: subject + body (specific pain point from gate analysis)
  - LinkedIn DM: connection request + value hook
  - Cold DM: Instagram/Facebook version
  Export: ~/Downloads/outreach.csv (Mailchimp import-ready)

Actor 10 — Apollo Campaign (MCP)
  apollo_emailer_campaigns_search → find/create sequence
  apollo_emailer_campaigns_add_contact_ids → add lead to sequence
  → automated follow-up drip (5 touches over 14 days)
```

Cold pitch formula:
```
"Hey [NAME], I built a demo website for [BUSINESS NAME] — took 10 minutes.
[Link to demo]. If you want the full version with animations + CMS, I do these for $1,500.
Interested?"
```

---

## MASTER 10-ACTOR PIPELINE (all connected)

```
[DAILY SWEEPS — automated]
  hmz-daily-leads (7AM) ─────────────────────────────────────────→ HMZ-Leads-Daily.xlsx
  hmz-bdm-morning (9AM) ─────────────────────────────────────────→ HMZ-BDM-Morning-[DATE].html
  hmz-bdm-evening (9PM) ─────────────────────────────────────────→ HMZ-BDM-Evening-[DATE].html
  hmz-indeed-mcp (on-demand) ────────────────────────────────────→ HMZ-Indeed-MCP-[DATE].html

[ON-DEMAND — triggered by user]
  Actor 1  Brief Generator (Kimi 8K) ──→ structured extraction spec
  Actor 2  Vibe Prospecting (MCP) ─────→ businesses + buying signals
  Actor 3  Apollo Enricher (MCP) ──────→ decision makers + verified emails
  Actor 4  Data Formatter (openpyxl) ──→ ~/Downloads/prospects.xlsx

  [For ≥80 scored leads only]
  Actor 5  Brief Extractor (Kimi 8K) ──→ prospect brand analysis
  Actor 6  Design Director (UI/UX Pro) → design spec JSON
  Actor 7  Component Selector (21st.dev)→ React components
  Actor 8  Site Builder (Claude Code) ─→ Next.js + Tailwind + Framer → Vercel preview

  Actor 9  Outreach Gen (Kimi K2.5) ───→ email + LinkedIn + DM + CSV
  Actor 10 Apollo Campaign (MCP) ──────→ add to sequence → 5-touch drip
```

---

## REVENUE MODEL

| Activity | Price | Time | Margin |
|---|---|---|---|
| Lead list (20 prospects) | $500 | 5 min | ~100% |
| Starter website | $1,500 | 2 hrs | ~90% |
| Growth website | $3,500 | 4 hrs | ~90% |
| Monthly retainer | $500/mo | ongoing | ~95% |
| **Monthly target** | **$10K+** | **20 hrs** | **~90%** |

---

## ONE-COMMAND ACTIVATION

```
"Run full agency pipeline for [NICHE] in [CITY]:
1. Pull today's leads from HMZ-Leads-Daily.xlsx (score ≥80)
2. Build demo website for top 3 leads
3. Write personalized cold DM + email for all leads
4. Add to Apollo email sequence
Export: prospects.xlsx + outreach.csv + demo URLs"
```

---

## SKILLS ORCHESTRATED

| Skill | Role |
|---|---|
| `lead-gen-ai` | All 4 sweep pipelines + Vibe/Apollo MCP extraction |
| `vibe-prospecting` | Business discovery + buying signals |
| `website-builder` | 5-actor site build pipeline |
| `framer-motion-builder` | Animation system for all sites |
| `ui-ux-promax` | Design system for site builds |
| `ugc-agency` | Video ad upsell for client sites |
| `airtable-sdk` | CRM — track prospects, deals, site builds |
| `market-social` | Social content for client websites (recurring upsell) |
| `client-hunting` | Additional lead sources (Indeed connector, Yelp) |

---

## OUTPUT FILES MAP

| File | Description |
|---|---|
| `~/Downloads/Leads/HMZ-Leads-Daily.xlsx` | Daily appended B2B leads (never wiped) |
| `~/Downloads/HMZ-Elite-Leads-[DATE].html` | Gold/green lead cards |
| `~/Downloads/HMZ-BDM-Morning-[DATE].html` | Morning job sweep report |
| `~/Downloads/HMZ-BDM-Evening-[DATE].html` | Evening job sweep + Reddit drafts |
| `~/Downloads/HMZ-Indeed-MCP-[DATE].html` | Indeed MCP job report |
| `~/Downloads/prospects.xlsx` | General lead extraction output |
| `~/Downloads/outreach.csv` | Mailchimp import-ready outreach |
| Vercel preview URLs | Demo sites per prospect |
