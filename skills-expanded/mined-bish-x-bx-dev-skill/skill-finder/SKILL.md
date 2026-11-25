---
name: skill-finder
description: "Skill library router. Searches the skill library by task context and loads matching skills on demand. Always active."
---

# Skill Finder

You have access to a skill library in this repository's `skill-library/`
folder, or the equivalent installed skill-library root in your Codex setup.
The root `INDEX.md` is the single source of truth for categories and bundled
skills.

## When to Search

Before starting any substantive task (coding, writing, reviewing, designing, planning, debugging, marketing), search for a matching skill.

**Skip search** for trivial tasks:
- Single-line fixes with explicit location ("fix typo on line 42")
- Simple read/info requests ("show me file X", "what does this function do?")
- One-off shell commands ("run tests", "git status")

**NOT trivial** (do search): "edit README", "update docs", "refactor X" — scope is unclear, skill may help.

## How to Search

### Step 1 — Pick category

Read `<skill-library-root>/INDEX.md` and match the task to a category:

| Category | Triggers |
|----------|----------|
| architecture | DDD, bounded contexts, domain modeling, architecture boundaries |
| backend | API, database, Postgres, Supabase, SQL, server, security, DevOps, Docker, K8s, CI/CD, debugging, monitoring, MCP |
| frontend | React, Next.js, UI, CSS, Tailwind, accessibility, design, mobile, React Native, Remotion, video |
| review-qa | code review, website audit, user research, QA, performance audit, E2E testing, Playwright |
| marketing | copy, SEO, CRO, ads, email, pricing, launch, content strategy, analytics, internal comms |
| general | planning, brainstorming, bash, git, diagrams, video/FFmpeg, legal, product work |
| system | Codex/OpenAI docs, image generation, plugins, skill creation/installation, migration, routing |

If no category matches — skip, no skill needed.

### Step 2 — Find skill

Use the "Full Index" section in `<skill-library-root>/INDEX.md`. Each entry is
listed as:
```
`category/skill-name`
```

Match by category, skill name, and task context. If still ambiguous, open the
smallest plausible `SKILL.md` and check its frontmatter description before
loading more.

### Step 3 — Load skill

Read `<skill-library-root>/<category>/<skill>/SKILL.md` and follow its instructions.

**Budget rule**: total loaded `SKILL.md` content must not exceed 1500 lines per
task. If a skill is large, read only the relevant section after checking its
frontmatter and headings.

## Disambiguation

If prompt is too generic and matches multiple skills, resolve by context:

| Generic term | Clarify by context |
|---|---|
| "review" | git diff → `code-review-expert`; codebase quality → `code-quality-review`; live URL → `audit-website` |
| "performance" | React/bundle → `vercel-react-best-practices`; Lighthouse/CWV → `performance-audit`; monitoring/SLO → `observability-design` |
| "security" | source review → `code-review-expert`; live website pentest → `security-pentest`; payments/PCI → `pci-compliance`; secrets/.env → `secrets-vault-manager` |
| "optimize form" | signup/registration → `signup-flow-cro`; lead capture/contact → `form-cro` |
| "email" | drip sequence → `email-sequence`; single copy → `copywriting`; analytics → `analytics-tracking` |
| "document" | write RFC/spec → `engineering/writing-plans` or `general/spec-driven-workflow`; legal file review → `general/legal-review`; meeting transcript analysis → `general/meeting-analyzer`; otherwise use the built-in file tools available in the current environment |

If still ambiguous after this table — ask the user one short clarifying question before loading.

## Multi-Category Tasks

If task spans 2+ categories, load skills in this order:

1. **Plan** — general (brainstorming, consultancy-practices)
2. **Context** — marketing/product-marketing-context, general/product-discovery, engineering/context-engineering
3. **Build** — backend, frontend, system/general support as relevant
4. **Verify** — review-qa, engineering/systematic-debugging
5. **Ship** — marketing (launch, copy, SEO)

Within one phase, load the most specific skill first.

## Budget Management

- Max budget: 1500 lines of SKILL.md content per task
- If no skill matches — proceed without one, don't force it
- Never load a skill "just in case" — only when there's a clear match
- If task spans multiple categories — load from each, respecting the budget
- **If compound task exceeds 1500 lines**: load skills sequentially by phase — execute phase 1, then unload and load phase 2. Never load all at once.
