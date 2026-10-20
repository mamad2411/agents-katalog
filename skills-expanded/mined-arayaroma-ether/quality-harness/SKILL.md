---
name: quality-harness
description: Use when asked to build, extend, or apply a "quality harness" (frontend, backend/API, security, or deploy/release) for a project — research-backed checklists + concrete tooling/CI, not a vibes-based review. Also use when asked "what makes this codebase good quality" or to set up automated testing/lint/CI gates from scratch.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Quality Harness

A harness is a project-specific, research-grounded checklist + workflow doc (`docs/<area>-quality-harness.md`)
paired with whatever concrete tooling/CI the checklist calls for — not a generic "best practices" essay. Four
areas, built one at a time, each in its own doc, tracked in a `docs/harnesses.md` index:

1. **Frontend** — perf (Core Web Vitals), accessibility (WCAG), test shape, framework-specific canon.
2. **Backend/API** — API contract/error shape, data-layer safety, OWASP API Top 10, testing shape, observability/resilience.
3. **Security** — OWASP Top 10 (web), secrets, supply chain, session/JWT internals, data privacy, infra hardening. Explicitly scoped to NOT re-cover what the backend harness's OWASP-API-Top-10 section already owns.
4. **Deploy/release** — versioning, rollout safety (rolling/blue-green/canary), migration-vs-rollout ordering, CI/CD structure, target-infra specifics (k8s or whatever this project actually deploys to), post-deploy observability.

Do them in that order if starting from zero — each is independent, but frontend/backend are usually the highest-value first two for a typical web app. Skip an area if it doesn't apply (e.g. no frontend in a pure API project).

## The two-pass process (do not collapse these)

**Pass 1 — research (delegate, don't do it inline).** Fork a subagent per harness with a prompt that:
- Names the project's actual stack (framework, ORM, deploy target) so the research is grounded, not generic.
- Points it at any *other* harness docs already written in this repo, so it matches their exact format (dense tables: Dimension / Source / Measurable bar / Why it matters / Status here) and doesn't re-cover ground another harness already owns.
- Asks for real sources (named standards/papers/vendor docs — OWASP, WCAG, Core Web Vitals, Kubernetes docs, Prisma/ORM migration guides, Kent C. Dodds' testing trophy, etc.), not platitudes.
- **Explicitly forbids the research agent from grepping the repo or guessing "covered vs. gap."** Every "Status here" cell it writes must read `NEEDS REPO VERIFICATION: <exact grep/file to check>` instead. A research agent that guesses repo state produces confidently wrong status cells — this happened in practice (a research pass claimed a `/health` endpoint was missing when one already existed) and had to be corrected in pass 2. Don't let it happen twice.

**Pass 2 — verify + implement (you do this yourself, not a subagent).**
- Run every `NEEDS REPO VERIFICATION` check for real (grep, read the file, run the tool) and rewrite each cell with the actual finding — "Covered", "Gap, confirmed", or "Partially covered" plus what's actually true, never leave a placeholder in the shipped doc.
- Fix what's cheap and clearly in-scope right there in the same pass (a missing security header, an unpinned JWT algorithm, a missing Dependabot config, a color-contrast bug an accessibility test just caught) — don't just document gaps you could close in one line.
- Leave a documented, scoped non-goal for anything that needs a real design decision or touches ops/infra config beyond the immediate fix (e.g. migrating an nginx image to run non-root touches the exposed port *and* the deploy manifest — flag it, don't rush it).
- Re-run the project's actual build/test suite after every code change in this pass. Confirm any pre-existing failures are pre-existing (check `git status`/`git diff` on the failing files) before writing "same baseline, not caused by this pass" — don't assert that without checking.

## Format every harness doc must follow

- Title + one-line scope statement (what this doc covers, what it deliberately excludes if another harness owns adjacent ground).
- `## Why these criteria (research summary)` — one or more dense tables, columns: `Dimension | Source | Measurable bar | Why it matters | Status here`. Every "Measurable bar" should be concrete where a real threshold exists (e.g. `LCP ≤ 2.5s`, `contrast ≥ 4.5:1`, `password MinLength(8)`) — vague qualitative bars only where no real metric exists (e.g. Nielsen heuristics).
- A framework/stack-specific canon section, naming the actual libraries/patterns this project uses.
- `## Workflow` — numbered, imperative, phase-shaped (before coding / while coding / tests / before calling it done / periodic-not-per-PR).
- `## Implemented this pass` — only if pass 2 made real fixes; list them tersely.
- `## Non-goals` — explicit, with the reason (YAGNI / needs a design decision / touches ops config).
- Sources list at the bottom, every citation a real link.

## Cross-harness index

Maintain `docs/harnesses.md`: a table of `Harness | Status | Doc link`, status one of `Not started / In progress / Implemented`. Update it every time a harness doc is created or its status changes — it's the one file a future session (or a future you) should be able to read cold to know what's done.

## Applying an existing harness later (not just building it)

A harness's job isn't done once the doc exists — re-run its checks against real pages/routes/endpoints
periodically or when asked to "improve" that area, and actually fix what a real tool finds, not just what's
already listed. Concrete example this caught: a full (not impact-filtered) `@axe-core/playwright` scan of a
page that already passed the harness's `critical`/`serious`-only test still turned up `moderate` findings
(`landmark-no-duplicate-main`, `landmark-unique`) — the app's shell layout already wrapped `<router-outlet>`
in a `<main>`, and every single page component *also* rendered its own top-level `<main>`, nesting/duplicating
the landmark on every authenticated route in the app. One page's fix would have been incomplete — the same
grep-and-fix had to be repeated across every page component (excluding the couple of pages, like a login
screen, that render outside the shell and legitimately own the top-level `<main>` themselves). Lesson:
when a real tool (axe, Lighthouse, etc.) finds something, check every other component built on the same
shared layout/pattern before calling the fix done — a structural bug like this is never scoped to just the
one page someone happened to ask about.

## Common mistakes this skill exists to prevent

- Writing a generic "best practices" doc with no project-specific verification — every status claim must be checked against the real codebase, not asserted from general framework knowledge.
- Letting the research subagent guess repo state instead of flagging it for verification (see Pass 1 above) — this is the single most common failure mode observed so far.
- Treating "wrote the doc" as "done" — a harness pass that finds a real, cheap, in-scope fix and doesn't apply it is half-finished.
- Duplicating OWASP API Top 10 ground between the backend and security harnesses — decide the split up front (backend owns API-shape security: BOLA, mass assignment, rate limiting, SSRF; security owns the general OWASP Top 10 2021 plus secrets/supply-chain/session-internals/privacy/infra) and say so explicitly in both docs' opening line.
