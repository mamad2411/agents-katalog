---
name: product-manager-skill
description: Turn analytics and customer signals into prioritized product decisions, PRD drafts, experiment plans, and implementation-ready GitHub backlog issues.
license: MIT
homepage: https://github.com/wotaso/analyticscli-skills
metadata: {"author":"wotaso","version":"0.8.2","openclaw":{"emoji":"📌","homepage":"https://github.com/wotaso/analyticscli-skills"}}
---

# Product Manager Skill

## Use This Skill When

- you need to prioritize product opportunities from analytics signals
- you want concise PM outputs that engineering can execute directly
- you need a PRD or experiment brief with measurable success criteria
- you need a decision memo with tradeoffs and recommendation
- you want analytics + code context converted into prioritized GitHub issues

## Core Rules

- Always state assumptions explicitly before recommendations.
- Prioritize with an `impact x confidence x effort` rationale.
- Tie every recommendation to at least one measurable KPI.
- Keep scope bounded: max 3 major opportunities or max 3-5 generated issues per pass.
- Avoid generic advice without concrete scope and acceptance criteria.
- Mark low-confidence conclusions clearly if data quality is weak.
- For implementation outputs, include explicit file/module hypotheses.
- For autopilot mode, run a preflight checklist and list missing dependencies/secrets explicitly.
- If the user says "start/run the skill", do not ask generic discovery questions first. Run the startup protocol below.
- In `start/run`, never require workspace-local helper files under `scripts/` or `data/` as a hard prerequisite.

## Required Inputs (Manual PM Mode Only)

- problem statement or objective
- at least one data source summary (analytics, feedback, revenue, errors)

## Optional Inputs

- constraints (timeline, team capacity, dependencies)
- strategic context (OKRs, business goals, target segment)
- existing roadmap or in-flight initiatives
- repository root (for file/module mapping when generating issue drafts)
- GitHub repo + token (required baseline; use least-privilege fine-grained token)

## Autopilot Preconditions (Mandatory)

Before running issue generation/autopilot mode, verify and report:

- Data sources:
  - `analytics_summary.json` (required)
  - `revenuecat_summary.json` (recommended for monetization decisions)
  - `sentry_summary.json` (recommended for stability prioritization)
  - `feedback_summary.json` (optional, but high value)
- Code-readiness:
  - `--repo-root` points to the target repository checkout
  - agent user has read access to the codebase
  - if needed, restrict scan with `--code-roots apps,packages`
- Runtime dependencies:
  - `node` for analyzer/runner
  - `analyticscli` CLI for analytics data extraction
  - `analyticscli-cli` skill must be installed/fetched (for canonical analytics source refresh workflow)
  - optional charting: `python3` + `matplotlib`
- Secrets:
  - `GITHUB_TOKEN` (required baseline; fine-grained PAT with repository `Issues: Read/Write`, `Contents: Read`)
  - `ANALYTICSCLI_READONLY_TOKEN` (recommended; required for non-keychain CLI auth)
  - `REVENUECAT_API_KEY`
  - `SENTRY_AUTH_TOKEN`
  - optional `FEEDBACK_API_TOKEN`

If anything is missing, stop autopilot and return a concrete "missing items" list with where to obtain each value.

## OpenClaw Startup Protocol (Mandatory)

When the user asks to start/run/kick off the skill, execute this exact sequence.
This protocol must work even when the user prompt is vague and even when repo-specific helper scripts are missing.

0. ClawHub layout (only when `scripts/openclaw-growth-start.mjs` is missing at workspace root):
   - ClawHub installs skills under `skills/<slug>/`. If `skills/product-manager-skill/scripts/openclaw-growth-start.mjs` exists but `scripts/openclaw-growth-start.mjs` does not, run once from workspace root:
     - `bash skills/product-manager-skill/scripts/bootstrap-openclaw-workspace.sh`
   - Then the standard paths `scripts/...` and `data/openclaw-growth-engineer/...` exist at the workspace root for tools that expect them.

1. Start in portable mode first (always):
   - Ensure dependencies and auth without asking for manual analytics summaries:
     - check `analyticscli` binary (`command -v analyticscli`)
     - check analytics auth (`analyticscli projects list` with token or existing login)
     - check `GITHUB_TOKEN` presence (fine-grained token: repository `Issues: Read/Write`, `Contents: Read`)
     - detect GitHub repo from `git remote origin` if available; if not available, ask once for `owner/repo`
   - If any check fails, return only a concrete blocker checklist with exact fix commands.
2. Portable mode execution:
   - run first pass directly via `analyticscli` commands (bounded, deterministic)
   - generate 3-5 prioritized issue drafts and create GitHub issues when allowed
3. After run:
   - report whether drafts were generated and whether GitHub issues were created
   - include command to repeat the same run path

Never block on "please provide goal + datasource" if config and sources already exist.
Never fail only because local helper files are missing in the workspace.
If config or runtime prerequisites are missing, return only a concrete missing-items checklist (config path, API keys, repo access, missing binaries/skills). Do not ask for manual data summaries in start/run mode.

## Standard Output Format

Return results in this order:

1. `Executive Summary` (3-5 lines)
2. `Top Opportunities` (max 3, ranked)
3. `Recommendation` (single preferred path + why)
4. `Execution Scope` (in-scope, out-of-scope, dependencies)
5. `KPIs And Targets` (baseline, target, measurement window)
6. `Acceptance Criteria` (implementation-ready)
7. `Risks And Mitigations`
8. `Next 7-Day Plan`

If the user explicitly asks for issue generation/autopilot mode, return this format instead:

1. `Executive Summary` (3-5 lines)
2. `Top Issue Drafts` (3-5, ranked)
3. `Recommendation` (single preferred execution path)
4. `Execution Order` (week 1 sequencing)
5. `Risks And Guardrails`

Each issue draft must include:

- `Problem`
- `Evidence`
- `Affected Files / Modules`
- `Proposed Implementation`
- `Expected Impact`
- `Confidence`
- optional PR prompt

## Output Quality Bar

- recommendations are testable within one iteration cycle
- each KPI has a concrete time window
- acceptance criteria can be copied into engineering tickets
- risk section includes at least one rollback or guardrail condition
- in issue mode, each issue has clear file/module hypotheses and measurable impact

## Anti-Patterns

- broad strategy talk without operational next steps
- recommendations that ignore technical or business constraints
- “improve UX” phrasing without affected flow/module hypothesis

## Portable Start Commands

Dependency/auth checks:

```bash
command -v analyticscli
analyticscli projects list
```

Baseline analytics pull (bounded):

```bash
analyticscli schema events --limit 200 --last 30d --format json
```

Optional additional signals:

```bash
analyticscli timeseries --metric unique_users --interval 1d --last 30d --format json
```

## References

- [README](README.md)
- [Required Secrets](references/required-secrets.md)
- [Setup And Scheduling](references/setup-and-scheduling.md)
- [Input Schema](references/input-schema.md)
- [Issue Template](references/issue-template.md)
