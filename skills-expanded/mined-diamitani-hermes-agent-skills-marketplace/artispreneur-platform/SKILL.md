---
name: artispreneur-platform
description: Build and maintain the Artispreneur multi-product music business platform — agent workspaces, pricing, Stripe, AWS, Terraform, and the dark gold design system.
---

# Artispreneur Platform Builder

## Trigger

When the user asks to build, update, deploy, or maintain any part of the Artispreneur ecosystem — landing pages, agent workspace, academy, directory, pricing, signup flow, architecture docs, or investment materials.

## Master Repo

```
github.com/diamitani/artispreneur-v217
```

Everything lives in ONE master repo. Do not create separate repos for separate products. 5 product families coexist under one codebase:
- **Pro Toolkit** — Contract Agent + EPK Builder
- **Directory & Outreach** — Outreach Agent + CRM + contact directory
- **Academy** — Tutor Agent + courses
- **Core** — Master Agent + Business Registration + PAL onboarding
- **Cataba Publishing** — Catalog Agent + splitsheets + ISRC

## Design System

```css
:root {
  --bg: #09090b;         /* Near-black */
  --surface: #111113;    /* Card backgrounds */
  --card: #18181b;       /* Elevated cards */
  --border: #252529;     /* Borders */
  --text: #fafafa;       /* Primary text */
  --text-muted: #a1a1aa; /* Secondary text */
  --text-dim: #63636b;   /* Dim text */
  --gold: #c9a227;       /* Brand gold */
  --gold-light: #e0b832; /* Hover gold */
  --gold-subtle: rgba(201,162,39,0.08);
}
```

**Fonts:** Inter (body), Playfair Display (headings), Geist Mono (code)
**Logo:** `logo.png` (113KB PNG wordmark) — always use `<img>` with height 22px
**Header pattern:** Sticky navbar with logo + "Artispreneur" text (gold on "preneur") + nav links (Rostr Agent, Academy, Directory, Pricing, Login) + "Get Started Free" CTA button

## Architecture

**Unified signup flow (ALL products):**
```
Sign Up → PAL Onboarding → ROSTR Compiles Soul.md → Provision Workspace → Install Tools → Agent Dashboard
```

**Multi-tenant Hermes runtime** — NOT per-user EC2. Free/Artist/Pro share one Hermes instance with isolated namespaces. Only Label/Enterprise gets dedicated EC2.

**AWS backend:** Cognito (auth), RDS PostgreSQL (data), S3 (outputs/assets), Lambda (FastAPI), Bedrock DeepSeek V3 (LLM), CloudFront (CDN), ElastiCache (sessions)

**Deploy:** GitHub push → Vercel auto-deploy → rostragent.com

## Stripe Pricing

| Tier | Monthly | Annual | Chats | Skills | PDFs | Storage |
|------|---------|--------|-------|--------|------|---------|
| Free | $0 | $0 | 10 + BYOK | — | — | — |
| Artist | $12 | $99 | 200 | 20 | 50 | 1GB |
| Pro | $25 | $199 | Unlimited | Unlimited | Unlimited | 5GB |
| Label | $59 | $499 | Unlimited | Unlimited | Unlimited | 10GB (5 seats) |

Stripe account: artispreneur@gmail.com. Live keys in FINANCE.md. Products: `prod_UtlY6wgThfo8Jb` (Artist), `prod_UtlY9Vuxe33ewb` (Pro), `prod_UtlYJ1W1aIbJcu` (Label).

## User Preferences

- **After every deploy:** CONFIRM with the user AND send the fresh Vercel production URL (the hash URL, not just the alias). Never assume they'll find it.
- **Before claiming done:** verify all pages, cross-links, and end-to-end data flow (signup → login → workspace).
- **Headers must be unified** across ALL pages — same logo, nav, CTA. Check this on every build.
- **Design for the actual user** (indie artist who doesn't know jargon). Use plain language. "Register your songs" not "PRO registration".
- **Code quality:** modular, clean, short files, production-grade. 13+ Python files, average ~22 lines each.
- **Frustration = fix immediately.** If the user says something doesn't work, stop and fix it — don't argue.

## Key Files

| File | Purpose |
|------|---------|
| `index.html` | Landing page with chat UI |
| `workspace.html` | Rostr Agent workspace (11 agents, sidebar, chat) |
| `signup.html` | 5-step PAL onboarding wizard |
| `login.html` | Email/password auth |
| `pricing.html` | Stripe checkout (annual toggle) |
| `success.html` | Post-checkout confirmation |
| `skills.html` | Skill Builder + PDF generation |
| `academy.html` | 16 courses listing |
| `directory.html` | 74+ contacts with filters |
| `architecture.html` | Full system architecture visual |
| `investment.html` | One-pager for investors |
| `backend/` | 30+ Python modules, 11 agents |
| `terraform/main.tf` | All AWS infrastructure |

## References

See `references/` for detailed docs on specific subsystems.
