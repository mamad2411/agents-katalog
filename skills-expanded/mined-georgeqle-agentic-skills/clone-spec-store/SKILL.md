---
name: clone-spec-store
description: Build a canonical lawful-functional-parity spec store for N software ideas in any domain, then use portfolio gates to seed only implementation-ready or explicit scaffold-only downstream repos.
type: planning
version: v0.0
argument-hint: "[--domain <label>] [--count <N>] [--owner <github-owner>] [--repo-slug-suffix <suffix>]"
---

# Clone Spec Store

Invoke as `$clone-spec-store`.

Produce a canonical specification store for N "clone" software ideas, then move selected ideas through a portfolio-gated downstream implementation pipeline using lawful functional-parity research only. Works for any software domain: mobile apps, web apps, desktop apps, CLIs, devtools, games, services, libraries.

This skill generalizes the `GeorgeQLe/mobile-ideas` pattern, but corrects the default operating model: broad exploration is cheap, while implementation-ready specs, downstream repos, and active builds are gated portfolio assets.

For ongoing operation after a spec store has become a multi-repo queue, pair this with `$project-fleet`. `clone-spec-store` defines the lawful clone/spec-store pipeline; `$project-fleet` owns generic fleet orchestration patterns such as scoring, active-build caps, guarded batches, blocker ledgers, status dashboards, and productive fallback work while waiting on external limits.

## Invocation

Default arguments:

- `--domain`: human label for the target software class. Examples: `mobile apps`, `web apps`, `CLI tools`, `Obsidian plugins`, `VS Code extensions`, `indie games`, `SaaS products`, `Rust crates`. Default: `mobile apps`.
- `--count`: number of ideas. Default: `100`. Must be >= 1.
- `--owner`: GitHub owner (user or org) for downstream repos. Required before Phase 6 remote execution.
- `--repo-slug-suffix`: suffix for each downstream repo name. Default derived from domain: mobile apps -> `-mobile-clone`, web apps -> `-web-clone`, CLI tools -> `-cli-clone`, games -> `-game-clone`, generic -> `-clone`.

If the user says "like `GeorgeQLe/mobile-ideas`" or similar, mirror that pipeline exactly with substituted tokens.

## Guardrails

- **Lawful functional parity only.** Reproduce workflows, interaction models, data contracts, and edge cases. Never copy proprietary source code, private APIs, trademarks as branding, logos, screenshots, store media, copyrighted content, paywalled content, production credentials, or real user data.
- **Non-affiliation.** Every artifact must explicitly state the project is independent and not affiliated with, endorsed by, sponsored by, certified by, or connected to the inspiration product owner.
- **Manual verification blockers.** Any behavior requiring a real account, paid subscription, regional availability, device permission, regulated sandbox, physical hardware, or sensitive-data handling stays marked blocked until lawful hands-on evidence exists.
- **Downstream repos private by default.** No `--public` visibility until the downstream repo has original code, original assets, and passes its own legal/name/license/attribution review.
- **Spec-ready seeding by default.** Do not seed downstream repos until the source spec is implementation-ready unless the item is explicitly marked `scaffold-only`.
- **Portfolio caps before implementation.** Do not move a seeded item into active build work unless it is `spec-ready` and fits the active-build cap recorded by `$project-fleet`.
- **Spec store private until release approved.** The top-level spec store stays private until the open-source checklist is complete and publication is explicitly approved.
- **Category-specific risk review** for finance, health, location, marketplace, communications, media, minors, smart-home, education, security, identity.

## Pipeline

Execute phases in order. Mark each phase complete in `tasks/roadmap.md` before advancing.

### Phase 1 - Backlog And Draft 0

1. Create repo scaffold:
   - `AGENTS.md` - Codex project conventions using the structure below.
   - `CLAUDE.md` - optional Claude mirror when the user wants the store usable from both agents.
   - `README.md` - purpose, repo map, legal scope.
   - `tasks/ideas.md` - backlog table of N ideas.
   - `tasks/roadmap.md` - six-phase plan.
   - `tasks/history.md`, `tasks/todo.md` - lifecycle docs.
   - `specs/README.md` - spec index.
2. Brainstorm N inspiration products in `--domain` ranked by public visibility (public marketplace rankings, community lists, public download counts). Record each as a row in `ideas.md` with columns: `#`, `Inspiration`, `Category`, `Clone-Spec Focus`, `Planning Prompt`.
3. Create Draft 0 specs under `specs/batch-XX/NNN-<slug>.md` (20 per batch). Include one H1, one-paragraph summary, placeholder sections, and enough structure to reserve IDs.
4. Record Draft 0 gaps in `tasks/spec-quality-audit.md`.

### Phase 2 - Draft 1 Normalization

Rewrite every spec to canonical sections (exactly one H1, stable Markdown headings):

```md
# <Original Project Name>-Style Clone Spec

> Metadata
> - Inspiration: <product>
> - Category: <category>
> - Readiness status: <Draft 1 | Implementation-ready as of YYYY-MM-DD>
> - Verification basis: <public sources used>
> - Manual verification blockers: <blockers>
> - Legal scope: functional parity only; original code, brand, copy, assets, integrations.

## Overview
## Goals
## Non-Goals
## Research Sources
## Detailed Design
## Core User Journeys
## Screen Inventory
## Data Model
## API And Backend Contracts
## Realtime, Push, And Offline Behavior
## Permissions, Privacy, And Safety
## Analytics And Monetization
## Edge Cases
## Test Plan
## Acceptance Criteria
## Open Questions
## Build Plan
## Next Steps
```

For non-GUI domains, rename `Screen Inventory` to the appropriate surface type and adapt realtime/offline language as described in Domain Adaptation Notes.

Validate: exactly one H1 per file, every ID `001`-`NNN` present, every spec has Research Sources, Open Questions, Next Steps.

### Phase 3 - Portfolio Scoring And Implementation Readiness

Score candidates before deepening all specs. Use project-specific criteria when present; otherwise score implementation leverage, demo value, legal/provider risk, reusable components, data/API availability, user or market signal, and build cost. Mark each item as `candidate`, `shortlisted`, `archived`, or `blocked`.

For shortlisted specs, upgrade to implementation-ready:

- Replace any discovery link with exact first-party URLs (official marketplace listing, vendor help center, policy pages, official docs).
- Distinguish verified behavior from inferred requirements.
- Enumerate concrete screens/surfaces, data entities, API routes, permissions, subscription states, edge cases, analytics events, test matrix, and build plan phases.
- Add category-specific risk review notes where applicable.
- Mark blocked flows with explicit owner/path for later verification.

Pilot one app first (for example, the most architecturally-teaching example), then extend the same structure to the top scored candidates in batches. The pilot becomes the reference template for the other specs. Do not treat N implementation-ready specs as required unless the user explicitly wants a complete spec encyclopedia rather than a portfolio funnel.

### Phase 4 - Downstream Planning Pilot And Active Cap

- Pick one top-scored, implementation-ready candidate from the backlog.
- Produce a build plan inside its spec: route map, API schema, data model, seed-data policy, test checklist.
- Create the first downstream implementation repo manually (private) and seed it with the source spec copy plus `tasks/roadmap.md` and `tasks/todo.md`.
- Use this pilot to finalize the downstream seed template.
- Record the active-build cap. Default to 5 active downstream repos if the project has no explicit cap.

### Phase 5 - Portfolio Implementation Queue

Populate `tasks/roadmap.md` Phase 5 with a portfolio queue table:

```md
| ID | <Product> | State | Score | Source Spec | Downstream Repo | Next Milestone |
```

Each row references `specs/batch-XX/NNN-<slug>.md` and records whether the item is `candidate`, `shortlisted`, `spec-ready`, `seeded`, `active-build`, `shipped`, `archived`, or `blocked`. Purpose: `$project-fleet` can select the next highest-return item without re-reading the whole spec store.

If `--count` is not 100, create a row for every requested ID and title the phase accordingly. Rows may remain `candidate`; do not force every row to become `spec-ready` or seeded.

### Phase 6 - Downstream Repo Seeding And Spec-Store Release

1. **Manifest.** Create `tasks/repo-seeding.md` with a `## Per-Repo Checklist` table for `spec-ready` targets and explicit `scaffold-only` exceptions:

   ```md
   | Done | ID  | App | State | Target Repo | Source Spec | Gate |
   | :--: | :-: | --- | ----- | ----------- | ----------- | ---- |
   | [ ]  | 001 | ... | spec-ready | `<owner>/<slug><suffix>` | `specs/batch-01/001-<slug>.md` | spec-ready |
   ```

   Include a `### Failures And Blockers` subsection and a `## Open-Source Spec Store Checklist`.

2. **Templates** under `templates/downstream/`:
   - `README.md` with placeholders: `{{PROJECT_NAME}}`, `{{PROJECT_SUMMARY}}`, `{{APP_ID}}`, `{{APP_NAME}}`, `{{TARGET_REPO}}`, `{{SOURCE_SPEC_PATH}}`, `{{SOURCE_SPEC_FILENAME}}`, `{{SOURCE_SPEC_STORE_URL}}`, `{{NON_AFFILIATION_NOTICE}}`, `{{LEGAL_SCOPE}}`, `{{ORIGINAL_ASSETS_REQUIREMENT}}`, `{{MANUAL_VERIFICATION_BLOCKERS}}`.
   - `docs/plans/README.md` - empty phase-plan scaffold.
   - `tasks/roadmap.md` - three-phase downstream roadmap (Plan -> Build -> Parity Review).
   - `tasks/todo.md` - executable Phase 1 tasks.
   - `.gitignore` - stack-neutral defaults.

3. **Seeding utility** at `scripts/seed-downstream-repos.mjs`:
   - Parses `tasks/repo-seeding.md` manifest, validating every listed row.
   - Single-target only (`--target <id|app|owner/repo>`); batch creation is intentionally unsupported.
   - Modes: `--dry-run` (writes preview dir, prints exact `gh`/`git` commands, never runs remote); `--execute` (checks `gh auth status`, refuses `--public`/`--visibility public`/`--all`, creates private via `gh repo create ... --private --clone=false`, clones, seeds, commits, pushes).
   - Refuses existing target repos unless `--reconcile-existing` is supplied.
   - Refuses non-`spec-ready` rows unless the manifest gate is explicitly `scaffold-only`.
   - Extracts `Manual verification blockers` and `Legal scope` from the source-spec metadata block to fill placeholders.
   - Fails fast on unresolved `{{PLACEHOLDER}}` tokens.
   - Appends failure evidence to `### Failures And Blockers` unless `--no-record-blockers`.

4. **Execution order:**
   - Step 6.1: Audit manifest.
   - Step 6.2: Add templates.
   - Step 6.3: Add seeding utility, run local dry-run on one low-risk non-pilot target.
   - Step 6.4: Add public-release docs to spec store (`README.md`, `LICENSE` - CC BY 4.0 recommended for docs with explicit exclusions for third-party marks/media/APIs/data, `CONTRIBUTING.md`, `SECURITY.md`).
   - Step 6.5: Run one private non-pilot dry-run seed end-to-end. Record created repo URL, seeded files, commit SHA.
   - Step 6.6: Reconcile the Phase 4 pilot repo with the shared seed structure.
   - Step 6.7: Seed remaining eligible repos in controlled private batches. Stop on any auth/permission/naming/rate-limit/template-validation failure and record the blocker.
   - Step 6.8: Verify every target repo either exists privately with expected seeded files and source-spec backlink, or has an explicit blocker note. Confirm no downstream repo is public and no proprietary assets were seeded.
   - Step 6.9: Spec-store publication. Complete the open-source checklist and run `gh repo edit <owner>/<spec-store-repo> --visibility public` only after explicit user approval.
   - Step 6.10: Route ongoing queue execution through `$project-fleet --plan` or `$project-fleet --execute` so scoring, active-build caps, blockers, and runnable milestones govern future work.

## Canonical AGENTS.md

Use this structure (substitute domain):

```md
# <Domain> Ideas Project Conventions

## Overview
Planning and specification workspace for <domain> clone ideas. Not runtime code.

## Goals
- Lawful backlog of <domain> clone ideas.
- Turn each idea into a detailed technical specification before implementation.
- `tasks/` for planning; `specs/` for specifications.
- Preserve distinction between public-source research, inferred requirements, and hands-on verified behavior.

## Non-Goals
- No runtime app code here.
- No proprietary source code, private APIs, trademarks, logos, screenshots, copyrighted media, paywalled content, or unlicensed datasets.
- Do not treat inferred product behavior as verified one-for-one clone requirements.

## Detailed Design
- "Clone" = lawful functional parity with original implementation and original assets.
- Every numbered spec must include source orientation, legal scope, privacy/safety, edge cases, test plan, acceptance criteria, open questions, next steps.
- Every source-discovery link must be replaced with exact first-party URLs before implementation.
- Account-, subscription-, region-, permission-, hardware-, or regulator-gated behavior stays blocked until verified.
- Generated docs must use one H1 and stable Markdown headings.

## Test Plan
- Run hygiene checks after structural doc changes.
- Run spec-structure checks after bulk spec rewrites.
- Verify every numbered spec has canonical sections and one H1.
```

When creating a dual-agent store, mirror the same content to `CLAUDE.md` with agent-specific command examples adjusted from `$...` to `/...`.

## Domain Adaptation Notes

- **Mobile apps / desktop apps / web apps**: use "Screen Inventory"; include iOS/Android/OS platform sections; map permission prompts, push, offline, store listings.
- **CLI tools / devtools / libraries**: rename "Screen Inventory" to "Command/Surface Inventory"; replace "Push/Offline" with "Runtime/Error-Handling Behavior"; add "CLI Contracts" (flag/subcommand matrix) and "Install/Distribution" sections.
- **Games**: add "Core Loop", "Progression", "Content Pipeline"; keep "Screen Inventory" for menus/HUD.
- **Services/APIs**: replace "Screen Inventory" with "Endpoint Inventory"; expand "API And Backend Contracts"; add "Deployment/Ops" section.
- **Browser extensions / plugins**: add "Host Integration Points", "Permissions Manifest", "Marketplace Review Risk".

In every case, keep: Metadata block, Research Sources, Goals/Non-Goals, Data Model, Permissions/Privacy/Safety, Edge Cases, Test Plan, Acceptance Criteria, Open Questions, Build Plan, Next Steps.

## Process When Invoked

1. Resolve `--domain`, `--count`, `--owner`, `--repo-slug-suffix`. Ask only for values needed to proceed safely; `--owner` is required before Phase 6 remote execution.
2. Check if the current directory already has a partial pipeline (look for `tasks/ideas.md`, `specs/`, `tasks/repo-seeding.md`). Resume at the earliest incomplete phase rather than restarting.
3. Work one phase at a time. After each phase: update `tasks/roadmap.md`, commit with a conventional message (`feat(seeding): complete Phase N step X.Y ...`), push if `--owner` is configured and the user has approved remote actions.
4. Never advance to Phase 6 remote execution without explicit user approval for each batch.
5. Never flip the spec store to public visibility without explicit user approval.
6. After Phase 5 exists and the user's request is about selecting candidates, continuing batches, enforcing active caps, repairing blockers, summarizing cross-repo status, or advancing downstream repos, route through `$project-fleet` unless the requested change is clone/spec specific.

## Reference Implementation

The exact pattern this skill reproduces: `GeorgeQLe/mobile-ideas`. Key artifacts to mirror structurally:

- `AGENTS.md` and, for dual-agent stores, `CLAUDE.md`
- `README.md`, `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`
- `tasks/ideas.md`, `tasks/roadmap.md`, `tasks/repo-seeding.md`, `tasks/history.md`, `tasks/todo.md`, `tasks/spec-quality-audit.md`
- `specs/batch-NN/NNN-<slug>.md` (20 per batch by convention; adjust if N is not 100)
- `templates/downstream/{README.md,docs/plans/README.md,tasks/roadmap.md,tasks/todo.md,.gitignore}`
- `scripts/seed-downstream-repos.mjs`

If accessible, read those files for the exact wording and reuse structure with domain-appropriate substitutions.

## Acceptance Criteria

- N ideas in `tasks/ideas.md`.
- N numbered specs under `specs/batch-*/`, each with canonical sections; shortlisted specs have implementation-ready content before downstream build work.
- `tasks/roadmap.md` with all six phases; Phase 5 table populated with all N portfolio rows, states, scores, source specs, downstream repo fields, and next milestones.
- `tasks/repo-seeding.md` with eligible `spec-ready` rows and explicit `scaffold-only` exceptions, command pattern, open-source checklist, and blocker log.
- `templates/downstream/` complete and placeholder-safe.
- `scripts/seed-downstream-repos.mjs` passes a local dry-run for at least one target.
- Private downstream repos exist only for eligible `spec-ready` rows or explicit `scaffold-only` exceptions, with source-spec copy and scaffolded planning docs, or explicit blocker notes in the manifest.
- No proprietary assets committed anywhere. No public visibility changes without explicit user approval.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page at `alignment/clone-spec-store-{topic}.html`. Use a normalized topic slug derived from the app, feature, research subject, report subject, or output filename.

**Full content requirement.** The alignment page must contain the complete content of every proposed markdown deliverable -- every section, every finding, every detail, every list item. It is a thorough interactive review document, not a summary. Render the full deliverable content in clean, readable HTML with appropriate hierarchy, styling, and navigation. If the skill writes multiple scoped deliverables in one run, build one alignment page that contains all deliverables with anchor-linked navigation. Durable tracker artifacts, such as `research/assumption-tracker.md`, remain canonical markdown outputs but must also be fully rendered into the alignment page before approval.

**Dark-mode styling.** Use a dark color scheme by default. Base CSS variables: `--bg: #0d1117; --surface: #161b22; --border: #30363d; --text: #c9d1d9; --text-muted: #8b949e; --accent: #58a6ff; --green: #3fb950; --red: #f85149; --orange: #d29922; --purple: #bc8cff;`. Apply `background: var(--bg); color: var(--text);` on body. Use `--surface` for cards, nav, and table headers. Use `--border` for all borders. Use `--purple` for question blocks and gate headings. Use `--accent` for links and section headings. Keep headings `color: #fff` or `var(--accent)` for hierarchy. Question block backgrounds should use `#1c2333`.

**Alignment gates.** Treat gates as explicit review sections inside the HTML page. A gate blocks finalization until its required inline questions are answered and compiled into YAML. Include every gate that applies to the skill output, and include these gate types whenever relevant: evidence coverage, assumptions/confidence, scope/non-goals, candidate/verdict decisions, artifact destination, proposed file changes, coverage checkpoint, and post-approval route.

**Report-only research gates.** For report-only or pre-approval research skills, the alignment page must explicitly contain evidence coverage, assumptions/confidence, recommended path, proposed file changes, and approval gates before any canonical research, spec, or task file is created or updated.


**Required inline questions.** Each gate must contain at least one required inline question placed directly under the content it governs, inside a visually distinct question block. Each question must use radio-button inputs and include two standing options after the skill-generated choices: "Other / None of the above" backed by a multi-line text box for free-form input, and "Need clarification" backed by an optional notes box where the user can explain what is unclear. When any radio option other than "Other" or "Need clarification" is selected, show an optional "Additional notes" text box beneath it so the user can qualify their choice. Generate questions based on what genuinely needs user input -- do not add filler questions. Do not create a separate bottom "Decisions & Clarifications" section.

**Gate YAML contract.** At the bottom of the page, include a "Compile Answers" button that aggregates answers from all inline gate questions throughout the page, including free-text notes. The button remains disabled until every required question has a selection, shows a count of remaining unanswered questions, and scrolls to the first unanswered question if clicked early. When every question is answered, generate a structured YAML block with one item per gate answer using this stable shape: `section`, `gate_type`, `status` (`answered`, `other`, or `needs-clarification`), `answer`, optional `notes`, and optional `target_artifact` or `target_path` when the gate controls file output. After successful compilation, automatically attempt to copy the YAML to the clipboard with the Clipboard API, display copy status, and display the YAML in a read-only textarea with an explicit "Copy YAML" button. The copy button must retry clipboard copy when supported and fall back to selecting the textarea contents when clipboard access is unavailable or blocked.

**Pre-approval stop.** Before user approval, the next action is review of the HTML alignment page, not downstream routing. Ask the user to review the page and provide the compiled YAML answers. Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language until after compiled YAML has been provided and the approved artifacts have been written or updated.

**Diff highlighting on updates.** When the agent updates an existing alignment page after receiving compiled answers, highlight what changed since the previous version. The agent chooses inline annotation or side-by-side layout per situation.

**Archiving.** Before replacing an existing alignment page, archive it to `docs/history/archive/YYYY-MM-DD/HHMMSS/alignment/clone-spec-store-{topic}.html`.

**Browser open.** Attempt to open the resulting HTML page in the browser and report whether the open succeeded or was blocked. A blocked browser-open attempt does not make the skill fail when the files were written correctly.

