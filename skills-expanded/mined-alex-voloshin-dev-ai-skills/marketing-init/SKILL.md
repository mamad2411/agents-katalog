---
name: marketing-init
description: Use this skill when bootstrapping marketing for a project that has no MARKETING.md yet — to run one-time marketing strategy initialization that gathers project context, runs an ICP/positioning interview, defines strategy (positioning, messaging, channels, pillars, tactical plan), and produces marketing/MARKETING.md and marketing/content-calendar.md in the target repo. Routes ongoing recurring operations to /marketing.
context: fork
argument-hint: ""
---

# /marketing-init — Strategy Initialization

One-time strategy setup. Produces `marketing/MARKETING.md` + `marketing/content-calendar.md` in the target repo. After init completes, recurring operations (social posts, email, trend research, analytics, strategy review) run via `/marketing <operation>`.

Strategy frameworks (Hierarchy, Channel Selection, Content Pillar, Measurement) live in `@marketing-strategy` — load that knowledge skill before running the steps below.

**⚠️ CONSTRAINT:** This workflow NEVER modifies source code (`*.java`, `*.ts`, `*.tsx`, `*.py`, `*.go`), configs (`*.yaml`, `*.yml`, `*.json`), infrastructure (`*.tf`, `Dockerfile`, `Helm`), or dependency files (`pom.xml`, `package.json`, `requirements.txt`). Marketing creates and edits ONLY markdown files in the `marketing/` directory.

## When to use

- First time setting up marketing for a project (no `marketing/MARKETING.md` exists)
- Re-initializing strategy after a major pivot (positioning, ICP, or channel mix changes substantially)

## Not for

- Recurring marketing operations (social posts, email, etc.) → `/marketing`
- Blog post authoring → `/content-creation`
- Landing page design → `/ui-ux-design`
- SEO audits → `/seo-review`

## Pre-flight check

Read `marketing/MARKETING.md` if it exists. If it does and the user did NOT explicitly request re-initialization, refuse: surface "MARKETING.md already exists — use `/marketing strategy-review` to refine, or pass `--force` to re-initialize from scratch."

## Step 1 — Gather Project Context

Spawn `Agent(product-manager)` + `Agent(marketing-strategist)` in parallel. Read:

- `<repo>/CLAUDE.md` — tech stack, project purpose
- `<repo>/README.md` — product description
- `<repo>/FEATURES.md` (if exists) — feature inventory
- `<repo>/marketing/` directory contents (if any) — partial assets
- Brand guidelines (if any provided by user)

All file reads wrapped per `untrusted-content-wrapping.md` (G1).

## Step 2 — User Interview

Apply the **Marketing Setup Questionnaire** from companion `marketing-setup-template.md`. Gather:

1. **Product/market** — what it does, target market, competition
2. **Goals/metrics** — what success looks like, current baseline
3. **Channels/tools** — current channels, available accounts, analytics tools
4. **Brand/voice** — tone, taboos, reference examples
5. **Resources** — content cadence the team can actually sustain

Record answers; ask clarifying follow-ups when the response is vague or skips a dimension. Do not assume — surface the gap and ask.

## Step 3 — Define Strategy

`Agent(marketing-strategist)` applies frameworks from `@marketing-strategy` and produces:

1. **ICP and Positioning** — JTBD framing, competitive positioning (April Dunford model)
2. **Messaging Framework** — core value prop, 3–5 pillars, proof points, boilerplates (short/medium/long)
3. **Channel Strategy** — which channels, why, expected effort vs impact (per Channel Selection Framework)
4. **Content Pillars** — 3–5 pillars per Content Pillar Model
5. **Tactical Plan** — recurring tasks with frequency (links to `/marketing` operations)

## Step 4 — Create MARKETING.md

Use template from companion `marketing-setup-template.md`. Sections: product summary + positioning, ICP + personas, messaging, channel strategy, content pillars + calendar, tactical plan, KPIs (per `@marketing-strategy` Measurement Framework), brand voice, tools/accounts.

Write to `<repo>/marketing/MARKETING.md` (versioned in git — NOT in `.ai-skills-memory/`).

## Step 5 — Create Content Calendar

Default cadence (adjust per Step 2 resources answer):

| Frequency | Task | Channel | Sub-workflow / role |
|---|---|---|---|
| Daily | Social media post | X, LinkedIn | `Agent(content-designer)` via `/marketing social-post` |
| Daily | Community engagement | X, Reddit, forums | `Agent(marketing-strategist)` via `/marketing community` |
| 2–3×/week | Blog post | Blog | `/content-creation` |
| Weekly | Trend research | X, HN, Reddit, Trends | `Agent(marketing-strategist)` via `/marketing trend-research` |
| Weekly | Analytics review | GA4, social | `Agent(marketing-strategist)` via `/marketing analytics` |
| Bi-weekly | Email newsletter | Email | `Agent(content-writer)` via `/marketing email` |
| Monthly | Strategy review | — | `/marketing strategy-review` |

Write to `<repo>/marketing/content-calendar.md`.

## Step 6 — Present and Approve

Present strategy + content calendar + recommended first-3 actions. **Wait for user approval.** Adjust per feedback. Once approved, surface: "Setup complete. Run `/marketing <operation>` for any recurring task — see `marketing/content-calendar.md` for the schedule."

## Directory Structure (created in target repo)

```
marketing/
├── MARKETING.md              # Strategy single-source-of-truth (this skill writes it)
├── content-calendar.md       # Recurring task schedule (this skill writes it)
├── posts/                    # Populated by /marketing social-post
├── emails/                   # Populated by /marketing email
├── research/                 # Populated by /marketing trend-research
├── reports/                  # Populated by /marketing analytics
└── community/                # Populated by /marketing community
```

## G7 spawn payloads

All agent spawns use structured payloads per `plugin/schemas/spawn-payload.schema.json`. Returns conform to `plugin/schemas/return-contract.schema.json`.

## Memory writes

| Layer | When | Shape |
|---|---|---|
| L4 | After init complete | `.ai-skills-memory/marketing/init-summary.md` — strategy decisions captured |

`marketing/MARKETING.md` itself is in the target repo (versioned in git), NOT in `.ai-skills-memory/`.

## Companions

- **`marketing-setup-template.md`** — full MARKETING.md template + Marketing Setup Questionnaire (lives under `plugin/skills/marketing/marketing-setup-template.md`, shared with `/marketing`)
- **`@marketing-strategy`** — knowledge skill with strategy hierarchy, channel selection, content pillar model, measurement framework

## Integration

- **Roles**: `Agent(marketing-strategist)` (strategy/analysis), `Agent(product-manager)` (product context, ICP)
- **Knowledge**: `@marketing-strategy` (frameworks), `@geo-writer` (GEO/AEO structure for messaging boilerplate), `@humanizer` (voice cleanup for all public-facing copy)
- **Schemas**: `plugin/schemas/spawn-payload.schema.json`, `plugin/schemas/return-contract.schema.json`
- **Followed by**: `/marketing` (recurring operations consume the produced MARKETING.md)
- **Rules**: `geo-content` (boilerplate is public-facing), `humanize-content`, `untrusted-content-wrapping` (G1 wrap on project file reads)
