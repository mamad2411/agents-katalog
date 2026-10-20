---
name: yasser
description: >-
  Yasser — the universal super-hub for ALL Cursor skills in this repo. Use for any task
  when you want everything available at once (/yasser). Routes to every domain master
  (ui, tailwind, color, video, integrations, payments, marketplace, travel, backend,
  devops, git, testing, analytics, ai-mcp, business, communications, documents, mobile,
  planning, code-quality, debugging, browser, content-seo, fullstack, ads-agent,
  skills-meta, productivity, Remotion install/create-video) and their bundled GUIDE.md
  files. Prefer a single domain
  master (e.g. ui-master) when the task is narrow. Invoke as yasser or /yasser.
---

# Yasser — الكل في الكل (Universal Super-Hub)

**Yasser** = meta-router لكل الـ **34 domain masters** + **ads-agent** + **437 bundled skills**.

> **مهم:** الـ masters المنفصلة (`ui-master`, `payments-master`, …) **تفضل موجودة** — استخدمها لو عايز تخصص. استخدم **Yasser** لما تحب الـ agent يختار من كل الدنيا.

## How Yasser works

```
1. Understand user goal (any domain).
2. Pick one or more domain masters from the table below.
3. Open that master's SKILL.md (same folder name under ~/.cursor/skills/).
4. Read the relevant skills/<name>/GUIDE.md before acting.
5. Combine masters when the task spans domains (e.g. marketplace + payments + ui).
```

**Paths (global install):** `~/.cursor/skills/<master-name>/SKILL.md`  
**Sub-skills:** `~/.cursor/skills/<master-name>/skills/<skill-name>/GUIDE.md`

Quick decision tree → `skills/yasser-universal-routing/GUIDE.md`

---

## All domain masters (route here)

| Master | Use when | Open |
|--------|----------|------|
| **ui-master** | UI, frontend, forms, brand, charts, Figma-grade DS, effects | `ui-master/SKILL.md` |
| **tailwind-master** | Tailwind v4, shadcn, Radix, RTL, UAE DLS, tokens | `tailwind-master/SKILL.md` |
| **color-design-master** | Palettes, OKLCH, WCAG, AI color harmony | `color-design-master/SKILL.md` |
| **video-ai-master** | AI video, Veo/Kling, **Remotion install** (`create-video`), ffmpeg, social export | `video-ai-master/SKILL.md` → **`remotion-programmatic-video/GUIDE.md`** |
| **integrations-master** | GitHub, Slack, CRM, cloud, webhooks, 80+ APIs | `integrations-master/SKILL.md` |
| **backend-api-master** | REST/GraphQL, auth, MFA, DB, Stripe patterns, QR, maps | `backend-api-master/SKILL.md` |
| **payments-master** | Gateways worldwide + Africa, checkout, PCI | `payments-master/SKILL.md` |
| **communications-master** | Chat, WhatsApp, helpdesk, email, omnichannel bot | `communications-master/SKILL.md` |
| **marketplace-master** | Amazon/Talabat-style multi-vendor | `marketplace-master/SKILL.md` |
| **travel-tech-master** | OTA, GDS, channel manager, extranet, mapping | `travel-tech-master/SKILL.md` |
| **business-master** | CRM, ERP, accounting (A→Z), affiliate, white-label, multi-tenant, e-invoicing | `business-master/SKILL.md` |
| **systems-platforms-master** | MongoDB, Supabase, Neon, Cloudflare, Postman, email servers | `systems-platforms-master/SKILL.md` |
| **cross-platform-apps-master** | Desktop (Electron/Tauri), mobile, one-codebase web+desktop+mobile | `cross-platform-apps-master/SKILL.md` |
| **ride-hailing-maps-master** | Uber/Careem apps, matching/dispatch, live tracking, **maps design**, routing | `ride-hailing-maps-master/SKILL.md` |
| **gps-tracking-master** | GPS/GNSS, RTK, device protocols, geofencing, fleet tracking, PostGIS | `gps-tracking-master/SKILL.md` |
| **cybersecurity-master** | Protect sites from hackers: OWASP, hardening, auth, pentest, WAF/DDoS, IR | `cybersecurity-master/SKILL.md` |
| **visual-5d-master** | Cinematic 5D video, 5D images/logos, 3D render, color grading | `visual-5d-master/SKILL.md` |
| **fullstack-stacks-master** | Next/Node, Python, Go, Laravel stacks | `fullstack-stacks-master/SKILL.md` |
| **devops-master** | Docker, K8s, Terraform, CI/CD, Cloudflare | `devops-master/SKILL.md` |
| **git-workflow-master** | Commits, PRs, `gh`, CI triage | `git-workflow-master/SKILL.md` |
| **testing-master** | Unit, E2E, Playwright, TDD | `testing-master/SKILL.md` |
| **code-quality-master** | Review, security audit, perf, bugs | `code-quality-master/SKILL.md` |
| **debugging-master** | Systematic debug, ports, profiling | `debugging-master/SKILL.md` |
| **planning-master** | PRD, ADR, architecture, prototyping | `planning-master/SKILL.md` |
| **documents-master** | DOCX, PDF, PPTX, docs sites | `documents-master/SKILL.md` |
| **analytics-master** | PostHog, flags, experiments, warehouse | `analytics-master/SKILL.md` |
| **ai-mcp-master** | MCP servers, prompts, vision, god-mode agent | `ai-mcp-master/SKILL.md` |
| **mobile-master** | React Native, Expo, Flutter, iOS | `mobile-master/SKILL.md` |
| **browser-automation-master** | Visual QA, Puppeteer, flows | `browser-automation-master/SKILL.md` |
| **content-seo-master** | Copy, blog, SEO audit | `content-seo-master/SKILL.md` |
| **productivity-master** | Context, onboarding, parallel explore | `productivity-master/SKILL.md` |
| **skills-meta-master** | Author skills, rules, hooks | `skills-meta-master/SKILL.md` |
| **prompt-master** | Elite prompt engineering + 10 expert personas (PhD researcher, competitive intel, content/business/strategy/branding/LinkedIn/marketing/viral) | `prompt-master/SKILL.md` |
| **ads-agent** | Composer max power, multi-agent ship | `ads-agent/SKILL.md` |

---

## Remotion (install + render) — via Yasser

When user says **Remotion**, **create-video**, **React to MP4**, or programmatic video:

1. Route → `video-ai-master`
2. Read → `video-ai-master/skills/remotion-programmatic-video/GUIDE.md`
3. Run install if needed:

```bash
npx create-video@latest
cd <project> && npm install && npm run dev
```

4. Combine with `ai-video-api-fal-runway` if mixing AI clips + Remotion overlays.

---

## Multi-master combos (common)

| Goal | Masters |
|------|---------|
| SaaS product launch | `planning-master` → `ui-master` + `tailwind-master` → `backend-api-master` → `devops-master` |
| Gov portal UAE | `tailwind-master` + `color-design-master` + `integrations-master` + `ui-master` |
| Marketplace MENA | `marketplace-master` + `payments-master` + `communications-master` + `ui-master` |
| Travel OTA | `travel-tech-master` + `payments-master` + `integrations-master` |
| Full stack feature | `fullstack-stacks-master` + `testing-master` + `git-workflow-master` |
| Ship fast (max agent) | `ads-agent` + `yasser` routing to domain guides |
| Promo video (AI + text) | `video-ai-master` → `remotion-programmatic-video` + `ai-video-cinematic-prompts` |

---

## Agent rules when Yasser is active

1. **Do not guess** — read the domain `GUIDE.md` for the matched skill.
2. **Narrow is OK** — if user says "only Stripe", use `payments-master` not every master.
3. **Minimize scope** — pick fewest masters that cover the task.
4. **Cross-read** when boundaries blur (integrations + backend for webhooks).
5. **359 skills** live under domain folders — Yasser does not duplicate them.

---

## Usage

```
/yasser build a multi-vendor food app with Paymob and RTL Arabic UI
```

```
use yasser — integrate GitHub, deploy on Vercel, add PostHog
```

For **one domain only**, slash the specific master: `/ui-master`, `/payments-master`, etc.

## Note

Yasser is a **router hub** only (`SKILL.md` + routing guide). All real instructions remain in each `*-master/skills/*/GUIDE.md`.
