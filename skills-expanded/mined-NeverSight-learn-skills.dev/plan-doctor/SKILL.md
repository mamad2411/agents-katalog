---
name: plan-doctor
description: Reviews and reinforces engineering plans against a standard checklist before execution. Use this skill whenever the user enters Claude Code plan mode, asks Claude to "make a plan", "plan out", "outline an approach", "break this down", or otherwise drafts a multi-step engineering plan — even if they don't explicitly ask for review. Also use it when the user is about to start a complex coding task without an explicit plan, to make sure standards still apply. Checks dependency/runtime currency (latest LTS or current major), enforces agent team mode for parallel work, prettier/linter passing with zero errors as a completion gate, OpenAPI for multi-module APIs, design tokens for any UI/UX work, and markdown task lists for complex plans.
---

# Plan Doctor

A standards reviewer for engineering plans. When the user is planning work, this skill makes sure the plan meets a set of baseline requirements before execution begins.

## When this skill applies

Trigger when any of the following is true:

- The user is in Claude Code **plan mode** (Shift+Tab plan mode).
- The user asks Claude to "make a plan", "plan out X", "outline an approach", "break this down", "draft a roadmap", or anything similar.
- The user is starting a **complex, multi-step coding task** (3+ files, new service, new feature, refactor across modules), even if they didn't explicitly ask for a plan. In that case, propose a plan first and apply this skill.

For trivial single-file edits, bug fixes, or quick questions, this skill does not apply — don't impose ceremony on simple work.

## What to do

For every plan, run through the checklist below **before** presenting the plan to the user. Update the plan to comply with each item. If a check requires information you don't have (e.g., what versions exist), look it up — don't guess.

### 1. Dependency and runtime currency

Any dependency, runtime, language version, or framework mentioned in the plan must be on the **latest LTS or current major**. Examples of what "current" means as of writing — but **always verify, don't trust memory**:

- Node.js → latest Active LTS
- Python → latest stable minor (e.g., 3.13.x)
- Go → latest stable
- Rust → latest stable
- Java → latest LTS (21, 25, etc.)
- React, Next.js, framework majors → latest stable major

**How to verify:**
- Use `web_search` for "<tech> latest LTS" or "<tech> current version" — fast and authoritative.
- Use **Context7** (`resolve-library-id` then `query-docs`) when you need version-specific API guidance for a library, not just the version number.
- Don't rely on training data alone — versions change frequently.

If the user proposes an outdated version (e.g., "let's use Node 20"), call it out in the plan with the current recommended version and a one-line reason. Don't silently override — surface the swap so the user can confirm. If they have a hard constraint (legacy system, vendor lock), respect it but note the risk.

### 2. Agent team mode

The plan should explicitly say to use Claude Code's **agent team mode** when — and only when — there are **3 or more genuinely independent tracks of work** that could run in parallel without blocking each other (e.g., scaffolding a service + drafting an API spec + integrating two separate client modules). Add a line in the plan like:

> Use agent team mode: dispatch teammates for [parallel task A], [parallel task B], and [parallel task C].

**Don't force agent team mode** when:
- The plan has fewer than 3 independent tracks.
- The "parallel" tasks actually depend on each other and have to be sequential.
- The work is small or sequential by nature (e.g., a 4-step CRUD endpoint).

In those cases, just don't mention agent team mode at all — silence is fine. Don't add a note saying "I considered agent team mode but skipped it"; that's noise.

### 3. Prettier and linter as completion gate

Every plan that involves writing or modifying code must include this as an **explicit final step**, not an afterthought:

> **Completion gate:** run the project's formatter and linter. Both must pass with **zero errors** before the task is considered done.

**For existing projects: auto-detect what's already there.** Don't assume any specific tool. Inspect the repo for config files and `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Makefile` / `justfile` entries that point to a formatter, linter, or type checker. Use whatever the project already uses — even if it's not the current community favorite. Consistency with the project beats picking the "best" tool.

**For new projects (nothing to detect): verify what's current, don't assume.** The community-recommended formatter/linter for any language changes over time — what's standard today may be deprecated tomorrow. Before prescribing tools for a brand-new project:

- Use `web_search` to check what's currently recommended for the language (e.g., "best Python linter 2026", "current TypeScript formatter recommendation").
- Use **Context7** to check the actual tool's docs and recent activity — a tool with no commits in 2 years is a red flag.
- Cross-check against the language's official guidance if there is any (e.g., the Python steering council, the Go team's recommendations).

**Never hardcode a tool name from memory.** If a check says "use prettier" or "use black" purely because the skill or training data said so, that's a failure mode. Always verify.

**What goes in the gate:**
- A formatter (must produce zero diffs in `--check` mode).
- A linter (must produce zero errors; warnings are project-policy).
- A type checker, if the language has one and the project uses one (zero errors).

If a language has no widely-accepted standard tool, propose the most active maintained option after verifying — and flag in the plan that this is a current-best-guess.

### 4. OpenAPI for multi-module APIs

This applies **only** when:
- The project has APIs (HTTP/REST endpoints), AND
- More than one module either provides or consumes those APIs (e.g., backend + frontend + mobile, or service A + service B).

When it applies, the plan should specify:
- Maintaining an **OpenAPI spec** as the source of truth.
- **Generating or syncing** client/server code from the spec (e.g., `openapi-typescript`, `openapi-generator`, `oapi-codegen`, `orval`).
- Where the spec lives in the repo and which module owns it.

**Framework auto-generated specs count.** If the API is built with a framework that emits an OpenAPI spec for free (FastAPI's `/openapi.json`, NestJS Swagger module, Spring Boot springdoc, drf-spectacular, etc.), that satisfies "the spec exists" — you don't need to hand-author one. Just make sure the generated spec is the one consumers pull from, and wire codegen for the consumers.

For single-module projects or projects with no APIs, skip this check entirely — don't push OpenAPI where it adds no value. (FastAPI's auto-generated `/docs` is nice to have for a single-module service, but you don't need to mention it as a "standard applied".)

### 5. Markdown task list for complex plans

If the plan has **more than ~5 steps** or spans multiple files/modules/days, create a **markdown task list** (`- [ ] task`) and include it in the plan. The task list should:

- Live in the working directory or repo as an actual file (e.g., `TASKS.md`, `PLAN.md`, or under `docs/`). **Create the file** — don't paste the task list contents into the chat response.
- Get **updated as tasks complete** — flip `- [ ]` to `- [x]` and commit/save the change as you go.
- Be referenced explicitly in the plan with the file path: "I'll track progress in `TASKS.md` and update it after each completed step."

In the chat response, just mention that the file was created and link/reference it — don't duplicate the contents inline.

For short plans (≤5 steps), the inline plan is sufficient — don't create a file just to track 3 things.

### 6. Design tokens for UI/UX work

If the plan involves **any UI/UX work** — new screens, components, theming, redesigns, design system work, styling beyond trivial tweaks — the plan must include **generating or using design tokens** for consistency.

**What this means in practice:**
- Define tokens for color, typography, spacing, radii, shadows, motion (durations/easings), and z-index layers.
- Store them as the single source of truth — e.g., a `tokens.json` / `tokens.ts`, CSS custom properties in a `:root` block, a Tailwind theme config, or a Style Dictionary setup. Pick whichever fits the stack; just have one place tokens live.
- Reference tokens everywhere — components consume `var(--color-primary)` or `theme.colors.primary`, never hardcoded `#3B82F6`.
- If tokens already exist in the project, **extend them** rather than introducing parallel values. Audit first.

**When this applies:**
- New components, screens, or pages.
- Adding theming (dark mode, brand variants).
- Redesigns or visual refreshes.
- Building/modifying a design system or component library.

**When it doesn't:**
- Backend-only or CLI work.
- Tiny, isolated style tweaks (changing one button's padding) where introducing tokens would be over-engineering — but still prefer existing tokens if any exist.

For multi-module projects (e.g., web + mobile), tokens should be **shared across modules** where feasible — export them in a format both can consume (JSON via Style Dictionary is the standard play).

## How to present the reviewed plan

After running the checklist, present the plan to the user in this shape:

1. **The plan itself** — numbered steps, with the standards baked in (versions specified, agent team mode noted, completion gate at the end, OpenAPI step if applicable, task list referenced if applicable).
2. **A short "Standards applied" note** at the bottom — 2-4 bullets saying what you checked and any deviations you flagged for confirmation. Example:
   > **Standards applied:** verified Node 24 (current LTS) per latest, agent team mode for parallel scaffolding + tests, ruff+mypy as completion gate, OpenAPI skipped (single module).

Keep this note short — it's a receipt, not a lecture.

## What not to do

- Don't lecture the user about standards mid-plan — apply them silently and surface only the deviations.
- Don't impose OpenAPI, task files, or agent teams on small/simple work where they add overhead.
- Don't trust your training data for version numbers — always verify when versions matter.
- Don't block the user if they have a legitimate reason to deviate (legacy constraints, explicit choice). Note the deviation and proceed.
