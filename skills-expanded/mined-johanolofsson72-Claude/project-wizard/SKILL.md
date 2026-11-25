---
name: project-wizard
description: "Inception wizard (50 questions, 9 categories) creating CLAUDE.md, speckit constitution, design system, and project brief. Use when starting a new project, brainstorming an idea, or bootstrapping a repo. Triggers: new project, inception, bootstrap."
argument-hint: "[brief project idea description]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion, Glob, Grep
---

# Project Inception Wizard

You are a senior solutions architect conducting a project inception interview. Your job is to extract every critical decision from the user's head and turn it into three foundation documents:

1. **`CLAUDE.md`** — full project configuration that tells Claude how to work in this project
2. **`.specify/memory/constitution.md`** — core principles and technical constraints (speckit format)
3. **`PROJECT-BRIEF.md`** — human-readable project description for stakeholders

This is NOT a feature spec. This is the project's DNA — the foundation that all future speckit specs, plans, and implementations build on.

## Input

```text
$ARGUMENTS
```

## Process

### Phase -1: Project Bootstrap (AUTOMATIC — runs before anything else)

This phase ensures speckit is installed/updated and the project has the latest Claude Code configuration synced from the template repo. It runs automatically — no user interaction needed unless something goes wrong.

**Steps 1–4 — spec-kit (pinned):** nothing to run here. spec-kit is installed and initialised by
`scripts/speckit-sync.sh --init-new` inside Step 5 (sync-prompt Step 0.5), at the tag pinned in the
template's `scripts/speckit-version`. That script backs up and restores the constitution around the
init and applies `speckit-extension-policy.sh` afterwards, so the old backup / init / restore /
policy steps that lived here are one call now — and, unlike the old unconditional
`specify init --force`, a re-run on an initialised project is a no-op instead of restoring
spec-kit's two pipeline stops. If `uv` is missing the script says so and stops; install it
(`curl -LsSf https://astral.sh/uv/install.sh | sh`, Windows: `irm https://astral.sh/uv/install.ps1 | iex`).

**Step 5 — Run the COMPLETE template sync (identical to `/project-update`):**

This single step puts **everything** in place — every skill (`allium`, `tla`, `code-review`, `explore-codebase`, `deploy-checklist`, `sync-template`, `update-template`), every rule (`allium.md`, `specs.md`, `continuous-execution.md`, `validation-followup.md`, `feature-pipeline.md`, `spec-interview.md`, `spec-register.md`, `spec-hardening.md`, `carve-budget.md`, the stack rules), every doc, every hook script (including the `spec-interview-guard` that hard-blocks implementation until each spec has its 15–25 anti-drift questions answered — base auto-answered with the recommended option by default, human overflow when a spec is flagged large/advanced), the deterministic local-LLM wiring, AND the Graphify wiring + bootstrap. **After this step the project is fully configured. The wizard IS the full sync — there is no separate `/project-update` pass required afterward.** If you ever catch yourself about to tell the user "now run `/project-update` to get allium/graphify", you skipped part of this step — go back and finish it. That handoff is the exact bug this step exists to kill.

The wizard does NOT paraphrase the sync into a summary and curl files one at a time — that approach reliably dropped `allium`, the pipeline rules, and the graphify wiring on the floor. Instead it resolves the template **locally** (cloning once if absent, which is far more reliable than ~50 individual HTTP fetches) and executes the canonical `sync-prompt.md` verbatim — the exact same instruction set `/project-update` runs. Single source of truth, zero drift.

**Step 5.1 — Resolve `$TEMPLATE`:** run the Step -1 block of `sync-prompt.md` exactly as written. It
asks the sync engine for the clone (`template-autosync.sh --template-dir`, which honours
`$CLAUDE_TEMPLATE_DIR` and the usual macOS/Linux locations), clones once to `~/repos/Claude` when
the machine has none, and fast-forwards a clone that is behind. Before any clone exists, read that
block from `https://raw.githubusercontent.com/johanolofsson72/Claude/main/scripts/sync-prompt.md`.
This skill keeps no candidate list of its own: four copies of that list is how they came to disagree.

**Step 5.2 — Execute the canonical sync flow verbatim:**

Read `$TEMPLATE/scripts/sync-prompt.md` and **execute every step it defines (Step -1 through Step 10) against the current project, exactly as written** — substituting the locally-resolved `$TEMPLATE` for any example `/Users/jool/...` path. Do NOT abbreviate it, do NOT skip its sub-steps. That file is the authoritative definition of a complete configuration; running it here is what guarantees the wizard and `/project-update` can never diverge. The steps that MUST complete (fail-hard on non-zero):

1. **Step 1–5 / 5b** — copy every missing skill, rule, doc, agent, and hook script. On a fresh project all of them are "missing", so this is where `allium/SKILL.md`, `tla/SKILL.md`, `rules/allium.md`, `rules/specs.md`, and the continuous-execution / validation-followup / feature-pipeline / spec-register rules actually land. None of these are optional.
2. **Step 5c** — `python3 scripts/sync-local-llm-hooks.py "$TEMPLATE/.claude/settings.json"` (deterministic local-LLM wiring + script mirror) AND `python3 scripts/sync-core-hooks.py "$TEMPLATE/.claude/settings.json"` (deterministic core-hook wiring — pipeline/spec-register/execution/tech-stack, script-presence gated). Both are mandatory; the second is what guarantees the pipeline + register enforcement hooks land without a follow-up `/project-update`.
3. **Step 5d** — `python3 scripts/sync-graphify-wiring.py "$TEMPLATE/.claude/settings.json"` then `bash scripts/graphify-bootstrap.sh` (deterministic Graphify wiring, then install + AST graph build; the bootstrap eligibility-gates itself under 30 source files).
4. **Step 6 / 6b** — install the external skills (`frontend-design` via anthropics/skills, superpowers, qa-test, playwright-skill, ui-ux-pro-max, …) and the TLC model checker.
5. **Step 0.5** — the sync engine and then `bash scripts/speckit-sync.sh --init-new` (the wizard is the one caller that passes `--init-new`: it is creating the project's `.specify/`).
6. **Step 8 / 8b** — normalize hook paths (`python3 scripts/fix-hook-paths.py .claude/settings.json`; The settings guard (spec 089) refuses this from the agent's shell once it is wired: ask the developer to run it with `!`) and confirm the stamp `.claude/.template-sync` carries a `sha=` line.

**Step 5.3 — Exit gate (BLOCKING — the wizard does not proceed until this prints `[OK]`):**

The Allium/TLA pipeline and Graphify are base requirements, not nice-to-haves. Before leaving Phase -1, verify every load-bearing artifact actually landed — this gate is what makes "you have to run `/project-update` afterward" impossible:

```bash
fail=0
for f in \
  .claude/skills/allium/SKILL.md \
  .claude/skills/tla/SKILL.md \
  .claude/rules/allium.md \
  .claude/rules/specs.md \
  .claude/rules/continuous-execution.md \
  .claude/rules/validation-followup.md \
  .claude/rules/feature-pipeline.md \
  .claude/rules/spec-register.md \
  .claude/rules/spec-interview.md \
  .claude/rules/spec-hardening.md \
  .claude/rules/carve-budget.md \
  .claude/rules/github-actions.md \
  .claude/rules/scenarios.md \
  .claude/rules/design-references.md \
  .claude/docs/design-reference-library.md \
  scripts/allium-hook.sh \
  scripts/tla-hook.sh \
  scripts/spec-interview-guard-hook.sh \
  scripts/scenario-map-reminder-hook.sh \
  scripts/sync-graphify-wiring.py \
  scripts/sync-core-hooks.py \
  scripts/graphify-bootstrap.sh \
  scripts/speckit-sync.sh \
  scripts/speckit-version \
  .specify/init-options.json; do
  [ -e "$f" ] || { echo "[MISSING] $f"; fail=1; }
done
python3 -m json.tool .claude/settings.json >/dev/null 2>&1 || { echo "[INVALID] settings.json is not valid JSON"; fail=1; }
# Core-hook gate: every mandatory enforcement script must EXIST *and* be wired.
# Checking only "present → wired" reports green on a project where the script was
# never copied at all — i.e. a project with no guards.
for s in pipeline-trigger-match emit-pipeline-reminder spec-register-guard-hook pipeline-state-guard-hook spec-interview-guard-hook spec-md-coverage-reminder-hook scenario-map-reminder-hook continuous-execution-hook stop-validation-hook repeat-failure-guard-hook spec-run-log-hook lane-orientation-hook; do
  if [ ! -f "scripts/$s.sh" ]; then echo "[MISSING] scripts/$s.sh never copied — re-run the core-script mirror in sync-prompt.md Step 5c"; fail=1;
  elif ! grep -q "$s.sh" .claude/settings.json; then echo "[UNWIRED] core hook $s present on disk but not wired — run sync-core-hooks.py"; fail=1; fi
done
# Graphify is only enforced on eligible (>=30 source-file) projects; the bootstrap self-gates below threshold.
if bash scripts/graphify-bootstrap.sh --eligibility-check >/dev/null 2>&1; then
  { command -v graphify >/dev/null && test -f graphify-out/graph.json && grep -q 'graphify-fire-hook.sh' .claude/settings.json; } \
    || { echo "[MISSING] graphify wiring/graph on an eligible project"; fail=1; }
fi
if [ "$fail" -eq 0 ]; then
  echo "[OK] Full template sync verified — allium, tla, pipeline rules, and graphify all in place"
else
  echo "[FAIL] Bootstrap incomplete — re-run Step 5 until green. Do NOT tell the user to run /project-update; finish the sync here."
  exit 1
fi
```

If this prints `[FAIL]`, go back into `$TEMPLATE/scripts/sync-prompt.md`, re-run the step that produces the missing artifact, and re-run the gate until it is green. Only a green gate unlocks Phase 0.

**Step 6 — Report bootstrap status:**

After the sync completes, present a brief summary:

```markdown
## Bootstrap Complete

**Speckit**: [initialised at pin vX.Y.Z / already at pin / FAIL: <speckit-sync.sh output>]
**Sync-prompt**: fetched from johanolofsson72/Claude (main)
**Files synced**: [count created] created, [count updated] updated, [count skipped] skipped
**Constitution**: [preserved from backup / fresh from speckit / not found]
**Skill audit** (sync-prompt Step 8e, report-only): [N] skills installed (~[T]k tokens baseline); stack-gated installs skipped: [bundles or none]; [REVIEW]/[CEILING]: [summary or "within ceiling"]. (On a fresh project the stack is not yet decided, so Step 6 installs all bundles and the audit flags any that turn out irrelevant once the stack is set.)

⚠️ **IMPORTANT**: Speckit skills (`/speckit-specify`, `/speckit-plan`, etc.) were installed to `.claude/skills/` but are NOT available as slash commands in this session. Claude Code loads skills at session start — new skills installed mid-session require a restart. After this wizard completes, exit Claude and start a new session to use the speckit commands.

Proceeding to project inception interview...
```

Then proceed to Phase 0.

---

### Phase 0: Context Absorption (MANDATORY — do this BEFORE asking a single question)

Before you open your mouth, you read everything available. Scan the following files IN THIS ORDER. For each file: if it exists, read it and absorb. If it doesn't exist, skip silently.

**Step 1 — Global configuration (the user's standards across ALL projects):**

```
~/.claude/CLAUDE.md
```

This contains the user's global persona, language preferences, code review style, and tone. Everything you generate must respect these global rules.

**Step 2 — Existing project files (if any exist in the current directory):**

```
./CLAUDE.md
./CLAUDE.local.md
./.specify/memory/constitution.md
./.specify/init-options.json
```

If any of these exist, this is NOT a blank-slate project. Adapt your questions — skip what's already decided, probe what's missing or unclear.

**Step 3 — Reference documentation (read ALL that exist):**

```
./.claude/docs/project-template.md
./.claude/docs/conventions.md
./.claude/docs/security.md
./.claude/docs/testing.md
./.claude/docs/spec-testing-checklist.md
./.claude/docs/deployment.md
./.claude/docs/git.md
./.claude/docs/workflows.md
./.claude/docs/agents-templates.md
./.claude/docs/skills.md
./.claude/docs/stress-testing.md
```

These contain established patterns, naming conventions, security rules, testing requirements, deployment procedures, and git workflows. The generated CLAUDE.md must be consistent with these if they exist.

**Step 4 — Rules (auto-loaded constraints):**

```
./.claude/rules/*.md
```

Use `Glob` to find all rule files. Read each one. These are hard constraints that the project must follow.

**Step 5 — Settings and hooks:**

```
./.claude/settings.json
```

If this exists, it defines hooks (UserPromptSubmit, PreToolUse, PostToolUse, PreCompact, SessionStart) that are part of the project's workflow. The generated CLAUDE.md must reference these.

**Step 6 — Existing skills and agents (for awareness):**

```bash
ls .claude/skills/ 2>/dev/null
ls .claude/agents/ 2>/dev/null
ls .claude/commands/ 2>/dev/null
```

Know what tooling already exists so you don't recommend recreating it.

**Step 7 — Speckit templates (if speckit is installed):**

```
./.specify/templates/constitution-template.md
./.specify/templates/spec-template.md
./.specify/templates/plan-template.md
./.specify/templates/tasks-template.md
```

If these exist, the constitution you generate must follow the template format.

**Step 8 — Existing design system:**

```
./design-system/MASTER.md
./design-system/pages/*.md
```

If a design system already exists, the visual design questions can be shortened — just confirm the existing direction.

**Step 9 — Sibling projects (for pattern reference):**

Run `ls ../` to see what other projects exist nearby. If the user has established patterns across projects (same stack, same conventions), your recommendations should align unless there's a reason to deviate.

---

After absorbing all available context, present a brief summary to the user:

```markdown
## Context Absorbed

**Global config**: [found/not found] — [key details: persona, language, tone]
**Existing CLAUDE.md**: [found/not found] — [key details if found]
**Existing constitution**: [found/not found] — [key details if found]
**Reference docs found**: [list of docs that exist]
**Rules found**: [list of rule files]
**Speckit installed**: [yes/no] — version [X] if found
**Skills/agents found**: [count] skills, [count] agents
**Sibling projects**: [list relevant ones with their tech stacks if recognizable]

[If context was found]: I've absorbed the existing project context. I'll skip questions that are already answered and focus on what's missing.

[If blank slate]: This is a fresh project with no existing configuration. I'll walk you through everything from scratch.
```

Then proceed to Phase 1.

### Phase 1: Introduction

If `$ARGUMENTS` is not empty, acknowledge the project idea and summarize your understanding in 2-3 sentences.

If `$ARGUMENTS` is empty, ask:
> What's the project idea? Give me the elevator pitch — one paragraph is fine.

Wait for the response, then proceed to Phase 2.

### Phase 2: The Interview

Ask questions **one at a time** using `AskUserQuestion`. This is a wizard — each step gets ONE focused question, the user answers, then you move to the next. NEVER dump multiple questions in a single message.

**Grouping exception**: Questions that are tightly related and trivially short (e.g., "Backend language?" + "Framework?") MAY be grouped into a single `AskUserQuestion` with max 2-3 sub-questions. But the default is ONE question per turn.

**Flow for each question:**
1. Use `AskUserQuestion` with a clear, specific question
2. If relevant, provide concrete options (not open-ended when avoidable)
3. Mark your recommended option with a star (★)
4. Wait for the answer
5. Acknowledge briefly, then ask the next question

**IMPORTANT**: If Phase 0 already answered a question (from existing files), state what you found and ask the user to confirm or override. Don't re-ask what's already decided.

For each question: if the user says "I don't know" or "not sure", offer 2-3 concrete options with your recommended choice marked with a star. Never leave a question unanswered — either the user decides or you recommend.

If a user answers in their native language, respond in the same language for that exchange, but keep all generated documents in English (code-facing) or as specified by the language decision.

**Smart skipping**: For simple projects (vanilla HTML, static sites, small games), many questions are irrelevant. If the project scope makes a question obviously N/A (e.g., "Multi-tenancy?" for a single-page Snake game), skip it and note your assumption. The user can always override later.

---

#### Category 1: Vision & Identity (ask one at a time)

1. **Project Name**: What is the project called? (will be used for repo name, kebab-case)
2. **Elevator Pitch**: One sentence — what does it do and for whom?
3. **Problem Statement**: What specific problem does this solve? Who has this problem today and how are they currently dealing with it?
4. **Target Users**: Who are the primary users? Describe 2-3 user personas (role, tech-savviness, frequency of use).
5. **Core Modules**: What are the major functional areas? (e.g., "Tickets, Time Tracking, Billing" — NOT individual features, but high-level modules)

#### Category 2: Core Principles (one at a time — these become constitution principles)

6. **Non-Negotiables**: What are the 3-5 things that are SACRED in this project? Things you will never compromise on. (e.g., "multi-tenant isolation", "offline-first", "Swedish UI, English code", "Excel parity")
7. **Architecture Philosophy**: Monolith or microservices? Convention over configuration? Shared code or duplication? What's your gut feeling?
8. **Data Ownership**: Who owns the data? Single database or per-tenant? Self-hosted or cloud? Any data sovereignty requirements?
9. **Integration First**: Will this system integrate with external services? Which ones are critical? (e.g., Fortnox, Stripe, Slack, email providers)
10. **Automation Stance**: What should be automated vs manual? What calculations, notifications, or workflows should happen without human intervention?

#### Category 3: Tech Stack (group backend + frontend as 2-3 per turn max)

11. **Programming Language**: Backend language? Any constraints or preferences?
12. **Backend Framework**: Framework choice? (e.g., ASP.NET Minimal API, Express, Django, Spring Boot)
13. **Frontend Stack**: Frontend framework + CSS approach + component library? (e.g., React + Tailwind + shadcn/ui)
14. **Database Engine**: Which database and why? (PostgreSQL, SQLite, SQL Server, MongoDB, etc.) ORM or raw SQL?
15. **State Management**: Client state management approach? (e.g., TanStack Query for server state, Zustand for client state)

#### Category 4: Authentication & Multi-tenancy (skip if N/A for project scope)

16. **Auth Method**: How do users log in? (email/password, OAuth, SSO/SAML, passkeys/WebAuthn, magic links)
17. **Authorization Model**: Simple roles, RBAC, ABAC, or per-resource permissions?
18. **Multi-tenancy**: Single-tenant or multi-tenant? If multi-tenant: shared DB, schema-per-tenant, or DB-per-tenant?
19. **Auth Provider**: Build your own or use a service? (ASP.NET Identity, Auth0, Clerk, Keycloak, Supabase Auth)

#### Category 5: Frontend & UX Principles (one at a time)

20. **Application Type**: SPA, SSR, SSG, hybrid, or admin dashboard?
21. **Component Library**: Existing component library or custom? (Tailwind + Headless UI, shadcn/ui, Material UI, Ant Design, Bootstrap, custom)
22. **Responsive Strategy**: Desktop-first, mobile-first, or responsive? Native mobile needed?
23. **Language & Localization**: UI language? Code language? Commit message language? Multi-language support needed?
24. **Accessibility**: WCAG level target? (A, AA, AAA)

#### Category 6: Visual Design & Identity (one at a time — feeds `frontend-design` and `ui-ux-pro-max` skills)

25. **Design Personality**: What feeling should the UI evoke? Pick one or describe your own:
    - Brutally minimal / clean
    - Maximalist / bold / loud
    - Soft / pastel / approachable
    - Luxury / refined / editorial
    - Playful / toy-like / fun
    - Industrial / utilitarian / raw
    - Retro-futuristic / sci-fi
    - Organic / natural / earthy
    - Corporate / professional / trustworthy
    - Other — describe it
26. **Color Direction**: What's the color mood? (e.g., "dark mode with neon accents", "warm earth tones", "monochrome with one pop color", "brand colors: #XX #YY"). Do you need both light and dark mode?
27. **Typography Feel**: What should the text feel like? (e.g., "modern sans-serif", "elegant serif headings with clean body", "monospace/technical", "handwritten/casual", "bold geometric"). Any specific fonts you love or hate?
28. **Visual Assets Strategy**: How will you source imagery?
    - Stock photos (Unsplash, Pexels, paid stock)
    - Custom illustrations (hand-drawn, vector, isometric)
    - Icons only (Heroicons, Lucide, Phosphor, custom SVG)
    - AI-generated imagery
    - Photography (original/branded)
    - Abstract/geometric patterns and textures
    - Mixed approach — describe it
29. **Animation Philosophy**: How should the UI move?
    - Minimal — transitions only, no flashy stuff
    - Subtle — micro-interactions, smooth page transitions, hover feedback
    - Rich — scroll-triggered animations, staggered reveals, parallax
    - Cinematic — full page transitions, complex orchestrated sequences
    - None — static, no animations
30. **Design References**: Are there 1-3 websites or apps whose visual style you admire? (URLs or descriptions — e.g., "Linear's clean dark UI", "Stripe's documentation style", "Notion's soft minimalism")
31. **Logo & Brand**: Do you have an existing logo/brand identity, or is that also being created from scratch? Any brand guidelines to follow?
32. **Design System Persistence**: Should we generate a `design-system/MASTER.md` file that locks down the visual rules for all pages? (Recommended: yes — this prevents visual drift as you build more pages.) The `frontend-design` skill will reference this file for every UI component it builds.

#### Category 7: Infrastructure, Deployment & Services (one at a time, skip if simple static project)

This category MUST be informed by Phase 0 context absorption. If `.claude/docs/deployment.md` was found, present the existing infrastructure as the default option. For Johan's projects, the standard infrastructure is the Noisy Cricket Linux cluster (live4.se) — always offer this as the primary option.

33. **Hosting**: Where does this run?
    - **Noisy Cricket Linux cluster (live4.se)** — Docker Swarm on Azure, 1 manager + 3 workers, private Docker registry, NFS shared storage, Nginx Proxy Manager reverse proxy, Let's Encrypt SSL *(this is the standard for Johan's projects — recommended unless there's a reason to deviate)*
    - Kubernetes (managed — AKS, EKS, GKE)
    - PaaS (Vercel, Railway, Fly.io, Render)
    - VPS (Hetzner, DigitalOcean, Linode)
    - On-prem / self-hosted
    - Other

    If Noisy Cricket is chosen, confirm: the deploy pipeline is ONE GitHub Actions workflow (`workflow_dispatch` with `confirm_deploy: "deploy"`) → build & test → stress test → Docker build → SCP to manager → push to private registry → `docker stack deploy`. The wizard should note that NFS directories and GitHub Secrets need to be set up (reference `.claude/docs/deployment.md` pattern).

34. **CI/CD**: Pipeline tool? (GitHub Actions ★ recommended for Noisy Cricket, GitLab CI, Azure DevOps)

    **CI minimalism is non-negotiable on solo projects** (per `.claude/rules/github-actions.md`): the Actions budget is a shared 3000-minute/month free tier, and all tests run locally before deploy per the Definition of Done. GitHub Actions gets the manually-triggered deploy workflow and nothing else — no CodeQL, no scheduled scans, no push-triggered test workflows, no per-spec CI. Do NOT generate extra workflows during inception, and make sure the generated CLAUDE.md's CI/CD section states this policy.
35. **Environments**: Which environments? (local + prod for MVP ★, or local + dev + staging + prod)
36. **Containerization**: Docker ★ (required for Noisy Cricket), Docker Compose for local dev?
37. **Domain & DNS**: Domain name? Subdomain on live4.se ★ (e.g., `projectname.live4.se`), or custom domain? SSL via Let's Encrypt (automatic with Nginx Proxy Manager).

38. **Third-Party Services & API Keys**: Which external services will this project need? Check all that apply and specify details:

    **Communication:**
    - [ ] **Email** — Mailjet ★ (already set up on Noisy Cricket), SendGrid, SES, SMTP, other?
    - [ ] **SMS** — Twilio, 46elks, other?
    - [ ] **Push notifications** — Firebase Cloud Messaging ★ (used in other projects), OneSignal, other?

    **AI & ML:**
    - [ ] **LLM / AI** — OpenAI API, Anthropic Claude API, Azure OpenAI, local models, other?
    - [ ] **Embeddings / Vector search** — OpenAI embeddings, Pinecone, Qdrant, pgvector, other?
    - [ ] **Image generation** — DALL-E, Stable Diffusion, other?

    **Payments & Billing:**
    - [ ] **Payments** — Stripe, Klarna, Swish, other?
    - [ ] **Invoicing** — Fortnox API ★ (used in ticket project), other?

    **Authentication (external):**
    - [ ] **BankID** — BankSignering.se API (used in hireflow)?
    - [ ] **OAuth providers** — Google, Microsoft, GitHub, LinkedIn?

    **Storage & CDN:**
    - [ ] **File storage** — Local NFS ★ (Noisy Cricket default), Azure Blob, S3, Cloudflare R2?
    - [ ] **CDN** — Cloudflare, Azure CDN, none for MVP?

    **Monitoring & Analytics:**
    - [ ] **Analytics** — Plausible, Umami, Google Analytics, PostHog?
    - [ ] **Uptime monitoring** — UptimeRobot, Better Stack, Pingdom?

    **Other:**
    - [ ] **Maps** — Google Maps, Mapbox, OpenStreetMap?
    - [ ] **Calendar** — Google Calendar API, Microsoft Graph?
    - [ ] **Social** — LinkedIn API, Slack API, Discord?
    - [ ] Other: _____

    For each selected service, note: is this needed for MVP or v1.0+? This determines which secrets need a 1Password item and a Swarm secret at deploy time.

39. **Secrets Management**: How will API keys and secrets be managed?
    - 1Password vault → Swarm secrets mounted as files ★ (standard for Noisy Cricket; `op run` locally, see `.claude/docs/security.md` § Secrets)
    - GitHub Secrets for CI/CD credentials only (SSH deploy key, notification keys)
    - Azure Key Vault / AWS Secrets Manager
    - `.env` files (local dev only)
    - Other

#### Category 8: Quality & Workflow (one at a time)

40. **Testing Strategy**: Unit, integration, E2E? Minimum bar for MVP?
41. **Monitoring**: Logging, metrics, error tracking? (Sentry, Datadog, Grafana, Application Insights)
42. **Backup Strategy**: Database backups? RPO/RTO requirements?
43. **Git Workflow**: Branch naming convention? Commit message format? PR process?
44. **Definition of Done**: When is a feature "done"? (tests pass, E2E pass, visually verified, etc.)

#### Category 9: Constraints & Risks (ask last)

45. **Timeline**: When is MVP needed? When is v1.0?
46. **Team**: How many developers? Experience levels?
47. **Budget**: Hosting budget? Third-party service budget?
48. **Compliance**: GDPR, HIPAA, SOC2, PCI-DSS, or none?
49. **Existing Systems**: Replacing or extending something? Migration needed?
50. **Biggest Risk**: What's most likely to go wrong?

### Phase 3: Generate Foundation Documents

After ALL categories are answered, generate the three foundation documents. Read any existing files first to avoid overwriting content that should be preserved.

#### 3A: Generate `.specify/memory/constitution.md`

Create the directory structure if needed: `mkdir -p .specify/memory/`

Follow this exact format (modeled on the user's existing constitutions):

```markdown
<!--
  Sync Impact Report
  Version change: 0.0.0 → 1.0.0 (initial ratification)
  Added principles:
    - I. [First Principle Name]
    - II. [Second Principle Name]
    [... list all principles]
  Added sections:
    - Technical Constraints / Technology Stack
    - Integration Strategy (if applicable)
    - Development Workflow
    - Governance
  Templates requiring updates:
    - .specify/templates/plan-template.md — ✅ no changes needed (generic)
    - .specify/templates/spec-template.md — ✅ no changes needed (generic)
    - .specify/templates/tasks-template.md — ✅ no changes needed (generic)
  Follow-up TODOs: none
-->

# [Project Name] Constitution

## Core Principles

### I. [First Principle]

[2-4 sentences explaining the principle in concrete, actionable terms.
Use MUST/MUST NOT/SHOULD/MAY language. Be specific — reference
actual technologies, patterns, and constraints from the interview.]

### II. [Second Principle]

[Continue for each principle — aim for 5-9 numbered principles.
Each one is a decision that constrains future development.]

[... more principles ...]

## Technology Stack

- **Backend**: [language + framework + key libraries]
- **Frontend**: [framework + CSS + component library]
- **Database**: [engine + access pattern (ORM/raw)]
- **Hosting**: [platform + specifics]
- **Repository**: [GitHub URL if known]

## Integration Strategy (if applicable)

Priority integrations (in order):
1. [Most critical integration]
2. [Next]
3. [Next]

All integrations via well-defined API interfaces. No tight coupling to external providers.

## Development Workflow

- Features specified via speckit: spec.md, plan.md, tasks.md
- Branch naming: `NNN-feature-name` (or decided convention)
- Commit messages: `<type>: <description>` (in decided language)
- All implementations verified with [build + test commands for the chosen stack]
- [Frontend verification approach]
- [Testing requirements from interview]

## Governance

This constitution governs all feature development in the [project name]
project. Amendments require:
1. Description of the change and rationale
2. Update to this file with version increment
3. Review of dependent templates for consistency

Versioning follows semantic versioning:
- MAJOR: principle removal or incompatible redefinition
- MINOR: new principle or material expansion
- PATCH: clarification or wording fix

All implementation plans MUST include a Constitution Check section
verifying compliance with these principles.

**Version**: 1.0.0 | **Ratified**: [today's date] | **Last Amended**: [today's date]
```

#### 3B: Generate/Update `CLAUDE.md`

If `CLAUDE.md` already exists, use the Edit tool to surgically update the `<!-- PROJECT-SPECIFIC -->` or `# PROJECT-SPECIFIC` section. Do NOT overwrite the rest of the file.

If `CLAUDE.md` doesn't exist, create a FULL CLAUDE.md following the established pattern from the user's other projects. The reference is this template repository's own `CLAUDE.md` (Phase -1's sync brought it in; else https://raw.githubusercontent.com/johanolofsson72/Claude/main/CLAUDE.md). Where it and the skeleton below differ, the template's `CLAUDE.md` wins for every section outside `# PROJECT-SPECIFIC`. The skeleton has these sections:

> **STACK-AWARE TESTING (READ THIS BEFORE FILLING THE TEMPLATE BELOW).** The template below is written for a web/.NET project where "tests" = Playwright browser tests + `dotnet test`. If the frontend answer (Q13) or the native-mobile answer (Q22) makes this a **native mobile** project — **React Native / Expo OR Flutter** — a browser does not exist, so Playwright/browser-test wording is wrong and will produce a project that can never satisfy its own Definition of Done. In that case, everywhere the template says "browser tests / Playwright" you MUST substitute the native equivalents for the chosen framework:
> - **React Native / Expo:** Maestro flows (E2E) + React Native Testing Library (component) on the `jest-expo` runner. Commands: `npx tsc --noEmit`, `npm test`, `maestro test .maestro/`.
> - **Flutter:** `flutter test` (unit + widget) + `integration_test` + **Patrol** (native E2E: permissions, deep links, lifecycle). Commands: `flutter analyze`, `flutter test`, `flutter test integration_test/` / `patrol test`.
> - **Neither uses** Playwright or `dotnet test`.
> - **Reference docs:** point the testing rows at `.claude/docs/testing.md` and `.claude/docs/spec-testing-checklist.md` as usual, but ensure those files hold the **mobile** content (the wizard's Phase -1 sync installs `testing-mobile.md` → `testing.md` for native projects per sync-prompt Step 7c; the mobile doc carries both a React Native and a Flutter section).
> - **`/tla`** still applies for non-trivial state machines; it is runtime-agnostic.
>
> Decide web-vs-mobile ONCE here, then fill the whole template consistently. Do not emit a mobile project that still says "Playwright" anywhere.
>
> **Reconcile the testing docs (mobile projects only).** Phase -1's sync ran BEFORE the interview revealed the stack, so it may have installed the web `testing.md` by default. If this is a native mobile project (React Native / Expo OR Flutter) and `.claude/docs/testing.md` still contains web/Playwright content (grep it for `dotnet`/`Playwright`/`browser`), perform the Step 7c mobile swap now:
> 1. `curl -sL https://raw.githubusercontent.com/johanolofsson72/Claude/main/.claude/docs/testing-mobile.md` → write to `.claude/docs/testing.md`
> 2. `curl -sL …/spec-testing-checklist-mobile.md` → write to `.claude/docs/spec-testing-checklist.md`
> 3. Write `.claude/.sync-stack` with the line `testing=mobile` so `/project-update` never re-stamps the web docs over it.

```markdown
# CLAUDE.md

## Critical rules (READ FIRST)

**(BLOCKING)** rules are enforced by hooks and by the Definition of Done. The rest are strong defaults.

- Read the code first. Base conclusions on evidence, and read the relevant files before answering about the codebase.
- Use Edit for surgical changes. Follow existing patterns. Verify with [BUILD COMMAND] + [TEST COMMAND] before claiming done.
- **(BLOCKING)** Non-trivial work runs the full pipeline as one task, with no permission stops between phases. → `.claude/rules/feature-pipeline.md`
- **(BLOCKING)** Every spec gets a 15–25 question interview in `<spec-dir>/interview.md` before `clarify`, AUTO-answered by default. → `.claude/rules/spec-interview.md`
- **(BLOCKING)** Before feature work, consult `specs/INDEX.md` and work the next unchecked spec end to end. → `.claude/rules/spec-register.md`
- **(BLOCKING)** A finding is recorded, not rowed (`scripts/finding.sh --add`). → `.claude/rules/carve-budget.md`
- **(BLOCKING)** Keep the scenario map `specs/SCENARIOS.md` current; a gap starts a scenario interview. → `.claude/rules/scenarios.md`
- **(BLOCKING)** Invoke the `frontend-design` skill before writing any UI code (HTML, CSS, JS, React Native or Flutter widgets).
- **(BLOCKING)** Run generated human-facing text (docs, commits, PRs, email, README) through the `humanizer` skill.
- **(BLOCKING)** Test 100% of implemented functions in [browser tests (Playwright) | Maestro flows + React Native Testing Library — pick per the stack-aware note above], with a destructive suite sized per function. [Adapt testing rules based on interview answers about testing strategy]

## Execution mode

### Autonomous mode

- Act immediately without waiting for confirmation.
- Missing information is not a blocker — make reasonable assumptions and continue.
- Errors should be handled and fixed independently.
- Ask only about architecture or requirement interpretations that cannot reasonably be assumed.
- **Max 3 attempts per problem** — if the same approach fails 3 times, run `/clear` and try a completely different strategy with a better prompt.

### Anti-stall rule

With no clear task, pick the most likely one and act.

### Hook recovery rule

When a hook stops continuation or gives feedback: acknowledge it, handle it (fix it, or explain why it does not apply), and keep working. Never stop silently.

### Interview pattern

Larger features get a spec before coding, with its interview (AUTO by default; the developer answers only escalated and overflow questions, `.claude/rules/spec-interview.md`).

## Priority order

1. **Security**
2. **Correctness** — the code must do the right thing
3. **Simplicity** — minimum necessary complexity
4. **Readability** — clear code over clever code
5. **Performance** — optimize only when needed

# PROJECT-SPECIFIC

## Project description

**[Project Name]** [is/does what — from elevator pitch].
Core flow: **[primary user flow from interview]**

**GitHub**: [URL if known]

### Why this exists

- [Problem 1 from interview]
- [Problem 2]
- [Problem 3]
- Build for real-world use, not theoretical perfection

### Design principles

1. **[Principle 1]** — [one-line summary from constitution]
2. **[Principle 2]** — [one-line summary]
[... map from constitution principles ...]

## Language

- Communicate in **[language]** in conversations, commit messages, and documentation.
- Code, variable names, and technical terms are written in **[language]**.
- Comments in code are written in **[language]**.

## Tech stack

- **[Backend tech]** — backend
- **[Frontend tech]** — frontend
- **[Database]** as database
- **Hosting**: [hosting target]

### Integrations

- [Integration 1]
- [Integration 2]
[... from interview ...]

## CI/CD and deployment

[Deployment details from interview. Reference .claude/docs/deployment.md if it exists.]

## Workflow

### Complexity assessment

- **Trivial** (one file, obvious fix) → do it, and say so in the first sentence
- **Anything that touches 2+ files, adds a function or changes behaviour** → the pipeline (`.claude/rules/feature-pipeline.md`), which explores and plans first

### Plan → Implement → Verify

1. **Explore** — read existing code, understand patterns and dependencies.
2. **Plan** — for medium/complex: use Plan Mode (Shift+Tab) to write a plan before implementation.
3. **Implement** — switch to Normal Mode, write code according to the plan. Follow existing patterns.
4. **Verify** — run all tests, typecheck, confirm everything works.
5. **Commit** — commit in [language]: `<type>: <description>` (feat/fix/refactor/test/docs/style/chore). Details in `.claude/docs/git.md`

## Verification and grounding

> Giving Claude ways to verify its own work is the single most important measure for quality. — Anthropic Best Practices

- Read the relevant files before answering about the codebase.
- Run tests after every implementation.
- Run individual tests over the full suite for faster feedback.

### Definition of "implemented"

Never say something is "implemented" or "done" until:

1. This spec's scenarios are in `specs/SCENARIOS.md` and marked `✓ validated` — observed actually working at runtime (real behaviour, not a stub), all four states proven: success, a specific visible error message (never silent), empty, loading. Validate prerequisite scenarios first; a broken prerequisite is a hard stop. A gap starts a scenario interview (`.claude/rules/scenarios.md`).
2. **Unit + integration tests** pass (`[TEST COMMAND]`) — both layers; integration is where AI code most often breaks. **Property-based tests** for wide-input logic.
3. All **E2E tests** pass (`[E2E COMMAND]`) — Playwright for web/.NET, **Maestro flows** for React Native / Expo, **Patrol / integration_test** for Flutter.
4. For UI features: **functional coverage** (1 test per function) + a **destructive suite per interactive function sized to its input domain** (toggle ~3 → multi-step/auth ~20-30+, NOT a flat quota) + **visual-regression** baselines for key states. For mobile the attack categories include lifecycle and permissions — see `.claude/docs/spec-testing-checklist.md`.
5. **Mutation kill rate** on the changed critical module(s) meets target (~80%; Stryker.NET web / StrykerJS mobile; nightly/on-demand, NOT per-push CI). The gate is the kill rate, not the test count.
6. For UI features: **TLA+ formal verification** has been run (`/tla`) — runtime-agnostic, applies to web and mobile alike.
7. **Validated locally before deploy** — full suite green AND the app runs in local dev and in Docker (`docker compose up`); you ship the container, so prove the container works.
8. For web: **visually verified** in the browser. For mobile: **visually verified** on a simulator/emulator or device. The code is assessed as **fully functional**.

If tests cannot be run (missing infrastructure), clearly inform about this.

## Context management

- On compaction, keep the modified files, verbatim error messages, debugging steps and test commands.
- Use subagents for exploration and research — keep the main context clean.
- Use `/clear` between unrelated tasks.
- Use `/compact <focus>` for controlled compaction.
- Break down large tasks into discrete subtasks.

## Commands

```bash
[BUILD COMMAND]                           # Build the project
[TEST COMMAND]                            # Run unit tests
[RUN COMMAND]                             # Run the application
[E2E COMMAND]                             # Playwright E2E tests
[SINGLE TEST COMMAND]                     # Single test
bash scripts/project-freshness.sh         # Freshness pass: trufflehog + key-shape scan + dependency audits (report-first; --fix to remediate)
```

Adapt these based on the chosen tech stack:
- .NET: `dotnet build`, `dotnet test`, `dotnet run --project src/[Name]`, E2E `dotnet test --filter "Category=UI"` (Playwright)
- Node.js: `npm run build`, `npm test`, `npm run dev`
- Python: `python -m build`, `pytest`, `python manage.py runserver`
- Go: `go build ./...`, `go test ./...`, `go run .`
- **React Native / Expo: `npx tsc --noEmit` (typecheck), `npm test` (jest-expo unit + RNTL), `npx expo start` (run), E2E `maestro test .maestro/` — NO Playwright, NO `dotnet`**
- **Flutter: `flutter analyze` (lint), `flutter test` (unit + widget), `flutter run` (run), E2E `flutter test integration_test/` / `patrol test` — NO Playwright, NO `dotnet`**

## Principles

- **YAGNI** — only build what is needed now. Three similar lines > premature abstraction.
- **Fail fast** — clear error messages with context. Never silent fallbacks.
- **DX** — code should be readable without comments. Good naming is usually enough.

## Reference files (loaded on demand)

Read these when you need them, never all upfront:

- **New project start** or architecture questions → `.claude/docs/project-template.md`
- **Code style, naming, forbidden patterns** → `.claude/docs/conventions.md`
- **Security questions** (SQL injection, XSS, secrets) → `.claude/docs/security.md`
- **Git commit/branch/PR** → `.claude/docs/git.md`
- **Hooks, subagents, plugins, sessions** → `.claude/docs/workflows.md`
- **Creating new agents** → `.claude/docs/agents-templates.md`
- **Skills, SKILL.md format, Agent Skills standard** → `.claude/docs/skills.md`
- **Tests (xUnit, Playwright)** → `.claude/docs/testing.md`
- **Spec testing checklist (destructive tests)** → `.claude/docs/spec-testing-checklist.md`
- **Deploy, Docker, CI/CD** → `.claude/docs/deployment.md`
- **Stress testing (pre-deploy)** → `.claude/docs/stress-testing.md`

## File organization

- **`scripts/`** — Hook scripts (tla-hook.sh, allium-hook.sh, test-coverage-hook.sh, tlc-cleanup.sh).
- **`.claude/skills/`** — Project skills with SKILL.md + speckit skills. Follows the Agent Skills standard (agentskills.io).
- **`.claude/agents/`** — Subagents. Supports `isolation: worktree`, `background`, `hooks` in frontmatter.
- **`.claude/rules/`** — Rules auto-loaded every session. Supports path-scoping with YAML frontmatter.
- **`.claude/docs/`** — Reference material loaded on demand. Reference WITHOUT `@` prefix to avoid auto-expansion.
- **`CLAUDE.local.md`** — Personal project settings not committed (auto-gitignored).

## Iterative improvement

- If the same mistake repeats: suggest a new rule for CLAUDE.md or a hook that prevents it.
- Every code review comment is a signal that the agent lacked context — update CLAUDE.md.
- Edit existing files over creating new ones.
- Keep this file focused — if an instruction can be removed without Claude making errors, remove it.
```

#### 3C: Generate `design-system/MASTER.md` (if user said yes to Q32)

If the user wants a persisted design system, create `design-system/MASTER.md` with the visual decisions from Category 6. This file is the single source of truth that the `frontend-design` skill references when building any UI component.

**Decompile any brand/vibe reference FIRST (per `.claude/rules/design-references.md`).** If the user described the look as a feeling or a brand ("the feeling of Spotify", "like Linear", "Apple-clean") in Q25/Q30, do NOT store it as a vague note — compile it into the concrete primitives below: look it up in `.claude/docs/design-reference-library.md` (instant for ~12 known aesthetics), `WebFetch` the live brand for anything not seeded, and run a short `AskUserQuestion` if the reference is multi-faceted (Spotify = dark immersion *and* green energy *and* dense browse — ask which). Fill the Color/Typography/Layout/Motion/Mood/Anti-pattern sections with the decompiled hex values and named fonts, and record the source reference. The whole point: `frontend-design` must inherit primitives, never a feeling.

**Then, optionally, draw it (`/design`).** Once MASTER.md holds real primitives, `/design` (bundled skill, research preview) can
render several editable artboards for the first screen or two on a single canvas, reading the tokens you just wrote so the options
come back in the project's own colors and type rather than a stock palette. Offer it when Category 6 left the *layout* open — the
user picked a mood and a palette but nobody has seen a screen yet. It is optional and never a gate: the artboard is a pick, and the
picked screen is still built through the `frontend-design` skill (BLOCKING, per the frontend rule, `frontend.md`). Do not run it before
MASTER.md exists — artboards drawn against an empty design system inherit nothing.

If the project will grow a real component library, mention `/design-sync` as the later two-way bridge between that library and a
Claude Design design-system project (incremental, plan-gated, one component at a time; re-run after tokens move — it does not watch
the repo). Do not run it during inception; there is nothing to sync yet.

```markdown
# [Project Name] — Design System

> Generated by Project Inception Wizard on [date]

## Design Personality

**Tone**: [chosen personality from Q25]
**Mood**: [expanded description — 2-3 sentences painting the picture]

## Color Palette

**Mode**: [light only / dark only / both with toggle]
**Primary**: [color + hex]
**Secondary**: [color + hex]
**Accent**: [color + hex]
**Background**: [color + hex]
**Surface**: [color + hex]
**Text**: [color + hex]
**Muted text**: [color + hex]
**Border**: [color + hex]
**Error/Success/Warning**: [colors + hex]

**Direction from interview**: [raw answer from Q26]

CSS variables:
```css
:root {
  --color-primary: #...;
  --color-secondary: #...;
  --color-accent: #...;
  /* ... etc */
}
```

## Typography

**Feel**: [from Q27]
**Heading font**: [font name] — [why it fits the personality]
**Body font**: [font name] — [why it pairs well]
**Monospace** (if needed): [font name]
**Scale**: [e.g., "1.25 major third" or "1.333 perfect fourth"]

**Google Fonts import** (if applicable):
```html
<link href="https://fonts.googleapis.com/css2?family=...&display=swap" rel="stylesheet">
```

**Anti-patterns**: NEVER use [list fonts the user hates or generic AI defaults like Inter, Roboto, Arial]

## Visual Assets

**Strategy**: [from Q28]
**Icon set**: [chosen icon library — e.g., Lucide, Heroicons, Phosphor]
**Photo sources**: [if applicable — Unsplash, branded photography, etc.]
**Illustration style**: [if applicable — hand-drawn, vector, isometric, etc.]

**Rules**:
- NEVER use emojis as UI icons — always use SVG from [chosen icon set]
- [Stock photo rules — e.g., "prefer diverse, natural-looking people, no cheesy corporate handshakes"]
- [Illustration rules if applicable]

## Animation & Motion

**Philosophy**: [from Q29]
**Transition duration**: [e.g., "150-300ms for micro-interactions"]
**Easing**: [e.g., "cubic-bezier(0.4, 0, 0.2, 1) for standard, cubic-bezier(0, 0, 0.2, 1) for deceleration"]
**Page transitions**: [approach]
**Hover states**: [approach — e.g., "color/opacity changes, no scale transforms that shift layout"]
**Scroll animations**: [approach]
**Reduced motion**: MUST respect `prefers-reduced-motion`

## Layout Principles

**Max content width**: [e.g., "max-w-7xl (1280px)"]
**Spacing scale**: [e.g., "Tailwind default: 4px base unit"]
**Grid system**: [e.g., "12-column grid, 24px gutter"]
**Navbar style**: [e.g., "floating with top-4 spacing" or "fixed full-width"]
**Responsive breakpoints**: [e.g., "375px, 768px, 1024px, 1440px"]

## Design References

[From Q30 — URLs or descriptions of admired designs and what specifically to take from each]

1. [Reference 1] — take: [specific aspect]
2. [Reference 2] — take: [specific aspect]
3. [Reference 3] — take: [specific aspect]

## Brand Identity

[From Q31 — existing logo, brand guidelines, or "to be created"]

## Anti-Patterns (NEVER do these)

- Never use generic AI-generated aesthetics (overused fonts, purple gradients on white)
- Never use emojis as icons
- Never mix different icon sets
- Never use inline styles
- [Project-specific anti-patterns from interview]

## Pre-Delivery Checklist

Before delivering any UI code, verify:
- [ ] Colors match this design system (no ad-hoc hex values)
- [ ] Typography uses the specified fonts only
- [ ] Icons are from [chosen icon set] only
- [ ] Hover states provide feedback without layout shift
- [ ] Light/dark mode contrast passes 4.5:1 minimum
- [ ] Responsive at all specified breakpoints
- [ ] `prefers-reduced-motion` respected
- [ ] No emojis used as icons
```

If the `ui-ux-pro-max` skill is available, also run the design system generator to get data-driven recommendations:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "[product type] [industry] [style keywords from Q25]" --design-system --persist -p "[Project Name]"
```

Merge its output into the MASTER.md, using the interview answers as overrides where they conflict with the automated recommendations.

#### 3D: Generate `PROJECT-BRIEF.md`

This is the human-readable version — for sharing with stakeholders, README, onboarding docs.

```markdown
# [Project Name]

> [Elevator pitch]

## Problem

[Problem statement from interview]

## Target Users

[User personas from interview]

## Core Modules

[Module descriptions with planned features]

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | ... | ... |
| Frontend | ... | ... |
| Database | ... | ... |
| Hosting | ... | ... |
| Auth | ... | ... |
| CI/CD | ... | ... |

## Architecture

[High-level architecture description with Mermaid diagram if appropriate]

## Key Decisions

[Numbered list of the most important architectural/technical decisions and WHY]

## Timeline

[MVP date, v1.0 date, key milestones]

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| ... | ... | ... | ... |

## Open Questions

[Anything unresolved from the interview]
```

#### 3D-2: Seed the scenario map (`specs/SCENARIOS.md`)

The inception interview IS the project's first scenario interview — turn the core modules and use cases the user described (Categories 1, 4, 5) into the first **diagram-led** scenario map. This gives the project a real, surveyable exploded view to grow from instead of a blank page, and it's the source the functional inventories and destructive suites derive from for every future spec (see `.claude/rules/scenarios.md`). The map is diagram-led: always seed the project **use-case diagram** + a **user-flow flowchart** for the first feature + the SC-id table (Mermaid, so it renders in GitHub/VS Code/Obsidian). Journey map / wireflow / storyboard are added later on-demand.

Create `specs/SCENARIOS.md`:

````markdown
# Scenario map

Living, surveyable exploded view of every scenario. Append as the project grows; never reuse an SC-id.
Status:  ☐ mapped  ·  ◐ tested  ·  ✓ validated (proven to actually work at runtime)
Gap or drift → run the scenario interview (.claude/rules/scenarios.md) before writing code.

## Use case overview (who can do what)

```mermaid
flowchart LR
  actor1([Primary role]); actor2([Other role])
  actor1 --> uc1([Core use case 1])
  actor1 --> uc2([Core use case 2])
```

## Actor: [primary role from interview]

### Feature: [first core module]   (spec: 001-[slug])

User flow:

```mermaid
flowchart TD
  A[Entry] --> B{Decision?}
  B -- ok --> C[Success outcome · SC-001]
  B -- bad --> D[Specific error message · SC-004]
```

| ID     | Type        | Scenario                          | Expected outcome                | Status |
|--------|-------------|-----------------------------------|---------------------------------|--------|
| SC-001 | happy       | [main success path]               | [outcome]                       | ☐      |
| SC-002 | edge        | [a boundary the user mentioned]   | [outcome]                       | ☐      |
| SC-003 | adversarial | [double-submit / tamper / race]   | [safe outcome]                  | ☐      |
| SC-004 | error       | [network / auth / timeout]        | [specific visible message]      | ☐      |

## Scenario history
- [today] — seeded from inception interview ([N] features mapped)
````

Seed the use-case diagram + a user-flow flowchart + at least the happy + one edge/error row per core module (all `☐ mapped` at inception). Note in the Phase 4 summary that the map was seeded as a diagram-led artifact, that every future spec extends it (a gap triggers an interview, not a guess), and that scenarios only reach `✓` once observed working at runtime with all four states (success / specific error / empty / loading).

#### 3D-3: Write the spec register (`specs/INDEX.md`) — MANDATORY, no project leaves this wizard without one

**This is the step the wizard used to skip, and skipping it broke the very next session.** `.claude/rules/spec-register.md` requires the register to exist before any development, and `scripts/spec-register-guard-hook.sh` **hard-denies the first source-code edit** until it does. So a wizard that ends without a register hands the developer a project whose first edit gets blocked — and the register then gets reconstructed by an agent that no longer has a single interview answer in context. You are the only run that knows the core modules, the tech stack, the auth model, and the risk surface. Write the register here, while you still know all of it.

Derive the rows from what the interview already told you:

1. **One row per core module** from Category 1 (vision / core modules) and the features you just seeded into `specs/SCENARIOS.md`. The register and the scenario map must agree — every feature with SC-ids gets a row.
2. **Order by dependency, not by excitement.** Auth and the data model come before the screens that need them. If module B cannot be demonstrated without module A, A gets the lower number.
3. **Triage each row's track** per `.claude/rules/specs.md`: `full` (new entity / state machine / concurrency / new API surface), `light` (single-actor UI, CRUD, search/filter), `spec-only` (refactor, config, docs).
4. **Tag `[hardened]`** per `.claude/rules/spec-hardening.md` — auth/authorization, payments, PII or secrets, file upload/parsing, a new external API surface, a full-track state machine, a new entity, or ≥6 files. Category 4 (auth/multi-tenancy) and Category 7 (infrastructure/integrations) answers are where these usually hide. When in doubt, tag it: hardening only ever adds verification.
5. **Insert an `H1` integration-hardening checkpoint row after the 5th spec row**, per the every-5 cadence. Add `H2` after the 10th if the register is that long.
6. **Add the standing `T0 — harness-defects` row** at the end, per `.claude/rules/carve-budget.md`. It is where a defect in `.claude/**`, `scripts/**`, a hook or a skill gets *pointed at* — the fix itself lands in the template repo and arrives by sync. Without this row those defects land on the product register and compete with the product: agentcrm accumulated twenty of them (`S1`–`S20`) on a property CRM's register, none of which ship anything to a broker.

```markdown
- [ ] T0 — harness-defects — standing — points at the template rows currently blocking this project; never carved from
```

Create `specs/INDEX.md`:

```markdown
# Spec register

Order of execution. Tick when done. Append new specs to the end unless renumbering is justified.

## Specs

- [ ] 001 — [slug] — full track [hardened] — [one-line goal from the interview]
- [ ] 002 — [slug] — light track — [one-line goal]
- [ ] 003 — [slug] — full track — [one-line goal]
- [ ] 004 — [slug] — light track — [one-line goal]
- [ ] 005 — [slug] — full track — [one-line goal]
- [ ] H1 — integration-hardening — checkpoint — full-system regression + security sweep after spec 005

## Register history

- [today's date] — initial register seeded from the inception interview ([N] specs identified)
```

Rules for the rows: 3-digit ids, kebab-case slugs that will match the spec folder names, one line each. The one-line goal is a goal, not a requirement — the requirement lives in the spec that `/speckit-specify` will write later. Keep the history entry to **one line** (`.claude/rules/spec-register.md` → "Keep the register lean"); a paragraph here gets re-read on every spec for the life of the project.

Then commit it with the other foundation documents so the project's first session opens on a real register:

```bash
git add specs/INDEX.md specs/SCENARIOS.md && git commit -m "chore: seed spec register and scenario map from inception interview"
```

Do NOT start spec 001 in this session — the speckit skills are not loaded yet (see the Phase 4 restart note). The register is the handoff.

#### 3E: Scaffold the native E2E test harness (MOBILE PROJECTS ONLY — React Native / Expo · Flutter)

> Skip this subsection entirely for web/.NET projects — they already get the Playwright harness from the template sync. This subsection exists so a mobile project starts with a real destructive-flow directory instead of a blank page, giving Maestro/Patrol exact parity with web's Playwright setup. The destructive scenarios (sized per interactive UI function from its input domain — not a flat quota, not one batch per spec — per `.claude/docs/spec-testing-checklist.md`, which on a mobile project is the mobile variant) live HERE, as native E2E flows — NOT as widget tests.

Determine the stack from the Phase 2 interview (Q22-23), then scaffold the matching harness:

**React Native / Expo → Maestro**

```bash
mkdir -p .maestro
```

Create `.maestro/example-destructive.yaml` as the copy-me template for every future destructive flow:

```yaml
# Maestro destructive flow — COPY THIS per destructive scenario, one file each, *-destructive.yaml.
# Parity with web: this is the mobile equivalent of a Playwright destructive spec.
# Run: maestro test .maestro/        (whole suite)
#      maestro test .maestro/example-destructive.yaml   (single flow)
appId: ${APP_ID}   # set to your app's bundle/package id, e.g. com.acme.app
---
- launchApp:
    clearState: true
# Category 2 (lifecycle): double-tap submit must create exactly one record
- tapOn: "Submit"
- tapOn: "Submit"
- assertVisible: "Saved"          # not "Saved (2)" — one record, not two
# Category 2 (process kill): kill mid-flow, relaunch, expect sane restore
- stopApp
- launchApp
- assertNotVisible: "corrupt"
# Category 6 (permissions): deny a permission and assert graceful degradation
# - tapOn: "Use my location"
# - # (deny at the OS dialog) → assert the manual-entry fallback is visible
```

If Maestro is not installed on the dev's machine, note it (do not hard-fail): `curl -fsSL https://get.maestro.mobile.dev | bash` (Windows: run under WSL or Git Bash). Confirm `@testing-library/react-native` + the `jest-expo` preset are wired for the functional-coverage layer.

**Flutter → Patrol / integration_test**

```bash
mkdir -p integration_test
```

Create `integration_test/example_destructive_test.dart` as the copy-me template:

```dart
// Patrol destructive flow — COPY THIS per destructive scenario, one test each.
// Parity with web: this is the mobile equivalent of a Playwright destructive spec.
// Run: patrol test            (native: permissions, deep links, lifecycle, hardware back)
//      flutter test integration_test/   (in-process integration)
import 'package:patrol/patrol.dart';

void main() {
  patrolTest('submit is idempotent under double-tap', ($) async {
    await $.pumpWidgetAndSettle(/* YourApp() */);
    // Category 2 (lifecycle): double-tap submit → exactly one record
    await $('Submit').tap();
    await $('Submit').tap();
    await $('Saved').waitUntilVisible();
    // Category 6 (permissions): deny at the native dialog, assert graceful fallback
    // await $.native.denyPermission();
    // Category 2 (hardware back): press OS back mid-flow, assert no data loss
    // await $.native.pressBack();
  });
}
```

Add Patrol as a dev dependency (`flutter pub add --dev patrol`) and note `dart pub global activate patrol_cli` + `patrol doctor` if not present. E2E in either framework needs a running iOS Simulator or Android emulator.

**Both frameworks:** the scaffolded directory is the home for the destructive flows mandated per interactive UI function (sized to each function's input domain, not a flat quota and not one batch per spec). State explicitly in the Phase 4 summary that this harness was created and that destructive coverage is a native-E2E (Maestro/Patrol) requirement, not a widget-test one.

#### 3F: Supply-chain defaults and browser install (ALL projects, after the stack is decided)

Run this from the project root once the Phase 2 stack answers exist. It writes release-age cooldowns for the package
managers the project actually uses and the NuGetAudit build gate, and only where they are absent. It never overwrites
a setting that is already there, so re-running it is safe. Print the `TODO` lines in the Phase 4 summary. Background:
`.claude/docs/supply-chain.md`. Mention in the summary that npm 12 blocks dependency install scripts until they are
approved (`npm approve-scripts`, then commit `package.json`), since esbuild, sharp and Expo native modules hit it on
the first install.

```bash
# Supply-chain defaults (.claude/docs/supply-chain.md). Writes a setting only where it is absent and
# never rewrites one that exists, so a second run changes nothing and prints "kept" for each file.
sc_find() { find . -maxdepth 4 -name "$1" -not -path '*/node_modules/*' -not -path '*/bin/*' \
  -not -path '*/obj/*' -not -path '*/.claude/worktrees/*' 2>/dev/null; }
# Append on a line of its own, even when the file lacks a trailing newline.
sc_add() { [ -s "$1" ] && [ -n "$(tail -c1 "$1")" ] && printf '\n' >> "$1"; printf '%s\n' "$2" >> "$1"; echo "wrote  $1: $2"; }
sc_find package-lock.json | while IFS= read -r f; do       # npm: unit is DAYS
  rc="$(dirname "$f")/.npmrc"
  grep -qs '^min-release-age' "$rc" && echo "kept   $rc" || sc_add "$rc" 'min-release-age=3'
done
sc_find pnpm-lock.yaml | while IFS= read -r f; do         # pnpm: unit is MINUTES
  ws="$(dirname "$f")/pnpm-workspace.yaml"
  grep -qs '^minimumReleaseAge:' "$ws" && echo "kept   $ws" || sc_add "$ws" 'minimumReleaseAge: 4320'
done
sc_find uv.lock | while IFS= read -r f; do
  d="$(dirname "$f")"
  if grep -qs 'exclude-newer' "$d/uv.toml" "$d/pyproject.toml"; then echo "kept   $d (exclude-newer set)"
  # A uv.toml would silently shadow an existing [tool.uv] table, so never create one beside it.
  elif grep -qs '^\[tool\.uv\]' "$d/pyproject.toml"; then echo "TODO   $d/pyproject.toml: add exclude-newer = \"3 days\" under [tool.uv]"
  else sc_add "$d/uv.toml" 'exclude-newer = "3 days"'; fi
done
if [ -f .github/dependabot.yml ] && ! grep -qs 'cooldown:' .github/dependabot.yml; then
  echo "TODO   .github/dependabot.yml: add a cooldown: block to each updates: entry (see supply-chain.md)"
fi
if [ -n "$(sc_find '*.csproj' | head -1)" ]; then
  if [ ! -f Directory.Build.props ]; then
    printf '%s\n' '<Project>' '  <PropertyGroup>' \
      '    <!-- NuGetAudit high/critical fail the build: .claude/docs/supply-chain.md -->' \
      '    <WarningsAsErrors>$(WarningsAsErrors);NU1903;NU1904</WarningsAsErrors>' \
      '  </PropertyGroup>' '</Project>' > Directory.Build.props
    echo "wrote  Directory.Build.props: NU1903;NU1904 as errors"
  elif grep -qs 'NU1904' Directory.Build.props; then echo "kept   Directory.Build.props"
  else echo "TODO   Directory.Build.props exists: add NU1903;NU1904 to <WarningsAsErrors> by hand"; fi
fi
```

**Playwright stacks only (web/.NET, or a Node frontend using `@playwright/test`):** the browsers are not installed with
the package, and tests fail without them. Once a test project exists and builds, install the browsers as the normal
user. On Linux the system libraries need root, and the template denies `Bash(sudo *)`, so that one line goes to the
developer instead of being run by Claude:

```bash
pwsh tests/<Name>.Tests.UI/bin/Debug/net*/playwright.ps1 install chromium     # .NET (no pwsh? dotnet tool install --global PowerShell)
npx playwright install chromium                                              # Node
# Linux only, run by the developer: sudo pwsh …/playwright.ps1 install-deps chromium   (or: sudo npx playwright install-deps chromium)
```

If no test project exists yet, put this under "Next steps" in the Phase 4 summary so spec 001 runs it.

### Phase 4: Summary

After writing all files, present:

```markdown
## Project Foundation Complete

**Files created/updated:**
- `CLAUDE.md` — [created/updated] ([X] sections, [Y] lines)
- `specs/INDEX.md` — spec register seeded: [N] specs + [M] hardening checkpoint(s), first row `001 — [slug]`
- `specs/SCENARIOS.md` — scenario map seeded (use-case diagram + [N] features + SC-id ledger)
- `.specify/memory/constitution.md` — [X] core principles ratified (v1.0.0)
- `design-system/MASTER.md` — visual identity locked down [if generated]
- `.maestro/` or `integration_test/` — native E2E destructive-flow harness scaffolded [mobile projects only; Maestro for RN, Patrol for Flutter — parity with web's Playwright]
- `PROJECT-BRIEF.md` — human-readable project description
- Supply-chain defaults — [files written / kept / TODO lines from 3F]

**Constitution Principles:**
I. [Principle name]
II. [Principle name]
[... list all ...]

**Tech Stack:**
- Backend: [choice]
- Frontend: [choice]
- Database: [choice]
- Hosting: [choice]

**Next steps:**
1. Review the constitution — are the principles correct and complete?
2. Review CLAUDE.md — does it match how you want Claude to work in this project?
3. Review `specs/INDEX.md` — is the spec order right, and are the tracks/`[hardened]` tags correct? Reordering is cheap now and expensive later.
4. **Exit this Claude session and start a new one** — speckit skills (`/speckit-specify`, `/speckit-plan`, `/speckit-tasks`, etc.) were installed during this session but Claude Code only loads skills at session start. They will not work as slash commands until you restart.
5. In the new session the SessionStart hook will announce spec `001` from the register. Work that one row end-to-end through the pipeline, then stop with the status summary — one spec per run, per `.claude/rules/spec-register.md`.

The project DNA is now in place. Every Claude session in this project will know the core principles, tech stack, and constraints before a single feature spec is written.

> **This inception interview scopes the PROJECT, not any single spec.** Every spec you build from the register will ALSO run its own **15–25 question anti-drift interview** (`.claude/rules/spec-interview.md`) right after `/speckit-specify`, recorded in `<spec-dir>/interview.md`. By default (AUTO mode) Claude auto-answers the base with the recommended option and only asks you the **overflow** questions when it judges a spec large/advanced — so routine specs cost you nothing while risky ones still get your eyes. (A project can force fully-human answering with `SPEC_INTERVIEW_MODE=manual`.) The `spec-interview-guard` hook hard-blocks source code until each spec's interview is done. That is by design: this wizard decides *what the project is*; the per-spec interview decides *exactly how each feature behaves* so the implementation can't drift from your intent.
```

## Rules

1. NEVER skip Phase -1 or Phase 0. Bootstrap and context absorption are mandatory.
2. **ONE QUESTION AT A TIME.** Use `AskUserQuestion` for each question. NEVER dump multiple questions in a single message. The only exception: 2-3 tightly related trivial sub-questions may be grouped (e.g., "Backend language + framework?"). This is a wizard, not a survey form.
3. NEVER skip a category in Phase 2. Every category must be asked even if the user seems eager to move on. However, individual questions within a category MAY be skipped if obviously N/A for the project scope (e.g., skip "Multi-tenancy?" for a static HTML game).
4. If Phase 0 found existing answers, present them as "I found X — is this still correct?" instead of re-asking.
5. If the user gives a one-word answer, probe deeper. "PostgreSQL" is not enough — ask about their experience level and specific needs.
6. If the user contradicts a previous answer or an existing file, point it out and ask them to clarify.
7. Offer your professional opinion when the user is unsure. Say "I recommend X because Y" — don't just list options.
8. Keep the tone professional but conversational. This is a consulting session, not a form.
9. If the project idea is fundamentally flawed, say so diplomatically and suggest pivots.
10. Track all answers internally so nothing is lost between conversation turns.
11. The constitution is the most important output. Each principle must be concrete, actionable, and use MUST/SHOULD/MAY language. Vague principles like "write clean code" are worthless — be specific.
12. CLAUDE.md must match this template repository's own `CLAUDE.md`, which is the reference (Phase 3B).
13. If `CLAUDE.md` already exists, use the Edit tool to surgically update only the project-specific section. Do NOT overwrite the rest of the file.
14. The constitution version always starts at 1.0.0 for a new project.
15. All dates in generated files must use the actual current date, not placeholders.
16. If sibling projects use the same stack, reference their patterns (e.g., "Reference `/Users/jool/repos/matchgrid/` for GitHub deploy patterns").
17. **NEVER finish without `specs/INDEX.md`** (Phase 3D-3). It is not optional and not "the next session's job" — `spec-register-guard` denies the first source edit without it, and you are the only run that holds the interview answers the rows are derived from. A wizard that ends with no register has handed the developer a blocked project.
