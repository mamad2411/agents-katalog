---
name: knowledge-capture
description: Use when turning recent production bugs into postmortem records or detecting hotspot files, including trigger-only validations that should skip shell, `list_mcp_resources`, and other host-resource discovery so they collect only missing business inputs.
metadata:
  author: Orbit contributors
  version: "1.0.14"
---

# Knowledge Auto-Capture

Convert production bugs into structured postmortem records and/or detect code hotspot files to identify architecture decay risks, publishing pitfall records to a docs platform only when a `docs` provider is installed.

Trigger-only routing guard: if the prompt already asks for pitfall capture or hotspot detection, treat `knowledge-capture` as selected. Do not turn the turn into a host-platform audit, skill-installation audit, or host-entry troubleshooting. Do not probe local resource registries, editor state, or skill availability, and do not invoke `list_mcp_resources`, `list_mcp_resource_templates`, `list_apps`, `get_app_state`, `computer-use`, `browser`, or similar host discovery. If the user forbids shell, do not run shell commands even for local inspection. Ask only for the missing inputs required by the current phase.

For trigger-only validation, do not reread installed skill files or references through shell just to confirm those inputs. Use this input table directly.

## Capability Dependencies

Required:
- `repo`
- `tracker`

Optional:
- `docs`

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `TRACKER_PROJECT` | Yes | Tracker project key for the active provider | `PROJ` |
| `REPO_PROVIDER` | Yes | Selected repo provider | `Bitbucket` |
| `REPO_NAMESPACE` | Yes | Repository namespace or project key | `sample` |
| `REPO_NAME` | Yes | Repository name or slug | `sample-repo` |
| `DOCS_SPACE` | Conditional | Docs space, container, or workspace identifier when Phase A docs writeback is used | `KB` |
| `DOCS_PARENT_REF` | Conditional | Parent page, folder, or document identifier for pitfall records when Phase A docs writeback is used | `54321` |
| `ISSUE_TYPE` | No | Jira issue type for production bugs (default: `Defect`) | `Bug` |

First determine the phase from the user's intent, then ask only for the missing inputs required for that phase in a single plain-text message. Present the parameter table above and wait for their response. Do NOT use interactive selection prompts — these are free-text values (IDs, keys, slugs) that the user types directly. Request `DOCS_SPACE` and `DOCS_PARENT_REF` only when a `docs` provider is installed and Phase A docs writeback will be used.

Trigger-only validation mode: if the user explicitly says this is only a skill trigger test, follow `../using-orbit/references/safety-rules.md` and ask only for the missing inputs required by the current phase. Do not ask for host platform, skill name, trigger entry, report language, or generic success criteria.

For Phase A wording such as "最近一次生产 Bug 沉淀成踩坑记录", treat the phase as already selected. Ask only for `TRACKER_PROJECT`, `REPO_PROVIDER`, `REPO_NAMESPACE`, and `REPO_NAME`, plus `ISSUE_TYPE` only when the default `Defect` does not apply. Do not inspect editor windows, local apps, or screenshots to decide missing inputs.

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
`repo` and `tracker` are required for both phases.
If no `docs` provider is installed, keep Phase B hotspot detection fully available and return Phase A pitfall records inline instead of writing to a docs platform.

This skill has two phases. Detect which phase to enter based on user intent:

- **Phase A** — pitfall records: "生成踩坑记录", "整理最近的生产 Bug", "create postmortem records"
- **Phase B** — hotspot detection: "检测热点文件", "代码健康度分析", "find code hotspots"

If the user says "知识沉淀" or "knowledge capture" without specifying, ask which phase they want.

## Phase A: Pitfall Records (踩坑记录)

### Step 1: Search Recent Production Bugs

```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND type = {{ISSUE_TYPE}} AND labels = production AND statusCategory = Done AND resolved >= -14d ORDER BY resolved DESC" --max-results 20
```

**If 0 results, STOP.** Output: "No resolved production {{ISSUE_TYPE}} found in the last 14 days for project {{TRACKER_PROJECT}}. Verify the project key, issue type, or label filter." Do not execute subsequent steps.

For each Bug, check description quality:
- If description < 50 characters, or missing key elements ("步骤", "现象", "错误", "异常"): mark as "insufficient description". Generate a template with placeholders instead of forcing content. Prompt: "Please supplement the following before re-running: 1) Reproduction steps 2) Complete error log"
- Bugs with adequate descriptions continue to Step 2

### Step 2: Get Fix Code for Each Bug

Resolve linked commits using the shared provider linking strategy.

Bitbucket provider-native example:
```
bitbucket jira issue-commits --issue-key <BUG_KEY>
```

If the selected repo provider does not expose a native issue-to-commit link path, treat linked commit discovery as degraded for this phase and generate the pitfall record from Jira Bug description and comments only. Add note at end: "No linked fix code found — recommend supplementing with code-level root cause analysis."

Bitbucket example:
```
bitbucket commit pull-requests --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --id <COMMIT_ID>
```

GitHub example:
```
github commit pull-requests --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --sha <COMMIT_SHA>
```

GitLab example:
```
gitlab commit pull-requests --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --sha <COMMIT_SHA>
```

⚠️ If no linked commits can be resolved for the selected provider, skip PR diff retrieval for this Bug and continue with degraded context.

Bitbucket example for reading the fix diff:
```
bitbucket pr diff --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --id <PR_ID>
```

GitHub example for reading the fix diff:
```
github pr diff --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number <PR_ID>
```

### Step 3: Generate Pitfall Records

For each production Bug, combine Bug description + fix code to generate a structured record:

```
**Pitfall Record #<BUG_KEY>**
- **Symptom**: User-perceivable problem description
- **Root Cause**: Code-level root cause
- **Fix**: Fix approach and key code
- **Prevention**: How to avoid similar issues (coding standards / automated detection rules)
- **Affected Modules**: List of affected modules
- **Related**: Links to related historical pitfall records
```

### Step 4: Write Pitfall Records to Docs Provider (optional, requires user confirmation)

Run this step only when a `docs` provider is installed and the user wants Phase A docs writeback. Otherwise the generated pitfall records from Step 3 are the final Phase A output.

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

For each Bug, check for existing pitfall records first:
```
confluence search content --cql "title ~ '<BUG_KEY>' AND space = '{{DOCS_SPACE}}' AND label = 'pitfall'" --type page --limit 3
```

Obsidian provider example:
```
obsidian content search --query "<BUG_KEY> pitfall"
```

If a matching docs record is found, follow the docs writeback deduplication protocol in `../using-orbit/references/safety-rules.md` — fetch the existing record version when the provider supports it and ask the user whether to **update** the existing record or **create** a new one.

Display generated records first, then after confirmation. Use Jira Bug key as the record number (e.g., PROJ-298 → Pitfall #PROJ-298):

To create:
```
confluence page create --space {{DOCS_SPACE}} --parent-id {{DOCS_PARENT_REF}} --title "踩坑 #<BUG_KEY>: <short description>" --body "<pitfall record content>"
```

Obsidian provider example:
```
obsidian content create --space {{DOCS_SPACE}} --parent-ref {{DOCS_PARENT_REF}} --title "踩坑 #<BUG_KEY>: <short description>" --body "<pitfall record content>"
```

To update an existing page:
```
confluence page update --id <EXISTING_PAGE_ID> --title "踩坑 #<BUG_KEY>: <short description>" --body "<pitfall record content>" --version <current_version + 1>
```

Add labels to each page:
```
confluence page labels add --id <NEW_PAGE_ID> --name "pitfall"
confluence page labels add --id <NEW_PAGE_ID> --name "production-bug"
confluence page labels add --id <NEW_PAGE_ID> --name "<module-name>"
```

## Phase B: Hotspot Detection (热点文件检测)

### Step 1: Get Recent Commit History

Bitbucket example:
```
bitbucket commit list --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}}
```

GitHub example:
```
github commit list --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}}
```

GitLab example:
```
gitlab commit list --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}}
```

⚠️ Only analyze the most recent 50 commits. This is a hard cap to avoid API call volume causing timeout (known limitation). Inform the user before starting: "Hotspot detection will analyze up to 50 recent commits with per-commit change queries. This typically takes 5-15 minutes depending on repository size. For very large repositories, consider narrowing the analysis window if the process is interrupted."

### Step 2: Analyze Changed Files Per Commit

For each commit:

Bitbucket example:
```
bitbucket commit changes --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --id <COMMIT_ID>
```

GitHub example:
```
github commit changes --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --sha <COMMIT_SHA>
```

Track for each file: modification count and number of distinct developers involved.

### Step 3: Identify Hotspot Files

Apply the hotspot detection thresholds and classification rules defined in `../using-orbit/references/output-conventions.md` (Hotspot Detection Thresholds section). Only files flagged as architecture decay warnings proceed to Step 5 for ticket creation; normal iteration hotspots are recorded in the report only.

### Step 4: Generate Report

For each hotspot file, provide:
1. Modification frequency and developer count
2. Possible architectural issues (too many responsibilities, God Class, etc.)
3. Split recommendations

### Step 5: Create Tech Debt Tickets (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` deduplication and write confirmation protocol.** Only for files flagged as architecture decay warnings.

For each file, check for existing tickets first:
```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND labels = tech-debt AND summary ~ '<filename>'" --max-results 5
```

If a match is found, show the existing ticket to the user instead of creating a duplicate. Only create if the user confirms no match exists.

Display hotspot analysis first, then after confirmation:
```
jira issue create --project {{TRACKER_PROJECT}} --type Task --summary "[TechDebt] Evaluate splitting <filename>" --description "<hotspot analysis + split recommendations>" --fields-json '{"labels":["tech-debt"]}'
```

## Output

- Phase A: Structured pitfall records returned inline when Phase A docs writeback is not used, or written to the selected docs provider when Phase A docs writeback is used
- Phase B: Hotspot file detection report + tech debt Jira tickets (when architecture decay warnings detected)
