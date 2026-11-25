---
name: web-terminal-git-worktree
description: Creates and registers an isolated git worktree for Web Terminal agent sessions. Use when developing in Web Terminal (WEB_TERMINAL_WINDOW_ID set), when the user requires git worktree isolation, or before running claude/codex/cursor/acpx in a managed terminal.
---

# Web Terminal Git Worktree

Web Terminal only tracks Git state for **agent-created linked worktrees**. Follow this skill in every agent session inside a Web Terminal shell.

## Prerequisites

- `WEB_TERMINAL_WINDOW_ID` is set (Web Terminal managed shell).
- Current directory is inside a **git repository** (main checkout to start, or an existing linked worktree to re-register). The scripts work from subdirectories.
- Run the bundled shell scripts by path from this skill directory, but keep the command `cwd` inside the target git repository.

## Workflow

Copy and track progress:

```text
- [ ] Step 1: init-worktree (create + print worktree path + register)
- [ ] Step 2: do all edits and git operations inside the worktree
- [ ] Step 3: git commit in the worktree when done
- [ ] Step 4: run migration conflict gate if migrations changed
- [ ] Step 5: merge the agent branch back into main (required)
- [ ] Step 6: confirm automatic cleanup or explicitly keep the worktree
```

### Step 1: Create Worktree (Required)

From anywhere inside the **main repository checkout** or a linked worktree, run the setup script from this skill directory:

```bash
SKILL_DIR="/path/to/web-terminal-git-worktree"
bash "$SKILL_DIR/scripts/setup-git-worktree.sh"
```

`init-worktree.sh` remains as a compatibility wrapper.

```bash
SKILL_DIR="/path/to/web-terminal-git-worktree"
bash "$SKILL_DIR/scripts/setup-git-worktree.sh" my-feature --frontend
```

Optional branch suffix:

```bash
SKILL_DIR="/path/to/web-terminal-git-worktree"
bash "$SKILL_DIR/scripts/setup-git-worktree.sh" my-feature
# branch: agent/my-feature
```

This setup script:

1. Creates `.web-terminal-acp/worktrees/$WEB_TERMINAL_WINDOW_ID` with branch `agent/<suffix>`.
2. Enters the worktree inside the script process.
3. Registers the worktree with Web Terminal (OSC marker).
4. Copies `backend/.venv` and `frontend/node_modules` from the main checkout into the worktree by default.
5. Prints `Next command cwd: <worktree-root>`.

Dependency setup flags:

- `--frontend`: only copy `frontend/node_modules`.
- `--backend`: only copy `backend/.venv`.
- Default: copy both.

`cp -a` is used instead of linking because those dependency directories are writable. Sharing them across worktrees would leak installs and file edits into other sessions.

Important: a shell script cannot change the parent agent-client process directory. After `setup-git-worktree.sh` finishes, make every future tool call use the printed worktree path as its working directory, or run:

```bash
cd "$(git rev-parse --show-toplevel)/.web-terminal-acp/worktrees/$WEB_TERMINAL_WINDOW_ID"
```

**Do not** develop in the main checkout. **Do not** ask the user to run `git worktree add` manually.

### Step 2: Already In A Worktree?

If you are already anywhere inside a linked worktree but Git UI is missing, register only:

```bash
SKILL_DIR="/path/to/web-terminal-git-worktree"
bash "$SKILL_DIR/scripts/register-worktree.sh"
```

### Step 3: Develop And Commit

- All file edits and `git add` / `git commit` happen **inside the worktree**.
- Web Terminal does not commit for you. Uncommitted changes show a red **G** on the terminal title until you commit.

### Step 4: Migration Conflict Gate

If the task adds or edits migration files, run this gate before landing:

1. From the agent worktree, merge current `main`:

```bash
git merge main
```

2. Check migration filenames, Alembic `revision`, and `down_revision` values. If another branch already used the same version number or revision, rename your migration to the next unique version, update its `revision` and `down_revision`, and confirm the migration graph has one head.
3. Run the repository's SQLite Alembic migration test. For Web Terminal ACP:

```bash
cd backend
uv run pytest tests/unit/test_models_schema_constraints.py::test_alembic_revision_graph_has_unique_single_head -q
tmp_db="$(mktemp -u /tmp/web-terminal-alembic-XXXXXX.db)"
DATABASE_URL="sqlite+aiosqlite:///$tmp_db" uv run alembic upgrade head
rm -f "$tmp_db"
```

4. If you changed a migration version, revision, or conflict resolution after this check, merge `main` again and repeat the migration conflict gate before running the final merge CLI.

### Step 5: Merge Back Into `main` (Required)

Worktree branches (`agent/<suffix>`) are **integration branches**, not the final destination. When the task is done (or the user asks to land the work), run the merge-agent CLI from the **linked agent worktree**:

```bash
python3 "$SKILL_DIR/scripts/merge-agent-branch.py"
```

- The CLI serializes landing with a repo-wide file lock, merges current `main` into the agent worktree, and updates `main` with `git merge --ff-only`.
- Before fast-forwarding `main`, the CLI checks files changed by the agent branch after merging current `main`. If any `frontend/` file changed, it must run `cd frontend && npm run test`. If any `backend/` file changed, it must run `cd backend && uv run pytest tests -n 8 -q`. A failing required suite blocks the merge.
- After a successful fast-forward, the CLI removes the landed managed worktree by default with plain `git worktree remove`, then deletes the landed branch with `git branch -d`.
- Automatic cleanup is limited to linked `agent/*` worktrees under `.web-terminal-acp/worktrees/`. Cleanup failures are reported but do not roll back a successful merge.
- Use `--keep-worktree` for debugging or review, or `--keep-branch` to remove the worktree while preserving the landed branch.
- If conflicts occur, resolve them in the agent worktree, commit the resolution, rerun focused tests, rerun the migration conflict gate if migrations changed, and rerun the CLI. Do not leave conflicts in the main checkout.
- **Do not** leave completed work only on `agent/*` -- production and other agents expect `main` to contain landed changes.
- After merge, `main` should include version bumps and any `.gitignore` updates from the worktree branch.

### Step 6: Confirm Cleanup

Default merge cleanup usually removes the agent worktree. If your shell remains inside a removed worktree, `cd` to the main checkout before continuing:

```bash
cd /path/to/main-checkout
```

If you used `--keep-worktree` or need to manually clean a leftover worktree later, run from the **main checkout**:

```bash
SKILL_DIR="/path/to/web-terminal-git-worktree"
bash "$SKILL_DIR/scripts/remove-worktree.sh"
```

The remove script also works from inside the linked worktree.

## Rules

| Rule | Detail |
|------|--------|
| One terminal, one worktree | Use the path under `.web-terminal-acp/worktrees/$WEB_TERMINAL_WINDOW_ID` |
| Use the printed worktree path | `init-worktree.sh` cannot change the parent agent-client cwd; set future tool calls to `Next command cwd` |
| Register after entering worktree | `init-worktree.sh` registers automatically; never skip registration |
| No main-checkout edits | `git rev-parse --show-toplevel` with a `.git` directory = main checkout -- do not develop feature code here; only merge and cleanup |
| Merge to `main` when done | Land `agent/<suffix>` on `main` before considering the task complete |
| Full tests before merge | `merge-agent-branch.py` runs the full frontend test suite for `frontend/` changes and the full backend pytest suite for `backend/` changes before fast-forwarding `main` |
| Migration gate before landing | After merging `main`, changed migrations must have unique versions/revisions and pass SQLite Alembic upgrade; after changing migration versions, merge `main` again and repeat the gate |
| Cleanup is default | `merge-agent-branch.py` removes landed managed `agent/*` worktrees unless `--keep-worktree` is used |
| Read-only platform git | Web Terminal only snapshots; it never runs commit/checkout for you |

## Scripts

| Script | Purpose |
|--------|---------|
| [scripts/setup-git-worktree.sh](scripts/setup-git-worktree.sh) | Create worktree, register it, and seed backend/frontend dependencies |
| [scripts/init-worktree.sh](scripts/init-worktree.sh) | Create worktree, enter it in the script process, print path, register |
| [scripts/merge-agent-branch.py](scripts/merge-agent-branch.py) | Serialize landing an agent branch back into main, then clean up |
| [scripts/register-worktree.sh](scripts/register-worktree.sh) | Register current linked worktree from any subdirectory |
| [scripts/remove-worktree.sh](scripts/remove-worktree.sh) | Remove this terminal's worktree from main or worktree subdirectories |

Make scripts executable once per install:

```bash
chmod +x "$SKILL_DIR"/scripts/*
```

## Claude EnterWorktree

If using Claude's built-in EnterWorktree instead of `init-worktree.sh`, you **must** still `cd` into the linked worktree and run `register-worktree.sh` so Web Terminal can bind the session.
