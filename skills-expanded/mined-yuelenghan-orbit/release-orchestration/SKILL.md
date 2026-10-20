---
name: release-orchestration
description: "Orchestrate release preparation, execution, and reporting across tracker, repo, ci, and docs providers. Use for release readiness assessment, release branch creation, tagging, build triggering, tracker version management, or publishing release notes. Trigger phrases: '准备发布', '创建 release 分支', '发版', 'release 1.2', '发布准备', '发布执行', '发布报告', '打 tag', '触发 release build', '生成 changelog', '发布说明'."
license: MIT
metadata:
  author: Orbit contributors
  version: "1.0.3"
---

# Release Orchestration

Orchestrate the full release lifecycle — from collecting issues and generating a changelog, through cutting release branches, tagging, triggering CI builds, transitioning tracker issues, to publishing release notes on the docs provider. Each phase can run independently or as a continuous pipeline.

## Capability Dependencies

- **Phase A (Release Preparation):**
  - One `tracker` provider skill such as `jira` or `github-issue`
  - One `repo` provider skill such as `bitbucket`, `github`, or `gitlab`
- **Phase B (Release Execution):**
  - One `tracker` provider skill (configured)
  - One `repo` provider skill (configured)
  - One `ci` provider skill such as `jenkins` or `github-workflow`
- **Phase C (Release Report):**
  - One `tracker` provider skill (configured)
  - A `docs` provider skill such as `confluence` or `obsidian`

Optional quality-gate providers (Phase A only):
- SonarQube Skill when `sonarqube` quality gate should be checked
- Fortify Skill when `fortify` gate status should be checked

## Inputs

### Phase A — Release Preparation

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `VERSION_NAME` | Yes | Target release version name (tracker version + Git tag) | `1.2.0` |
| `TRACKER_PROJECT` | Yes | Selected tracker project/container key (Jira project key, or GitHub Issue `owner/repo`) | `PROJ` |
| `REPO_TARGETS` | Conditional | Comma-separated `<provider>:<namespace>/<repo>` targets for multi-repo releases; derived from tracker evidence when possible | `bitbucket:sample-org/sample-service,bitbucket:sample-org/sample-web` |
| `FIX_VERSION_JQL` | No | Override JQL to select issues (Jira only); default uses `fixVersion = <VERSION_NAME>` | `project = PROJ AND fixVersion = "1.2.0" AND status = Done` |
| `RELEASE_BRANCH_PREFIX` | No | Prefix for release branches (default: `release`) | `release` |
| `QUALITY_GATE_PROVIDERS` | No | `none`, `sonarqube`, `fortify`, or `auto`; when omitted or `auto`, check installed+configured providers (default: `auto`) | `auto` |
| `SUBAGENT_MODE` | No | Follows the shared definition in `parallel-dispatch.md` (default: `auto`) | `auto` |
| `MAX_CONCURRENT_REPOS` | No | Follows the shared `MAX_CONCURRENT_<UNIT>` convention in `parallel-dispatch.md`; unit = Repos (default: `3`) | `3` |
| `CROSS_REVIEW_COUNT` | No | Number of independent cross-review subagents for changelog and readiness review (default: `5`) | `5` |
| `RE_REVIEW_SEVERITY` | No | Severity threshold for adversarial re-review of changelog and readiness findings: `high` (only blocking items), `medium` (default quality issues), `all` (every finding) (default: `medium`) | `medium` |

### Phase B — Release Execution

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `CI_JOB` | Conditional | CI provider job/workflow path for release build; required only when triggering a build | `folder-a/release-build` |
| `BUILD_PARAMS` | No | JSON parameters for the ci build trigger; default includes `BRANCH` and `VERSION` from current release context | `'{"BRANCH":"release/1.2.0","VERSION":"1.2.0"}'` |
| `SMOKE_TEST_JOB` | No | Optional CI provider job/workflow path for post-deploy smoke test | `folder-a/smoke-test` |

### Phase C — Release Report

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DOCS_SPACE` | Conditional | Selected docs space/container (Confluence space key, or Obsidian top-level folder); only when publishing | `PROJ` |
| `DOCS_PARENT_REF` | Conditional | Parent page or folder identifier for release notes; only when publishing | `1531709516` |

Follow the shared missing-input stop rule in `../using-orbit/references/safety-rules.md`.

Scenario-specific input rule:
- Phase A can start with `VERSION_NAME` and `TRACKER_PROJECT` alone
- ask for `REPO_TARGETS` only when conservative scope derivation fails and repo operations are needed
- when the request is preparation-only, do not ask for `CI_JOB`, `DOCS_SPACE`, or `DOCS_PARENT_REF`
- Phase B asks only for the still-missing execution fields
- Phase C asks only for the still-missing publication fields

## Missing-input collection rules

- Ask for missing inputs in one plain-text message, requesting only the smallest still-missing set for the current phase.
- Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract (`TRACKER_PROJECT`, `REPO_TARGETS`, `DOCS_SPACE`, `DOCS_PARENT_REF`).
- `VERSION_NAME`, `FIX_VERSION_JQL`, `RELEASE_BRANCH_PREFIX`, `BUILD_PARAMS`, `CROSS_REVIEW_COUNT`, and `RE_REVIEW_SEVERITY` are scenario-specific business inputs. `CI_JOB` / `SMOKE_TEST_JOB` are provider-native route inputs scoped to the selected `ci` provider.

## Critical Prompt-Shape Override

When the user asks for release preparation and already provides `VERSION_NAME` and `TRACKER_PROJECT`, treat it as sufficient to start Phase A. Make the first live stop boundary the tracker/repo preflight — if config is missing, return only the exact missing values and stop. Defer all ci and docs questions until the user enters Phase B or Phase C.

If the user says "发布" or "release" without specifying the workflow phase, detect the phase from intent:
- "准备发布", "发布准备", "创建 release 分支", "changelog" → Phase A
- "执行发布", "发布执行", "打 tag", "触发 build" → Phase B
- "发布报告", "发布说明", "release notes" → Phase C
- "发版" or "release X.Y.Z" without further qualification → ask which phase to start with

## Before You Start

Before resolving the first stop boundary, read only the Missing-Input Stop Rule section of `../using-orbit/references/safety-rules.md`.

### Preflight Configuration Check

This skill has three phases with different capability requirements:

- **Phase A** (preparation): follow the preflight protocol in `../using-orbit/references/safety-rules.md` for the selected **tracker, repo** providers.
- **Phase B** (execution): follow the same protocol for the selected **tracker, repo, ci** providers in addition to the already-resolved Phase A context.
- **Phase C** (report): follow the same protocol for the selected **tracker, docs** providers in addition to the already-resolved context.

Optional quality-gate providers in Phase A: check **SonarQube** and/or **Fortify** config only when `QUALITY_GATE_PROVIDERS` resolves to include them.

### After boundary resolved

Read `../using-orbit/references/safety-rules.md`, `../using-orbit/references/cli-patterns.md`, and `../using-orbit/references/output-conventions.md`.
Read `../using-orbit/references/parallel-dispatch.md` before dispatching per-repo workers.
Read `../using-orbit/references/cross-review.md` only when entering changelog cross-review / re-review stages.
Use those shared references for common execution policy. This skill file remains responsible for the scenario-specific three-phase release workflow, changelog generation, quality gate evaluation, and release report behavior.

## Phase A: Release Preparation (发布准备)

### Step 1: Verify Tracker Version Exists

Check whether the target version already exists in the tracker project.

Jira example:
```
jira meta project-versions --project {{TRACKER_PROJECT}}
```

If `VERSION_NAME` is not found in the returned list, offer to create it:
```
jira meta version-create --project {{TRACKER_PROJECT}} --name "{{VERSION_NAME}}"
```

**GitHub Issue degraded path:** GitHub Issues has no native "version" concept — milestones are the closest analog. If the selected tracker is `github-issue`, map `VERSION_NAME` to a milestone via `github-issue sprint get`/milestone creation instead of Jira-style version ops, and record this degraded mapping in the output. The changelog grouping below still applies.

**This is a write operation.** Follow `../using-orbit/references/safety-rules.md` write confirmation protocol before creating a new version/milestone.

If the user declines creation, STOP. Output: "Version {{VERSION_NAME}} does not exist in project {{TRACKER_PROJECT}} and creation was not confirmed. Create the version in the tracker first, then rerun."

If the version exists, capture `VERSION_ID` for later use.

### Step 2: Collect Issues by fixVersion

Get all issues assigned to the target version.

Jira example:
```
jira issue search --jql "project = {{TRACKER_PROJECT}} AND fixVersion = '{{VERSION_NAME}}' ORDER BY priority DESC" --max-results 100 --start-at 0
```

If `FIX_VERSION_JQL` was provided, use it instead of the default JQL.

GitHub Issue example (select issues by milestone):
```
github-issue sprint issues --namespace {{OWNER}} --repo {{REPO}} --id <MILESTONE_ID>
```

Repeat Jira pagination with `--start-at 100`, `200`, ... until the returned page size is smaller than `--max-results`. Do not treat the first page as the full dataset.

**If 0 results, STOP.** Output: "No issues found for version {{VERSION_NAME}} in project {{TRACKER_PROJECT}}. Verify the version name or assign issues to this version first."

Capture the full issue list. For each issue, extract: key, summary, type, status, priority, resolution, labels.

### Parallel Per-Issue Detail Fetching

Each issue's detail and linked-PR evidence is independent. Follow the shared dispatch rules in `../using-orbit/references/parallel-dispatch.md`.

- **Work unit**: One issue key → fetch detail via `jira issue get --key <ISSUE_KEY>`, find linked repo commits via the provider linking strategy (see Step 3).
- **Batch size**: `MAX_CONCURRENT_REPOS` (default 3).

Use the shared worker prompt structure from `parallel-dispatch.md`; supply the issue key and return only the per-issue detail and commit/PR evidence needed for changelog generation.

### Step 3: Find Linked Merged PRs in the Repo Provider

Tracker↔repo linkage is provider-specific; follow `../using-orbit/references/provider-linking-strategy.md` for the selected pair. Bitbucket provides a direct tracker↔commit command:

Bitbucket example:
```
bitbucket jira issue-commits --issue-key <ISSUE_KEY>
```

For each commit, find the containing PR:
```
bitbucket commit pull-requests --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --id <COMMIT_ID>
gitlab commit pull-requests --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --sha <COMMIT_SHA>
```

For repo providers without a native tracker-link command, derive linked commits from the tracker issue's remote links and a repo PR search, then correlate by commit SHA.

Filter to PRs that are merged. Collect PR metadata: id, title, repo, merged date, author.

If `REPO_TARGETS` was not explicitly provided, derive it conservatively from the collected PR evidence. If the derived repo set is unambiguous, set `REPO_TARGETS` accordingly and note the inference in the final output. If evidence narrows only to namespace-level boundaries and multiple plausible repositories remain, ask the user for the smallest explicit `REPO_TARGETS` subset.

### Step 4: Auto-Generate Structured Changelog

From the collected issues and PRs, generate a structured changelog grouped into categories:

**Changelog categories**:
- **Features** — issues of type `Story` or `New Feature` with status `Done`
- **Improvements** — issues of type `Task` or `Improvement` with status `Done`
- **Bug Fixes** — issues of type `Bug` or `Defect` with status `Done`
- **Breaking Changes** — issues labeled `breaking-change` or with `breaking` in the summary/description

For each entry, include:
- Issue key + summary
- Linked PR(s) with repo slug and PR id
- Component/module if available from the tracker

If an issue has no linked PR, include it in the changelog with a note: "No linked PR found."

If an issue is not in `Done` status, include it under an **Incomplete** section with its current status and a warning marker.

### Step 4b: Cross-Review Changelog Quality (交叉评审)

After the initial changelog is generated, dispatch cross-review subagents to independently validate changelog completeness and accuracy before any downstream writes.

Follow the cross-review dispatch, merge, and retention rules in `../using-orbit/references/cross-review.md`.

- **Work unit**: One review lens → independently evaluate the full changelog and the underlying tracker/repo evidence.
- **Batch size**: `CROSS_REVIEW_COUNT` (default 5). Dispatch all configured lenses in one batch.
- **Inline fallback**: Process lenses sequentially when dispatch unavailable.

**Cross-review lenses**:

| Lens | Focus | Key Question |
|------|-------|-------------|
| `completeness` | Issue coverage | Are there issues with the target fixVersion that the changelog missed, or issues included that should not be in this release? |
| `categorization` | Category accuracy | Are issues correctly classified as features/fixes/breaking, or are there misclassifications based on type and labels? |
| `pr-traceability` | PR linkage | Does every changelog entry have verified PR evidence? Are there PRs merged to the target branch that map to unlisted issues? |
| `breaking-change-signal` | Breaking change detection | Are there changes that could be breaking but are not flagged — API signature changes, config format changes, dependency removals? |
| `incomplete-risk` | Incomplete-item risk | Are incomplete issues in the changelist safe to defer, or do they block the release? |

Each cross-reviewer returns:
- Missing issues or PRs
- Categorization corrections
- Breaking-change warnings the initial pass missed
- Incomplete-item risk assessments

**Merge**: Apply cross-review merge rules. Findings agreed by ≥ 2 cross-reviewers are `CONFIRMED`. Single-reviewer findings are `UNIQUE` and must be re-reviewed before altering the final changelog. Direct contradictions are `CONFLICT` and surfaced to the user.

### Step 4c: Re-Review Changelog Findings (复审)

For each cross-review finding selected by `RE_REVIEW_SEVERITY`, plus all `UNIQUE` findings regardless of threshold, dispatch a re-review verifier subagent that attempts to **refute** the finding.

Follow the re-review dispatch, verdict, and retention rules in `../using-orbit/references/cross-review.md`.

- **Work unit**: One changelog finding → verify whether the criticism is supported by the tracker/repo evidence.
- **Batch size**: All selected findings dispatched concurrently.
- **Inline fallback**: Process each finding sequentially when dispatch unavailable.

Each verifier receives:
- The specific changelog entry and cited finding
- The underlying tracker issue content and linked PR/commit evidence
- The adversarial verification instructions from `cross-review.md`

Each verifier returns one of:
- `CONFIRMED` — the changelog finding is real and must affect the final changelog
- `REFUTED` — the finding is not supported and should be removed
- `ADJUSTED` — the finding is real but its scope or rationale needs correction

**After re-review**: Remove `REFUTED` findings. Apply `ADJUSTED` findings to the final changelog. Only the final changelog after re-review proceeds to Step 5.

### Step 5: Create Release Branch in Target Repos (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the planned release branches first, then after confirmation:

Each repo in `REPO_TARGETS` gets one release branch. Follow the shared dispatch rules in `../using-orbit/references/parallel-dispatch.md` for multi-repo parallel branch creation.

- **Work unit**: One repo → create release branch.
- **Batch size**: `MAX_CONCURRENT_REPOS` (default 3).

For each repo, determine the start point (default branch HEAD):

Bitbucket example:
```
bitbucket branch default-get --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}}
bitbucket branch create --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --name {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} --start-point {{DEFAULT_BRANCH}}
```

GitHub example:
```
github repo default-branch-get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}}
github branch create --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --name {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} --start-point {{DEFAULT_BRANCH}}
```

GitLab example:
```
gitlab repo default-branch-get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}}
gitlab branch create --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --name {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} --start-point {{DEFAULT_BRANCH}}
```

If the branch already exists, skip creation and note: "Release branch {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} already exists in {{REPO_NAME}}."

### Step 6: Quality Gate Check

Follow the **Quality Gate Provider Selection** pattern in `../using-orbit/references/cli-patterns.md` to resolve `QUALITY_GATE_PROVIDERS`, run the SonarQube and/or Fortify checks per repo, and aggregate per-repo results. For SonarQube, set `{{BRANCH}}` to `{{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}}`.

When `QUALITY_GATE_PROVIDERS=none`, output: "Quality gate check skipped (QUALITY_GATE_PROVIDERS=none)." When `auto` resolves to no installed providers, output: "No quality-gate providers installed or configured. Quality gate check skipped."

Aggregate results per repo:

| Repo | SonarQube Gate | Fortify Gate | Overall |
|------|---------------|-------------|---------|
| sample-service | PASSED | N/A | PASSED |
| sample-web | FAILED | PASSED | FAILED |

**If any repo has a FAILED quality gate, the release is BLOCKED.** Output: "Release {{VERSION_NAME}} is BLOCKED: quality gate FAILED for <repo list>. Resolve gate failures before proceeding to Phase B (Release Execution). Suggestion: run the gate-remediation skill to repair findings."

If all gates PASSED (or no providers checked), output readiness assessment.

### Phase A Output

```
## Release {{VERSION_NAME}} — Readiness Assessment

### Changelog (after cross-review)

**Features (3)**
- PROJ-101: User authentication refresh flow [PR #42 in sample-service]
- PROJ-103: Dashboard widget customization [PR #44 in sample-service]
- PROJ-105: Export to PDF [PR #45 in sample-web]

**Bug Fixes (2)**
- PROJ-102: Session timeout not respected [PR #43 in sample-service]
- PROJ-104: Pagination offset error [No linked PR]

**Breaking Changes (1)**
- PROJ-100: API v2 migration — removed /api/v1/users endpoint [PR #41 in sample-service]

**Incomplete (1)**
- ⚠ PROJ-106: Mobile responsive layout [Status: In Progress] — may block release

### Quality Gate
| Repo | SonarQube | Fortify | Overall |
|------|-----------|---------|---------|
| sample-service | PASSED | -- | PASSED |
| sample-web | PASSED | PASSED | PASSED |

### Release Branches
| Repo | Branch | Status |
|------|--------|--------|
| sample-service | release/1.2.0 | Created |
| sample-web | release/1.2.0 | Created |

### Cross-Review Quality
- Reviewers: 5 dispatched, 5 succeeded
- CONFIRMED findings: 3
- UNIQUE findings: 1
- CONFLICT items: 0
- After re-review: 2 CONFIRMED, 1 REFUTED, 1 ADJUSTED

### Readiness: PASSED
```

## Phase B: Release Execution (发布执行)

**Prerequisite**: Phase A must have completed successfully. The quality gate must be PASSED for all repos (or skipped with `QUALITY_GATE_PROVIDERS=none`). If Phase A has not been run in the current session, verify the release branch exists in each repo before proceeding and warn about the skipped quality gate. Do not block if the user explicitly confirms.

### Step 1: Tag Release in Repo Providers (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the planned tags first, then after confirmation:

Each repo in `REPO_TARGETS` gets one tag. Follow the shared dispatch rules for multi-repo parallel tag creation.

- **Work unit**: One repo → create tag.
- **Batch size**: `MAX_CONCURRENT_REPOS` (default 3).

For each repo, tag the release branch HEAD:

Bitbucket example:
```
bitbucket tag create --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --name v{{VERSION_NAME}} --start-point {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} --message "Release v{{VERSION_NAME}}"
```

GitHub example:
```
github tag create --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --name v{{VERSION_NAME}} --start-point {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} --message "Release v{{VERSION_NAME}}"
```

GitLab example:
```
gitlab tag create --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --name v{{VERSION_NAME}} --start-point {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}} --message "Release v{{VERSION_NAME}}"
```

If the tag already exists, skip creation and note: "Tag v{{VERSION_NAME}} already exists in {{REPO_NAME}}."

### Step 2: Trigger CI Release Build (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.** Triggering a CI build is a write operation.

If `CI_JOB` was not provided, ask for it now and stop until the user provides it.

Display the build parameters before triggering. Default parameters:
```json
{"BRANCH": "release/{{VERSION_NAME}}", "VERSION": "{{VERSION_NAME}}"}
```

Override with `BUILD_PARAMS` if provided. After confirmation:

Jenkins example:
```
jenkins job build-with-params --job {{CI_JOB}} --params-json '{"BRANCH":"release/{{VERSION_NAME}}","VERSION":"{{VERSION_NAME}}"}'
```

GitHub Workflow example:
```
github-workflow job build --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --workflow {{CI_JOB}} --ref {{RELEASE_BRANCH_PREFIX}}/{{VERSION_NAME}}
```

Capture the queue ID / run ID from the response.

If multiple repos require separate build jobs, trigger each in sequence. Ask the user to confirm each build trigger.

### Step 3: Follow Build Status Until Completion

Poll the build status.

Jenkins example:
```
jenkins queue get --id <QUEUE_ID>
```

Repeat until the response includes an `executable` build number, then switch to:
```
jenkins build get --job {{CI_JOB}} --number <BUILD_NUMBER>
```

GitHub Workflow example:
```
github-workflow build get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number <RUN_ID>
```

Poll until the build reaches a terminal state (`SUCCESS`, `FAILURE`, `UNSTABLE`, or `ABORTED`, or the GitHub Workflow conclusion).

If the build fails, read the console/log:
```
jenkins build console --job {{CI_JOB}} --number <BUILD_NUMBER> --tail 50
github-workflow build console --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number <RUN_ID>
```

**If the build result is FAILURE, STOP.** Output: "Release build #<BUILD_NUMBER> FAILED for job {{CI_JOB}}. Console output (last 50 lines): <output>. Do not proceed with tracker transitions. Investigate the build failure and rerun after fixing."

If the build result is UNSTABLE, warn the user: "Release build #<BUILD_NUMBER> is UNSTABLE. Proceed with caution. Some tests may be failing."

### Step 4: Deploy Verification

If the build succeeded:

1. Record the build result and number.
2. If `SMOKE_TEST_JOB` was provided, trigger it and follow its status using the same polling pattern as Step 3.
3. If the smoke test fails, STOP and report the failure.

Output: "Release build #<BUILD_NUMBER> SUCCESS. Smoke test: <PASSED / SKIPPED / FAILED>."

### Step 5: Transition Tracker Issues to Released Status (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the list of issues to transition and their target status before confirming.

For each issue in the changelog with status not yet `Released`:

First, check available transitions (Jira):
```
jira issue transition list --key <ISSUE_KEY>
```

Then apply the `Released` transition (or the closest equivalent in the project's workflow):
```
jira issue transition apply --key <ISSUE_KEY> --transition Released
```

**GitHub Issue degraded path:** GitHub Issues has no `Released` transition. If the selected tracker is `github-issue`, map "released" to closing issues in the milestone (`github-issue issue update --state closed`) and record the degraded mapping.

If the `Released` transition is not available for an issue, note it and skip: "Issue <ISSUE_KEY> does not have a 'Released' transition available. Current status: <STATUS>. Available transitions: <list>."

### Step 6: Update Tracker Version to Released (requires user confirmation)

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the version update before confirming:

**Known limitation**: `jira meta version-update` only supports `--name` and `--description` flags. It does not expose `released` or `releaseDate` parameters. To mark a version as released, guide the user to update it in the Jira UI:
1. Open the version page: `<JIRA_BASE_URL>/plugins/servlet/project-config/{{TRACKER_PROJECT}}/versions`
2. Set "Released" to Yes and set the release date.

If the CLI gains `--fields-json` support for `version-update` in the future, the command would be:
```
jira meta version-update --id {{VERSION_ID}} --fields-json '{"released":true,"releaseDate":"<TODAY>"}'
```

After the version is marked as released, confirm the update by re-reading the version:
```
jira meta version-get --id {{VERSION_ID}}
```

For the `github-issue` degraded path, close the milestone via the provider's milestone update and record it.

### Phase B Output

```
## Release {{VERSION_NAME}} — Execution Result

### Tags
| Repo | Tag | Status |
|------|-----|--------|
| sample-service | v1.2.0 | Created |
| sample-web | v1.2.0 | Created |

### Build
| Job | Build # | Result | Duration |
|-----|---------|--------|----------|
| folder-a/release-build | #42 | SUCCESS | 3m 12s |

### Deploy Verification
- Smoke test: PASSED

### Tracker Transitions
- PROJ-101: Done → Released ✓
- PROJ-102: Done → Released ✓
- PROJ-103: Done → Released ✓
- PROJ-106: In Progress → (skipped, not in Done status)

### Version Status
- Version {{VERSION_NAME}}: released = true, releaseDate = <today>
```

## Phase C: Release Report (发布报告)

**Prerequisite**: Phase A changelog must be available (either from the current session or re-collected). Phase B results (build number, build result) should be available if the release was executed.

If Phase C is run in a separate session from Phase A:
1. Read the persisted run state from `~/.config/release-orchestration/runs/<project-key>-<version-name>.json`. If the `phaseA.changelog` field is populated, use it directly.
2. If no persisted state exists, re-run Phase A Steps 1–4 to re-collect the issue list and regenerate the changelog. Skip Steps 5–6 (branch creation and quality gate) if the release branch already exists.
3. If Phase B was executed in a prior session, read `phaseB.buildResult` from the persisted state. If absent, note that build results are unavailable for the report.

### Step 1: Collect Release Summary

Assemble the release summary from available data:

- **Version**: `VERSION_NAME`
- **Release date**: current date (or Phase B execution date if available)
- **Issues**: full list from Phase A changelog, grouped by category
- **PRs**: merged PR list with repo, id, title, author
- **Build results**: CI build number(s) and result(s) from Phase B (if executed)
- **Quality gate**: gate status from Phase A (if checked)
- **Incomplete items**: issues not in Done status at the time of changelog generation

### Step 2: Generate Docs Release Notes Page (requires user confirmation)

Only enter this step when the user wants docs writeback. If `DOCS_SPACE` or `DOCS_PARENT_REF` is missing, ask for them at this point and stop until the user provides them.

Follow the preflight protocol in `../using-orbit/references/safety-rules.md` for the selected **docs** provider before continuing.

**Follow `../using-orbit/references/safety-rules.md` docs deduplication protocol.** Before creating, search for existing release notes.

Confluence example:
```
confluence search content --cql "title ~ 'Release {{VERSION_NAME}}' AND space = '{{DOCS_SPACE}}'" --type page --limit 5
```

Obsidian example:
```
obsidian content search --query "Release {{VERSION_NAME}}"
```

If a matching page/note is found, follow the shared docs deduplication and `TARGET_PAGE_ID` skeleton in `../using-orbit/references/safety-rules.md` — fetch the existing page version and ask the user whether to **update** the existing page or **create** a new one.

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the full release notes content first, then after confirmation:

Confluence create example:
```
confluence page create --space {{DOCS_SPACE}} --title "Release {{VERSION_NAME}}" --parent-id {{DOCS_PARENT_REF}} --body "{{RELEASE_NOTES_HTML}}"
```

Confluence update example:
```
confluence page update --id <EXISTING_PAGE_ID> --space {{DOCS_SPACE}} --title "Release {{VERSION_NAME}}" --body "{{RELEASE_NOTES_HTML}}" --version <NEXT_VERSION>
```

Obsidian create example:
```
obsidian content create --space {{DOCS_SPACE}} --title "Release {{VERSION_NAME}}" --body "{{RELEASE_NOTES_MARKDOWN}}" --parent-ref {{DOCS_PARENT_REF}}
```

Release notes content structure:
- Version and release date
- Summary (total issues, features, fixes, breaking changes)
- Features section with issue links
- Bug Fixes section with issue links
- Breaking Changes section with migration guidance
- Incomplete items (if any) with current status
- Build results and quality gate status
- Contributors (derived from PR authors)

### Step 3: Add Remote Links from Tracker Issues to Docs Page

For each issue in the release, add a remote link pointing to the docs release notes page.

Jira example:
```
jira issue remote-link add --key <ISSUE_KEY> --url "<DOCS_PAGE_URL>" --title "Release {{VERSION_NAME}} Notes"
```

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.** Display the planned remote links before confirming. Batch-apply after confirmation.

### Phase C Output

```
## Release {{VERSION_NAME}} — Report Published

### Docs Page
- Title: "Release {{VERSION_NAME}}"
- Space: {{DOCS_SPACE}}
- URL: <page_url>
- Action: created / updated

### Remote Links
- <X> tracker issues linked to release notes page
```

## Local Persistence

Local state is stored under `~/.config/release-orchestration/`:
```
~/.config/release-orchestration/
  config.json                              # routine defaults
  runs/
    <project-key>-<version-name>.json      # per-release run state
```

`config.json` stores user preference defaults:
```json
{
  "releaseBranchPrefix": "release",
  "qualityGateProviders": "auto",
  "subagentMode": "auto",
  "maxConcurrentRepos": 3,
  "crossReviewCount": 5,
  "reReviewSeverity": "medium"
}
```

`runs/<project-key>-<version-name>.json` tracks per-release progress:
```json
{
  "projectKey": "PROJ",
  "versionName": "1.2.0",
  "repoTargets": ["bitbucket:sample-org/sample-service"],
  "phase": "A",
  "phaseA": {
    "versionId": "12345",
    "issues": [],
    "prs": [],
    "changelog": {},
    "releaseBranches": {},
    "qualityGate": {},
    "readiness": "PASSED"
  },
  "phaseB": {
    "tags": {},
    "buildResult": null,
    "trackerTransitions": {}
  },
  "phaseC": {
    "docsPageId": null
  }
}
```

Phase transitions: `A` → `B` → `C`. Each phase writes its state on completion. The run can be resumed from any completed phase.

Internal local-state persistence under `~/.config/release-orchestration/` is allowed in all phases without extra confirmation (same pattern as `gate-remediation` and `change-implementation`).

## Allowed Automatic Writes

- Local state persistence under `~/.config/release-orchestration/` (all phases)
- Git worktree creation for release branch checkout (when needed for local verification)

## Forbidden Automatic Writes

- Merge to the default branch
- repo `pr merge` / `pr decline`
- CI job configuration changes
- SonarQube or Fortify gate/profile changes
- Tracker issue creation
- Tracker version create / update / delete without confirmation
- Tracker issue transition apply without confirmation
- Tracker issue remote-link add without confirmation
- repo branch create / tag create without confirmation
- CI build trigger without confirmation
- docs page create / update without confirmation and dedup check
