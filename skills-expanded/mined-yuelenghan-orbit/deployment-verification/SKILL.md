---
name: deployment-verification
description: "Verify deployment outcomes by checking build status, PR merge state, quality gates, and optional smoke tests. Use for post-deploy verification, rollback decision support, or deployment health assessment. Trigger phrases: '验证部署', '部署验证', '检查部署状态', 'deploy check', 'verify deployment', 'smoke test', '回滚建议', '部署健康度'."
license: MIT
metadata:
  author: Orbit contributors
  version: "1.0.3"
---

# Deployment Verification

Verify deployment outcomes across CI builds, repo PR state, quality gates, and optional smoke tests. Provide structured pass/fail assessments with rollback decision support when verification fails.

## Capability Dependencies

- **Phase A (Verification):**
  - One `ci` provider skill such as `jenkins` or `github-workflow`
  - One `repo` provider skill such as `bitbucket`, `github`, or `gitlab`
- **Phase B (Report, optional):**
  - A `docs` provider skill such as `confluence` or `obsidian`

Optional quality-gate providers (Phase A):
- SonarQube Skill when `sonarqube` quality gate should be checked
- Fortify Skill when `fortify` scan status should be checked

## Inputs

### Phase A — Verification

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `CI_JOB` | Yes | CI provider job or workflow path for the deployment build (Jenkins job path, or GitHub workflow file/ref) | `folder-a/deploy-prod` |
| `BUILD_NUMBER` | No | Specific build/run number to verify; defaults to the latest completed build | `42` |
| `REPO_TARGETS` | Conditional | Comma-separated `<provider>:<namespace>/<repo>` targets for multi-repo verification, required when PR or commit verification is needed | `bitbucket:sample-org/sample-service` |
| `PR_NUMBER` | No | Specific PR/MR number to verify merge state | `16` |
| `COMPARE_FROM` | No | Git ref for the previous deployed version (used with `COMPARE_TO` to diff changes) | `v1.1.0` |
| `COMPARE_TO` | No | Git ref for the current deployed version | `v1.2.0` |
| `SMOKE_TEST_URLS` | No | Comma-separated URLs for HTTP health checks (status 200 = pass) | `https://app.example.com/health,https://api.example.com/status` |
| `SMOKE_TEST_JOB` | No | Optional CI provider smoke test job/workflow path | `folder-a/smoke-test` |
| `QUALITY_GATE_PROVIDERS` | No | `none`, `sonarqube`, `fortify`, or `auto`; when omitted or `auto`, check installed+configured providers (default: `auto`) | `auto` |
| `SUBAGENT_MODE` | No | Follows the shared definition in `parallel-dispatch.md` (default: `auto`) | `auto` |
| `MAX_CONCURRENT_REPOS` | No | Follows the shared `MAX_CONCURRENT_<UNIT>` convention in `parallel-dispatch.md`; unit = Repos (default: `3`) | `3` |

### Phase B — Report

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DOCS_SPACE` | Conditional | Selected docs space/container (Confluence space key, or Obsidian top-level folder); only when publishing | `PROJ` |
| `DOCS_PARENT_REF` | Conditional | Parent page or folder identifier for verification reports; only when publishing | `1531709516` |

Follow the shared missing-input stop rule in `../using-orbit/references/safety-rules.md`.

Scenario-specific input rule:
- Phase A can start with `CI_JOB` alone (build verification is the minimum scope)
- ask for `REPO_TARGETS` only when PR or commit verification is needed
- ask for `SMOKE_TEST_URLS` only when the user explicitly wants HTTP health checks
- when the request is verification-only, do not ask for `DOCS_SPACE` or `DOCS_PARENT_REF`
- Phase B asks only for the still-missing publication fields

## Missing-input collection rules

- Ask for missing inputs in one plain-text message, requesting only the smallest still-missing set for the current phase.
- Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract (`REPO_TARGETS`, `PR_NUMBER`, `DOCS_SPACE`, `DOCS_PARENT_REF`).
- `CI_JOB` / `SMOKE_TEST_JOB` are provider-native route inputs (Jenkins job path or GitHub workflow file) and stay scoped to the selected `ci` provider.

## Critical Prompt-Shape Override

When the user asks for deployment verification and already provides `CI_JOB`, treat it as sufficient to start Phase A. Make the first live stop boundary the ci/repo preflight — if config is missing, return only the exact missing values and stop. Defer all docs questions until the user enters Phase B.

If the user provides a `BUILD_NUMBER` or `PR_NUMBER`, carry those directly into the verification flow — do not ask for them again.

## Before You Start

Before resolving the first stop boundary, read only the Missing-Input Stop Rule section of `../using-orbit/references/safety-rules.md`.

### Preflight Configuration Check

This skill has two phases with different capability requirements:

- **Phase A** (verification): follow the preflight protocol in `../using-orbit/references/safety-rules.md` for the selected **ci** and **repo** providers.
- **Phase B** (report): follow the same protocol for the selected **docs** provider in addition to the already-resolved Phase A context.

Optional quality-gate providers in Phase A: check **SonarQube** and/or **Fortify** config only when `QUALITY_GATE_PROVIDERS` resolves to include them.

### After boundary resolved

Read `../using-orbit/references/safety-rules.md`, `../using-orbit/references/cli-patterns.md`, and `../using-orbit/references/output-conventions.md`.
Read `../using-orbit/references/parallel-dispatch.md` before dispatching per-repo workers.
Use those shared references for common execution policy. This skill file remains responsible for the scenario-specific two-phase verification/report flow and rollback decision logic.

## Phase A: Deployment Verification (部署验证)

### Step 1: Verify CI Build Status

Read the target build/run summary.

Jenkins example:
```
jenkins build get --job {{CI_JOB}} --number {{BUILD_NUMBER}}
```

GitHub Workflow example:
```
github-workflow build get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number {{BUILD_NUMBER}}
```

If `BUILD_NUMBER` was not provided, use the latest completed build:
```
jenkins build get --job {{CI_JOB}} --number lastCompletedBuild
```

Extract: build number, result (SUCCESS/FAILURE/UNSTABLE/ABORTED, or the GitHub Workflow conclusion), duration, timestamp, and any parameters (especially `BRANCH` and `VERSION`).

**Build result evaluation**:
- `SUCCESS` → proceed to next verification step
- `UNSTABLE` → warn the user: "Build #{{BUILD_NUMBER}} is UNSTABLE. Some tests may be failing. Proceed with caution."
- `FAILURE` → **STOP.** The deployment likely failed. Output failure details and proceed to rollback assessment.
- `ABORTED` → **STOP.** The build was manually aborted. Output: "Build #{{BUILD_NUMBER}} was ABORTED. Verify whether this was intentional before proceeding."

If the build failed, read the console/log for failure details:
```
jenkins build console --job {{CI_JOB}} --number {{BUILD_NUMBER}} --tail 100
github-workflow build console --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number {{BUILD_NUMBER}}
```

### Step 2: Verify Repo PR Merge State (conditional)

Only execute this step when `PR_NUMBER` is provided or when `REPO_TARGETS` is available.

**Single PR verification** (when `PR_NUMBER` is provided):

Bitbucket example:
```
bitbucket pr get --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --id {{PR_NUMBER}}
```

GitHub example:
```
github pr get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number {{PR_NUMBER}}
```

GitLab example:
```
gitlab pr get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number {{PR_NUMBER}}
```

Verify the PR is merged. Bitbucket/GitLab expose an explicit `MERGED` state; GitHub has no `MERGED` state — instead confirm `state == closed` and `merged_at` is non-null. If not merged:
- `OPEN` (or `open`) → warn: "PR #{{PR_NUMBER}} is still OPEN. The change has not been merged yet."
- `DECLINED` / `closed` without `merged_at` → warn: "PR #{{PR_NUMBER}} was not merged. The change was not accepted."

**Multi-repo verification** (when `REPO_TARGETS` is provided without specific `PR_NUMBER`):

For each target in `REPO_TARGETS`, list recently merged PRs targeting the release branch:

Bitbucket example:
```
bitbucket pr list --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --state MERGED --target {{RELEASE_BRANCH}} --after {{DEPLOY_DATE}}
```

GitHub example (filter `closed` by `merged_at` since GitHub has no `MERGED` list state):
```
github pr list --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --state closed
```

GitLab example:
```
gitlab pr list --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --state merged
```

Derive `RELEASE_BRANCH` and `DEPLOY_DATE` from the build parameters in Step 1 when available (e.g., `BRANCH` parameter for the branch name, `timestamp` for the date). If the build parameters do not include a branch name, fall back to listing all recently merged PRs without a target filter and filter by date only.

Each repo's PR check is independent. Follow the shared dispatch rules in `../using-orbit/references/parallel-dispatch.md`.

- **Work unit**: One repo → list and verify merged PRs.
- **Batch size**: `MAX_CONCURRENT_REPOS` (default 3).

### Step 3: Verify Deployed Commit Range (conditional)

Only execute when both `COMPARE_FROM` and `COMPARE_TO` are provided, or when they can be derived from the build parameters and previous build.

Compare the change range between the previous and current deployment.

Bitbucket example:
```
bitbucket compare commits --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --from {{COMPARE_FROM}} --to {{COMPARE_TO}}
bitbucket compare diff-stats-summary --project {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --from {{COMPARE_FROM}} --to {{COMPARE_TO}}
```

GitHub example:
```
github commit changes --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --sha {{COMPARE_TO}}
```

GitLab example:
```
gitlab commit changes --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --sha {{COMPARE_TO}}
```

Extract: commit count, files changed, insertions, deletions. This provides the exact change footprint of the deployment.

### Step 4: Quality Gate Check (conditional)

Follow the **Quality Gate Provider Selection** pattern in `../using-orbit/references/cli-patterns.md` to resolve `QUALITY_GATE_PROVIDERS`, run the SonarQube and/or Fortify checks per repo, and aggregate per-repo results. For SonarQube, set `{{BRANCH}}` to the deployed branch derived from the build parameters in Step 1.

### Step 5: Smoke Test (conditional)

Only execute when `SMOKE_TEST_URLS` or `SMOKE_TEST_JOB` is provided.

**HTTP health checks** (when `SMOKE_TEST_URLS` is provided):

For each URL, perform an HTTP GET and check for status 200:
```bash
curl -sS -o /dev/null -w "%{http_code}" --max-time 10 <URL>
```

If any URL returns a non-200 status or times out, mark the smoke test as FAILED for that endpoint.

**CI smoke test job** (when `SMOKE_TEST_JOB` is provided):

Check the latest smoke test build result:
```
jenkins build get --job {{SMOKE_TEST_JOB}} --number lastCompletedBuild
github-workflow build get --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --number <LATEST_RUN>
```

If the latest smoke test build is FAILURE, mark the smoke test as FAILED.

### Step 6: Rollback Assessment (when verification fails)

If any verification step FAILED, provide a structured rollback assessment:

1. **Identify the last known good build**: Query the last successful build:
   ```
   jenkins build get --job {{CI_JOB}} --number lastSuccessfulBuild
   ```

2. **Compare parameters**: Show the difference between the failed build and the last successful build (branch, version, parameters).

3. **Rollback recommendation**:
   - If the failure is in the build itself → recommend re-running the build after fixing the issue
   - If the failure is in smoke test → recommend rollback to the last successful build and investigate
   - If the failure is in quality gate → recommend running `gate-remediation` skill to fix findings before redeploying

4. **Rollback action** (requires user confirmation): If the user agrees to rollback, trigger the deployment job with the previous version parameters.

   Jenkins example:
   ```
   jenkins job build-with-params --job {{CI_JOB}} --params-json '{"BRANCH":"<PREVIOUS_BRANCH>","VERSION":"<PREVIOUS_VERSION>"}'
   ```

   GitHub Workflow example:
   ```
   github-workflow job build --namespace {{REPO_NAMESPACE}} --repo {{REPO_NAME}} --workflow {{CI_JOB}} --ref <PREVIOUS_BRANCH>
   ```

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol** before triggering any rollback build.

### Phase A Output

```
## Deployment Verification — {{CI_JOB}} #{{BUILD_NUMBER}}

### Build Status
| Item | Value |
|------|-------|
| Job | {{CI_JOB}} |
| Build # | {{BUILD_NUMBER}} |
| Result | SUCCESS / FAILURE / UNSTABLE |
| Duration | 3m 12s |
| Branch | release/1.2.0 |
| Version | 1.2.0 |

### PR Merge State
| Repo | PR | Title | State | Merged At |
|------|----|-------|-------|-----------|
| sample-service | #42 | Auth refresh flow | MERGED | 2026-06-12 |
| sample-web | #45 | Export to PDF | MERGED | 2026-06-12 |

### Change Range (v1.1.0 → v1.2.0)
- Commits: 12
- Files changed: 23
- Insertions: +847
- Deletions: -156

### Quality Gate
| Repo | SonarQube | Fortify | Overall |
|------|-----------|---------|---------|
| sample-service | PASSED | -- | PASSED |

### Smoke Test
| Target | Result |
|--------|--------|
| https://app.example.com/health | ✓ 200 OK |
| https://api.example.com/status | ✓ 200 OK |

### Overall Verification: PASSED / FAILED
```

If FAILED, include the rollback assessment section:
```
### Rollback Assessment
- Last successful build: #41 (v1.1.0)
- Recommendation: rollback to v1.1.0 and investigate smoke test failures
- Rollback command (pending confirmation): jenkins job build-with-params --job {{CI_JOB}} --params-json '{"BRANCH":"release/1.1.0","VERSION":"1.1.0"}'
```

## Phase B: Publish Verification Report (requires user confirmation)

### Step 1: Confirm publish intent

Only enter Phase B when the user explicitly asks to publish the verification report to the docs provider.

If `DOCS_SPACE` or `DOCS_PARENT_REF` is still missing, ask for them here and stop until the user provides them.

Follow the preflight protocol in `../using-orbit/references/safety-rules.md` for the selected **docs** provider before continuing.

### Step 2: Search existing report page

**Follow `../using-orbit/references/safety-rules.md` docs deduplication protocol.** Before creating, search for an existing report.

Confluence example:
```
confluence search content --cql "title ~ 'Deploy Verification {{BUILD_NUMBER}}' AND space = '{{DOCS_SPACE}}'" --type page --limit 5
```

Obsidian example:
```
obsidian content search --query "Deploy Verification {{BUILD_NUMBER}}"
```

If a matching page/note is found, follow the shared docs deduplication protocol — fetch the existing page version and ask the user whether to **update** or **create** a new one.

### Step 3: Preview and publish report

**Follow `../using-orbit/references/safety-rules.md` write confirmation protocol.**

Display the full report content first, then after confirmation:

Confluence create example:
```
confluence page create --space {{DOCS_SPACE}} --title "Deploy Verification {{CI_JOB}} #{{BUILD_NUMBER}}" --parent-id {{DOCS_PARENT_REF}} --body "{{REPORT_HTML}}"
```

Confluence update example:
```
confluence page update --id <EXISTING_PAGE_ID> --title "Deploy Verification {{CI_JOB}} #{{BUILD_NUMBER}}" --body "{{REPORT_HTML}}" --version <NEXT_VERSION>
```

Obsidian create example:
```
obsidian content create --space {{DOCS_SPACE}} --title "Deploy Verification {{CI_JOB}} #{{BUILD_NUMBER}}" --body "{{REPORT_MARKDOWN}}" --parent-ref {{DOCS_PARENT_REF}}
```

## Local Persistence

Local state is stored under `~/.config/deployment-verification/`:
```
~/.config/deployment-verification/
  runs/
    <job-path-slug>-<build-number>.json
```

Run state shape:
```json
{
  "ciJob": "folder-a/deploy-prod",
  "buildNumber": 42,
  "buildResult": "SUCCESS",
  "verificationResult": "PASSED",
  "prChecks": {},
  "qualityGate": {},
  "smokeTest": {},
  "rollbackAssessment": null,
  "reportPageId": null
}
```

Internal local-state persistence under `~/.config/deployment-verification/` is allowed without extra confirmation.

## Allowed Automatic Writes

- Local state persistence under `~/.config/deployment-verification/`
- HTTP health check requests (read-only GET, no side effects)

## Forbidden Automatic Writes

- CI build trigger without confirmation (including rollback builds)
- repo `pr merge` / `pr decline`
- docs page create / update without confirmation and dedup check
- Any SonarQube or Fortify gate/profile changes
