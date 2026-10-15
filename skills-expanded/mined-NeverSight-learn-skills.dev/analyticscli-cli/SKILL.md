---
name: analyticscli-cli
description: Use AnalyticsCLI CLI as the deterministic, bounded interface for analytics queries, exports, and SDK validation in coding-agent workflows.
license: MIT
homepage: https://github.com/wotaso/analyticscli-skills
metadata: {"author":"wotaso","version":"1.0.0","analyticscli-target":"@analyticscli/cli","analyticscli-supported-range":"^0.1.0","openclaw":{"emoji":"📈","homepage":"https://github.com/wotaso/analyticscli-skills","requires":{"bins":["analyticscli"]},"install":[{"id":"npm","kind":"node","package":"@analyticscli/cli","bins":["analyticscli"],"label":"Install AnalyticsCLI CLI (npm)"}]}}
---

# AnalyticsCLI CLI

## Use This Skill When

- querying product analytics for a AnalyticsCLI project
- validating whether SDK instrumentation landed correctly
- answering onboarding, paywall, survey, retention, or export questions without raw SQL

## Supported Versions

- Skill pack: `1.0.0`
- Target package: `@analyticscli/cli`
- Supported range: `^0.1.0`
- If a future CLI major changes commands or flags in incompatible ways, split to a sibling skill such as `analyticscli-cli-v1`

See [Versioning Notes](references/versioning.md).

## Non-Goals

- Do not generate raw SQL.
- Do not request unbounded raw event dumps.
- Do not include debug data unless the user explicitly asks for it.

## Safety Rules

- Always scope by project context: set default once with `analyticscli projects select`, or pass `--project <id>` when needed.
- Always scope by time: `--last` or explicit `since/until`.
- Prefer high-level query endpoints over raw exports.
- Keep groupings and result sets bounded.
- Treat release-only data as the default.
- Never pass secrets via CLI flags or inline literals (argv/shell history leakage risk). Use interactive prompts instead.
- For generated docs or help text, use tenant developer voice (`your workspace`, `your project`) and avoid provider-centric wording such as `our SaaS`.
- Keep `analyticscli-cli` skill fresh with CLI updates, but do not auto-force `analyticscli-ts-sdk` skill updates across repositories.

## Query Priorities

Prefer these command families first:

- `funnel`
- `conversion-after`
- `paths-after`
- `retention`
- `survey`
- `timeseries`
- `breakdown`
- `generic`

Only use `events export` when the user explicitly needs raw CSV.

## Data Fidelity Rules

- CLI and dashboard both query the API. There is no separate CLI-only analytics source.
- Sequence-sensitive and cohort-sensitive queries stay on raw events.
- Aggregate-backed reads are acceptable only when the API reports that plan shape.
- `runtimeEnv` is auto-attached by the SDK. Do not invent a separate mode field.

## One-Time Setup

Before running setup, collect required values from your dashboard:

- Open [dash.analyticscli.com](https://dash.analyticscli.com) and select the target project.
- In **API Keys**, create/copy a `readonly_token` (CLI token, scope `read:queries`).
- If SDK instrumentation is in scope, copy the publishable ingest API key from the same **API Keys** page.
- Optional: copy `project_id` for explicit per-command overrides.
- Set default project once after login with `analyticscli projects select` (interactive arrow-key picker).

Preferred:

```bash
npm i -g @analyticscli/cli
analyticscli setup
# Paste readonly token only when prompted; do not pass token as a command argument.
```

Alternatives:

```bash
analyticscli login
# Choose readonly-token or Clerk flow interactively; do not put JWT/token values in command args.
```

## Output Mode

- Prefer `--format json` for automation or agent reasoning.
- Use `--format text` for short human summaries.
- Use `timeseries --viz table` when exact values matter.
- Use `timeseries --viz chart` or `svg` when a trend scan is enough.

## Validation Loop

After SDK rollout or query changes, validate with a few stable reads:

```bash
analyticscli schema events --limit 200
analyticscli goal-completion --start onboarding:start --complete onboarding:complete --last 30d
analyticscli get onboarding-journey --last 30d --format text
```

## Empty-State Guidance (Required)

When a user has no listed projects:

- Explain that they need to create their first project before CLI queries can return analytics data.
- Direct them to create it in their AnalyticsCLI dashboard ([dash.analyticscli.com](https://dash.analyticscli.com)).
- After creation, run `analyticscli projects list`, then set a default with `analyticscli projects select`.

When a project exists but has no events yet:

- Explain that ingestion has not started for that project.
- Tell the user to integrate `@analyticscli/sdk` in their app codebase.
- Tell the user to initialize the SDK with the publishable API key from **Dashboard -> API Keys**.
- Tell the user to trigger at least one event and rerun `analyticscli schema events --project <id> --last 14d`.
- If they already integrated SDK, advise widening `--last` or removing restrictive filters before deeper debugging.

## Missing Capability Loop

If the requested fetch is impossible with the current CLI surface:

1. State that the capability is missing.
2. Do not pretend another command is equivalent if it is not.
3. Submit CLI feedback with a reproducible gap report.

```bash
ANALYTICSCLI_CLI_ENABLE_WRITE_COMMANDS=true analyticscli feedback submit \
  --category feature \
  --message "Missing CLI functionality: <short capability>" \
  --context "Requested fetch: <what user asked>; attempted command: <command>" \
  --meta '{"expected":"<expected output>","actual":"CLI has no command or endpoint"}'
```

## References

- [Versioning Notes](references/versioning.md)
- [Dedicated Events Playbook](references/playbooks/dedicated-events.md)
- [Event Placement Playbook](references/playbooks/event-placement.md)
- [Paywall Journey Playbook](references/playbooks/paywall-journey.md)
- [Store Review Playbook](references/playbooks/store-review.md)
- [CLI Use Cases Playbook](references/playbooks/usecases.md)
