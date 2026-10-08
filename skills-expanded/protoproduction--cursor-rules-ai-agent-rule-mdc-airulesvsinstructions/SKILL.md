---
applyTo: '**'
---

# AI Agent Rules

Canonical agent rules for this project. Keep the rule body mirrored across `docs/AIdocs/airules.mdc`, `.cursor/rules/ai-agent-rule.mdc/airulesVS.instructions.md`, `docs/AIdocs/copilot-instructions.md`, `.github/copilot-instructions.md`, and `AGENTS.md`.

## Orientation

- Project overview: `readme.md`
- Repo router skill: `.agents/skills/webgamedev-gram/SKILL.md`
- Domain glossary: `docs/CONTEXT.md`
- Implementation status: `docs/AIdocs/AIDescriptions_coregame.md`
- Ownership map: `docs/PROJECT_INFO.md`

Before non-trivial work, read the smallest relevant subset of those files. Do not assume planned folders or services exist; check the repo first.

## Plugin And Skill Precedence

- Repo-local skills under `.agents/skills/` are authoritative for this project.
- When a repo-local skill overlaps with a plugin-provided skill, use the repo-local skill.
- Do not use generic plugin workflows such as Game Studio or default Superpowers when `.agents/skills/webgamedev-gram/SKILL.md` routes to a local specialist instead.
- Use plugins for their tools and external integrations, such as GitHub, Gmail, Google Calendar, browser testing, or frontend tooling, when the task actually needs those capabilities.
- Use plugin-provided skills only when the user explicitly asks for that plugin workflow or no repo-local skill covers the task.

## Response Start

Start user-facing work with:

```text
AI check: <1-5> - <brief reason>
```

Use `1` for clear, low-risk work and `5` for broad, ambiguous, or high-risk work.

## Workflow Rules

- Do not commit changes unless the user explicitly asks.
- Do not start `npm run dev` unless the user asks.
- Do not run `npm run build` by default; run it only when asked or when the change risk justifies it.
- Do not run tests, lint, typecheck, or `git diff --check` after every small edit. Use focused verification when finishing meaningful work, for complex changes, or when requested.
- For version history, follow `docs/versionlog.md` and `.agents/skills/webgamedev-gram/SKILL.md`: versionlog updates happen after commits exist and claims must be tied to verified evidence.
- After major project updates, ask whether `readme.md` or project docs should be updated.

## Architecture Rules

- Business logic belongs in `src/lib/services/`.
- Supabase reads and writes belong in `src/lib/database/`.
- React pages and components should stay focused on presentation and interaction.
- Prefer barrel imports where they exist: `@/components/ui`, `@/hooks`, `@/lib/services`, `@/lib/utils`, and `@/lib/constants`.
- Use shared types from `src/lib/types/` and `src/components/UItypes.ts` when those files exist.
- Use named ES module imports at the top of files.
- Extract tunable gameplay numbers to `src/lib/constants/`.
- Persisted gameplay data should be company-scoped through the current company flow.
- Services should trigger global or topic updates after state-changing writes when that pattern exists.

## Frontend Rules

- Stack target: React, TypeScript, Vite, Tailwind, ShadCN UI, and Supabase.
- Use Tailwind and ShadCN/Radix primitives for UI composition.
- Prefer existing hooks such as `useLoadingState()`, `useGameStateWithData()`, and `useGameState()` when they exist and match the local pattern.
- Do not call Supabase directly from page components.
- Put top-level game pages under `src/components/pages/` and shared UI under `src/components/ui/` when those folders exist.

## Domain Rules

- Use terms from `docs/CONTEXT.md` only once they are defined.
- Do not reintroduce copied prior-project domain terminology, paths, or examples without explicit approval.
- Keep requirement categories, scoring concepts, and variable relationships separate unless explicitly redesigning them.
- Update `docs/VariableRelationshipMap.md` when meaningful variable dependencies are documented.

## Database Rules

- Supabase schema changes should be validated against the intended development database before migration SQL is finalized.
- Store SQL changes under `migrations/`.
- Keep database mappers and shared types aligned with schema changes.
- Do not add legacy field aliases or backward-compatibility branches unless the user explicitly requests them.

## Skill Routing

Use `.agents/skills/webgamedev-gram/SKILL.md` for the full routing matrix. In short:

- Bugs, regressions, and failing tests: `.agents/skills/superpowers/systematic-debugging/SKILL.md`
- React and TypeScript implementation: `.agents/skills/best-practices/js-ts-best-practices/SKILL.md`
- React performance or render behavior: `.agents/skills/best-practices/react-best-practices/SKILL.md`
- ShadCN/Radix UI work: `.agents/skills/best-practices/shadcn-best-practices/SKILL.md`
- Supabase/Postgres work: `.agents/skills/best-practices/supabase-best-practices/SKILL.md`
- Completion claims: `.agents/skills/superpowers/verification-before-completion/SKILL.md`
