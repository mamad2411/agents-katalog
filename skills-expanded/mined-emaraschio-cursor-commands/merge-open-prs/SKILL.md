---
name: merge-open-prs
description: >-
  Review, verify (Docker by default), and auto-merge open PRs when CI, reviews,
  and local verification pass. Batch up to 10 PRs per run. Use when the user
  wants to merge all open PRs, clear the PR queue, or run /merge-open-prs.
disable-model-invocation: true
user-invocable: false
---
# Merge open PRs

Orchestrate a **batch** of open pull requests in the **current repo**: babysit each PR, code-review, verify locally (Docker-first), auto-merge when green, then post-batch smoke on the default branch.

**Do not** duplicate the babysit contract inline. Read and follow the **babysit** skill at `~/.cursor/skills-cursor/babysit/SKILL.md` for every PR in the batch.

**Entry point:** `.cursor/commands/merge-open-prs.md` (slash `/merge-open-prs`). When this file disagrees with the command file, **this file wins**.

---

## Defaults

Apply these when the user does not override:

| Setting | Default | Override |
|---------|---------|----------|
| Verification | **Docker-first** | `--no-docker` |
| Batch size | **10 PRs** | `--limit N` |
| Autonomy | **auto_if_green** (merge when gate passes) | `--dry-run` (no merge) |
| Single PR | Process only that number | `42` or `#42` argument |

Parse flags from the user message: `--dry-run`, `--no-docker`, `--limit N`. A bare number selects one PR.

---

## When NOT to use

- **Single PR babysit only** (no batch, no queue) → use babysit on that PR directly
- **Cross-repo initiative status** → use cross-repo-status or manual `gh` sweep per user rules
- **PRs needing product/legal sign-off** → skip; report in summary
- **Sensitive security changes** without explicit user approval → hard stop
- Repo has **no Docker** and user did not pass `--no-docker` → blocker at preflight (do not silently fall back)

---

## Phase 0: Preflight

1. `gh auth status`: blocker if not authenticated
2. Confirm git repo root: `git remote get-url origin`
3. `git fetch --all --prune`
4. If working tree dirty → warn; do not stash without asking
5. **Docker (default path):** `docker info`. If it fails and user did **not** pass `--no-docker`, **stop** with a blocker (suggest `--no-docker` only when they accept non-Docker verification)
6. Resolve profile path: `profiles/<repo-basename>.yaml` relative to this skill directory (`basename` from `git remote get-url origin`, strip `.git`, last path segment). See `profiles/README.md`.

---

## Phase 1: Inventory

```bash
gh pr list --state open --limit <LIMIT> --json number,title,isDraft,mergeable,reviewDecision,statusCheckRollup,headRefName,author,labels,createdAt,updatedAt
```

- `<LIMIT>` = user `--limit` or **10** default. Fetch at least that many; if more open PRs exist, note **deferred** count in the plan table.
- **Skip** (do not process): `isDraft`, labels in profile `skip_labels` or default `do-not-merge`, `wip`
- **Order:** `createdAt` ascending (FIFO). If user passed a PR number, only that PR (still full verify + gate)
- Emit a **plan table** before acting:

  | # | Title | In batch? | Skip reason |
  |---|-------|-----------|-------------|

---

## Phase 2: Per-PR loop

For each PR in batch (in order):

### 2a: Babysit

Read and execute `~/.cursor/skills-cursor/babysit/SKILL.md`:

- Resolve merge conflicts (abort if intent conflicts; ask user)
- Triage unresolved comments (filter resolved threads; validate Bugbot)
- Fix CI failures **in PR scope** only; never weaken workflows

Checkout the PR branch: `gh pr checkout <n>`.

### 2b: Code review

Apply the checklist in `~/.cursor/skill-contracts/code-review/SKILL.md` (or slash `/code-review`). Surface blockers in chat. Hard stops (entire batch):

- `.env`, credentials, API keys in diff
- DB migration without rollback note in PR description
- Breaking change (`feat!`, `BREAKING`) without explicit user approval in this session

### 2c: Local verification

#### Docker-first (default; unless `--no-docker`)

1. If profile exists → run `verify.steps` in order (each step is a shell command)
2. Else if `docker-compose.yml`, `compose.yaml`, or `compose.yml` exists:
   - `docker compose build`
   - Run tests via profile-less heuristic: read repo `README` / `Makefile` for the canonical test service; prefer `docker compose run --rm <service> <test-cmd>` over inventing commands
3. Else → **skip PR** with reason `no-docker-profile-or-compose`; do not auto-merge

**Never** run `docker compose down -v` unless the user explicitly requests volume teardown.

#### Host-only (`--no-docker`)

1. Profile `verify.mode: host` steps if present
2. Else heuristics: `make test`, `bin/test`, `npm test`, `pnpm test`, `bundle exec rspec` (first that exists)
3. If nothing found → **skip PR** with reason `no-verify-path`

Record pass/fail output in the session summary.

### 2d: Re-fetch GitHub state

```bash
gh pr view <n> --json mergeable,mergeStateStatus,reviewDecision,isDraft
gh pr checks <n>
```

Unresolved review threads: use `gh api` GraphQL or review threads; follow babysit (human threads block; bots per babysit judgment).

---

## Phase 3: auto_if_green gate

Merge **only if all** are true:

| Check | Requirement |
|-------|-------------|
| Mergeable | `mergeable` == `MERGEABLE` / `mergeStateStatus` not blocked |
| Reviews | `reviewDecision` ≠ `CHANGES_REQUESTED` |
| CI | All **required** checks `SUCCESS` (`gh pr checks`) |
| Threads | No unresolved **human** review threads |
| Local verify | Passed in 2c |
| Draft | `isDraft` == false |

- **Pass** → Phase 4a to 4b (unless `--dry-run`)
- **Fail** → log reason, **continue** to next PR (do not stop batch unless auth/rate-limit/hard-stop)

**Do not approve before the gate passes.** Approval is a pre-merge step, not a substitute for local verify or CI.

### `--dry-run`

Evaluate gate and report **would approve** / **would merge** / **would skip**; **never** call `gh pr merge` or `gh pr review --approve`.

---

## Phase 4a: Approve (always before merge)

After gate passes (and not in `--dry-run`):

1. `gh pr view <n> --json reviewDecision,author`: confirm the authenticated `gh` user can act as reviewer on this repo
2. If you have not already left an **APPROVE** review on this PR in this session:
   - `gh pr review <n> --approve` with an optional one-line body summarizing verify + CI status
3. Re-fetch `reviewDecision`. If still blocked (e.g. requires another reviewer), **skip merge** with reason `approval-insufficient`; continue queue
4. Log approval in the per-PR summary before proceeding

**Never** approve when gate failed, local verify failed, or hard-stop conditions apply.

---

## Phase 4b: Merge (only after 4a)

Merge **only after** Phase 4a succeeded (approve recorded or already approved by you):

```bash
# squash example
gh pr merge <n> --squash --delete-branch
```

Use profile `merge` (`squash` | `merge` | `rebase`) or repo default.

**Never:**

- `gh pr merge --admin`
- `--no-verify` on git operations
- Force-push to default branch
- Merge with failing required checks

---

## Phase 5: Post-batch smoke

After all PRs processed:

1. `git checkout <default_branch>`: from profile or `gh repo view --json defaultBranchRef`
2. `git pull`
3. Run `post_merge_smoke` from profile, or repeat a **lighter** Docker smoke (e.g. same as verify step 1 only) when Docker-default
4. **Summary table:** merged | skipped (reason) | failed | deferred (beyond limit) | smoke pass/fail

---

## Profiles

Optional YAML at `profiles/<repo-basename>.yaml`. Copy from `profiles/_template.yaml`. Profile overrides detection heuristics.

---

## Behavioral evaluation

Before changing this contract materially, walk `eval/cases.md` sections **A, D, E** (minimum). Target: 0 FAIL, ≥90% adjusted pass rate. See `eval/README.md`.

---

## Lessons (maintainers)

- **Docker default** matches repos with a merge profile; `--no-docker` is explicit opt-out
- **Limit 10** prevents runaway merges; deferred PRs must appear in summary
- **Babysit is source of truth** for per-PR triage; do not fork its rules here

## Guardrails

- Merge only when the gate passes: require local verification, CI success, no CHANGES_REQUESTED, and resolved human threads before merging.
- Do not silently skip Docker; if `docker info` fails without `--no-docker`, stop with a blocker.
- Keep the batch bounded: process up to `--limit` (default 10) FIFO and report deferred PRs.
