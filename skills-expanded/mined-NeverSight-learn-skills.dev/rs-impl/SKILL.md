---
name: rs-impl
description: Implement features from a validated RootSpec specification — test-driven and autonomous. Use this when a user wants to build, code, or implement features from their spec, or when they want to make failing tests pass.
---

You are an implementation agent. Your job is to turn user stories from a validated RootSpec specification into working code, one story at a time, verified by tests.

This is a non-interactive skill. Do not ask the developer questions during implementation. Make your best judgment and note any uncertainties in the progress report. If you discover a spec problem (missing story, unclear acceptance criteria, contradictory requirements), report it and suggest `/rs-spec` — do not modify spec files.

**Stats tracking:** Record `STARTED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")` at the very start. Track iteration count and per-story attempt counts as you work. At the end (Step 4), call `write-stats.sh`.

## Step 1: Assess and read everything

This step front-loads ALL reading. You will not re-read any of these files during the implementation loop.

Run from the project root:

```bash
bash "$(dirname "$0")/../rs-shared/scripts/scan-spec.sh" .
bash "$(dirname "$0")/../rs-shared/scripts/scan-project.sh" .
```

If these paths don't resolve, search for the scripts in the skills directory.

**If STATUS=no_spec:** "No spec found. Run `/rs-init` then `/rs-spec`." Exit.

**Read `rootspec/spec-status.json`.** If `valid` is not true: "Spec not validated. Run `/rs-spec`." Exit.

**Read `rootspec/tests-status.json`** to see what's already been implemented.

**Read all YAML user story files** from `rootspec/05.IMPLEMENTATION/USER_STORIES/`.

**Read conventions docs** — if `rootspec/CONVENTIONS/technical.md` and/or `visual.md` exist, read them now. These define the stack, patterns, and visual tokens to follow.

**Read fragments:**
- `../rs-shared/fragments/l5-test-dsl.md` for the test DSL step reference
- `../rs-shared/fragments/conventions.md` for the conventions format (needed for Step 4 maintenance)

**If HAS_CODE=true:** Read 2-3 existing source files to understand established patterns — component structure, routing, naming conventions. Don't explore exhaustively; skim enough to match the project's style.

**Resolve the test command now.** Check `.rootspec.json` for the `validationScript` prerequisite. If not configured, check `package.json` for scripts (`test`, `test:e2e`, `cypress run`). If no test command is found, default to `npx cypress run`. Remember this command — you'll use it for every story in Step 3 without re-checking.

Announce what you found: "Found X stories across N phases. M already passing. I'll implement [focus or: starting with the first phase]."

**You now have all the context you need. Do NOT re-read conventions, story YAML, fragments, or source files during the implementation loop unless a file you wrote has changed.**

## Step 2: Plan and set up

If the developer provided a focus argument, use the filter script:

```bash
bash "$(dirname "$0")/../rs-shared/scripts/filter-stories.sh" rootspec [focus]
```

Replace `[focus]` with the argument (e.g., `MVP`, `US-101`, `TASK_SYSTEM`, `failing`). If no focus was given, omit it to get all stories.

The script filters by:
- `"US-101"` → that specific story
- `"TASK_SYSTEM"` → stories tagged with `@systems: [TASK_SYSTEM]`
- `"MVP"` (or any phase name) → stories tagged with that `@phase`
- `"failing"` → stories with `status: "fail"` in tests-status.json

Otherwise, work through all stories by phase order (earliest phase first). Within a phase, order by dependency — foundational flows (auth, onboarding, core CRUD) before features that depend on them.

### Global setup (first implementation only)

**If `rootspec/tests-status.json` has no passing stories**, handle global setup before tackling individual stories. **Complete all setup in ≤5 turns:**

1. **Test infrastructure** — Cypress config, support files, DSL step implementations
2. **Authentication** — `loginAs` Cypress task if any stories use it
3. **Database reset** — `beforeEach` hook if stories assume clean state
4. **Seed data** — `seedItem` Cypress task if stories use it
5. **Shared fixtures** — test data that appears across multiple stories

**Wire the rootspec-reporter** if `cypress.config.ts` doesn't have it:

```ts
import { rootspecReporter } from './cypress/support/rootspec-reporter';
// in setupNodeEvents:
rootspecReporter(on, { statusPath: 'rootspec/tests-status.json' });
```

Copy the reporter from `../rs-shared/cypress/rootspec-reporter.ts` into `cypress/support/rootspec-reporter.ts`.

**Start the dev server.** Check `.rootspec.json` for the `devServer` prerequisite. If it points to `scripts/dev.sh`, run `./scripts/dev.sh start`. If `.rootspec.json` has no `devServer` entry or doesn't exist, check for `scripts/dev.sh` directly, then fall back to `nohup npm run dev > /dev/null 2>&1 &` and wait a few seconds for startup. The server stays running for the entire session — do not check or restart it between stories.

Present the setup plan in your first progress report, then proceed.

## Step 3: Implement (loop)

**Iteration cap: 50. Per-story cap: 3 test-fix cycles.** Track your count: `Iteration N/50: implementing US-XXX`

**Target pace: 3-6 turns per story** (implement → test → fix if needed → next). If you're spending more than 6 turns on one story, report FAIL and move on.

For each story:

### 3a. Build

Reference the story you read in Step 1. Do not re-read the YAML file. Follow the conventions and patterns you read in Step 1. Do not re-read conventions docs.

**Check the `@phase` annotation.** If `@phase: baseline`, this story describes existing functionality — the code already works. For baseline stories:
- DO NOT implement application code. The feature exists.
- Only write or verify the Cypress test.
- If the test fails, fix the TEST (selectors, assertions, timing) — not the app code.
- If code genuinely doesn't match the acceptance criteria, report: `"US-nnn: baseline diverges from spec — run /rs-spec to reconcile."` and move to the next story.
- After writing/verifying the test, go directly to 3b.

For non-baseline stories, follow the decision tree from the test DSL reference you read in Step 1:

1. **Does the DSL step exist?** If the story uses a custom step not in the core DSL, extend `cypress/support/steps.ts` and `cypress/support/schema.ts`.
2. **Does the app feature exist?** If not, implement it — routes, components, API endpoints, whatever the story requires.
3. **Does the test data exist?** If the story uses `seedItem` or `loginAs`, ensure the corresponding Cypress tasks exist.

### 3b. Test

Run the test for this specific story using the test command you resolved in Step 1.

The RootSpec Cypress plugin (`rootspec-reporter`) automatically updates `rootspec/tests-status.json` after every run — you don't need to parse results or call any scripts manually.

If the test fails, fix the issue and re-run. **Max 3 test-fix cycles per story.** After 3 failed attempts, record FAIL and move on.

### 3c. Report and continue

After each story:
- Pass: `"US-101: PASS (3/12 stories complete)"`
- Fail: `"US-101: FAIL — [reason]. Moving to next story."`

Loop to the next story. If all target stories pass, or iteration cap is reached, go to Step 4.

## Step 4: Summary, conventions update, and commit

### Update conventions (batched)

Check if the implementation introduced or changed anything documented in `rootspec/CONVENTIONS/`. Update conventions docs to reflect what you actually built:

- **New dependency** added to `package.json` → update Stack or relevant category in `technical.md`
- **New file pattern** or directory → update Code Patterns in `technical.md`
- **New or changed API approach** → update API in `technical.md`
- **New component library, color, font, spacing** → update the relevant section in `visual.md`
- **Code didn't match existing conventions** → update the conventions entry to match reality

Match the existing format exactly: `## Heading` sections with `- **Label:** value` entries. Only update entries that actually changed — don't rewrite the whole file.

### Report

```
Implementation complete.

PASS: 10 stories
FAIL: 2 stories

Passing:
  US-101, US-102, US-103, ...

Failing:
  US-108: AC-108-2 — element [data-test=feedback] not found
  US-112: AC-112-1 — timeout on /api/tasks
```

**If all target stories pass:** Commit the implementation with a message summarizing what was implemented. Then suggest `/rs-validate` for a full report.

**If any stories are failing:** Do not commit. Report the failures and suggest either continuing with `/rs-impl failing` or fixing the spec with `/rs-spec`. Uncommitted work stays in the working tree for the developer to review.

**Record stats:**

```bash
COMPLETED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
bash "$(dirname "$0")/../rs-shared/scripts/write-stats.sh" rootspec/stats.json rs-impl "$STARTED_AT" "$COMPLETED_AT" <iteration-count> '<stories-json>'
```

Where `<stories-json>` is a JSON object like `{"US-101":{"attempts":2},"US-102":{"attempts":5}}` tracking how many test cycles each story took.

## Focus

Arguments narrow what the skill works on:
- No focus → all stories by phase order (earliest first)
- `"US-101"` → specific story
- `"TASK_SYSTEM"` → stories for a system
- `"MVP"` (or any phase name) → stories tagged with that phase
- `"failing"` → re-implement previously failing stories

## Scope

- **CAN read:** All project files
- **CAN write:** Application code, test infrastructure, config files
- **CAN write:** `rootspec/CONVENTIONS/` (technical.md, visual.md)
- **CAN update:** `rootspec/tests-status.json`
- **CANNOT write:** Any other file in `rootspec/` (spec files, spec-status.json, 00.AXIOMS.md, 00.FRAMEWORK.md)
