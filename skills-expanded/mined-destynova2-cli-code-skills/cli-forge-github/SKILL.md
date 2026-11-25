---
name: cli-forge-github
metadata:
  author: clement
description: >
  Audit and fix GitHub repository health: rulesets vs CI alignment, branch hygiene,
  PR lifecycle, release automation flow, permission issues, and transient CI failures.
  Detects misconfigurations that cause PRs to hang, CI to fail silently, branches to
  accumulate, and releases to stall. Use when the user says 'PR stuck', 'CI pending
  forever', 'branch cleanup', 'ruleset', 'release blocked', 'merge conflicts on
  sync-main', 'stale PRs', 'orphan branches', 'GitHub health', 'repo hygiene',
  'required checks', 'path pruning', 'release-plz stuck', 'auto-merge not working',
  'workflow scope', 'token permission'. Also triggers on 'gh api', 'rulesets',
  'branch protection', 'status checks'.
argument-hint: "[owner/repo or empty for current]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** Heavy content lives in `references/`. Load on demand.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

> **Gotchas:** Read `../gotchas.md` before producing output to avoid known mistakes.

# CLI Forge GitHub — Repository Health Auditor & Fixer

> *"The CI is green, the ruleset says pending, the PR has conflicts, the release is stuck, and 13 branches are dead. Welcome to GitHub."*

## Rules for the Auditor

1. **Read before touching.** Always `gh api` the current state before proposing changes. Rulesets, branch protections, and workflows interact in non-obvious ways.
2. **Fix the root cause, not the symptom.** A PR stuck on "pending" is not fixed by force-merging — find which check is missing and why.
3. **Never force-push protected branches.** Detect the base and release branches (main, develop, master, trunk) and never force-push them. Use `--force-with-lease` on feature branches only.
4. **Prefer API over UI.** Rulesets, checks, and branch cleanup are all automatable via `gh api`. The UI is for humans reviewing the result.
5. **Document every ruleset change.** Add a comment in ci.yml explaining WHY the ruleset requires specific checks. Future you (or a teammate) will re-add the wrong checks if there's no explanation.
6. **Transient failures get a rerun, not a fix.** Rate limits, runner timeouts, and network flakes are not code bugs. Rerun, don't refactor.
7. **Orphan branches are tech debt.** Clean them on every release, not "when we have time".
8. **Always enable auto-merge on every PR you create.** Every `gh pr create` is followed by `gh pr merge --auto --squash` (or `--rebase` / `--merge` per project policy). A PR without auto-merge is a PR somebody has to babysit — that is exactly the state this skill is designed to eliminate. The only exception is a **draft PR**: auto-merge is enabled when the draft is marked ready, not before. This rule applies to every agent that opens PRs through the skill (including the cli-forge-chef Sous-Chef).
9. **Always check conflicts between parallel PRs before dispatch, not after.** When N commis open N parallel PRs against the same base, the file-exclusion is enforced on the commis side (cli-forge-chef PERT + Fiedler partition). On the GitHub side, this skill verifies it didn't leak: for every pair of open PRs against the same base branch, compute the intersection of their changed-files sets; any non-empty intersection is a future merge conflict and must be reported *before* auto-merge lands the first one. Detection is cheap; post-merge rebasing N-1 branches is not.
10. **A PR is not done until the client has the fork in it.** "Auto-merge enabled" is *not* "merged". Any session with PRs in flight runs a post-merge landing watchdog (F9) that polls every 45 s, rebases BEHIND branches on cascade, reruns transient failures (max 2× per cause), and only declares "done" once the PR is `MERGED`, the release tag is cut (if applicable), orphan branches are deleted, and downstream PRs have been caught up. A brigade achieves this via the Maître d'hôtel role (cli-forge-chef references/maitre-dhotel.md); a single-agent session achieves it by calling F9 directly.

## Threat model — What goes wrong

| Problem | Root cause | Symptom | How often |
|---|---|---|---|
| PR pending forever | Ruleset requires a check that path pruning skipped | "Expected — Waiting for status to be reported" | Common |
| Release PR in conflict | release-plz bumps CHANGELOG.md, sync-main also touches it | "This branch has conflicts" | Every release |
| Orphan branches accumulate | Merged PRs don't always delete branches | 10+ stale remote branches | Gradual |
| Auto-merge doesn't trigger | Missing required checks or conflict blocks it | PR sits with auto-merge enabled but never merges | Common |
| PR created without auto-merge | cli-forge-chef Sous-Chef creates PRs but doesn't enable `--auto` | PR is mergeable but nobody merges it | Common (multi-agent) |
| Multi-agent push rejected | develop is protected, Sous-Chef tries direct push | `GH006: Protected branch update failed` | Common (multi-agent) |
| CI fails on transient error | GitHub API rate limit, runner OOM, network timeout | "error in connecting to agent.api.stepsecurity.io" | Occasional |
| Token can't push workflow files | OAuth token lacks `workflow` scope | "refusing to allow an OAuth App to create or update workflow" | On CI file edits |
| Stale PRs from old sprints | Feature branches abandoned but PRs left open | PR list cluttered with OPEN PRs from weeks ago | Gradual |
| Parallel PRs collide at merge | Two commis touched the same file despite the chef's file-exclusion | First PR merges, N-1 others block on conflict, sprint stalls | Common (multi-agent) |
| "Auto-merge enabled" mistaken for "merged" | Operator walks away; PR drifts into BEHIND/BLOCKED after release-plz or another PR lands | Several PRs stuck with `autoMergeRequest: true` but never landing | Common (multi-agent, release automation) |

## Input

`$ARGUMENTS` is the target repo:
- **`owner/repo`** → audit that repo
- **Empty** → detect from `git remote get-url origin`

## Mitosis — Scale to repo complexity

| Signal | Tier | Scope |
|---|---|---|
| Personal project, 1 branch, no rulesets | **S** | Branch cleanup + CI check only |
| Standard project (any branching model), rulesets | **M** | Full audit (all 8 dimensions) |
| Monorepo or multi-workflow with release automation | **L** | Full audit + release flow + cross-workflow analysis |

**Branching model detection:** Before auditing, detect which model the project uses. Do NOT assume Git Flow.

```bash
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef -q '.defaultBranchRef.name' 2>/dev/null)
HAS_DEVELOP=$(git branch -r 2>/dev/null | grep -c 'origin/develop')

# github-flow: only main, no develop
# github-flow-develop: develop + main (like grob)
# gitflow: develop + main + release/* branches
# trunk: single branch, everything goes to main/master
```

Adapt the audit to the detected model:
- **D4 (release flow)**: sync-main only applies to github-flow-develop and gitflow
- **F6 (sync-main conflicts)**: skip entirely for github-flow and trunk
- **Branch hygiene**: "orphan" definition depends on the model — in trunk, any non-main branch older than 7 days is suspect

## Workflow

### Phase 0 — Discover repo configuration

```bash
# Detect repo from git remote
REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null)

# Gather state (all in parallel)
gh api repos/${REPO}/rulesets 2>/dev/null > /tmp/gh-rulesets.json
gh api repos/${REPO}/branches 2>/dev/null > /tmp/gh-branches.json
gh pr list --repo ${REPO} --state open --json number,title,headRefName,createdAt,isDraft,autoMergeRequest > /tmp/gh-prs.json
gh run list --repo ${REPO} --limit 10 --json databaseId,status,conclusion,name,headBranch,event > /tmp/gh-runs.json
```

### Phase 1 — Audit 9 dimensions

Read `references/dimensions.md` for full scoring criteria.
Read `references/release-flow.md` for D4 release flow details and failure modes.

For each dimension, detect issues and score:

| # | Dimension | What to check |
|---|---|---|
| D1 | **Ruleset ↔ CI alignment** | Do rulesets require checks that path pruning can skip? |
| D2 | **Branch hygiene** | Orphan remote branches? Stale local branches? Dangling worktrees? |
| D3 | **PR lifecycle** | Open PRs > 7 days? Auto-merge enabled but stuck? Draft PRs abandoned? **Auto-merge enabled on every non-draft PR? Parallel PRs conflict-free (see §Parallel PR conflict scan)?** |
| D4 | **Release flow** | release-plz PR in conflict? sync-main diverged? Tag ↔ branch mismatch? See `references/release-flow.md` for 6 failure modes |
| D5 | **CI health** | Recent failures? Transient vs real? Flaky jobs? |
| D6 | **Permissions & scopes** | CODEOWNERS valid? Token scopes sufficient? CLA configured? |
| D7 | **Default branch config** | Squash-on-merge? Delete-branch-on-merge? Require linear history? |
| D8 | **Workflow hygiene** | Unused workflows? Deprecated actions? Pinned action versions? |
| D9 | **Prek ↔ CI alignment** | Local pre-commit/pre-push mirrors the fast CI checks? CI YAML validated locally? |

### Phase 2 — Fix detected issues

For each issue found, apply the fix. Read `references/fixes.md` for the fix catalog.

**Fix priority:**
1. **Blocking** — PRs stuck, CI broken, release stalled → fix immediately
2. **Degrading** — Orphan branches, stale PRs, config drift → fix in this pass
3. **Cosmetic** — Naming, labels, descriptions → note in report, don't fix

**Mandatory protocol per fix:**

```
FOR EACH issue:
  1. IDENTIFY: which dimension, what's broken, what's the root cause
  2. VERIFY: confirm the issue exists (gh api, not assumption)
  3. FIX: apply via gh api / gh pr / git commands
  4. CONFIRM: verify the fix worked (re-check the state)
  5. DOCUMENT: if the fix changes a ruleset or CI config, add a comment explaining why
```

### Phase 3 — Score and report

## GitHub Health Score (GHS)

| # | Dimension | Max | Scoring |
|---|---|---|---|
| D1 | Ruleset ↔ CI alignment | 15 | 0: checks required but skippable. 15: all required checks always emit a status |
| D2 | Branch hygiene | 10 | -2 per orphan branch (min 0). 10: zero orphans, auto-delete on merge |
| D3 | PR lifecycle | 10 | -2 per stale PR > 7d. 10: no stale PRs, auto-merge working |
| D4 | Release flow | 15 | 0: release PR in conflict. 15: release-plz + sync-main + tag all clean |
| D5 | CI health | 15 | -5 per real failure (not transient). 15: all recent runs green |
| D6 | Permissions & scopes | 10 | -5 per missing CODEOWNERS or broken CLA. 10: all configured |
| D7 | Default branch config | 10 | +5 squash-on-merge, +3 delete-branch-on-merge, +2 linear history |
| D8 | Workflow hygiene | 15 | -3 per deprecated action, -2 per unpinned action. 15: all pinned, no deprecated |

**Score capped at 100.**

| GHS | Grade | Meaning |
|-----|-------|---------|
| 85-100 | **A** | Healthy — repo is well-maintained |
| 70-84 | **B** | Good — minor issues, nothing blocking |
| 50-69 | **C** | Needs attention — some PRs or releases stuck |
| 30-49 | **D** | Degraded — multiple blocking issues |
| 0-29 | **F** | Broken — PRs can't merge, CI broken, branches chaos |

## Output format

```markdown
# GitHub Health Report — {owner/repo}

**Date:** {date}
**Branch:** {default branch}
**GHS:** {score}/100 ({grade})

## Dimension Summary

| # | Dimension | Score | Status | Issues |
|---|-----------|-------|--------|--------|
| D1 | Ruleset ↔ CI | 12/15 | Warning | 1 skippable required check |
| D2 | Branch hygiene | 4/10 | Critical | 3 orphan branches |
| D3 | PR lifecycle | 8/10 | OK | 1 PR > 7 days |
| D4 | Release flow | 15/15 | OK | — |
| D5 | CI health | 10/15 | Warning | 1 transient failure (rerun) |
| D6 | Permissions | 10/10 | OK | — |
| D7 | Default branch | 10/10 | OK | — |
| D8 | Workflow hygiene | 12/15 | Warning | 1 unpinned action |
| **Total** | | **81/100 (B)** | | |

## Issues Found & Fixes Applied

| # | Dimension | Issue | Severity | Fix | Status |
|---|-----------|-------|----------|-----|--------|
| 1 | D1 | Ruleset "Protect develop" requires Clippy but path pruning skips it | Blocking | Changed ruleset to require only `Required checks` | Fixed |
| 2 | D2 | 3 orphan branches: feat/old-1, feat/old-2, fix/stale | Degrading | `gh api -X DELETE` on each | Fixed |
| 3 | D5 | Coverage job failed (GitHub API rate limit) | Transient | Rerun: `gh run rerun --failed` | Fixed |

## Recommendations

- {specific recommendations for unfixed items}

## Branch Status

| Branch | Ahead/Behind develop | Last commit | Action |
|--------|---------------------|-------------|--------|
| main | 0 ahead, 0 behind | {date} | Synced |
| release-plz-* | 1 ahead | {date} | Auto-managed |

## PR Status

| # | Title | Age | Status | Auto-merge | Action |
|---|-------|-----|--------|------------|--------|
| #152 | release v0.36.6 | 1d | Open | No | Auto-managed by release-plz |
```

## Common fixes catalog (summary — full in references/)

### F1 — Ruleset requires skippable checks (the #153 bug)

**Symptom:** PR shows "Expected — Waiting for status to be reported" forever.

**Root cause:** Ruleset requires `Clippy (ubuntu-latest)` as a named check, but the CI has path pruning that skips Clippy when no Rust files changed. GitHub never receives the status → pending forever.

**Fix:**

```bash
# Get the ruleset ID
RULESET_ID=$(gh api repos/${REPO}/rulesets | jq '.[] | select(.name == "Protect develop") | .id')

# Replace individual job names with the summary job
gh api repos/${REPO}/rulesets/${RULESET_ID} --method PUT \
  --input <(jq '.rules |= map(
    if .type == "required_status_checks" then
      .parameters.required_status_checks = [{"context": "Required checks"}]
    else . end)' /tmp/gh-rulesets-current.json)
```

**Prevention:** Add a comment in ci.yml near the summary job:
```yaml
# This is the ONLY job referenced in the GitHub ruleset "Protect develop".
# Do NOT add individual job names to the ruleset — path pruning skips them.
```

### F2 — Release PR in conflict

**Symptom:** release-plz PR shows "This branch has conflicts" on CHANGELOG.md.

**Root cause:** release-plz bumps CHANGELOG.md, but another PR (e.g., sync-main) also touched it. release-plz doesn't auto-rebase.

**Fix:** Close the stale release PR. release-plz will recreate it on the next trigger.

```bash
gh pr close ${PR_NUMBER} --repo ${REPO} --comment "Stale: conflicts with develop. release-plz will recreate."
```

### F3 — Orphan branches

**Symptom:** `gh api repos/${REPO}/branches` returns branches whose PRs are already merged.

**Fix:**

```bash
# For each orphan branch
gh api -X DELETE repos/${REPO}/git/refs/heads/${BRANCH} 2>/dev/null
```

**Prevention:** Enable "Automatically delete head branches" in repo settings:
```bash
gh api repos/${REPO} --method PATCH -f delete_branch_on_merge=true
```

### F4 — Transient CI failure

**Symptom:** CI fails with rate limit, network timeout, or runner OOM — not a code bug.

**Detection:** Error message contains `rate limit`, `timeout`, `OOM`, `connection refused`, `stepsecurity`.

**Fix:**

```bash
gh run rerun ${RUN_ID} --repo ${REPO} --failed
```

### F5 — Token lacks workflow scope

**Symptom:** `refusing to allow an OAuth App to create or update workflow`

**Fix:** Temporary scope elevation + push + scope removal:

```bash
gh auth refresh -s workflow
git push origin ${BRANCH}
gh auth refresh  # removes workflow scope
```

### F6 — sync-main conflicts

**Symptom:** sync-main PR has conflicts on CHANGELOG.md, Cargo.toml, Cargo.lock.

**Fix:** Recreate the sync branch from develop, resolve conflicts with `--strategy-option theirs` (develop wins):

```bash
git checkout -B sync-main-v${VERSION} origin/develop
git merge origin/main --no-edit -X theirs
git push origin sync-main-v${VERSION} --force-with-lease
```

### F7 — PR opened without auto-merge

**Symptom:** `gh pr list --json number,autoMergeRequest` returns rows with `autoMergeRequest: null` that are **not drafts**. They sit waiting for a human.

**Fix — enable auto-merge on every affected PR:**

```bash
# Detect the project merge policy once (squash / rebase / merge)
POLICY=$(gh api repos/${REPO} --jq '
  if .allow_squash_merge then "--squash"
  elif .allow_rebase_merge then "--rebase"
  else "--merge" end')

# Enable auto-merge on every non-draft PR missing it
gh pr list --repo ${REPO} --state open \
  --json number,isDraft,autoMergeRequest \
  --jq '.[] | select(.isDraft == false and .autoMergeRequest == null) | .number' |
while read -r PR; do
  gh pr merge ${PR} --repo ${REPO} --auto ${POLICY} || \
    echo "PR #${PR}: auto-merge failed — check for conflicts or missing required checks"
done
```

**Prevention (for multi-agent flows):** The Sous-Chef of cli-forge-chef MUST chain `gh pr create` with `gh pr merge --auto` in the same command sequence. Never open a PR without immediately enabling auto-merge — the gap is exactly where PRs go to die.

```bash
gh pr create --title "feat(auth): JWT middleware" --body "..." --base develop && \
gh pr merge --auto --squash
```

### F8 — Parallel PR conflict scan (pre-merge)

**Symptom:** N commis have opened N parallel PRs against the same base. One merges cleanly; N-1 get blocked on conflict the moment it lands.

**Why this happens:** The chef's PERT + Fiedler partition is supposed to prevent overlapping write-sets across commis. But (a) a commis may have touched a file outside its cluster due to an unexpected refactor, (b) auto-merge from the previous sprint may have stale branches, (c) the Fiedler partition may be absent on small projects. GitHub won't tell you about the conflict until the first merge lands — by then you are stuck.

**Detection — run before enabling auto-merge on a batch:**

```bash
# List all open PRs against the same base
BASE=develop  # or main, per branching model
PRS=$(gh pr list --repo ${REPO} --base ${BASE} --state open \
  --json number,headRefName --jq '.[] | "\(.number) \(.headRefName)"')

# Build a map PR -> changed files
declare -A PR_FILES
while read -r NUM BRANCH; do
  FILES=$(gh pr view ${NUM} --repo ${REPO} --json files --jq '.files[].path' | sort -u | tr '\n' ' ')
  PR_FILES[${NUM}]="${FILES}"
done <<< "${PRS}"

# Compute pairwise intersections — any non-empty intersection is a future conflict
PRS_ARR=("${!PR_FILES[@]}")
for ((i=0; i<${#PRS_ARR[@]}; i++)); do
  for ((j=i+1; j<${#PRS_ARR[@]}; j++)); do
    A=${PRS_ARR[$i]}
    B=${PRS_ARR[$j]}
    OVERLAP=$(comm -12 \
      <(printf '%s\n' ${PR_FILES[$A]} | sort -u) \
      <(printf '%s\n' ${PR_FILES[$B]} | sort -u))
    if [[ -n "${OVERLAP}" ]]; then
      echo "CONFLICT: PR #${A} ↔ PR #${B} overlap on:"
      echo "${OVERLAP}" | sed 's/^/  /'
    fi
  done
done
```

**Partition-aware severity (when `.claude/tangle-partition.json` exists):**

A blind overlap is not all equally bad. Read the partition exported by `cli-audit-tangle` (same file the chef used to assign commis) and classify each overlap:

```bash
PART=.claude/tangle-partition.json
# A file that is a declared boundary function is an EXPECTED fan-in:
# the PERT already sequenced the plats that bridge it — lower severity.
BOUNDARY=$(jq -r '.boundary_functions[]?' "${PART}" 2>/dev/null | sort -u)
```

- **Overlap on a boundary file** → *expected*. The two plats were always going to meet here; the PERT sequenced them. Sequence per the PERT and move on.
- **Overlap on a non-boundary file between PRs assigned to different clusters** → **cross-cluster leak**: a commis escaped its assigned cluster (an unplanned refactor). This is the high-severity case — report it back to the chef as a file-exclusion breach, not just a routine rebase. It will recur next sprint unless the cluster assignment or the commis scope is fixed.
- **No partition present** (small project) → fall back to treating every overlap as a plain future conflict.

**Exit actions, in order of preference:**

1. **Sequence the two conflicting PRs** — pick one (lowest slack in the PERT, cf. cli-forge-chef pert-computation.md §4) and **disable auto-merge on the other** until the first lands, then rebase the loser:
   ```bash
   gh pr merge ${LOSER_PR} --disable-auto --repo ${REPO}
   # After the winner lands:
   gh pr checkout ${LOSER_PR} && git rebase origin/${BASE} && git push --force-with-lease
   gh pr merge ${LOSER_PR} --auto --squash
   ```
2. **Split the conflicting file out of one of the PRs** — if the overlap is a single file that one commis touched incidentally, the cleanest fix is to revert that file on one branch.
3. **Merge the two PRs into one** — only if the commits are small enough that a combined review is realistic.

**Running this scan proactively:**

- **Multi-agent sprints (cli-forge-chef):** the Sous-Chef runs the scan after every new PR is opened, before calling `gh pr merge --auto`. This is the structural defence — it catches any leak from the chef's file-exclusion.
- **Repo audit mode:** include the scan in Phase 1 Dimension D3 check when there are ≥ 2 open PRs against the same base. Report each pair under `D3 — PR lifecycle`.

### F9 — Post-merge landing watchdog (the "fork in the client" loop)

**Symptom:** PRs have auto-merge enabled but never actually land. `gh pr list` shows several open PRs, each with `autoMergeRequest: true`. The operator assumed "auto-merge enabled" meant "done" and walked away.

**Root cause:** Auto-merge is necessary but not sufficient. It waits for `CLEAN` + required checks; it does NOT rebase `BEHIND` branches when main moves, it does NOT rerun transient failures, it does NOT verify the release tag was cut. Every time release-plz or another PR lands, the remaining PRs drift into `BEHIND`, and auto-merge quietly gives up.

**Fix — the polling loop:**

```bash
#!/usr/bin/env bash
# F9 — Post-merge landing watchdog.
# Run this loop for as long as there is at least one in-flight PR.

set -euo pipefail
REPO=${REPO:-$(gh repo view --json nameWithOwner --jq .nameWithOwner)}
BASE=${BASE:-$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)}
POLICY=$(gh api repos/${REPO} --jq '
  if .allow_squash_merge then "squash"
  elif .allow_rebase_merge then "rebase"
  else "merge" end')

declare -A RELAUNCHES   # transient retries per run_id
declare -A FIRST_SEEN   # first-seen timestamp per PR

while true; do
  IN_FLIGHT=$(gh pr list --repo ${REPO} --base ${BASE} --state open \
    --json number,headRefName,mergeStateStatus,autoMergeRequest,updatedAt \
    --jq '.[] | select(.autoMergeRequest != null) | "\(.number)\t\(.headRefName)\t\(.mergeStateStatus)"')

  [[ -z "${IN_FLIGHT}" ]] && { echo "No in-flight PRs, watchdog exiting"; break; }

  while IFS=$'\t' read -r PR BRANCH STATE; do
    FIRST_SEEN[$PR]=${FIRST_SEEN[$PR]:-$(date +%s)}
    AGE=$(( $(date +%s) - ${FIRST_SEEN[$PR]} ))

    # Timeout: 2 hours stuck = escalate
    if (( AGE > 7200 )); then
      echo "ESCALADE: PR #${PR} stuck ${AGE}s"
      continue
    fi

    case "${STATE}" in
      MERGED)
        # Service 5 (Encaissement) — handled out-of-loop below
        ;;
      CLEAN|HAS_HOOKS|UNSTABLE)
        : # wait, auto-merge will fire
        ;;
      BEHIND)
        echo "Rattrapage: PR #${PR}"
        git fetch origin >/dev/null 2>&1
        git checkout ${BRANCH} 2>/dev/null || git checkout -b ${BRANCH} origin/${BRANCH}
        if git rebase origin/${BASE} 2>/dev/null; then
          git push --force-with-lease origin ${BRANCH}
          gh pr merge ${PR} --repo ${REPO} --auto --${POLICY} || true
        else
          git rebase --abort
          echo "Renvoi: PR #${PR} has rebase conflicts — manual resolution needed"
          gh pr merge ${PR} --repo ${REPO} --disable-auto
        fi
        ;;
      BLOCKED)
        # Look for transient failures
        FAILED=$(gh pr view ${PR} --repo ${REPO} --json statusCheckRollup \
          --jq '.statusCheckRollup[] | select(.conclusion == "FAILURE") | .detailsUrl' \
          | grep -oE 'runs/[0-9]+' | cut -d/ -f2 | sort -u)
        for RUN in ${FAILED}; do
          if gh run view ${RUN} --repo ${REPO} --log 2>/dev/null \
              | grep -qE 'rate limit|timeout|OOM|connection refused|stepsecurity'; then
            RELAUNCHES[$RUN]=$(( ${RELAUNCHES[$RUN]:-0} + 1 ))
            if (( ${RELAUNCHES[$RUN]} <= 2 )); then
              echo "Relance ${RELAUNCHES[$RUN]}/2: run ${RUN}"
              gh run rerun ${RUN} --repo ${REPO} --failed
            else
              echo "ESCALADE: run ${RUN} transient failed 3 times in a row"
            fi
          else
            echo "Renvoi: PR #${PR} real failure on run ${RUN}"
            gh pr merge ${PR} --repo ${REPO} --disable-auto
          fi
        done
        ;;
      DIRTY)
        # Merge conflict — try rebase, else disable auto-merge
        git fetch origin >/dev/null 2>&1
        git checkout ${BRANCH} 2>/dev/null || git checkout -b ${BRANCH} origin/${BRANCH}
        if git rebase origin/${BASE} 2>/dev/null; then
          git push --force-with-lease origin ${BRANCH}
          gh pr merge ${PR} --repo ${REPO} --auto --${POLICY}
        else
          git rebase --abort
          echo "Renvoi: PR #${PR} DIRTY, rebase conflicts — manual resolution"
          gh pr merge ${PR} --repo ${REPO} --disable-auto
        fi
        ;;
    esac
  done <<< "${IN_FLIGHT}"

  # Handle newly-merged PRs — cascade rattrapage on the rest
  JUST_MERGED=$(gh pr list --repo ${REPO} --base ${BASE} --state merged --limit 5 \
    --json number,mergedAt --jq '.[] | select(.mergedAt > "'$(date -u -d '@'$(( $(date +%s) - 60 )) +%FT%TZ)'") | .number')
  if [[ -n "${JUST_MERGED}" ]]; then
    echo "Cascade rattrapage after: ${JUST_MERGED}"
    # The outer loop picks them up on the next iteration (BEHIND will appear)
  fi

  sleep 45
done
```

**Exit conditions:**
- In-flight list is empty → the loop exits cleanly. All plats are served.
- Any PR escalated (timeout > 2 h, or 3 transient reruns on the same run) → the loop reports it and continues with the rest; the operator handles the escalade manually.

**Where to run it:**
- **Brigade mode:** the Maître d'hôtel runs a smarter version of this as its whole purpose (see `cli-forge-chef references/maitre-dhotel.md`). Do not run F9 separately in a brigade session — the two would race.
- **Single-agent mode:** the agent runs F9 in a background bash (`run_in_background: true`) immediately after opening a batch of parallel PRs. The agent can keep working on the next task; F9 reports back when the batch is done.
- **Repo audit mode:** F9 is the fix for any open PR in D3 with `autoMergeRequest: true` but not `CLEAN`.

## Anti-patterns

| # | Anti-pattern | Problem | Fix |
|---|---|---|---|
| G1 | **Individual checks in rulesets** | Path pruning skips them → eternal pending | Use a summary job as the single required check |
| G2 | **No auto-delete branches** | Orphans accumulate after every PR merge | Enable `delete_branch_on_merge` |
| G3 | **Force-merge to unblock** | Skips the broken check instead of fixing the root cause | Find why the check is missing |
| G4 | **Manual sync-main** | Conflict-prone, error-prone, forgotten | Automate with a workflow triggered on tag push |
| G5 | **Unpinned actions** | `actions/checkout@v4` could change behavior | Pin to SHA: `actions/checkout@<sha>` |
| G6 | **workflow scope left active** | Security risk — any `gh` call can modify CI | `gh auth refresh` immediately after push |
| G7 | **Stale release-plz PRs** | Conflict with develop, never auto-resolve | Close and let release-plz recreate |
| G8 | **No CI comment in rulesets** | Next dev re-adds individual checks to the ruleset | Comment in ci.yml explaining the design |
| G9 | **PR opened without auto-merge** | Somebody has to babysit it — exactly what this skill eliminates | Chain `gh pr create` with `gh pr merge --auto`, always. F7 fix |
| G10 | **No pre-merge conflict scan on parallel PRs** | First PR lands, N-1 others freeze on conflict | Run F8 before every batch auto-merge. Sequence or rebase the losers |
| G11 | **Walking away after `gh pr merge --auto`** | PRs stall on BEHIND/BLOCKED forever. Operator returns hours later to manual rebasing | Run F9 (post-merge landing watchdog). In a brigade, spawn the Maître d'hôtel. "Auto-merge enabled" is not "merged" |

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| CI YAML has optimization opportunities | `/cli-forge-pipeline` | Pipeline optimization (parallelism, caching, pruning) |
| Deprecated GitHub Actions detected | `/cli-audit-sync` | Check if README/docs reference the old action versions |
| Branch structure suggests architecture issues | `/cli-audit-tangle` | Module coupling analysis |
| Release flow involves shell scripts | `/cli-audit-shell` | Audit the release scripts |
| CONTRIBUTING.md references old branch protection | `/cli-audit-sync` | Doc-code coherence check |
| Stale PR waits on a silent human reviewer | `/cli-forge-plume` | Reviewer nudge message: relance ladder, calibrated humor |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relationship |
|---|---|
| `/cli-forge-pipeline` | Optimizes the CI YAML. cli-forge-github audits the **GitHub layer above** (rulesets, checks, PRs) |
| `/cli-git-conventional` | Handles commits/tags/branches. cli-forge-github handles the **repo config and PR lifecycle** |
| `/cli-audit-sync` | Checks doc-code coherence. cli-forge-github checks **GitHub config-code coherence** (rulesets match CI) |
| `/cli-cycle` | Should call cli-forge-github as part of the full project review |
| `/cli-forge-chef` | Multi-agent sprints create many branches/PRs. cli-forge-github cleans up after |

## What this skill does NOT do

- **Does not modify CI YAML** (that's `/cli-forge-pipeline`)
- **Does not write commit messages** (that's `/cli-git-conventional`)
- **Does not manage GitHub Issues** (out of scope — PRs only)
- **Does not configure GitHub Actions secrets** (security boundary)
- **Does not force-push main or develop** (ever)
