---
name: sprint-kickoff
description: Use when analyzing Sprint readiness or acceptance-criteria completeness for a specific Sprint, including trigger-only validations that should skip shell or host-resource discovery and collect only missing planning inputs.
metadata:
  author: Orbit contributors
  version: "1.0.14"
---

# Sprint Smart Kickoff

Analyze the current Sprint's readiness by scanning the backlog, checking AC quality, comparing historical velocity, and generating a readiness result inline or in the docs platform when a `docs` provider is installed.

Trigger-only routing guard: if the prompt already asks for Sprint readiness or AC completeness for a Sprint, treat `sprint-kickoff` as selected. Do not turn the turn into a host-platform audit, skill-installation audit, or host-entry troubleshooting. If the user forbids shell, do not run shell commands even for local inspection. Do not invoke `list_mcp_resources`, `list_mcp_resource_templates`, `list_apps`, `get_app_state`, `computer-use`, `browser`, or similar host discovery. Do not ask the user to restate the skill name or trigger path. Ask only for the missing planning inputs such as `SPRINT_ID`, `TRACKER_PROJECT`, and optional docs writeback fields when they are truly needed.

For trigger-only validation, do not reread installed skill files or references through shell just to confirm those inputs. Use this input table directly.

## Capability Dependencies

Required:
- `tracker`

Optional:
- `docs`

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SPRINT_ID` | Yes | Target Sprint ID | `149212` |
| `TRACKER_PROJECT` | Yes | Tracker project key for the active provider | `PROJ` |
| `DOCS_SPACE` | Conditional | Docs space, container, or workspace identifier when docs writeback is used | `PROJ` |
| `DOCS_PARENT_REF` | Conditional | Parent page, folder, or document identifier when docs writeback is used | `1531709516` |
| `SIMILAR_LABEL` | No | Label for finding similar historical Stories | `joyclaw` |

Ask the user for all missing required inputs in a single plain-text message. Present the parameter table above and wait for their response. Request `DOCS_SPACE` and `DOCS_PARENT_REF` only when a `docs` provider is installed and a docs writeback path will be used. Do NOT use interactive selection prompts — these are free-text values (IDs, keys, slugs) that the user types directly.

Trigger-only validation mode: if the user explicitly says this is only a skill trigger test, follow `../using-orbit/references/safety-rules.md` and ask only for the missing inputs from the table above, including docs writeback fields only when they are actually needed. Do not ask for host platform, skill name, trigger entry, report language, or generic success criteria.

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
`tracker` is required for backlog reads.
If no `docs` provider is installed, skip design-document discovery and any docs-provider write path, then report that limitation explicitly.

### Step 1: Read Tracker Sprint Backlog

Get Sprint metadata:
```
jira agile sprint get --id {{SPRINT_ID}}
```

GitHub Issue provider example (milestone-backed Sprint):
```
github-issue sprint get --namespace <OWNER_OR_ORG> --repo <REPO> --id {{SPRINT_ID}}
```

Get all issues in the Sprint:
```
jira agile sprint issues --id {{SPRINT_ID}}
```

GitHub Issue provider example:
```
github-issue sprint issues --namespace <OWNER_OR_ORG> --repo <REPO> --id {{SPRINT_ID}}
```

If the Agile endpoint response is paginated or the reported total is greater than the returned issue count, immediately switch to a full Sprint JQL read and use that full issue list as the source of truth for all subsequent checks:
```
jira issue search --jql "sprint = {{SPRINT_ID}}" --max-results 200
```

**If the issue list is empty, STOP.** Output: "Sprint {{SPRINT_ID}} has no Stories. Verify the Sprint ID or check if the backlog has been planned." Do not execute subsequent steps.

### Step 2: Check Each Story

For each issue in the Sprint, get details:
```
jira issue get --key <ISSUE_KEY>
```

Apply AC completeness rules only to Story issues. For non-Story issues, record them as out of scope for AC completeness instead of marking AC as missing.

Check the following (AC completeness rules):

1. **AC Structure** — Does the description contain structured acceptance criteria (Given/When/Then, condition+result, or numbered list)?
2. **AC Testability** — Does each AC include quantifiable/verifiable standards? ("loads" is NOT acceptable; "loads within 2 seconds" is acceptable)
3. **AC Presence** — If the description contains no AC-related keywords ("验收标准", "AC", "Acceptance Criteria"), mark as "AC missing"
4. **Story Points** — Are they estimated? If not filled, mark as missing. Do NOT infer.
5. **Dependencies** — Are there dependency annotations?

### Step 3: Check Linked Design Documents

If no `docs` provider is installed, skip this step. Record design-document checks as skipped and continue with Step 4.

For each Story, search the selected docs provider for linked documents using the exact issue key phrase so unrelated records that merely contain the numeric suffix do not count as a design-document match.

If `DOCS_SPACE` is available for this run, search that space first:
```
confluence search content --cql "space = '{{DOCS_SPACE}}' AND text ~ '\"<ISSUE_KEY>\"'" --type page --limit 5
```

Obsidian provider example:
```
obsidian content search --query "<ISSUE_KEY>"
```

If `DOCS_SPACE` is not available, fall back to:
```
confluence search content --cql "text ~ '\"<ISSUE_KEY>\"'" --type page --limit 5
```

If no results, mark the Story as "missing design document".

### Step 4: Get Team Historical Velocity

Search recently completed Sprints for total Story Points:
```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND issuetype = Story AND statusCategory = Done AND sprint in closedSprints() ORDER BY resolved DESC" --max-results 100
```

Group by Sprint, calculate completed Points per Sprint, take the average as rolling Velocity baseline.

### Step 5: Historical Comparison (Estimate vs Actual Cycle Time)

For each Story, search for similar completed Stories:

**If `SIMILAR_LABEL` was not provided by the user, skip this entire step.** Note in the report: "No SIMILAR_LABEL specified, historical estimate comparison skipped."

```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND issuetype = Story AND statusCategory = Done AND labels = {{SIMILAR_LABEL}} ORDER BY resolved DESC" --max-results 10
```

**If 0 results:** skip estimate comparison. Note in the report: "No historical similar Stories (label={{SIMILAR_LABEL}}), cannot compare estimates. Suggest first-time manual calibration."

For each historical Story, get details (extract `created`, `resolutiondate`, `story points`):
```
jira issue get --key <HISTORY_ISSUE_KEY>
```

Estimated Cycle Time (Lead Time) = resolutiondate - created.

**Apply data quality filters** (see `../using-orbit/references/output-conventions.md`): exclude stories where Cycle Time <= 0 or > 60 days. Report: "Valid samples: X / Total: Y".

Build an "Estimate vs Actual" comparison table:

| Historical Story | Points | Estimated Cycle Time (days) | Days/Point |
|---|---|---|---|
| PROJ-201 State machine optimization | 5 | 7 | 1.4 |
| PROJ-187 State machine refactor | 3 | 8 | 2.7 |

Evaluate current Story estimates:
- Calculate average days/point from historical data (valid samples only)
- Current estimate × average days/point = predicted duration
- If estimate deviation > 50% vs historical average → flag as risk (see `../using-orbit/references/output-conventions.md`)

### Step 6: Generate Readiness Report

Compile analysis into a report using these status markers (see `../using-orbit/references/output-conventions.md`):

- ✅ **Ready** — AC complete, design doc present, estimate reasonable
- ⚠️ **AC Incomplete** — list missing items + generate AC draft suggestions
- ❌ **Missing Design Doc** — list Stories with no linked docs record when a `docs` provider is installed
- 📊 **Risk Alert** — estimate deviation > 50%, Sprint capacity vs team Velocity comparison

If no `docs` provider is installed, generate the readiness result inline and mark design-document checks plus docs writeback as skipped.

### Step 7: Write AC Drafts to Jira (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display AC draft suggestions first, then after confirmation:

```
jira issue update --key <ISSUE_KEY> --description "<updated description with AC draft>"
```

### Step 8: Assign Unassigned Stories (optional, requires user confirmation)

If unassigned Stories were detected in Step 6, offer to assign them:

```
jira issue assign --key <ISSUE_KEY> --user <USER>
```

Ask the user for each Story's assignee. Skip if user declines.

### Step 9: Write Readiness Report to Docs Provider (optional, requires user confirmation)

Run this step only when a `docs` provider is installed and the user wants docs writeback. Otherwise the inline result from Step 6 is the final report.

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

**Follow `../using-orbit/references/safety-rules.md` docs writeback deduplication protocol.** Before creating, search for existing report on the selected docs provider:
```
confluence search content --cql "title ~ 'Sprint {{SPRINT_ID}}' AND title ~ '就绪度报告' AND space = '{{DOCS_SPACE}}'" --type page --limit 5
```

If a matching docs record is found, follow the docs writeback deduplication protocol in `../using-orbit/references/safety-rules.md` — fetch the existing record version when the provider supports it and ask the user whether to **update** the existing record or **create** a new one.

Display report content first, then after confirmation:

To create:
```
confluence page create --space {{DOCS_SPACE}} --title "Sprint {{SPRINT_ID}} 就绪度报告" --parent-id {{DOCS_PARENT_REF}} --body "<report HTML content>"
```

To update an existing page:
```
confluence page update --id <EXISTING_PAGE_ID> --title "Sprint {{SPRINT_ID}} 就绪度报告" --body "<report HTML content>" --version <current_version + 1>
```

## Output

- Sprint readiness report (Ready / AC Incomplete / Missing Doc / Risk Alert), returned inline when no `docs` provider is installed
- AC draft suggestions for incomplete Stories
- Estimate deviation warnings (vs historical similar Stories)
- Capacity overload alert (Sprint Points vs team Velocity)
