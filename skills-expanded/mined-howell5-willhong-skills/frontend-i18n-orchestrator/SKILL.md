---
name: frontend-i18n-orchestrator
description: "End-to-end i18n orchestration for frontend repositories. Use when a user wants to internationalize React/Vue/Next/Nuxt/Vite projects with minimal questions: auto-detect stack and current i18n state, ask only unresolved business decisions, migrate hardcoded strings to locale keys, localize formatting and routing/SEO, and enforce CI quality gates."
---

# Frontend I18n Orchestrator

## Overview

Internationalize frontend projects with an auto-first workflow:
1. Scan repository and infer facts.
2. Ask only business decisions that cannot be inferred reliably.
3. Execute migration in phases with verification gates.

Do not start bulk code edits before finishing detection and decision confirmation.

## Platform Compatibility

Use this skill in both Codex and Claude Code.

- In Claude Code, invoke with `$frontend-i18n-orchestrator` (or by selecting the skill in UI).
- In Codex, invoke the same skill name and follow the same workflow.
- Use the host platform's native shell/file tools for commands and edits.
- Resolve script paths relative to the skill directory first, then to repository root if copied locally.

## Workflow

### Step 1: Build i18n profile (no questions yet)

Run repository detection first.

Recommended command:

```bash
<skill_dir>/scripts/detect_i18n_profile.sh .
```

The script writes `i18n-profile.json` in repository root.

Detect at minimum:
- framework/runtime: React, Vue, Next, Nuxt, Vite
- package manager and lockfiles
- existing i18n libraries and locale files
- routing setup and locale routing hints
- SEO hints: `lang`, `hreflang`, canonical
- hardcoded string hotspots
- date/number/currency localization usage
- CI quality gate hints

### Step 2: Ask only unresolved decisions

Read `i18n-profile.json`, then ask only missing or ambiguous decisions.

Use question set from `references/question-flow.md`.

Never ask questions that are already confidently detected.

When presenting questions, start with a short auto-detection summary:
- what is certain
- what is ambiguous
- what decisions need user confirmation

### Step 3: Plan phased migration

Use framework-specific guidance from `references/framework-playbooks.md`.

Plan the migration with these phases:
1. Foundation: i18n library setup, locale structure, language switch, fallback behavior.
2. Migration: extract hardcoded UI strings and replace with translation keys.
3. Localization: dates, numbers, currency, pluralization, relative time.
4. Routing and SEO: locale routing, html `lang`, `hreflang`, canonical, sitemap.
5. Governance: lint/test/CI gates for missing keys and hardcoded regressions.

Prefer incremental slices (page/module by page/module) over big-bang rewrites.

### Step 4: Execute with safe checkpoints

For each phase:
1. apply minimal code changes
2. run project checks/tests
3. report changed files and remaining risk

If a phase introduces conflicts or uncertainty, stop and ask a targeted question.

### Step 5: Enforce quality gates

Run baseline validation:

```bash
<skill_dir>/scripts/validate_i18n_basics.sh .
```

Then integrate project-native checks (lint/test/build/CI) for:
- missing translation keys
- orphan keys
- hardcoded UI string regressions

Fail CI on configured strict rules after migration baseline is stable.

### Step 6: Produce delivery report

Always end with a concise report:
- detection summary and selected strategy
- implemented phases and touched files
- unresolved/needs-human-review items
- commands for ongoing verification

## Decision Rules

- Auto-detect first. Ask later.
- Ask only high-impact business choices.
- Never guess target locales.
- Prefer compatibility with existing stack conventions.
- Treat inconsistent existing i18n setups as an ambiguity and ask explicitly.

## Common Ambiguities (must ask)

- target locale list
- default locale and fallback policy
- URL strategy (`/en/...` vs subdomain vs domain)
- translation source strategy (placeholder, MT, human)
- rollout strategy (gradual vs all-at-once)
- strict CI enforcement timing

## Resources

- Question flow: `references/question-flow.md`
- Framework playbooks: `references/framework-playbooks.md`
- Claude Code usage: `references/claude-code-usage.md`
- Detection script: `scripts/detect_i18n_profile.sh`
- Baseline validation script: `scripts/validate_i18n_basics.sh`
