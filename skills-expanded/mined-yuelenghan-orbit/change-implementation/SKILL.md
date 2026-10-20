---
name: change-implementation
description: "Use when a scheduled or operator-initiated workflow should pull tracker work items through a provider-specific query, decompose them into one or more bounded repositories under a user-provided ROOT_DIR, run repo-understanding before editing, implement locally, and deliver one pull request per repository in the selected repo provider with optional CI follow-up."
metadata:
  author: Orbit contributors
  version: "0.2.0"
---

# Change Implementation

Use this skill for one recurring or operator-initiated automation flow that turns tracker work items into repository-local changes and one or more pull requests in the selected repo provider. `repo-understanding` is mandatory inside every repo-local implementation path, and repository search must stay inside the user-provided `ROOT_DIR`.

## Capability Dependencies

- One `tracker` provider skill such as `jira` or `github-issue`
- One `repo` provider skill such as `bitbucket`, `github`, or `gitlab`

A `docs` provider such as `confluence` or `obsidian` is an optional read helper when Story context is thin. A `ci` provider such as `jenkins` or `github-workflow` is an optional verification helper when a conservative remote path is already known. `repo-understanding` is a source-first local helper and must not be treated as a sibling packaged CLI requiring `config get` preflight.

## Inputs

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `ROOT_DIR` | Yes | Root directory that contains candidate repositories | `/path/to/workspace/sample-org` |
| `TRACKER_QUERY` | Yes | Provider-specific work-item query that selects the implementation queue | `assignee = currentUser() AND status = "Ready For Dev" ORDER BY priority DESC` |
| `MODE` | Yes | One of `shadow` or `implement` | `implement` |
| `DEFAULT_BRANCH_CANDIDATES` | Yes | Ordered default branch candidates | `master,main,develop` |
| `DELIVERY_MODE` | No | One of `single-repo` or `multi-repo` | `multi-repo` |
| `SUBAGENT_MODE` | No | One of `off` or `auto` | `auto` |
| `MAX_ITEMS_PER_RUN` | No | Maximum work items processed in one run | `3` |
| `MAX_ITERATIONS_PER_ITEM` | No | Maximum patch loops per item | `3` |
| `MAX_RUNTIME_PER_ITEM_MIN` | No | Maximum minutes per item | `120` |
| `MAX_REPOS_PER_ITEM` | No | Maximum repositories allowed for one tracker work item in `multi-repo` mode | `3` |
| `MAX_ACTIVE_REPO_WORKERS` | No | Maximum repo workers active at once for one tracker work item | `2` |

Ask for any missing required inputs in one plain-text message. Do not guess outside `ROOT_DIR`.

## Missing-input collection rules

Ask for any missing required inputs in one plain-text message.
Prefer the smallest missing set that unblocks the selected route.
Use normalized shared field names from `../using-orbit/references/common-input-contract.md` whenever the input belongs to the shared capability contract.
Avoid provider-specific aliases when the shared field name already expresses the same fact.

Default rules:

- default `DELIVERY_MODE` to `single-repo` for backward compatibility
- default `SUBAGENT_MODE` to `auto`
- default `MAX_REPOS_PER_ITEM` to `3`
- default `MAX_ACTIVE_REPO_WORKERS` to `2`
- in `DELIVERY_MODE=single-repo`, `CROSS_REPO_CHANGE` remains a stop condition
- in `DELIVERY_MODE=multi-repo`, the skill may decompose one item into multiple repository-local work units only when the repository set is conservative and bounded

## Interaction Efficiency Rules

### Clarification batching

When multiple points need user confirmation, list them all in a single turn. Do not ask one question, wait for the answer, then ask the next. If you discover new clarification needs while waiting, batch them with the current ask rather than producing a second clarification turn.

Exception: if a user's answer to an earlier question makes a later question irrelevant, drop the irrelevant question silently — do not ask it just because it was on the original list.

### Existing-pattern-first

Before creating a new annotation, aspect, utility class, configuration key, or framework abstraction, search the target repository for existing mechanisms that serve the same purpose. If one exists (for example `@DS` for dynamic datasource switching, or an existing cache service), reuse it instead of inventing a parallel mechanism. Only create a new abstraction when no existing pattern covers the need.

This applies to all repository-local code generation: imports, annotations, configuration, service beans, and test infrastructure.

### Edit fast-forward

When editing a file, if the same `old_string` match fails 2 consecutive times, switch to `Write` (full overwrite) instead of retrying `Edit`. Do not burn turns on repeated Edit failures against the same file.

## Critical first-turn boundary rules

This section outranks all later reference-reading guidance in this skill. Until the first live stop boundary is cleared, do not let later `Read ...`, launcher-discovery, config, or repo-inspection guidance override these rules.

When the prompt already names one tracker work item directly and clearly asks to change code, self-test, and raise a PR:

- treat a direct tracker key such as `PROJ-123` as the work-item selection input, not as a hint that still requires a full `TRACKER_QUERY`
- infer `MODE=implement` from wording such as "修一下", "改完", "自测", or "提 PR"
- if `ROOT_DIR` is still missing, make the first user-visible response only the `ROOT_DIR` question

**Why this matters**: Early reads of tracker, repo, docs providers, repos, or archived state are wasted before the execution boundary (`ROOT_DIR` + issue route) is known. The boundary question itself is the only required first output — everything else can wait until it's answered.

## Before You Start

Read:

- `../using-orbit/references/safety-rules.md`
- `references/usage.md`
- `references/commands.md`

Follow the packaged launchers for all external-system access. Do not call raw REST APIs.

The shared write confirmation protocol in `../using-orbit/references/safety-rules.md` still applies by default. `shadow` mode remains read and report only. In `implement` mode, only the writes listed under **Allowed Automatic Writes** may bypass the shared confirmation protocol. All other shared safety rules still apply.

Before using an optional `docs` or `ci` provider, run that provider's own `config get` checks first.

Keep repository-wide write-confirmation, stop-condition, and provider-resolution rules in the shared references instead of restating them in full here.

## Local Persistence

Persist local state under:

```text
~/.config/change-implementation/
```

Recommended layout:

```text
~/.config/change-implementation/
  config.json
  repos-index.json
  runs/
    <run-id>.json
  reports/
    <timestamp>-summary.md
  issues/
    <issue-key>/
      state.json
      events.jsonl
      context.md
      repos/
        <repo-key>/
          state.json
          events.jsonl
  worktrees/
    <issue-key>/
      <repo-key>/
```

Use the selected tracker work-item identifier exactly as it appears in the tracker for `issues/<issue-key>/`.
Use the repository key exactly as it appears in the repository index for `issues/<issue-key>/repos/<repo-key>/`.
Use lower-case only for Git branch names:

- `codex/<issue-key-lower>` in `DELIVERY_MODE=single-repo`
- `codex/<issue-key-lower>-<repo-slug>` in `DELIVERY_MODE=multi-repo`

## Recurring Run Order

1. Load tracked issue state from `~/.config/change-implementation/issues/`.
2. Re-read each tracked work item's latest tracker details and comments before deciding whether it is still safe to continue. When the selected tracker exposes only `tracker.issue.get` and not a separate comment-read helper, continue with the issue body plus any provider-native fields already returned there instead of inventing a missing comment command.
3. Process already-tracked items first only when the refreshed tracker facts still support the same repository-local work.
4. Query the selected tracker with the configured `TRACKER_QUERY` for new or untracked items.
5. Discover repositories only under `ROOT_DIR`.
6. Decide whether each item stays single-repository or enters conservative multi-repository decomposition.
7. Enqueue only new `AUTO_IMPLEMENTABLE` items that are not already tracked.
8. Emit one run summary and persist issue-root plus repo-child state changes.

## Workflow

### Issue-root states

- `DISCOVERED`
- `CONTEXT_GATHERING`
- `REQUIREMENT_GROUNDING`
- `CONTEXT_CONFLICTED`
- `REPO_DECOMPOSING`
- `REPO_EXECUTING`
- `WAIT_USER_REVIEW`
- `PARTIAL_USER_REVIEW`
- `BLOCKED`
- `EXHAUSTED`

### Repository-child states

- `REPO_SCOPED`
- `PATCHING`
- `LOCAL_VERIFYING`
- `PR_OPEN`
- `WAIT_REMOTE_VERIFY`
- `WAIT_USER_REVIEW`
- `BLOCKED`
- `EXHAUSTED`

Root-state semantics:

- root `WAIT_USER_REVIEW` means every required repository child reached `WAIT_USER_REVIEW`
- root `PARTIAL_USER_REVIEW` means at least one repository child is ready for review and at least one required repository child is `BLOCKED` or `EXHAUSTED`
- only the parent issue orchestrator may decide issue-root completion or report `PARTIAL_USER_REVIEW`

### Phase 1: Inventory

1. Read tracker work items with the configured `TRACKER_QUERY`.
   - Jira example: `jira issue search --jql "<TRACKER_QUERY>" --max-results 50`
   - GitHub Issue example: `github-issue issue search --namespace <OWNER_OR_ORG> --repo <REPO> --query "<TRACKER_QUERY>"`
2. Read each queued item's description and comments when the selected tracker exposes them.
   - Jira example: `jira issue get --key PROJ-123` plus `jira issue comment list --key PROJ-123`
   - GitHub Issue example: `github-issue issue get --namespace <OWNER_OR_ORG> --repo <REPO> --number <ISSUE_NUMBER>`
3. When a Story-like item's tracker context is thin and a `docs` provider is available, read matching design context by issue key.
   - Confluence example: `confluence search content --cql "text ~ 'PROJ-123'" --type page --limit 5`
   - Obsidian example: `obsidian content search --query "PROJ-123"`
4. Discover repositories only under `ROOT_DIR`.
5. Build the latest repository index.
6. Carry forward issue type, context quality, mapping hints, local verification hints, and remote verification hints into issue state.
7. Classify each item into `AUTO_IMPLEMENTABLE`, `MAPPING_AMBIGUOUS`, `CONTEXT_INCOMPLETE`, `LOCAL_VERIFY_UNKNOWN`, `CROSS_REPO_CHANGE`, or `EXHAUSTED`.
8. Reserve `REMOTE_VERIFY_UNKNOWN` for the post-PR path only.

Guardrails:

- use `MAPPING_AMBIGUOUS` only after issue-commit evidence, repo-name hints, and local overrides still do not produce a conservative repository set under `ROOT_DIR`
- use `CONTEXT_INCOMPLETE` when a Story still lacks testable acceptance criteria or a defect still lacks usable failure context after tracker readback plus optional docs readback
- when the selected tracker lacks a standalone comment-read command, do not block only for that reason; continue with the issue body and provider-native fields already returned by `tracker.issue.get`, then report the degraded tracker context explicitly
- use `CROSS_REPO_CHANGE` when `DELIVERY_MODE=single-repo` and the work clearly spans multiple repositories, or when `DELIVERY_MODE=multi-repo` still cannot produce a conservative bounded repository set
- use `LOCAL_VERIFY_UNKNOWN` only after config overrides, repository markers, and previously persisted successful commands still cannot yield a conservative repo-local verification path
- use `REMOTE_VERIFY_UNKNOWN` only after PR creation when remote verification is required and the CI verification path still cannot be tied conservatively to the current branch or PR head

### Phase 2: Decompose And Schedule

1. Reuse tracked issue state and repo children when they already exist.
2. In `DELIVERY_MODE=single-repo`, require exactly one repository child.
3. In `DELIVERY_MODE=multi-repo`, decompose one issue into multiple repository-local work units only when the repository set is conservative, bounded, and each repository can own one repo-local verification path plus one PR path.
4. Persist each repo child under `issues/<issue-key>/repos/<repo-key>/state.json`.
5. Optionally persist `dependsOn` edges when one repository must wait for another repo child to reach `WAIT_USER_REVIEW`.
6. Dispatch workers in batches up to `MAX_ACTIVE_REPO_WORKERS` when `SUBAGENT_MODE=auto`.
7. If worker dispatch is unavailable, continue sequentially with the same repo-child state model instead of stopping for orchestration reasons alone.

### Phase 3: Repo Execution To PR

For each repository child:

1. Reuse or create one repo-local worktree under `~/.config/change-implementation/worktrees/<issue-key>/<repo-key>/`.
2. Reuse or create one repo-local branch:
   - `codex/<issue-key-lower>` in `single-repo`
   - `codex/<issue-key-lower>-<repo-slug>` in `multi-repo`
3. Run `repo-understanding refresh`, then `search`, then `explain` before the first patch cycle.
4. Narrow the candidate code, config, test, and pipeline surfaces for that repository only.
5. Build one small repository-local patch plan aligned to Story AC or defect behavior.
6. Resolve one conservative local verification command for that repository child.
7. Apply one small patch set aligned to the grounded context.
8. Run local verification before every push.
9. Run `repo-understanding diff-impact` before final local verification and PR finalization.
10. Before creating a new PR, apply repo-provider reviewer enhancements only when the selected provider supports them. For Bitbucket, compute default reviewers with `bitbucket repo required-reviewers` and pass them into `bitbucket pr create --reviewers`. For GitHub, a conservative enhancement path is to read the existing reviewer state with `github pr requested-reviewers` when reusing an open PR, but PR creation must not block on a reviewer inference step. If the selected provider has no reviewer-enhancement path, continue without blocking PR creation.
11. Push the repo-local branch and create or update one PR for that repository child.
    - Bitbucket example: `bitbucket pr create --project PROJ --repo service-a --title "[PROJ-123] Implement service-a changes" --from refs/heads/codex/proj-123-service-a --to refs/heads/<default-branch> --description "<text>" --reviewers "<u1,u2>"`
    - GitHub example: `github pr create --namespace sample-org --repo service-a --title "[PROJ-123] Implement service-a changes" --head codex/proj-123-service-a --base <default-branch> --description "<text>"`
    - GitLab example: `gitlab pr create --namespace sample-org --repo service-a --title "[PROJ-123] Implement service-a changes" --head codex/proj-123-service-a --base <default-branch> --description "<text>"`
12. When a conservative CI verification path is known, wait for the existing branch or PR verification path.
    - Jenkins example: `jenkins build get --job folder-a/service-a-pr --number 182`
    - GitHub Workflow example: `github-workflow build get --namespace sample-org --repo service-a --number <RUN_ID>`
13. Move the repository child to `WAIT_USER_REVIEW` only when local verification passed and either remote verification is green for a known CI verification path or remote verification is configured as optional for that repository.
14. If remote verification is required but the CI verification path is still unknown after PR creation, stop that repository child as `REMOTE_VERIFY_UNKNOWN` with concrete next actions instead of guessing.

### Phase 4: Stop Reporting

1. State the stop classification and the concrete blocker facts.
2. Explain why that blocker prevents safe continuation in the current run.
3. Give the user a short `next actions` list.
4. Say whether rerun is useful immediately or only after the listed actions are completed.
5. Persist that guidance in the local report and in issue-root plus repo-child state.
6. Make the user-visible stop guidance concise Chinese by default.
7. If one repository child already has a PR, tell the user to continue from the same branch and PR instead of starting over.

## Allowed Automatic Writes

In `implement` mode only, these writes may bypass the shared confirmation protocol:

- local code edits
- local test edits
- local build or verification configuration edits
- repo-local branch creation or reuse
- commits on repo-local implementation branches
- PR create and PR update
- manual trigger of an existing CI job when the documented wait window expires and the job is triggerable
- local state files under `~/.config/change-implementation/`

## Forbidden Automatic Writes

- merge to the default branch
- tracker transition, comment, assign, or field update
- docs page or comment writes
- creating a new CI job or modifying CI configuration
- force-pushing over human-owned work without explicit user instruction

## Completion

An issue reaches successful completion only when the issue root is in `WAIT_USER_REVIEW`.

That requires:

- the issue has a conservative repository decomposition under `ROOT_DIR`
- Story or defect context is sufficient for every required repository child, including degraded tracker-provider paths such as `github-issue issue get` when no standalone comment-read helper exists
- every required repository child completed `repo-understanding` refresh, search, explain, and diff-impact
- every required repository child passed local verification
- one PR exists for each required repository child branch, including `gitlab pr create` paths when GitLab is the selected repo provider
- selected repo provider reviewer enhancements were carried into PR creation when available
- if a CI verification path was known for a repository child, the latest remote verification for that child's current branch or PR head is green, including `github-workflow build get` paths when GitHub Actions is the selected CI provider

`PARTIAL_USER_REVIEW` means some repository children are ready and some are not. It is an operator handoff state, not full completion.
`PR_OPEN`, `WAIT_REMOTE_VERIFY`, and repo-child `REMOTE_VERIFY_UNKNOWN` are not complete states. They must tell the user how to continue.
