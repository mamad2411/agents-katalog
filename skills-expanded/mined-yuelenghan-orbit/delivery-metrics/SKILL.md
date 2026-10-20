---
name: delivery-metrics
description: Use when collecting Sprint delivery data or analyzing Sprint efficiency and bottlenecks, including trigger-only validations that should skip shell or host-resource discovery and collect only missing metrics inputs.
metadata:
  author: Orbit contributors
  version: "1.0.14"
---

# Delivery Metrics Collection & Analysis

Automatically collect Sprint delivery data from the tracker and repository providers, calculate core metrics, diagnose bottlenecks, and generate an analysis report inline or in the docs platform when available.

Trigger-only routing guard: if the prompt already asks for Sprint delivery metrics or efficiency analysis, treat `delivery-metrics` as selected. Do not turn the turn into a host-platform audit, skill-installation audit, host-entry troubleshooting, or metric-design interview. Do not probe local resource registries, editor state, or skill availability, and do not invoke `list_mcp_resources`, `list_mcp_resource_templates`, `list_apps`, `get_app_state`, `computer-use`, `browser`, or similar host discovery. If the user forbids shell, do not run shell commands even for local inspection. Ask only for missing business inputs such as `SPRINT_ID`, `TRACKER_PROJECT`, and `REPO_TARGETS`.

For trigger-only validation, do not reread installed skill files or references through shell just to confirm those inputs. Use this input table directly.

## Capability Dependencies

Required:
- `tracker`
- `repo`

Optional:
- `docs`

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SPRINT_ID` | Yes | Target Sprint ID | `149212` |
| `TRACKER_PROJECT` | Yes | Tracker project key for the active provider | `PROJ` |
| `REPO_TARGETS` | Yes | Selected repo provider targets, comma-separated for multiple | `bitbucket:sample`, `github:sample-org/sample-repo`, or `gitlab:group-or-user/sample-repo` |
| `DOCS_SPACE` | Conditional | Docs space, container, or workspace identifier when docs writeback is used | `PROJ` |
| `DOCS_PARENT_REF` | Conditional | Parent page, folder, or document identifier when docs writeback is used | `1531709516` |
| `ISSUE_TYPE` | No | Jira issue type for production bugs (default: `Bug`) | `Defect` |

Ask the user for all missing required inputs in a single plain-text message. Present the parameter table above and wait for their response. Request `DOCS_SPACE` and `DOCS_PARENT_REF` only when a `docs` provider is installed and a docs writeback path will be used. Do NOT use interactive selection prompts — these are free-text values (IDs, keys, slugs) that the user types directly.

Trigger-only validation mode: if the user explicitly says this is only a skill trigger test, follow `../using-orbit/references/safety-rules.md` and ask only for the missing inputs from the table above, including docs writeback fields only when they are actually needed. Do not ask for host platform, skill name, trigger entry, report language, generic success criteria, Sprint source interpretation, statistic scope, completion definition, or bottleneck lenses.

## Missing-input collection rules

Ask for all missing required inputs in one plain-text message.
Prefer the smallest missing set that unblocks the selected route.
Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract.
Avoid provider-specific aliases when the shared field name already expresses the same fact.

## Before You Start

Read `../using-orbit/references/safety-rules.md`, `../using-orbit/references/cli-patterns.md`, and `../using-orbit/references/output-conventions.md` for shared conventions that apply to all steps below.

Keep repository-wide write-confirmation, input-normalization, and provider-resolution rules in the shared references instead of duplicating the full protocol here.

### Preflight Configuration Check

Follow the capability-based preflight protocol in `../using-orbit/references/safety-rules.md`.
`tracker` and `repo` are required.
If no `docs` provider is installed, still calculate the metrics and present the report inline instead of writing to a docs platform.

### Step 1: Collect Tracker Sprint Data

Get Sprint overview:
```
jira agile sprint get --id {{SPRINT_ID}}
```

Get all issues in the Sprint:
```
jira agile sprint issues --id {{SPRINT_ID}}
```

If the Agile endpoint response is paginated or the reported total is greater than the returned issue count, immediately switch to a full Sprint JQL read and use that full issue list as the source of truth for all subsequent metrics:
```
jira issue search --jql "sprint = {{SPRINT_ID}}" --max-results 200
```

**If the issue list is empty, or the Sprint state is `future` / `planned`:** inform the user that metrics cannot be calculated for a Sprint that has not entered execution. Output: "Sprint {{SPRINT_ID}} has no completed work yet — metrics will show N/A. Verify the Sprint ID or confirm the Sprint is active." Do not proceed to metric calculations; skip to Step 6 and generate a report with all metrics marked as N/A.

From the Sprint issue list, determine `DELIVERY_ISSUE_TYPES` before querying metrics:

- Exclude `Sub-task`, `Epic`, and pure container issue types by default.
- If `Story` exists in this Sprint, use `Story` as the primary delivery work-item type.
- If `Story` does not exist, use the standard issue types actually present in the Sprint that represent planned delivery work (for example `Task`, `Defect`) and report the detected set explicitly.
- Inspect the detected delivery issues for a numeric points field. If all detected delivery issues have no usable points value, keep throughput and completion-rate calculations in count mode and mark points-based metrics as `N/A` instead of fabricating them.

Get completed delivery issues (for Lead Time + throughput):
```
jira issue search --jql "sprint = {{SPRINT_ID}} AND issuetype in ({{DELIVERY_ISSUE_TYPES}}) AND statusCategory = Done" --max-results 100
```

For each completed delivery issue, get details:
```
jira issue get --key <ISSUE_KEY>
```
Extract `created` and `resolutiondate`. Estimated Cycle Time (Lead Time) = resolutiondate - created.

Get incomplete delivery issues (Carryover):
```
jira issue search --jql "sprint = {{SPRINT_ID}} AND issuetype in ({{DELIVERY_ISSUE_TYPES}}) AND statusCategory != Done" --max-results 50
```

Get production Bugs (defect escape rate):
```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND type = {{ISSUE_TYPE}} AND labels = production AND created >= -14d" --max-results 50
```

### Step 1.5: Discover and Select Repositories

For each selected repo provider target in `REPO_TARGETS`, discover repositories with the provider's repo list command.

Bitbucket examples:
```
bitbucket repo list --project <BITBUCKET_PROJECT>
```

GitHub examples:
```
github repo list --namespace <GITHUB_NAMESPACE>
```

GitLab examples:
```
gitlab repo list --namespace <GITLAB_GROUP_OR_USER>
```

Present a combined numbered table grouped by selected repo provider target (provider + namespace/project + repo slug + description if available) and ask the user which repos to include in the metrics. The user may select one or more from any target. Store the selections as `SELECTED_REPOS` (each entry is a provider/namespace-or-project/repo pair).

If only one repo exists across all targets, auto-select it and inform the user (no confirmation needed).

If the target provider is GitHub, keep the selected repo provider wording aligned with the `github repo content --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}}` pattern used elsewhere in the repo.

If the target provider is Bitbucket, continue using the Bitbucket project/repo pair for the selected repo provider target.

### Step 2: Collect Repo PR Data

For each selected repo provider target in `SELECTED_REPOS`, get merged PR list within the Sprint window. Use `startDate` / `endDate` from Step 1's `jira agile sprint get`.

Bitbucket example:
```
bitbucket pr list --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --state MERGED --after {{SPRINT_START_DATE}} --before {{SPRINT_END_DATE}}
```

GitHub example:
```
github pr list --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --state closed
```

For GitHub, read closed pull requests with the packaged command surface and then filter `closed_at` / `merged_at` inside the workflow logic to keep only PRs merged within the Sprint window.

The Bitbucket CLI can filter by `closedDate` directly; GitHub v1 should use post-read filtering instead of inventing unsupported CLI flags.

Extract `createdDate` and `closedDate` to calculate PR Cycle Time.

For each PR, get review activity details.

Bitbucket example:
```
bitbucket pr activities --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --id <PR_ID>
```

GitHub example:
```
github pr activities --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number <PR_ID>
```

Calculate: first review wait time, review round count.

Aggregate PR data across all selected repos before proceeding to metric calculation.

### Step 3: Read Previous Report (for trend comparison)

If no `docs` provider is installed, or this run is not using docs-space context such as `DOCS_SPACE`, skip previous-report lookup and any trend comparison that depends on docs-platform history. This includes inline-only runs where the final report will not be written back to the docs platform.

If a `docs` provider is installed and this run has the docs-space context needed for docs history, search for the previous analysis report:
```
confluence search content --cql "title ~ 'Sprint' AND title ~ '交付效率分析' AND space = '{{DOCS_SPACE}}'" --type page --limit 5
```

Obsidian provider example:
```
obsidian content search --query "Sprint {{SPRINT_ID}} 交付效率分析"
```

If found, read content and extract previous metrics:
```
confluence page get --id <LAST_REPORT_PAGE_ID> --expand body.storage
```

If no previous report exists, skip trend comparison — show only current period absolute values.

### Step 4: Calculate Core Metrics

**Apply data quality filters first** (see `../using-orbit/references/output-conventions.md`):
- Cycle Time <= 0 or > 60 days → mark as outlier, exclude from averages
- Report: "Valid Cycle Time samples: X / Total delivery issues: Y"

Calculate these 6 metrics:

1. **Estimated Cycle Time (Lead Time)** — average completed delivery-issue Lead Time (days), valid samples only
2. **Sprint Throughput** — completed delivery-issue count, plus total Points when the Sprint uses a points field
3. **Sprint Completion Rate** — completed Points / planned Points when the Sprint uses a points field; otherwise completed delivery-issue count / planned delivery-issue count
4. **PR First Review Wait Time** — average time from PR creation to first human review (exclude bot auto-comments)
5. **PR Average Rework Rounds** — average number of review round-trips
6. **Defect Escape Rate** — production Bug count / released delivery-issue count

### Step 5: Bottleneck Diagnosis

Analyze time spent in each phase, identify the slowest stage. Provide improvement recommendations based on data (not generic advice).

### Step 6: Generate Metrics Report

If no `docs` provider is installed, return the metrics report in the session output and skip docs-platform deduplication and write steps.

If a `docs` provider is installed and the user wants docs writeback:

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

**Follow `../using-orbit/references/safety-rules.md` docs writeback deduplication protocol.** Before creating, search for existing report on the selected docs provider:
```
confluence search content --cql "title ~ 'Sprint {{SPRINT_ID}}' AND title ~ '交付效率分析' AND space = '{{DOCS_SPACE}}'" --type page --limit 5
```

If a matching docs record is found, follow the docs writeback deduplication protocol in `../using-orbit/references/safety-rules.md` — fetch the existing record version when the provider supports it and ask the user whether to **update** the existing record or **create** a new one.

Display report content first, then after confirmation:

To create:
```
confluence page create --space {{DOCS_SPACE}} --title "Sprint {{SPRINT_ID}} 交付效率分析" --parent-id {{DOCS_PARENT_REF}} --body "<report HTML in Confluence storage format>"
```

Obsidian provider example:
```
obsidian content create --space {{DOCS_SPACE}} --title "Sprint {{SPRINT_ID}} 交付效率分析" --parent-ref {{DOCS_PARENT_REF}} --body "<markdown report body>"
```

To update an existing page:
```
confluence page update --id <EXISTING_PAGE_ID> --title "Sprint {{SPRINT_ID}} 交付效率分析" --body "<report HTML in Confluence storage format>" --version <current_version + 1>
```

Report includes:
- Core metrics dashboard (numbers + trend comparison with previous period when docs-history lookup ran and a previous docs report is available)
- Detected `DELIVERY_ISSUE_TYPES` and whether this Sprint used points mode or count mode
- Bottleneck diagnosis (biggest blocker this period)
- AI improvement recommendations
- Carryover root cause analysis

## Output

- 6 core metrics (Cycle Time / Throughput / Completion Rate / PR Review Time / Rework Rounds / Defect Escape Rate)
- Detected delivery issue set and point-availability note when points are `N/A`
- Bottleneck diagnosis + data-driven improvement recommendations
- Metrics report in the session output, or a docs-provider Sprint analysis record when docs writeback is used
