---
name: analyticscli-cli
description: Use AnalyticsCLI CLI as the deterministic, bounded interface for analytics queries, exports, and SDK validation in coding-agent workflows.
license: MIT
homepage: https://github.com/wotaso/analyticscli-skills
metadata: {"author":"wotaso","version":"1.0.7","analyticscli-target":"@analyticscli/cli","analyticscli-supported-range":">=0.1.3 <0.2.0","openclaw":{"emoji":"📈","homepage":"https://github.com/wotaso/analyticscli-skills","requires":{"bins":["analyticscli"]},"install":[{"id":"npm","kind":"node","package":"@analyticscli/cli","bins":["analyticscli"],"label":"Install/update AnalyticsCLI CLI (npm package @analyticscli/cli)"}]}}
---

# AnalyticsCLI CLI

## Use This Skill When

- querying product analytics for a AnalyticsCLI project
- validating whether SDK instrumentation landed correctly
- reviewing or submitting project feedback through AnalyticsCLI
- answering onboarding, paywall, survey, retention, or export questions without raw SQL

## Supported Versions

- Skill pack: `1.0.7`
- Target package: `@analyticscli/cli`
- Supported range: `>=0.1.3 <0.2.0`
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

## Error Recovery Order

When there are problems, errors, unexpected output, or missing CLI/API behavior:

1. Refetch this skill and update the CLI first.
2. Rerun the exact failing command or smallest reproducible command.
3. If no newer version is available, the update fails, or the newest version still has the problem, submit sanitized product feedback to the AnalyticsCLI SaaS owner with `analyticscli feedback submit`.

Recommended update check:

```bash
npx -y skills add wotaso/analyticscli-skills --skill analyticscli-cli
npm install -g @analyticscli/cli || npm install -g --prefix "$HOME/.local" @analyticscli/cli
export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"
analyticscli --help
```

Feedback must include the version/update attempt, failing command or endpoint, sanitized payload shape, status/error body, request id if present, expected behavior, actual behavior, and workaround.

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

## Feedback Commands

Use these when the task involves feedback about AnalyticsCLI itself, such as missing features, broken CLI/API/dashboard behavior, confusing errors, poor docs, or workflow friction:

```bash
analyticscli feedback list --last 30d --format json
analyticscli feedback summary --last 30d --format json
analyticscli feedback submit --category bug --message "Short symptom" --origin-name "dashboard feedback form" --location-id "dashboard/feedback"
```

Rules:
- do not confuse this with tenant-owned end-user feedback collected by the AnalyticsCLI feedback feature
- prefer `feedback summary --format json` when another tool or skill needs a bounded theme summary
- prefer `feedback list --format json` when exact raw messages matter
- always include `origin-name` and `location-id` on submit when they are known
- for API/CLI failures, first update/refetch the current skill and CLI; if the newest available version still fails, include sanitized endpoint/command, version/update attempt, status code, error body, request id if present, expected behavior, and the workaround used

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
npm install -g @analyticscli/cli
command -v analyticscli
npx -y @analyticscli/cli setup
# Paste readonly token only when prompted; do not pass token as a command argument.
```

Alternatives:

```bash
analyticscli login
# Choose readonly-token interactively; do not put tokens in command args.
```

If `analyticscli: command not found`, install or update the npm package. The package name is
`@analyticscli/cli`; the binary name is `analyticscli`.

Do not search npm for `analyticscli` or `analyticsscli`.

```bash
npm install -g @analyticscli/cli
analyticscli --help
```

On VPS hosts where global npm installs are blocked, use a user-local prefix:

```bash
mkdir -p "$HOME/.local"
npm install -g --prefix "$HOME/.local" @analyticscli/cli
export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"
analyticscli --help
```

Fetching or updating this skill is not enough by itself.
After every skill update, also update the npm package and verify the binary:

```bash
npx -y skills add wotaso/analyticscli-skills --skill analyticscli-cli
npm install -g @analyticscli/cli || npm install -g --prefix "$HOME/.local" @analyticscli/cli
export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"
command -v analyticscli
analyticscli --help
```

If `command -v analyticscli` is still empty but a user-local binary exists, update shell profile files yourself before reporting success:

```bash
for f in "$HOME/.profile" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.zshrc" "$HOME/.zprofile"; do
  touch "$f"
  grep -Fq 'export PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"' "$f" ||
    printf '\n# AnalyticsCLI CLI user-local npm bin\nexport PATH="$HOME/.local/bin:$HOME/.local/analyticscli-npm/bin:$PATH"\n' >> "$f"
done
bash -lc 'source "$HOME/.bashrc" 2>/dev/null || true; source "$HOME/.profile" 2>/dev/null || true; command -v analyticscli && analyticscli --help >/dev/null'
```

Do not say analyticscli is fixed until `command -v analyticscli && analyticscli --help >/dev/null` succeeds in the same command context you control.

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
3. Submit CLI feedback with a reproducible gap report to the AnalyticsCLI feedback store.

```bash
analyticscli feedback submit \
  --category feature \
  --message "Missing CLI functionality: <short capability>" \
  --origin-name "analyticscli cli" \
  --location-id "analyticscli-cli" \
  --context "Requested fetch: <what user asked>; attempted command: <command>" \
  --meta '{"expected":"<expected output>","actual":"CLI has no command or endpoint"}'
```

## Auto Feedback Rule

When a user reports broken behavior, unexpected output, or missing functionality, first update/refetch
the current skill and CLI and retry the smallest repro. If no newer version is available, the update is
blocked, or the newest version still fails, submit one concise `analyticscli feedback submit` report
automatically after explaining the issue.

Include:
- clear symptom in `--message`
- exact failing command or flow in `--context`
- expected vs actual behavior in `--meta`
- installed version and update attempt in `--context` or `--meta`

## References

- [Versioning Notes](references/versioning.md)
- [Dedicated Events Playbook](references/playbooks/dedicated-events.md)
- [Event Placement Playbook](references/playbooks/event-placement.md)
- [Paywall Journey Playbook](references/playbooks/paywall-journey.md)
- [Store Review Playbook](references/playbooks/store-review.md)
- [CLI Use Cases Playbook](references/playbooks/usecases.md)
