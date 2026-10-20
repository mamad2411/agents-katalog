---
name: gate-remediation
description: "Use when a scheduled or operator-initiated workflow should resolve `REPAIR_PROVIDERS` against the discovered installed provider set or an explicit provider selection, normalize selected-provider quality/security findings into issue clusters, expand conservatively across one or more local repositories inside the allowed target boundary, drive repo-scoped remediation to PRs, and wait for fresh provider evidence before reporting the cluster repaired."
metadata:
  author: Orbit contributors
  version: "0.2.1"
---

# Gate Remediation

Use this skill for scheduled or operator-initiated remediation whose repair scope is resolved from `REPAIR_PROVIDERS` against the current discovered installed provider set or an explicit provider selection. The workflow should normalize findings from the selected providers, cluster them into issue-level repair scope, expand conservatively across one or more repositories when the issue clearly requires it, drive each repository through repo-scoped worktrees and PRs, and wait for fresh selected-provider evidence before considering the issue repaired.

## Critical Interactive Prompt-Shape Override

When an interactive run omits `REPAIR_PROVIDERS` or uses `REPAIR_PROVIDERS=auto`, and multiple providers are installed for the current run:

- treat provider-choice collection as a standalone input-only stage that outranks repo inspection, historical-run recovery, and provider-specific preflight
- discover the installed-provider set silently first
- Do not use memories, prior reports, or old session transcripts to infer which providers are installed for the current run or what the provider-choice question should look like. Use only current live local discovery for this run.
- before the provider-choice question is asked and answered, skip any generic memory lookup or repo-history quick pass that the host would normally run for repo tasks; Do not read `MEMORY.md` or any other memory file for this stage
- before the provider-choice question is asked and answered, limit local reads to the current installed sibling-skill tree, the direct user inputs already present in the conversation, and only the minimal current workspace metadata needed to enumerate installed providers
- before the provider-choice question is asked and answered, Do not read `report/`, `~/.config/gate-remediation/reports/`, `~/.config/gate-remediation/runs/`, `~/.config/gate-remediation/clusters/`, prior `state.json` files, `~/.codex/memories/`, `~/.codex/sessions/`, archived sessions, rollout summaries, or target repository source trees
- before the provider-choice question is asked and answered, Do not resume an old run, Do not validate repositories, inspect Git state, read prior provider findings, or Do not call provider CLI or selected provider CLIs
- then make the very first user-visible assistant message the provider-choice question itself
- suppress any acknowledgement, progress update, commentary, or "I will inspect/check first" sentence that the base host environment would normally emit before exploring
- if local discovery requires reading installed skill files or other local metadata, do that discovery silently and ask the question immediately after discovery completes
- keep the concrete discovered provider labels plus `all` visible in that first question, but do not freeze the wording to any one canned sentence, fixed provider list, or fixed provider count
- After the user answers `all`, resolve `selectedProviders` internally to the full discovered installed-provider set for the current run and continue without asking the user to restate it as `REPAIR_PROVIDERS=...`
- this prompt-shape override takes precedence over generic host progress-update habits for this specific input-collection step

## Capability Dependencies

- One `repo` provider skill such as `bitbucket`, `github`, or `gitlab` for remediation branches, PR reuse, and review-policy enhancements
- SonarQube Skill when `sonarqube` is in the selected repair scope
- Fortify Skill when `fortify` is in the selected repair scope
- One `ci` provider such as `jenkins` or `github-workflow` when remote verification or selected-provider post-merge follow-up is required

`repo-understanding` is a source-first local helper used during diagnosis and patching. Do not treat it as a sibling packaged CLI that requires `config get` preflight.

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `MODE` | Yes | One of `shadow` or `repair` | `repair` |
| `REPAIR_PROVIDERS` | No | One of `auto`, one installed provider name, or a comma-separated explicit provider list; when omitted, resolve it with the same installed-provider rules as `auto`. Interactive runs ask when multiple providers are installed, and automation runs select the installed-plus-configured subset | `auto` |
| `REPO_PATHS` | Conditional | Comma-separated absolute local repository paths; highest-priority targeting input | `/path/to/workspace/sample-org/sample-portal,/path/to/workspace/sample-org/sample-admin-web` |
| `REPO_NAMES` | Conditional | Comma-separated repository names resolved only under `ROOT_DIR` | `sample-portal,sample-admin-web` |
| `ROOT_DIR` | Conditional | Discovery root for `REPO_NAMES` or full-inventory mode; optional containment check for `REPO_PATHS` | `/path/to/workspace/sample-org` |
| `DEFAULT_BRANCH_CANDIDATES` | No | Override `config.json` default branch candidates | `master,main,develop` |
| `MAX_CONCURRENT_REPOS` | No | Override `config.json` concurrency limit | `2` |
| `MAX_ITERATIONS_PER_REPO` | No | Override `config.json` per-repository iteration cap | `3` |
| `MAX_RUNTIME_PER_REPO_MIN` | No | Override `config.json` per-repository runtime cap | `120` |
| `SUBAGENT_MODE` | No | One of `off` or `auto`; controls repair-worker dispatch for eligible repo work items | `auto` |

Normally provide:

- one repository-targeting route
- and optionally one provider-selection route

Repository-targeting routes:

- `REPO_PATHS`
- `REPO_NAMES` plus `ROOT_DIR`
- `ROOT_DIR`

Provider-selection routes:

- omit `REPAIR_PROVIDERS` and resolve it with the same rules as `auto`
- `REPAIR_PROVIDERS=auto`
- `REPAIR_PROVIDERS=<installed-provider-name>`
- `REPAIR_PROVIDERS=<provider-a>,<provider-b>,...`

`REPO_PATHS` may also be paired with `ROOT_DIR` when `ROOT_DIR` should act as the dependent-repository expansion boundary instead of only an exact-set containment check.

If multiple targeting inputs are present, resolve them in this order: `REPO_PATHS`, then `REPO_NAMES + ROOT_DIR`, then `ROOT_DIR`. Validate lower-priority scope constraints against the winning input and stop on conflicts.

## Missing-input collection rules

Ask for any missing required inputs in one plain-text message.
Prefer the smallest missing set that unblocks the current targeting route and provider-selection route.
Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract.
Avoid provider-specific aliases when the shared field name already expresses the same fact.

## Before You Start

Read:

- `../using-orbit/references/safety-rules.md`
- `references/usage.md`
- `references/commands.md`

Follow the packaged launchers for all external-system access. Do not call raw REST APIs.

The shared write confirmation protocol in `../using-orbit/references/safety-rules.md` still applies by default. `shadow` mode remains repo/remote read/report only, but internal local-state persistence under `~/.config/gate-remediation/` remains allowed in both `shadow` and `repair`, including routine run-state writes and non-provider local config persistence in `config.json`. In `repair` mode, only the additional repo-local or remote writes listed under **Allowed Automatic Writes** may bypass the shared confirmation protocol. All other shared safety rules still apply.

Keep repository-wide provider-resolution, write-confirmation, and stop-condition rules in the shared references instead of duplicating the full protocol here.

## Config Guidance

- Run packaged `config get` checks for the sibling CLIs needed by the active phase.
- Discover sibling provider skills before any provider `config get` checks; `installed` and `configured` are separate facts.
- For an explicit `REPAIR_PROVIDERS` list, first verify every requested provider skill is installed, then run `config get` for those requested providers.
- For omitted provider input or `REPAIR_PROVIDERS=auto`, first discover installed supported provider skills. In interactive runs, resolve the user's choice from that installed set before provider `config get` checks for the chosen providers. In automation runs, run `config get` for those installed supported provider skills first, then resolve `selectedProviders` from the installed-plus-configured subset.
- If config is missing and the user provides the values, run the matching `config set` yourself, rerun `config get`, then continue.
- Do not ask the user to edit config files manually when the packaged CLI already supports `config set`.
- One selected `repo` provider and one selected `quality` provider are baseline-required for the normal repair path.
- `jenkins` or `github-workflow` becomes required when remote verification or post-merge follow-up is in scope and a `ci` provider is installed or selected.
- Missing config for the current `security_scan` provider should degrade that inventory or follow-up route rather than block a safe quality-first remediation path by itself.

## Installed Versus Configured Providers

- A provider counts as installed when its sibling skill is present and callable through the expected packaged launcher.
- A provider counts as configured only when the packaged `config get` succeeds.
- Keep `installed` and `configured` as separate facts in both run state and operator guidance.
- Do not redefine "user has this provider" to mean `config get` succeeds.

## Provider Selection

- Explicit `REPAIR_PROVIDERS` is the hard repair scope for the run. First verify every requested provider skill is installed, then run `config get` for every requested provider.
- When `REPAIR_PROVIDERS` is omitted, resolve it exactly like `REPAIR_PROVIDERS=auto`. Do not read or bootstrap provider-selection behavior from `~/.config/gate-remediation/config.json`, and ignore any legacy `repairProvidersDefault` field if it is still present there.
- In an interactive run with omitted provider input or `REPAIR_PROVIDERS=auto`, first discover installed providers. Select the only installed provider automatically. When multiple providers are installed, ask the user to choose one provider from the discovered installed-provider list for the current run, or choose the menu label `all`.
- Build that interactive question from the actual discovered installed-provider set for the current run. Phrase it naturally for the current conversation language instead of reusing one fixed sentence template, but inline the discovered option labels in the question itself and ask the user to reply with exactly one provider name or `all`. Do not hardcode provider names into the question text, do not hardcode provider counts such as "two providers", and do not ask the user to reply with a literal `REPAIR_PROVIDERS=...` assignment in that first choice prompt.
- In that interactive menu, `all` resolves internally to the full discovered installed-provider set for the current run; it is not a literal accepted `REPAIR_PROVIDERS` value, and the user must not be asked to restate `all` as a comma-separated assignment before continuation.
- In a Chinese interactive run, do not pin the first question to one canned wording. Generate the wording from the actual discovered installed-provider set for that run, keep the concrete provider labels and `all` visible in the question, and still require exactly one provider name or `all`.
- In an automation run with omitted provider input or `REPAIR_PROVIDERS=auto`, do not ask the user. First discover installed supported provider skills, then run `config get` for those installed supported provider skills, and finally resolve `selectedProviders` from the installed-plus-configured subset.
- If an explicitly selected provider is installed but `config get` fails, stop as `WAIT_USER_CONFIG` and guide the user through the matching `config set` instead of silently narrowing scope.
- If an explicitly selected provider is not installed, stop as `BLOCKED` and tell the user which provider skill must be installed.
- If automation with omitted provider input or `auto` finds installed providers but none with successful `config get`, stop as `WAIT_USER_CONFIG`.
- If omitted provider input or `auto` finds no supported provider skill installed at all, stop as `BLOCKED` instead of pretending the run has no repair scope.
- Persist the resolved run snapshot as `selectedProviders`; do not mutate it mid-run.

## Repository Targeting

- When `REPO_PATHS` is present, validate those repositories directly and skip recursive `ROOT_DIR` discovery unless conservative dependent-repository expansion later requires an allowed `ROOT_DIR` boundary.
- When `REPO_NAMES` is present, resolve names only under `ROOT_DIR` and skip unrelated repositories.
- When only `ROOT_DIR` is present, keep the current full-inventory discovery behavior.
- In targeted modes, continue only tracked repositories inside the explicit target set unless issue-cluster expansion is required and still inside the allowed boundary.
- Treat zero-hit or multi-hit `REPO_NAMES` resolution as `MAPPING_AMBIGUOUS`.

## Local Defaults

Persist routine defaults in `~/.config/gate-remediation/config.json`.

Recommended defaults:

- `defaultBranchCandidates=["master","main","develop"]`
- `maxConcurrentRepos=2`
- `maxIterationsPerRepo=3`
- `maxRuntimePerRepoMin=120`
- `subagentMode="auto"`

Do not drive provider selection from `config.json`. If an older local config file still contains `repairProvidersDefault`, ignore that legacy field or remove it during routine local cleanup; omitted `REPAIR_PROVIDERS` now follows the same rules as `auto`.

## Local Persistence

Persist local state under:

```text
~/.config/gate-remediation/
```

Use that root for candidate lists, per-repository state, reports, isolated worktrees, and routine non-provider local config persistence.

## Hourly Run Order

1. For an interactive run where `REPAIR_PROVIDERS` is omitted or `auto` and multiple providers are installed, silently discover installed providers first and ask the provider-choice question from the discovered installed-provider list plus `all` as the first user-visible question; before that choice is answered, do not load tracked state, resolve the active target set, or run provider-specific preflight.
2. Load tracked repository state from `~/.config/gate-remediation/repos/`.
3. Resolve the active target set from `REPO_PATHS`, `REPO_NAMES + ROOT_DIR`, or `ROOT_DIR`.
4. Resolve the provider-selection route for the run: if `REPAIR_PROVIDERS` is omitted, treat it exactly like `auto`; continue from the already collected provider choice when step 1 applied; otherwise discover installed providers, ask from the discovered installed-provider list plus `all` when interactive `auto` has multiple installed providers, resolve the user's choice first, run provider `config get` only for the providers required by that path, and persist the resolved `selectedProviders` set for the run.
5. Refresh findings only from the selected providers.
6. Normalize those findings into `finding` records and cluster them into issue-level repair scope.
7. Expand to additional repositories only when the cluster clearly requires them and the target boundary allows it.
8. Enqueue or continue one `repo_work_item` per required repository.

### Cluster states

- `DISCOVERED`
- `NEEDS_REPAIR`
- `PATCHING`
- `WAIT_USER_CONFIG`
- `WAIT_USER_MERGE`
- `WAIT_PROVIDER_REFRESH`
- `BLOCKED_DEPENDENT_SCOPE`
- `BLOCKED`
- `EXHAUSTED`
- `DONE`

### Repo work item states and parent-managed waits

- keep the existing repo-local state machine where possible
- keep legacy `WAIT_MASTER_BUILD`, `WAIT_MASTER_SONAR`, and `MASTER_REGRESSED` only for the SonarQube default-branch follow-up path
- add `WAIT_CLUSTER` for repositories whose local patching work is finished but whose issue cluster is still waiting on other repositories or selected providers; this is a parent-managed per-repository waiting state, and the matching repo work item is inactive until the parent clears `WAIT_CLUSTER`

### Parent responsibilities

- resolve `REPAIR_PROVIDERS`
- record `installedProviders`, `providerConfigStatus`, and `selectedProviders`
- normalize provider findings into `finding` records
- cluster findings into issue-level repair scope
- decide dependent-repo expansion conservatively
- persist cluster state and repo work items
- when a reopened cluster returns from selected-provider refresh to `NEEDS_REPAIR`, clear `WAIT_CLUSTER` and reactivate the required repo work items for the next repair cycle
- decide cluster completion and blocking
- produce the final operator summary

### Worker responsibilities

- own one repository only
- execute one `repo_work_item` for one cluster
- reuse the tracked worktree and branch
- diagnose repo-local blockers
- apply patches
- run local verification
- create or update one PR
- return repo-local facts to the parent
- never widen repo scope or declare cluster completion

### Worker eligibility rules

- `MODE=repair`
- the repository is inside the active target set
- the repository is required by an active issue cluster that is in `NEEDS_REPAIR` or `PATCHING`
- no foreign active lock owns `codex/auto-gate-remediation`
- the repository is not already in a parent-managed waiting state such as `WAIT_CLUSTER`
- use `MAX_CONCURRENT_REPOS` as the worker batch ceiling
- if `SUBAGENT_MODE=off` or worker dispatch is unavailable, process the repository inline with the same tracked branch, worktree, PR, and verification semantics

### Phase 1: Inventory

1. Resolve the provider-selection route for the run: if `REPAIR_PROVIDERS` is omitted, treat it exactly like `auto`; then discover installed providers, ask from the discovered installed-provider list plus `all` when interactive `auto` has multiple installed providers, resolve the user's choice first, run provider `config get` only for the providers required by that path, and persist the resolved `selectedProviders` set for the run under the provider-selection rules above.
2. Read findings only from the selected providers.
3. Normalize those findings into provider-agnostic `finding` records.
4. Cluster conservative matches into issue-level repair scope.
5. Expand to additional repositories only when the cluster clearly requires them and the target boundary allows it.
6. If a required dependent repository is unresolved or outside allowed scope, mark the cluster `BLOCKED_DEPENDENT_SCOPE`.

### Phase 2: Repair To PR

1. Fetch the remote state for `codex/auto-gate-remediation`.
2. If the branch exists and belongs to another active owner, skip the repository.
3. Reuse the existing remediation branch and PR when they already exist.
4. In `SUBAGENT_MODE=auto`, dispatch eligible repositories in batches up to `MAX_CONCURRENT_REPOS`; if worker dispatch is unavailable, continue inline instead of stopping for orchestration reasons alone.
5. Inside the active repair worker or inline fallback path, when the original evidence is too broad, cross-cutting, or failed to converge on the first pass, refresh or reuse the `repo-understanding` cache and use its local search or explain helpers to narrow likely edit targets before the next patch cycle. If it does not improve focus, fall back to the normal remediation flow without blocking on it.
6. Diagnose repo-local failures by root cause.
7. Attempt one small repo-local baseline-enabling repair first when the default branch baseline is red but still fixable in-repo.
8. Apply a small patch set for the selected-provider findings that are clearly repairable in this repository for the active issue cluster, including cheap repo-local Fortify findings when they are in scope.
9. Run local verification before every push.
10. Before creating a new remediation PR, compute selected repo-provider reviewer enhancements when available. For Bitbucket, call `bitbucket repo required-reviewers` and pass the resulting reviewers into `bitbucket pr create --reviewers`; for GitHub, use the equivalent repository review-policy enhancement when the selected provider exposes one; for GitLab, continue with plain `gitlab pr create` / `gitlab pr update` and record degraded reviewer behavior.
11. Push the remediation branch and create or update one PR.
12. Follow repo-scoped verification and selected-provider evidence until the repository either converges, remains patchable, or stops.
13. If the active repair attempt is still red or unclear, read the matching scoped issue or finding details from the selected providers before choosing the next patch or stop reason.
14. When the selected `ci` provider is `github-workflow`, tie remote verification to the known workflow run and use `github-workflow build get` plus `github-workflow build console` for follow-up instead of assuming Jenkins-only paths.

### Phase 3: Post-merge Follow-up

1. When the tracked remediation PR becomes `MERGED`, switch from PR-scoped follow-up to parent-owned post-merge follow-up.
2. Record `mergedAt` and the merged revision from the tracked PR metadata as `expectedDefaultRevision`. When `selectedProviders` includes `sonarqube`, fetch `origin/<default-branch>` only to confirm when the default branch has reached that same merged revision; do not rebind follow-up to newer unrelated head commits.
3. When `selectedProviders` includes `sonarqube`, use `WAIT_MASTER_BUILD` and `WAIT_MASTER_SONAR` only for the SonarQube default-branch follow-up subpath while waiting for the existing default-branch Jenkins path or GitHub Workflow path and the fresh default-branch SonarQube analysis.
4. When `selectedProviders` includes `sonarqube` and that existing path does not auto-start within the wait window and the job is triggerable, trigger that existing CI path manually through the selected provider.
5. When `sonarqube` is outside `selectedProviders`, keep the repository in `WAIT_CLUSTER` while the parent tracks selected-provider refresh or other cluster-level follow-up instead of forcing `WAIT_MASTER_BUILD` or `WAIT_MASTER_SONAR`. `WAIT_CLUSTER` remains parent-managed until the cluster is either cleared or reopened.
6. In dual-provider or multi-provider runs, once the SonarQube default-branch subpath is fresh and clear, if any other selected provider still needs refresh or is still pending, move the repository into `WAIT_CLUSTER` while the parent keeps the cluster in `WAIT_PROVIDER_REFRESH`.
7. Poll the selected providers until fresh post-change evidence is available for the recorded post-merge evidence target for this repair attempt, such as the merged revision or another provider-specific patched target.
8. Keep the issue cluster `WAIT_PROVIDER_REFRESH` until every selected provider required for completion is fresh and clear for the current repair attempt.
9. If fresh selected-provider evidence still shows the issue unresolved, return the cluster to `NEEDS_REPAIR`. Use legacy repo state `MASTER_REGRESSED` only for the SonarQube default-branch regression path; if SonarQube is already fresh and clear but another selected provider later returns fresh unresolved evidence for the recorded post-merge evidence target, keep or move the repository in `WAIT_CLUSTER` until the parent clears that waiting state and re-enqueues or reactivates the required repo work items so they become repairable again on the next cycle. Reopen another repair cycle only when no active remediation PR already exists and the same recorded post-merge evidence target plus `failureFingerprint` pair is still new. Once a reopen attempt for that pair is recorded in cluster or per-repository state, treat it as already handled and suppress duplicate reopen.

`WAIT_PROVIDER_REFRESH` means the code-side change is already in place for the current repair attempt, but at least one selected provider has not yet produced fresh post-change evidence tied conservatively to that repair attempt.

### Phase 4: Stop Reporting

1. State the stop classification and the concrete blocker facts.
2. Explain why that blocker prevents a safe remediation continuation in the current run.
3. Give the user a short `next actions` list.
4. Say whether rerun is useful immediately or only after the listed actions are completed.
5. Persist that operator guidance in the local report and per-repository state.
6. Make the user-visible stop guidance concise Chinese by default.
7. If a selected-provider remediation PR was still safe to produce, report any remaining cross-repository or out-of-scope follow-up work as follow-up guidance instead of a hard stop reason.
8. When the blocker is `BLOCKED` because of missing provider installation, distinguish the cases explicitly: name the missing provider skill when selection came from an explicit provider list; otherwise, if the run used omitted provider input or `auto`, tell the user that no supported provider skill is installed and that at least one provider skill must be installed before rerun.

## Allowed Automatic Writes

Internal local-state persistence under `~/.config/gate-remediation/` is allowed in both `shadow` and `repair`, including routine `config.json` updates for non-provider defaults plus normal run-state and report persistence.

In `repair` mode only, these additional repo-local or remote writes may bypass the shared confirmation protocol:

- local code edits
- local test edits
- local build or scanner configuration edits
- remediation branch creation or reuse
- commits on `codex/auto-gate-remediation`
- PR create and PR update
- manual trigger of the existing default-branch Jenkins job or GitHub Actions workflow only when the run is already in the SonarQube default-branch post-merge follow-up path, the documented wait window expires, and the path is triggerable

## Forbidden Automatic Writes

- merge to the default branch
- tracker writes
- docs writes
- SonarQube server-side gate or profile changes
- Fortify suppression or waiver actions
- review comments or approvals that impersonate a human reviewer

## Completion

An issue cluster is `DONE` only when:
- `selectedProviders` is fixed for the run
- every required repository in the cluster is complete
- no required dependent repository is unresolved
- every selected provider has fresh clear evidence for the current repair attempt

If `selectedProviders=["sonarqube","fortify"]`, both providers must clear before the cluster is done.
If `selectedProviders=["sonarqube"]`, Fortify may be reported as follow-up but must not block completion.
If `selectedProviders=["fortify"]`, SonarQube may be reported as follow-up but must not block completion.

## Final Run Report

The terminal final answer is an operator handoff, not a replay log.

Report priority:

1. current issue cluster state
2. whether the user must do anything now
3. 1-3 key facts that justify the current state
4. what the automation will do next

Report rules:

- In a single-repository run, use at most four short Chinese lines or bullets for that issue cluster in this order:
  - `<cluster>: <state>` or `<repo>: <state>` when one cluster maps cleanly to one repository
  - `现在要做：...` or `现在不用做：...`
  - `关键事实：...`
  - `下一步：...`
- In a multi-repository run, start with one Chinese dashboard line that gives counts for `need user action`, `automation continues`, and `blocked`, then list only issue clusters that need user action or are blocked. Collapse normal tracked clusters into counts unless the user explicitly asked for full inventory.
- Mention out-of-scope provider follow-up only when it creates a separate actionable follow-up. Do not repeat advisory follow-up counts in every green-PR or wait-for-merge case.
- Mention the concrete blocker reason only when the run stopped or the repository needs manual takeover.
- Do not include preflight-passed boilerplate, local state file paths, reviewer-fallback internals, exact local verification command lists, or root-cause file paths unless they change the current operator decision.
- Persist full detail under `~/.config/gate-remediation/`; keep the terminal final answer short.
