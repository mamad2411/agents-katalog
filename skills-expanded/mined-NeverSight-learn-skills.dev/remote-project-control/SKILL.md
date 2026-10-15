---
name: remote-project-control
description: Coordinate local, Git remote, and SSH/HPC/RunAI research projects. Use for server state, sync safety, job submission, interactive sessions, logs, artifact lookup, context recovery, raw SSH commands, remote shell one-liners, SSH quoting issues, remote-cmd, remote-bash, or avoiding local shell expansion of remote variables.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Remote Project Control

## Before Acting — Mandatory

1. **Detect scope**: run `git rev-parse --git-common-dir` vs `--show-toplevel`. In a project-control-root layout, `<ProjectName>/` and `<ProjectName>/code/` are independent repos — inspect them separately.
2. **Read project memory** if `memory/BRIEFING.md` exists in the project root:
   - `memory/BRIEFING.md` — compact project state snapshot
   - `memory/project-conventions.md` — active conventions including SSH wrappers, server paths, and scope constraints for this project
3. **If inside a worktree**: read `.agent/worktree-status.md` first; write in-progress server state there, not into root `memory/`.
4. **Treat volatile state (queue, server load, job status) as requiring fresh verification** — do not act on cached session memory for these values.

Skipping this step risks using stale server state, wrong environment paths, or violating project-specific SSH wrapper conventions.

---

Help the user operate a project whose code is edited locally but actually runs on one or more servers over SSH. Establish project memory first, then coordinate safe local, Git remote, and server actions.

Terminology used by this skill:

- `local`: the user's local development machine, usually the Mac where the agent is running
- `remote` or `git remote`: the Git hosting remote such as GitHub or GitLab, e.g. `origin`
- `server`: an execution machine or cluster reached by SSH, such as `quest`, `ibex-vscode`, or `epfl-haas`

The skill name is historical. In project memory and user-facing summaries, prefer `server` for SSH/HPC/RunAI execution environments and reserve `remote` for Git remotes unless quoting an existing field name.

Pair this skill with `research-project-memory` when server execution state should be linked to project-level experiments, evidence, actions, or worktree status. Pair with `run-status-monitor` after job submission when lightweight progress checks or artifact-bounded monitoring are needed without pulling raw logs into context.

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
├── references/
│   ├── memory-model.md
│   ├── operations.md
│   └── ssh-command-wrappers.md
├── scripts/
│   ├── remote-cmd
│   └── remote-bash
├── template_manifest.json
└── templates/
    ├── infra/remote-projects.yaml
    ├── docs/ops/current-status.md
    ├── docs/ops/decision-log.md
    └── agent/local-overrides.yaml
```

## Progressive Loading

- Always read `references/memory-model.md`
- Read `references/operations.md` when the user wants to inspect, sync, run, monitor, or fetch artifacts
- Read `references/ssh-command-wrappers.md` before composing SSH commands that include loops, shell variables, command substitution, pipes, globs, `find`, `awk`, or multi-line logic
- Use `templates/` as the source of truth when bootstrapping memory files into the target project
- If the repo has `memory/`, summarize verified server execution facts into `research-project-memory` boards without duplicating the server manifest.

## Core Principles

- Memory is bootstrap context, not execution truth
- Stable shared facts belong in the repo; private machine-specific facts belong in a local override file
- Verify volatile state before acting on it
- Prefer GitHub/GitLab or the configured Git remote for local-to-server code sync; do not improvise ad hoc source copying unless the project explicitly uses it
- Never use destructive server-side git commands without explicit user approval
- Treat network access as a separate failure mode for `gh`, `git`, `ssh`, `curl`, and scheduler/API commands; DNS, timeout, or connection errors in a sandboxed agent runtime must be retried with network permission before diagnosing credentials or configuration
- Treat GitHub/GitLab API access as separate from normal `git` SSH access: `git push` may work while `gh repo create`, `gh repo view`, or `gh repo fork` fails because `gh` is not authenticated
- Treat GitHub/GitLab API network access as separate from authentication: in sandboxed agent runtimes, `gh` may fail to reach `api.github.com` unless the command is rerun with network permission
- Treat GitHub Projects as GitHub API operations, not Git remotes. `gh project ...` needs a token with the `project` scope; refresh it with `gh auth refresh -s project` before project-board commands when the scope is missing.
- In project-control-root layouts, inspect root and component repos separately; `<ProjectName>/` and `<ProjectName>/code/` may be independent Git repos with different remotes and permissions
- Use `remote-cmd` for simple argv-style server commands and `remote-bash` for scripts, loops, or anything with shell syntax. See **Forbidden SSH Patterns** below.

## Forbidden SSH Patterns

Never compose these directly in the transcript or agent command output:

| Anti-pattern | Use instead |
|---|---|
| `ssh <alias> "cd <path> && <cmd>"` | `remote-cmd <alias> <repo> -- <cmd>` |
| `ssh <alias> "<cmd> $VAR"` (shell variable) | `remote-cmd <alias> <repo> -- <args>` |
| `ssh <alias> "<cmd> \| <cmd>"` (pipe / loop / find / awk) | `remote-bash <alias> <repo> <script>` |
| `ssh <alias> "<cmd1> ; <cmd2>"` (chained) | `remote-bash <alias> <repo> <script>` |
| `ssh A "ssh B '<nested cmd>'"` (nested one-liner) | project-local `scripts/ops/` wrapper called via `remote-bash` |

**Exception**: single-word no-argument commands with no shell syntax are fine (`ssh <alias> "pwd"`, `ssh <alias> "hostname"`).

**Why**: local shell expands `$VAR`, `~`, globs, and quotes before the SSH command is sent, silently corrupting the intended server-side command. Wrappers quote correctly and keep the transcript clean.

## Memory Files

This skill manages four project-memory files with distinct roles:

- `infra/remote-projects.yaml`: stable shared facts such as local repo path, Git remote/branch, server repo mapping, scheduler type, launch modes, key paths, and safety policies
- `docs/ops/current-status.md`: working memory for the current phase of the project, including active branch, focus, latest known job, open issues, and next step
- `docs/ops/decision-log.md`: durable explanations for why stable workflow decisions were made
- `.agent/local-overrides.yaml`: optional private overrides for one user's machine, ssh aliases, usernames, and private paths; this file should usually be gitignored

If one or more files are missing, bootstrap them from the bundled templates before trying to infer project context from scratch.

## Step 1 — Orient and Load Memory

1. Detect the project root:

```bash
git rev-parse --show-toplevel 2>/dev/null || pwd
```

2. Read the existing memory files if present:

- `<project-root>/infra/remote-projects.yaml`
- `<project-root>/docs/ops/current-status.md`
- `<project-root>/.agent/local-overrides.yaml`
- `<project-root>/docs/ops/decision-log.md`

3. If `infra/remote-projects.yaml` is missing, bootstrap the project memory using the templates in this skill. Ask only for the minimum critical fields:

- project name
- local repo root
- default server name
- ssh alias
- server repo root
- scheduler type
- default launch mode
- environment activation command

4. If `.agent/local-overrides.yaml` is missing but private overrides are clearly needed, offer to create it and recommend adding `.agent/` to `.gitignore`.

5. If the project appears to be a control root with component repos, inspect each relevant repo independently instead of assuming one Git remote:

```bash
git -C <project-root> remote -v
git -C <project-root>/code remote -v
git -C <project-root>/paper remote -v
```

Missing remotes in one repo do not imply missing remotes in another.

## Step 2 — Build the Session Bootstrap Summary

Merge the loaded files into a concise project context summary. Always show the user a compact bootstrap summary before doing substantial remote work.

Include, when known:

- project name
- local repo root, current branch, short commit, and whether the tree is dirty
- default server and server repo root
- Git remote name and branch used for sync
- scheduler type and default launch mode
- environment activation command
- key data, checkpoint, scratch, and logs roots
- current focus
- latest known job
- open issues
- next planned step
- any missing required fields

## Step 3 — Re-validate Volatile State Before Action

Before any remote action, verify the pieces of state that could have changed since the last session.

At minimum:

```bash
git rev-parse --short HEAD
git branch --show-current
git status --short
```

For the chosen server, verify the server-side repo and git state using the configured `ssh_alias` and `remote_repo_root` or `server_repo_root`:

```bash
ssh <ssh-alias> "cd <remote-repo-root> && pwd && git branch --show-current && git rev-parse --short HEAD && git status --short"
```

For repeated checks, prefer the safer wrapper equivalent:

```bash
remote-cmd <ssh-alias> <remote-repo-root> -- git status --short
remote-bash <ssh-alias> <remote-repo-root> scripts/ops/status.sh
```

If the request involves job submission or monitoring, also verify the scheduler tool and relevant log or output paths on the server.

## Step 4 — Classify the Request and Execute

Choose one of the following flows and follow the detailed guidance in `references/operations.md`:

- `bootstrap`: create or repair the memory files from templates and fill the minimum required fields
- `inspect`: compare local and server git state, verify paths, env activation, scheduler availability, and summarize the current situation
- `git-remote-setup`: inspect or create GitHub/GitLab repositories, set remotes, fork upstream repos, link optional GitHub Projects, or prepare local-to-server sync through a Git remote
- `sync-code`: prepare local commits, push through the configured Git remote, and update the server repo with non-destructive fast-forward pulls only
- `run-job`: use the server context to submit a job safely; if a new reproducible job script is needed, use `run-experiment` after this skill has established the environment
- `interactive-session`: prepare the correct `salloc`, `srun`, or equivalent command and run subsequent commands from the server repo with the configured environment activation
- `monitor`: inspect queue state and tail logs from the configured log roots
- `artifacts`: locate remote checkpoints, outputs, and logs; do not bulk-transfer large data unless the user explicitly asks
- `closeout`: update project memory at the end of a session

If the runtime cannot execute SSH commands directly, still use this skill: generate the exact commands in the correct order, explain the assumptions, and keep the memory files up to date.

Before any `gh` operation that uses GitHub's API, including `gh repo ...` and `gh project ...`, run:

```bash
gh auth status
```

Interpret failures carefully:

- If the output says it cannot connect to `api.github.com`, `github.com`, or asks to check the internet connection, treat it as network/sandbox access first. Rerun the same `gh` check with network permission before asking the user to log in again.
- If `gh auth status` has network access and still reports an invalid token, missing account, or failed login, stop the GitHub API flow and tell the user to re-authenticate with `gh auth login -h github.com`.
- Do not interpret either failure as a repository creation failure, Git remote failure, SSH key failure, or server problem.

For GitHub Projects:

- Verify `gh auth status` shows the `project` scope before `gh project create`, `gh project view`, `gh project link`, `gh project item-*`, or `gh project field-*`.
- If the scope is missing, run or ask the user to run `gh auth refresh -s project`.
- If normal sandboxed `gh auth status` fails but a network/keyring-enabled check succeeds, treat the normal failure as sandbox or Keychain access, not a real logout.
- Record the GitHub Project URL/number in root `memory/project.yaml` when the code repo belongs to a project-control-root layout.

Apply the same network-first classification to other commands:

- `git fetch`, `git push`, `git pull`, `git ls-remote`: DNS or connection failure is network/sandbox access until rerun with network permission.
- `ssh <server>`: hostname resolution, timeout, or network unreachable is network/VPN/sandbox reachability until rerun with the expected network permission and VPN state.
- `curl`, package managers, and scheduler/API CLIs: connection failure is not enough to prove credentials or server configuration are wrong.

## Step 5 — Write Back to the Right Memory Layer

When new information becomes trustworthy, persist it to the appropriate file:

- stable mapping and policy changes -> `infra/remote-projects.yaml`
- current branch, latest known server job, current focus, blockers, and next step -> `docs/ops/current-status.md`
- durable workflow rationale -> `docs/ops/decision-log.md`
- user-specific ssh aliases, usernames, and private paths -> `.agent/local-overrides.yaml`

If the repo also uses `research-project-memory`, write only cross-project pointers:

- `memory/evidence-board.md`: verified job/run pointer for linked `EXP-###`
- `memory/action-board.md`: monitor, fetch-artifact, rerun, or report actions
- `memory/current-status.md`: latest verified server execution summary and next verification step
- worktree `.agent/worktree-status.md`: server run status when tied to a branch/worktree purpose

Do not write volatile scheduler output or one-off shell command results into the stable manifest.

## Step 6 — End Every Substantial Session with Closeout

Before finishing, update `docs/ops/current-status.md` whenever the session materially changed project state. Capture:

- branch or commit the user should resume from
- what was changed locally
- what was pushed to the Git remote and pulled into the server repo
- latest known submitted or running job
- log or output paths worth checking next
- the next concrete action for the next session

If a new stable practice was established, add a short entry to `docs/ops/decision-log.md`.

If a new project-specific SSH/remote convention was established (e.g., a new wrapper alias, a server path, a RunAI pool, a scheduler flag), write it to `memory/project-conventions.md` under the `ssh` or `compute` category. When server infrastructure changes make a convention obsolete, move it to Expired with the reason.

If the project has `memory/current-status.md`, update it with a concise cross-component pointer rather than copying the full remote status.

## Bootstrap Targets

When bootstrapping a project, materialize these files from `templates/`:

- `templates/infra/remote-projects.yaml` -> `<project-root>/infra/remote-projects.yaml`
- `templates/docs/ops/current-status.md` -> `<project-root>/docs/ops/current-status.md`
- `templates/docs/ops/decision-log.md` -> `<project-root>/docs/ops/decision-log.md`
- `templates/agent/local-overrides.yaml` -> `<project-root>/.agent/local-overrides.yaml` when private overrides are needed

Preserve existing files unless the user explicitly asks to overwrite them.
