# CLAUDE.md — Template Rules (v2.0)

Read `experiment/experiment.yaml` before every task. It is the single source of truth for what to build.

Rules are in priority order. When two rules conflict, the lower-numbered rule wins.

## Rule 0: Scope Lock
- Only build what is described in `experiment/experiment.yaml`
- If a behavior isn't listed in `behaviors`, don't build it
- Pages are derived from `derive_scope_pages()` (`.claude/scripts/lib/derive_pages.py`) — see `.claude/templates/experiment-yaml.md` for the canonical schema. The page set is the union of `golden_path[*].page`, `behaviors[*].pages` (web-app archetype, required field), and auth-derived pages.
- If you're unsure whether something is in scope, it isn't
- To add a new behavior, use the /change skill — it updates experiment.yaml first, then implements
- When asked to do something outside a defined skill (/ads-ready, /audit, /spec, /bootstrap, /change, /deploy, /distribute, /iterate, /observe, /optimize-prompt, /resolve, /retro, /review, /rollback, /solve, /teardown, /upgrade, /verify), ask the user to clarify before proceeding

## Rule 1: PR-First Workflow
- Never commit directly to `main`
- Every change goes on a feature branch and gets a PR (for audit trail)
- Skills write delivery artifacts (`.runs/commit-message.txt`, `.runs/pr-title.txt`, `.runs/pr-body.md`); `lifecycle-finalize.sh` handles commit, push, PR creation, and auto-merge after audit gates pass (see `.claude/patterns/auto-merge.md` for safety gates)
- Branch naming: `feat/<topic>`, `fix/<topic>`, `chore/<topic>`, `change/<topic>`
- Use `gh pr create` to open PRs
- Fill in the PR template at `.github/PULL_REQUEST_TEMPLATE.md` for every PR

## Rule 2: Analytics (when `stack.analytics` is present)
- When `stack.analytics` is present in experiment.yaml, every page (web-app) or endpoint (service) and user action must fire events defined in `experiment/EVENTS.yaml` — that file is the **canonical** list of all events; always read it for the full specification. When `stack.analytics` is absent, skip analytics implementation entirely. For CLI projects: analytics must be **opt-in** — check for a consent flag or environment variable before calling `trackServerEvent()`. See the CLI archetype file for details.
- Use the analytics library for all tracking calls — never call the analytics provider directly. See your analytics stack file (`.claude/stacks/analytics/<value>.md`) for the file path, exports, and import conventions.
- Use typed event wrappers (see analytics stack file) for all events defined in experiment/EVENTS.yaml — this provides compile-time validation. When `/change` or `/distribute` adds a new event to EVENTS.yaml, add a corresponding typed wrapper to `events.ts`. Typed wrappers are client-side only (nextjs web-apps); for non-nextjs frameworks (CLI, service), `events.ts` is not generated — call `trackServerEvent()` directly (see the analytics stack file's "When framework is NOT nextjs" section). For server-side events (webhooks, API routes), use `trackServerEvent(event, distinctId, properties?)` from the server analytics library — `distinctId` identifies the user (e.g., `user.id`; use `"server"` when no user context is available).
- The analytics library auto-attaches global properties defined in experiment/EVENTS.yaml `global_properties` to every event — these distinguish experiments in the shared analytics project.
- Wire each event from the experiment/EVENTS.yaml `events` map to its corresponding page, filtering by `requires` (match experiment stack) and `archetypes` (match experiment type). If no page provides a natural trigger for an event (e.g., no signup page), omit that event.
- Events with `requires: [payment]` in experiment/EVENTS.yaml are included only when `stack.payment` is present in experiment.yaml.
- If you rename the project in experiment.yaml (`name` field), update the analytics library constants — see your analytics stack file for which constants to change.

## Rule 3: Use Stack from experiment.yaml
- Default stack: Next.js (App Router), Vercel, Supabase, PostHog, shadcn/ui
- The optional `type` field in experiment.yaml selects a product archetype (default: `web-app`). Each archetype is defined at `.claude/archetypes/<type>.md` and specifies required stacks, file structure, and funnel shape.
- Per-service values (`runtime`, `hosting`, `ui`, `testing`) live under `stack.services[]`. Shared values (`database`, `auth`, `analytics`, `payment`) live directly under `stack`.
- For per-service values, the stack file is at `.claude/stacks/<category>/<value>.md`. The category-to-directory mapping: `runtime` → `framework/`, `hosting` → `hosting/`, `ui` → `ui/`, `testing` → `testing/`. Shared values use their key name directly (e.g., `stack.database: supabase` → `.claude/stacks/database/supabase.md`).
- To add support for a new technology (e.g., Firebase), create the corresponding stack file — don't modify skill files.
- Do not add frameworks or libraries not listed in experiment.yaml `stack` section
- Exception: small utility packages (clsx, date-fns, zod) are fine
- If a feature requires a library not in `stack`, ask the user before adding it
- Bootstrap installs latest versions of all packages (no version pinning). `package-lock.json` locks exact versions for reproducibility

### Archetype-Feature Matrix

| Feature | web-app | service | cli |
|---------|---------|---------|-----|
| Pages (src/app/<page>/page.tsx) | ✅ | ❌ | ❌ |
| API routes (src/app/api/) | ✅ | ✅ | ❌ |
| Commands (src/commands/) | ❌ | ❌ | ✅ |
| Landing page | ✅ | surface | surface |
| Variants (A/B messaging) | ✅ | ❌ | ❌ |
| Fake Door components | ✅ | stub routes | stub commands |
| Browser tests (Playwright) | ✅ | ❌ | ❌ |
| API/unit tests (Vitest) | ✅ | ✅ | ✅ |
| /distribute (ad campaigns) | ✅ | ✅ (if surface) | ✅ (if surface) |
| /deploy | ✅ | ✅ | surface only |
| Analytics (client-side) | ✅ | ❌ | ❌ |
| Analytics (server-side) | ✅ | ✅ | ✅ |
| SEO/AEO (meta, sitemap, llms.txt) | ✅ | surface only | surface only |

## Rule 4: Keep It Minimal
- Prefer well-known libraries over custom code
- Bootstrap creates page-load smoke tests when `stack.testing` is present. Use `/change` for full funnel tests and `/verify` to run tests and fix failures.
- Business logic (calculations, state machines, data mutations, auth, payment) MUST have unit tests (see `patterns/tdd.md`). If you're writing complex algorithms, consider whether you're overbuilding.
- Every /change Feature, Fix, or Upgrade spawns implementer agents (see `agents/implementer.md`) with task dependency ordering
- /verify adds spec-reviewer as an additional parallel agent (see `agents/spec-reviewer.md`)
- `stack.testing` is required — /change and /bootstrap will stop if testing stack is absent.
- No abstraction layers unless there's concrete duplication (3+ copies)
- Ship the simplest thing that works
- No premature optimization — no caching, no memoization, no lazy loading unless there's a measured problem

## Rule 5: Deploy-Ready
- Every PR must pass `npm run build` with zero errors before committing
- Skills use the verification procedure in `.claude/patterns/verify.md` (3-attempt retry with error tracking). All skills follow the state machine execution pattern — see Rule 13.
- No broken imports, no missing env vars in code
- Reference `.env.example` for all environment variables
- Every page (web-app) must render and every endpoint (service) must respond without runtime errors

## Rule 6: Security Baseline
- Secrets go in environment variables, never in code
- Validate and sanitize all user input with zod or similar
- Add rate limiting to auth and payment API routes. See hosting stack file for deployment-specific constraints (e.g., serverless rate-limiting limitations).
- Run `npm audit` before deploying — critical vulnerabilities must be acknowledged before going to production
- Use database-level access control (e.g., RLS) for all data access — never trust the client. See database stack file for details.
- Never expose database admin/service keys to the client
- These rules are enforced by `.claude/patterns/security-review.md` during verification
- Follow `.claude/patterns/incident-response.md` for production incidents and secret rotation

## Rule 7: File Conventions
```
src/
  app/              # Pages and API routes (see framework stack file)
    api/            # API route handlers (all mutations go here)
    <page-name>/    # One folder per page derived from golden_path
      page.tsx      # Page component
  components/       # Reusable UI components (see UI stack file)
    ui/             # UI library components (auto-generated)
  lib/              # Utilities
    analytics.*     # Analytics tracking (see analytics stack file for filename)
experiment/           # experiment.yaml lives here
```
> This tree shows the default layout (Next.js). See your framework stack file for the actual file structure and extensions.
> For `type: service`, the structure replaces page folders with API routes only:
> ```
> src/
>   app/
>     api/            # API route handlers
>       <endpoint>/
>         route.ts    # Route handler
>   lib/              # Utilities
>     analytics.*     # Server-side analytics only for services
> experiment/           # experiment.yaml lives here
> ```
- One component per file
- Colocate page-specific components in the page's folder
- API routes: see your framework stack file for the route handler convention

## Rule 8: Communication Style
- Commit messages: imperative mood, ≤72 chars (e.g., "Add signup flow with email verification")
- PR descriptions: bullet points, reference experiment.yaml behaviors by ID
- Fill in every section of the PR template — don't leave sections empty

## Rule 9: Framework Patterns
Follow the framework patterns defined in your active framework stack file (`.claude/stacks/framework/<value>.md`). That file specifies page conventions, routing patterns, data fetching approach, and restrictions. When no stack file exists for the configured framework, use your knowledge of that technology and follow the same structural patterns.

## Rule 10: Database
Follow the database patterns defined in your active database stack file (`.claude/stacks/database/<value>.md`). That file specifies migration format, schema conventions, access control setup, and typing requirements. When no stack file exists for the configured database, use your knowledge of that technology and follow the same structural patterns. Always follow Rule 6 for security, and keep the schema minimal — only create tables that experiment.yaml features require.

## Rule 11: Memory
- After fixing build errors in the verification procedure, save project-specific patterns to auto memory
- Universal patterns that apply to any project with this stack belong in `.claude/stacks/<category>/<value>.md` — not in auto memory
- Planning patterns (auth flow interactions, stack integration quirks, codebase conventions) are project-specific — save to auto memory under "Planning Patterns" heading, consulted during `/change` Phase 1 exploration
- Auto memory is an accelerator, not a dependency — skills must function correctly with empty auto memory (fresh developer, fresh machine)

## Rule 12: Template Observations
Template-rooted issues are detected and filed automatically.
`lifecycle-finalize.sh` runs the epilogue for all skills:
1. The command file reads `.claude/patterns/finalize-epilogue.md` which calls `.claude/patterns/skill-epilogue.md`
2. `skill-epilogue.md` derives observation scope from `skill.yaml` and calls `.claude/patterns/observation-phase.md` — the unified observation procedure for all skills
3. **Cross-file coherence findings** (Step 5b-coherence in observation-phase.md): `lifecycle-finalize.sh` Step 4.5 runs `verify-linter.sh` against declarative rules in `.claude/patterns/template-coherence-rules.json` (cached, content-addressed). Findings emit as the `cross_file_contradiction` category and are folded into observation candidates via the same 3-condition test as fix-log entries.
4. **Manual observation** (/observe): Use `/observe --file <path> --symptom "<desc>"` to manually file observations outside of automated flows

No manual note-taking is required during skill execution. For ad-hoc fixes
outside of a skill context, use `/observe` to evaluate and file template
observations.

## Rule 13: Skill Execution Pattern
All 16 lifecycle skills use state machines with JIT (Just-In-Time) dispatch (the utility skill /optimize-prompt is standalone). Each skill is defined by `skill.yaml` (declarative config) and state files at `.claude/skills/<skill>/state-*.md`. The command file (`.claude/commands/<skill>.md`) is a thin dispatcher. Read only one state file at a time — never read ahead.
- Each state file has 6 required sections: PRECONDITIONS, ACTIONS, POSTCONDITIONS, VERIFY, STATE TRACKING, NEXT
- `.claude/patterns/state-registry.json` maps every skill's states to VERIFY commands, enforced at runtime by `.claude/hooks/state-completion-gate.sh`
- Context files (`.runs/<skill>-context.json`) track execution state with base schema: `{skill, branch, timestamp, completed_states}`
- To modify a skill's behavior, edit the corresponding state files (`.claude/skills/<skill>/state-*.md`) — don't modify the orchestrator (`.claude/commands/<skill>.md`) without also updating state files and `state-registry.json`
- To add or remove states, update both the state file on disk and the registry entry — they must stay in sync
- Never remove the VERIFY or STATE TRACKING sections from a state file
- **VERIFY ownership:** `state-registry.json` owns all VERIFY commands. State files own prose (ACTIONS, POSTCONDITIONS, narrative). When modifying a VERIFY check, edit `state-registry.json` only, then run `make sync-verify` to propagate to state files. Never edit state file VERIFY code fences directly. Run `.claude/scripts/verify-linter.sh` to detect drift (DIVERGED is blocking). States with `"true"` VERIFY must include a `<!-- VERIFY=true: <reason> -->` comment in the state file.
- **When to split a state:** Split when a state exhibits any of: (a) mixes user-interactive and non-interactive steps (different retry semantics), (b) mixes validation and orchestration concerns (different failure domains), or (c) exceeds 10 execution steps with 0 intermediate artifact writes
- **Sub-ID convention:** Format is `<number><letter>` (e.g., 3a, 13a). Single depth only -- never `3a1`. Sub-IDs are peers inserted between N and N+1 in the canonical sequence, not hierarchical children of N

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
