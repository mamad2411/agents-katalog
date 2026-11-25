---
name: easy-ssh
description: >
  Use the easy-ssh CLI to run computations on a remote server using local project files.
  Trigger when the user asks to run code remotely, execute on a server, submit a job,
  sync files to a remote machine, pull results from a server, check remote job status,
  or mentions "easy-ssh", "remote run", "server-side", "GPU server", or "cluster".
  Also trigger when the user has a local project and wants to execute it somewhere
  with more compute (GPU, RAM, CPU cores).
---

# easy-ssh — Remote Execution Skill

Run local project code on a remote server via SSH. No agent or daemon needed on the server — just SSH access and rsync.

## When to use

- User wants to run a command on a remote server using local files
- User mentions "run this on the server", "submit a job", "GPU", "cluster", "remote"
- User wants to sync code, pull results, or check job status
- Project already has `.easy-ssh.conf` (check with `ls .easy-ssh.conf`)

## Prerequisites

- `easy-ssh` CLI must be on PATH (check: `which easy-ssh`)
- SSH key-based auth configured in `~/.ssh/config` for the target host
- `rsync` available locally and on the server

## Workflow

### Step 0 — Detect setup state

```bash
ls .easy-ssh.conf 2>/dev/null
```

- **File exists**: read it to learn `host` and `remote_dir`, then skip to the relevant command.
- **File missing**: the project hasn't been initialized yet. Ask the user for:
  1. SSH host (as configured in `~/.ssh/config`)
  2. Remote directory path (e.g., `~/projects/mypackage`)

  Then run `easy-ssh init` interactively, or create `.easy-ssh.conf` directly:

  ```bash
  cat > .easy-ssh.conf <<'EOF'
  host='<user-provided-host>'
  remote_dir='<user-provided-path>'
  EOF
  ```

### Step 1 — Determine the right command

| User intent | Command |
|---|---|
| Sync files only | `easy-ssh push` |
| Run and wait for output | `easy-ssh run "<cmd>"` |
| Launch long job, return immediately | `easy-ssh submit "<cmd>"` |
| Check running job output | `easy-ssh logs` |
| Live-stream job output | `easy-ssh monitor` |
| Check if job finished | `easy-ssh status` |
| Fetch result files locally | `easy-ssh pull <relative-path>` |
| Remove stale remote files | `easy-ssh clean --force` |
| Preview what clean would delete | `easy-ssh clean` |

### Step 2 — Execute

#### Sync + run (short tasks, < ~5 min)

```bash
easy-ssh run "<command>"
```

Pushes local files, runs the command, waits, returns stdout/stderr and exit code.
Use for quick scripts, compilation, tests, data generation.

#### Sync + submit (long tasks)

```bash
easy-ssh submit "<command>"
```

Pushes local files, launches the command via nohup, returns immediately.
Use for training runs, batch processing, anything > 5 min.

After submitting, monitor with:

```bash
easy-ssh monitor  # live-stream output, auto-stops when job ends (Ctrl+C to detach)
easy-ssh status   # job state: running/finished + exit code
easy-ssh logs     # last 50 lines of output (configurable via EASY_SSH_LOG_LINES)
```

#### Pull results back

```bash
easy-ssh pull <path>
```

`<path>` is relative to the remote project directory. Examples:

```bash
easy-ssh pull results/model.pkl
easy-ssh pull output/                  # whole directory
easy-ssh pull checkpoints/epoch_10.pt
```

**Constraints**: path must be relative, no `../` allowed.

### Step 3 — Report to user

- For `run`: show the command output and exit code.
- For `submit`: confirm job launched, remind user to check `easy-ssh status` / `easy-ssh logs`.
- For `pull`: confirm files fetched, show local path.
- On failure: show the error message. Common issues:
  - `ssh connection failed` → check host in `~/.ssh/config`, key auth
  - `directory is XXXmb` → add patterns to `.easy-ssh-ignore` or use `--force`
  - `job already running` → wait for it or kill via `easy-ssh run "kill <pid>"`

## File exclusions

`easy-ssh` already skips `.git` and `.venv` automatically.

If the project has other large local-only files that shouldn't sync (datasets, build artifacts, caches), create `.easy-ssh-ignore` with gitignore-style patterns:

```
__pycache__/
*.pyc
data/
node_modules/
```

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `EASY_SSH_SIZE_WARN_KB` | 512000 | Warn if effective sync size exceeds this (KB) |
| `EASY_SSH_CONNECT_TIMEOUT` | 5 | SSH timeout (seconds) |
| `EASY_SSH_LOG_LINES` | 50 | Lines shown by `logs` |

## Common patterns

### Edit locally → run remotely → pull results

```bash
# 1. User edits code locally (you help with this)
# 2. Run on server
easy-ssh run "python train.py --epochs 10"
# 3. Pull output
easy-ssh pull results/metrics.json
```

### Long training with checkpoints

```bash
easy-ssh submit "python train.py --epochs 100 --save-every 10"
# ... later ...
easy-ssh logs                          # check progress
easy-ssh status                        # check if done
easy-ssh pull checkpoints/             # grab all checkpoints
```

### Julia project

```bash
easy-ssh run "julia --project=. -e 'using Pkg; Pkg.instantiate()'"
easy-ssh run "julia --project=. src/main.jl"
easy-ssh pull output/
```

### Clean remote state

```bash
easy-ssh clean           # dry-run: shows what would be deleted
easy-ssh clean --force   # actually delete remote-only files
```
