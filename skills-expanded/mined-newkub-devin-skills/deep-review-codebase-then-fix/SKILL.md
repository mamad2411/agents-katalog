---
name: deep-review-codebase-then-fix
description: Review first, then fix in context, asking the user to confirm
argument-hint: "[scope]"
related:
  - deep-thinking
  - deep-analyze
  - review
  - fix
  - watch-browser
  - follow-best-practice
  - deep-review-codebase
  - create-plan-in-dot-devin
  - suggest-next-action
  - resolve-errors
  - run-review
  - run-test

---

## Goal

Canonical fix skill — review then fix findings in every domain per the Domain Map, through this skill's `## Execute` fix steps; `deep-review-codebase/SKILL.md` holds only the review principles, fixes live here

## Scope

Use when you want both review and fix without a specific target; supports code, docs, and skills

- Small/narrow scope → use the matching `/review` domain; whole-codebase scope → use `/deep-review-codebase` as the review pass
- Fix findings after review per the Domain Map below
- Fix mode: user confirms per finding (default), follows the original suggestion (`/follow-your-suggestion`), or `fix all` as the user specifies

See also: /deep-review-codebase

## Domain Map

Fixes run through this skill's fix steps (`## Execute` 4-5) per the domain of the finding — the review side is always `/deep-review-codebase` with that dimension; metric domains route to `/optimize <scope>`

| Domain | Review dimension | Fix route |
|--------|-------------|-----------|
| seo | `/deep-review-codebase` | `## Fix` — meta, structured data, sitemap, CWV |
| security | `/deep-review-codebase` | `## Fix` — secrets rotation, headers, vuln deps (`/run-audit`) |
| auth | `/deep-review-codebase` | `## Fix` — sessions, tokens, OAuth, MFA; authz/RBAC UI → review-auth + review-frontend slices |
| api | `/deep-review-codebase` | `## Fix` — contract drift, versioning, errors |
| backend | `/deep-review-codebase` | `## Fix` — services, handlers, data flow |
| frontend | `/deep-review-codebase` | `## Fix` — components, state, rendering, hydration; scoped slices: forms, i18n, a11y |
| data-validation | `/deep-review-codebase` | `## Fix` — schemas, boundary validation |
| database | `/deep-review-codebase` | `## Fix` — migrations, schema + query perf → `/optimize queries` |
| dependencies | `/deep-review-codebase` | `## Fix` — updates (`/update-version-to-latest`, `/run-audit`) |
| bundle+assets+build speed | `/deep-review-codebase` | `/optimize bundle` |
| performance | `/deep-review-codebase` | `/optimize perf` (network → `/optimize network`; startup → `/optimize startup`) |
| memory | `/deep-review-codebase` | `/optimize memory` |
| cost | `/deep-review-codebase` | `/optimize cost` |
| ci/pipeline | `/deep-review-codebase` | `/optimize ci` |
| docker | `/deep-review-codebase` | `/optimize docker` (guided workflow → `follow-create-docker/workflows/optimize-image`) |
| tests | `/deep-review-codebase` | `## Fix` (flaky → `/check-flaky-tests`) + `/update-tests` for writing new tests |
| uxui | `/deep-review-codebase` | `## Fix` — design system/interaction/motion/UX copy + `/watch-browser fix` (browser pass) |
| observability / iac / platform | `/deep-review-codebase` | `## Fix` — metrics, tracing, alerting, infra code |
| accessibility | `/deep-review-codebase` | `## Fix` — WCAG, keyboard, contrast |
| i18n | `/deep-review-codebase` | `## Fix` — catalogs, RTL, formats |
| events | `/deep-review-codebase` | `## Fix` — schemas, ordering, idempotency, DLQ (queue ops same route, per scope-map boundaries) |
| compliance | `/deep-review-codebase` | `## Fix` — consent, retention, PII handling |
| business | `/deep-review-codebase` | `## Fix` — domain logic vs requirements |
| release | `/deep-review-codebase` | `## Fix` — versioning, changelog, publish |
| delivery | `/deep-review-codebase` | `## Fix` — CI/CD, release pipeline |
| stability | `/deep-review-codebase` | `## Fix` — crash/recovery (error paths/UI → error-handling slice; messaging → events slice) |
| error-handling | `/deep-review-codebase` | `## Fix` (sole owner: error paths, retries, recovery, error states, error UI, error boundaries) |
| architecture | `/deep-review-codebase` | `/follow-architecture` (choose + apply pattern; move files/split layers → `/refactor`) |
| migration | `/deep-review-codebase` | `## Fix` — backward compat, data integrity, rollback, cutover |
| quality/types | `/deep-review-codebase` | `## Fix` — complexity, imports |
| usage | `improve-usage-md` | `/update-usage-md` + verify via `/deep-test usage` |
| others (cli, config, docs, mobile, desktop, browser-ext, dx, sdk, ai, mcp, workflow, writing) | `/deep-review-codebase` | `## Fix` section of that dimension — fix per the findings directly |

## Execute

### 1. Identify Scope

> Goal: Know what to review and fix

1. Run `/deep-thinking` to analyze the context and the scope's goal before starting; when the scope's shape is unclear, take structure/dependency evidence from `/deep-analyze` first
2. Identify the target files or area; run `/review` to find issues — scope findings precisely, separate root cause from symptom, estimate blast radius per finding, search related code paths
3. Record findings with severity and evidence

### 2. Plan Fixes

> Goal: Plan the fixes

1. Run `/create-plan-in-dot-devin` to plan the fixes in detail before starting
2. Prioritize by severity then effort; order fixes critical → high → medium → low; map dependencies between fixes
3. Identify the files to change — minimal fix strategy, no scope creep
4. Run `/report-before-after` to summarize the plan before starting
5. Record findings with severity and evidence

### 3. Confirm

> Goal: Get approval before fixing

1. Use `ask_user_question` to ask the user whether to approve the fixes
2. Surface the risks of each fix and note alternatives
3. If the user declines → stop and report; if the user approves → continue

### 4. Apply Fixes

> Goal: Fix the issues per the plan

1. Use `edit` or `write` to fix files one step at a time — minimal, surgical, atomic, reviewable diffs with consistent style; preserve behavior except the intended change
2. If the issue is complex or an error occurs → run `/resolve-errors`
3. Dispatch approved fixes by domain — group findings, then map them to the fix route per the Domain Map above; a domain not in the table → `/ask-me` before fixing
4. Record findings with severity and evidence

### 5. Verify

> Goal: Check the results after fixing

1. Run tests/build/typecheck according to the ecosystem — each fix verified immediately (test/build/run), regression check, `/run-check` pass
2. Run `/deep-validate`
3. Capture before/after evidence via `/report-before-after`
4. Run `/suggest-next-action`

## Rules

### 1. Review Before Fix
- Must `/review` and report before editing
- Never edit without confirmation

### 2. Incremental Fix
- Fix one file or a small batch at a time
- Verify after each fix

### 3. Evidence
- Every fix must have a reason from the review
- Cite file path and line number

### 4. Phase Checklist

- Scope — findings scoped precisely (root cause vs symptom), blast radius estimated, related code paths searched
- Planning — minimal fix strategy, no scope creep; fix order critical → high → medium → low; dependencies between fixes mapped
- Confirmation — user confirm before changes (per global rules); fix risks surfaced, alternatives noted
- Application — fixes minimal + surgical, style consistent; behavior preserved except intended change; atomic, reviewable changes
- Verification — each fix verified immediately (test/build/run); regression check, `/run-check` pass; before/after evidence (`/report-before-after`)

- Use /fix if you want to fix per the suggestion or fix all
- Use /watch-browser fix if needed
- Use /follow-best-practice if needed
- Use /deep-review-codebase if needed
- Use /suggest-next-action if needed
- Use /resolve-errors if needed

## Metrics

- Fix score: fixes verified / fixes attempted × 100 — grade A (90+), B (80+), C (70+), D (60+), F (<60)

Supplementary metrics:

| No. | Metric | Description | How To Calculate |
|-----|--------|-------------|------------------|
| 1 | Review Coverage Ratio | % reviewed items in scope that were fixed and verified | fixed / total × 100 |
| 2 | False Positive Rate | % fixes reverted or not accepted | reverted fixes / total fixes × 100 |
| 3 | Evidence Strength Score | % findings with evidence (file/line) | findings with evidence / total findings × 100 |
| 4 | Actionability Score | % findings with clear recommendation | actionable findings / total findings × 100 |
| 5 | Severity Distribution | count of findings per severity | count of Critical/High/Medium/Low/Info |
| 6 | MTTR Estimate | estimated time to fix and verify | Critical=1d, High=3d, Medium=7d, Low=14d average |
| 7 | Before/After Trend | score improvement over time | (after - before) / before × 100 |
| 8 | Risk Exposure Index | high-severity unfixed issues in critical areas | count of Critical/High findings in critical scope |
| 9 | Scope Boundary Adherence | % fixed issues inside declared scope | in-scope findings / total findings × 100 |
| 10 | Documentation/Report Quality | % fixes with file/line and reason | documented findings / total × 100 |

Domain-specific metrics:

| No. | Metric | Description | How To Calculate |
|-----|--------|-------------|------------------|
| 1 | Fix Success Rate | % fixes that pass verification | fixed verified / total fixes × 100 |
| 2 | Regression Rate After Fix | % fixed issues that reintroduce problems | regressions / total fixed × 100 |
| 3 | Verification Coverage | % findings covered by a verification step | verified findings / total findings × 100 |

## Fix

> This section is the canonical fix boilerplate — `deep-review-codebase` is report-only by contract

1. Rank findings by severity — critical first, then fix one at a time with verification immediately after each fix
2. Pick the fix route matching each finding from the Domain Map above (then fix)
3. Every fix preserves existing behavior, passes `/run-check` and `/run-test` if present, then summarizes with `/report-before-after`

## References

- Use /run-review if needed
- Use /create-plan-in-dot-devin if needed
- Re-run via /run-test <domain> after fixing to verify tests are green

## Subagents

> Goal: Independent work that can be spawned in parallel — profiles live in this section, no separate files needed

### fix-worker — apply the fixes the user approved within a single module/domain, then verify and return changed files + results (use when findings span several modules that can be fixed in parallel without collision)

- **Inputs**: `findings` (the approved findings list for this module/domain — finding id, severity, `file:line`, recommendation), `scope` (the single module/domain it owns, e.g. `src/auth/`, `domain=security`, `package=ui`), `fix-guides` (optional — paths of the matching domain's `## Fix` section or workflow `SKILL.md`), `verify-commands` (optional — commands for verifying, e.g. `bun run typecheck`, `bun run test`)
- **Tools**: `read`, `grep`, `find_file_by_name` (read fix guides and the source to be fixed), `edit`/`write` (apply only the approved fixes), `exec` (run lint, typecheck, tests after each fix)
- **Execute**:
  1. Read the fix route for the matching domain (per the Domain Map above) — if none exists, fix directly per the finding's recommendation
  2. Rank findings by severity — `critical` first, then fix one at a time
  3. Each fix must preserve the original behavior — minimal diff, no refactoring beyond the finding
  4. Verify immediately after each fix with `verify-commands` or checks the scope supports
  5. If a fix breaks a check → revert that fix and mark it `failed` with the reason, then continue
- **Output**: table `| No. | Finding | Status | Changed Files | Verify Result |` — `status`: `fixed`/`failed`/`skipped` (out of scope or missing approval); close with a summary of total fixed/failed/skipped, all changed files, and aggregate verify (`pass`/`fail`); if aggregate verify fails → list the reverted fixes and residual risk
- **Constraints**: fix only the findings in the `findings` list within the assigned `scope` — never touch another module's findings; never apply unapproved fixes — if unclear, mark `skipped` with a reason; every fix must pass its own verify — on failure revert immediately, never leave a broken state; never touch files outside `scope` unless a finding requires it (e.g. a shared import) — must be noted in the output; no commits — the parent commits after merging all worker results

## Expected Outcome

- Issue report before fixing
- Issues fixed as the user agreed
- Verification passed
- Next-action summary with `/review` and `/fix`
