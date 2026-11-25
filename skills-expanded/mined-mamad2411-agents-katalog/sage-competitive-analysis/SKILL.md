---
name: sage-competitive-analysis
description: "Analyze competitive landscape and market positioning. Use when user says 'competitive analysis', 'positioning', 'who are our competitors', 'benchmark', 'market analysis', or any reference to competitors, market positioning, or competitive advantages."
---

# Competitive Analysis — Market Positioning

Skill to analyze the competitive landscape of Evolution Foundation and identify positioning opportunities.

**Always respond in English.**

## Workflow

### Step 1 — Collect internal data

Fetch current Evolution metrics:
- Stars/forks from GitHub repos (`/int-github-review`)
- MRR and Stripe subscriptions (`/int-stripe`)
- Discord community size
- Number of installations/instances (if available)

### Step 2 — Research competitors

Use WebSearch/WebFetch to research the main competitors in the space of:
- APIs de WhatsApp (Baileys, wa-automate, Venom, wppconnect)
- CRMs com IA para WhatsApp (Kommo, Respond.io, Wati, MessageBird)
- Plataformas de automação (ManyChat, Botpress, Landbot)

For each competitor, gather:
- Model (open source vs SaaS vs enterprise)
- Pricing
- Main features
- GitHub stars/forks (if open source)
- Strengths and weaknesses

### Step 3 — Map positioning

Create positioning matrix:

| Dimension | Evolution | Concorrente A | Concorrente B |
|----------|-----------|--------------|--------------|
| Model | Open source + SaaS | SaaS only | Enterprise |
| Price | Freemium + plans | R$X/mês | R$X/mês |
| WhatsApp Unofficial | ✅ Baileys | ❌ | ❌ |
| WhatsApp Cloud API | ✅ | ✅ | ✅ |
| Integrated CRM | ✅ Evo CRM | ❌ | ✅ |
| Community | ✅ Discord + open source | ❌ | ❌ |
| IA/Agentes | ✅ Evo AI | Parcial | ❌ |

### Step 4 — Identify opportunities

- Gaps that no competitor covers
- Features where Evolution leads
- Threats (fast-growing competitors)
- Moats (advantages hard to copy)

### Step 5 — Save report

Save to `workspace/strategy/analyses/[C] YYYY-MM-DD-competitive.md`

## Rules
- Real data — research properly, do not fabricate
- Honesty about weaknesses — do not hide where the competition is better
- Focus on actionable — every analysis should end with "what to do about it"
- Update at most every 3 months (the market does not change every week)
