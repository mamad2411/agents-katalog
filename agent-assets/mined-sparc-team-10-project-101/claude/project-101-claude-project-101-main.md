# Project standards

> Fill in the `[PLACEHOLDER]` sections once the idea and stack are locked.
> Keep this file lean — every line here is loaded into every subagent call,
> for every module. Stack-specific detail belongs in the nested CLAUDE.md
> files below, not here.

## Project

- **Idea**: Community Health Hub (CHH) — a mobile-first web platform
  connecting blood donors, seekers, hospitals, and NGOs: OTP-first login,
  real-time proximity alerts for blood requests and events, hospital
  inventory/resource visibility, and facility verification. Source of
  truth: PRD-CHH-v2.2 (Confluence) and the Jira `CHH` project.
- **Modules**:
  - `backend` — ASP.NET Core 8 Web API + PostgreSQL, single service (see `backend/CLAUDE.md`)
  - `frontend` — React + TypeScript + Vite, mobile-first responsive web (see `frontend/CLAUDE.md`)

## Repo structure

This is a monorepo: one git history, backend and frontend live as plain
subfolders (no git submodules). Each has its own nested `CLAUDE.md` with
stack-specific standards — Claude Code auto-loads whichever is closest to
the files an agent is touching, so a backend coder agent never loads
frontend-only rules and vice versa.

- `backend/CLAUDE.md` — backend stack, coding standards, backend-only DoD
- `frontend/CLAUDE.md` — frontend stack, coding standards, frontend-only DoD

The Architect agent creates these nested files (and the folders) when it
locks the tech stack per module — see `.claude/agents/architect.md`.

## Coder pipeline for backend/frontend modules

The generic `coder-{module}` stage referenced elsewhere in this file (and
in `docs/AGENTIC_SDLC.md`) is, for this project, implemented by a richer
sub-pipeline: `.claude/agents/orchestrator.md`, driving a
Startup → Knowledge → Planning → Coding → Code Review → Unittest → PR flow
with its own developer/lead approval gates and Confluence-published
implementation plans.

- **It supersedes `coder-backend-template.md` / `coder-frontend-template.md`**
  for backend and frontend module tickets. Once the Architect creates a
  module's Jira ticket, hand it to the orchestrator (paste the Jira URL, or
  `/task <TICKET_ID>`) rather than copying a generic `coder-<module>` agent.
- The orchestrator's own **Code Review Agent** and **Unittest Agent** stages
  fulfill the role of the macro `reviewer.md` / `tester.md` agents for these
  tickets — the macro Reviewer/Tester are **not** separately invoked for
  backend/frontend module work.
- The macro `reviewer.md` / `tester.md` and the generic `coder-template.md`
  remain the path for any module **outside** the backend/frontend split
  (e.g. a standalone infra module).
- Concrete agent files: `backend-*-agent.md` (backend side) and
  `frontend-*-agent.md` (frontend side) in `.claude/agents/`; `startup-agent`
  and `pr-agent` are shared across both sides. Full roster and behavior:
  `backend/CLAUDE.md` §Agent Directory (the orchestrator's entry point doc).

## QA execution (post-merge)

After a developer's PR is merged into `main` (a manual GitHub action — nothing
in this repo auto-merges; see `.claude/agents/pr-agent.md`), a **QA
automation tester** runs the **QA Execution Agent**
(`.claude/agents/qa-execution-agent.md`) independently, by handing it the
feature-wise QA Test Case Design directly — the Confluence page URL and the
Feature's ticket ID, e.g. "QA Execution Agent, run these test cases:
`<ConfluenceUrl>`, `CHH-F04`". This agent is a **fully separate entity**: it
is not part of the developer pipeline above, is never invoked by the
Orchestrator, and never itself starts, resumes, or feeds into any SDLC
pipeline stage in either direction. It never searches Confluence to find
what to test — the tester always hands it the exact page.

It executes exactly the test cases on the page(s) it was given against
`.github/workflows/qa-tests.yml`, publishes a QA Execution Report to
Confluence, and — on failure, with the QA tester's confirmation — opens a
Jira Bug ticket as a tracking record only. Creating that ticket triggers
nothing automatically; a developer may separately choose to pick it up later
via the existing `/dev <TICKET_ID> <BASE_BRANCH>` bugfix entry point, but the
QA Execution Agent itself never invokes that, and never hands off to the
Coding Agent, Code Review Agent, or PR Agent.

## Shared coding standards (apply to every module)

- Commit message format: `<type>(<module>): <short summary>`
  (types: feat, fix, refactor, test, docs, chore)
- Cross-module interfaces (API contracts, shared types) are documented in
  Confluence by the Architect and must not change unilaterally — see each
  coder agent's "what not to do."

## Definition of done (checked by the Reviewer agent)

A module/ticket is "done" only when all of the following are true:

- [ ] Matches the acceptance criteria in the linked Jira ticket / Confluence page
- [ ] Passes lint/format checks (enforced by hook, not manual)
- [ ] Passes its own test suite
- [ ] No unresolved Reviewer comments on the ticket
- [ ] Public functions/interfaces documented with a one-line docstring/comment
- [ ] If the module exposes or consumes a cross-module interface, it matches
      the documented contract exactly (no silent drift between backend/frontend)

Module-specific additions to this checklist (e.g. "matches OpenAPI spec",
"passes accessibility lint") live in that module's nested CLAUDE.md.

## Context engineering rules

- **Global context (this file)**: stable, low-churn, shared by every module.
  Only updated via a deliberate Decisions Log entry — never grows by
  accumulation. Backend/frontend-specific standards go in the nested files
  instead of being added here.
- **Per-module context (nested CLAUDE.md)**: stable per module, only loaded
  by agents working inside that module's folder.
- **Per-feature context**: lives in the module's Jira ticket + linked
  Confluence page. Only the coder agent working that ticket loads it.
- **Compaction**: when a module is marked done, the Reviewer agent (or a
  dedicated compaction step) writes a 2-3 line summary into the Decisions
  Log below. Future agents read the summary, not the full ticket history.

## Decisions log

> One entry per architectural decision or completed module. Keep each entry
> to 2-3 lines. This is what keeps global context small as the project grows.

- **2026-09-02 — Pipeline reconciliation**: Locked Idea as Community Health
  Hub (CHH, PRD-CHH-v2.2); replaced backend content that had been copied in
  from an unrelated prior template ("KTA"). Simplified the orchestrator
  sub-pipeline from multi-repo/microservices assumptions (shared NuGet repo,
  sibling cloned repos) down to this repo's actual single-monorepo shape,
  and dropped the RCA bugfix workflow (no bug tickets exist yet — add back
  when needed). Added `frontend-*-agent.md` counterparts (React + TS + Vite)
  alongside the existing `backend-*-agent.md` set, and a design-readiness
  check in the Planning Agent for tickets labeled `needs-design`.
- **2026-09-05 — Deployment targets locked**: Frontend deploys to **Vercel**
  (git-push-to-deploy from the `frontend/` folder); backend deploys to
  **AWS** (App Runner/Elastic Beanstalk + RDS PostgreSQL). Split-cloud, not
  all-AWS — chosen for Vercel's faster Vite/React deploy experience. Backend
  CORS must allow the Vercel origin(s); see `backend/CLAUDE.md` and
  `frontend/CLAUDE.md` for the per-side detail.
- **2026-09-08 — CHH-73 interim SystemAdmin mechanism settled**: Two
  independent fixes for the same PR review comments (hardcoded admin mobile
  number → real mechanism) landed on the same branch — one adding
  `IndividualProfile.IsAdmin`, the other a separate `AdminUser` table. Kept
  `IndividualProfile.IsAdmin` (see `.claude/rules/api-standards.md` §5); the
  `AdminUser` table/repository were removed. Routing (the global
  `RoutePrefixConvention` + controller-naming coupling — see
  `.claude/rules/api-standards.md` §1) was untouched by this decision.
- **2026-09-09 — Codebase-scan caching + pipeline drift check added**:
  Codebase Analysis Agent now caches known Service/Repository/Controller
  classes in `.claude/backend-symbol-map.md`, keyed to `codebaseRef`, and
  only re-scans git-diffed files (falls back to a full scan if the map is
  missing/stale or >25% of tracked files changed — never trusts cache for
  anything the diff flags as changed). **Correction, same day:** the map is
  git-ignored, not committed — it's a derived, disposable artifact, and
  committing it would create merge conflicts between concurrent feature
  branches instead of just triggering a cheap rebuild. Added a maintainer-run
  `pipeline-regression-skill` plus `.claude/golden-tickets.md`
  (CHH-8/35/38) to catch silent drift in agent `.md` files after edits —
  advisory only, not part of the per-ticket workflow.
- **2026-09-09 — Git safety guardrails added**: New `.claude/rules/git-safety.md`
  forbids `--force` pushes, `reset --hard`, `clean -f`, force-deleting
  branches, amending pushed commits, rebase, and `--no-verify` across the
  whole pipeline (not just the coder), and restates that a reviewed GitHub
  PR merge is the only path onto `gitBaseBranch`. Wired in via Orchestrator
  Rule 13 and referenced from `backend-coding-agent.md`,
  `frontend-coding-agent.md`, `pr-agent.md`, `git-branch-skill.md`, and
  `github-pr-skill.md`.
- **2026-09-09 — BA gap-flag flow added**: Prompted by CHH-43 (QR check-in
  dropped from scope with no rationale recorded anywhere). Knowledge Agent
  and Planning Agent now flag `Owner: BA` gaps/Open-Questions rows to the
  ticket's Jira reporter via a new `gap-flag-skill` (Confluence footer
  comment + Jira comment, always confirmed with the developer first) —
  see Rule 10's narrow exception in `orchestrator.md`. Jira status
  transitions and all other comment uses remain prohibited.
- **2026-09-08 — CHH-68 Emergency Services Hub breakdown**: Split into
  backend ticket CHH-82 and frontend ticket CHH-83, extending the existing
  Facility domain (no new module/folder) — see the CHH-F06 Technical Design
  Confluence page linked from both tickets. `Facility` gains nullable
  `Latitude`/`Longitude`; `FacilityCategory` gains `Ambulance` (additive,
  non-breaking). Ambulance-operator self-registration stays out of scope
  (CHH-F03 concern) — ambulance rows are admin-seeded for now.
- **2026-09-08 — Post-merge QA execution added**: Added a standalone QA
  Execution Agent (`.claude/agents/qa-execution-agent.md`), run by a QA
  automation tester **after** a PR merges — not wired into the developer
  pipeline or `orchestrator.md`'s Task Workflow (an earlier same-day attempt
  to gate it pre-merge, before PR, was reverted — wrong actor and wrong
  timing). It reads the Feature's Confluence QA Test Case Design +
  Automation Mapping pages, runs `.github/workflows/qa-tests.yml`, publishes
  a QA Execution Report to Confluence, and on failure (with tester
  confirmation) opens a linked Jira Bug ticket that re-enters development via
  the existing `/dev` bugfix path. Runs in a degraded "Coarse Mode"
  (job-status only) until `qa-tests.yml` gains real per-test-case
  (`TC-CHH-F0X-NN`) aggregation, tracked separately. See root `CLAUDE.md`
  §"QA execution (post-merge)".

## Non-goals / out of scope

- Live GPS tracking of moving ambulances
- Active sleep tracking (UI placeholder only — no functional tracking)
- Medical diagnosis or clinical advice
- Multi-tenant / multi-repo infrastructure (this is a single-team, single-repo build)
