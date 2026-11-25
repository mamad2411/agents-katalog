---
name: loom-dev-setup
description: Sets up an isolated Loom environment for one task — a worktree from origin/main, its own virtualenv, its own ClickHouse on free ports, migrations, a server from source. Use when starting a Loom change, or when asked to run the server or the integration tests locally.
argument-hint: "<branch-name>"
metadata:
  internal: true
---

# Loom dev setup

Everything a task touches is private to it: the branch, the checkout, the virtualenv, the ClickHouse and the server port. Shared state (the primary checkout's `main`, the git stash, a ClickHouse someone else started, a deployment's containers) is read, never written.

## 1. Worktree

In Claude Code, run `git fetch origin main` (the tool reuses a fetch up to a day old), then enter one with the `EnterWorktree` tool: it creates `.claude/worktrees/<name>` from `origin/main` and moves the session there, so the worktree's own `CLAUDE.md`, rules and settings load. Rename its branch (`git branch -m worktree-<name> <branch>`), run `pwd` (that is `<worktree>` below) and continue at §2. A path-scoped rule loads for files under the session's project directory, so a session that edits a sibling checkout from outside it works without the rules. Other agents create the worktree with git and start their session inside it:

```bash
BRANCH="$ARGUMENTS"          # Claude Code fills this in; elsewhere write the branch name, e.g. fix/search-floor
git fetch origin main
git worktree add --no-track -b "$BRANCH" "../loom-${BRANCH//\//-}" origin/main   # no upstream until the first push sets one
cd "../loom-${BRANCH//\//-}" && pwd   # the worktree's absolute path: <worktree> below
```

An agent's shell does not keep its working directory or variables between calls, so every block below starts with `cd <worktree> &&`, the absolute path printed here. Without it, `uv sync` rewrites the launch checkout's `.venv` and the server serves the launch checkout's code.

Branch from `origin/main`, not a local `main` or `FETCH_HEAD` (a concurrent fetch rewrites `FETCH_HEAD`). `main` and the stash are shared with every other worktree (`AGENTS.md`): set work aside with a WIP commit.

## 2. Virtualenv

```bash
cd <worktree> && uv sync --locked --python 3.12 --extra dev --extra code   # the lockfile CI installs: same ruff, mypy, pytest
.venv/bin/python -P -c 'import server; print(server.__file__)'   # must be inside this worktree
```

The make targets use `.venv/bin/python`. Run repository scripts as modules (`.venv/bin/python -m scripts.ops.dump_schema`): a script run by path can import `server` from another checkout.

## 3. A private ClickHouse

Pick free ports and a name that cannot be mistaken for a deployment's containers (`loom-blue`, `loom-green`, `loom-proxy`, `loom-server`, `loom-workers`, `loom-<colour>-workers`, `loom-ch`, `loom-extractor` are taken by convention):

```bash
cd <worktree> && LOOM_CH_CONTAINER="ch-$(basename "$PWD")" LOOM_CH_HOST_PORT=18123 LOOM_CH_NATIVE_HOST_PORT=19000 bash dev/ci_start_clickhouse.sh
docker ps --filter "name=^ch-$(basename "$PWD")$" --format '{{.Names}} {{.Ports}}'   # yours, on your ports
curl -s "http://loom:loomdev@localhost:18123/?query=SELECT+count()+FROM+system.tables+WHERE+database='loom'"   # 0 before the first migrate
```

The script refuses a port that is already taken (pick others and re-run), so a failed start cannot hand your migrations to another server. Remove it when done: `docker rm -f "ch-$(basename "$PWD")"`.

Keep a list of every container, compose project and volume you start, and remove exactly those, by full name. Never clean up by a pattern (`docker ps --filter name=loom-local-`, `cht-*`): other sessions on the same machine start containers with the same prefixes.

## 4. One `.env` for this worktree

An agent's shell keeps no variables between calls, and a server started without them falls back to `localhost:8123` and migrates whatever answers there at boot. Put the worktree's values in its own `.env` (ignored; a fresh worktree has none), which the server, `make migrate` and the tests all read. `LOOM_CH_PORT` is the HTTP port §3 started ClickHouse on (18123 there; change both if you picked others). A variable already exported in the agent's environment wins over `.env`, so check for one first:

```bash
cd <worktree> || exit 1
env | grep -E '^LOOM_(CH_|BASE_URL|ENV_FILE|BACKGROUND_WORKERS|AUTH_REQUIRED|EMBEDDING_MODEL|LLM_PROVIDER)' && {
  echo "these override .env in every later call: remove them from the shell profile, or start each later command with env -u NAME"; exit 1; }
bash -c '(exec 3<>/dev/tcp/127.0.0.1/7790)' 2>/dev/null && {   # bash's /dev/tcp; zsh has none
  echo "port 7790 is taken: pick another for the label, URL and --port"; exit 1; }
test -e .env && { echo ".env exists: check its LOOM_CH_* before migrating"; exit 1; }
cat > .env <<ENV
LOOM_CH_HOST=localhost
LOOM_CH_PORT=18123
LOOM_BASE_URL=http://localhost:7790
LOOM_BACKGROUND_WORKERS=off
LOOM_JWT_SECRET=$(openssl rand -hex 16)
LOOM_AUTH_REQUIRED=false
LOOM_EMBEDDING_MODEL=fake-ngram-1024
LOOM_LLM_PROVIDER=fake
LOOM_LATENCY_BUDGET_MULTIPLIER=10
LOOM_RUNTIME_OVERRIDES_REFRESH_SECONDS=1
ENV
make migrate
```

The last five lines are the posture of CI's main integration pass (`.github/workflows/ci.yml`). A server with auth on fails dozens of tests written for that pass: that is the posture, not a bug. CI runs `test_cross_principal_leakage.py` a second time against an auth-on server. Workers stay off: a live supervisor drains the tests' rows.

## 5. Server from source

Run it in the background (`run_in_background`, or `&`), from the worktree root:

```bash
cd <worktree> && LOOM_INSTANCE_LABEL="iso:$(pwd | cksum | cut -d' ' -f1):7790" LOOM_BUILD_COMMIT=$(git rev-parse --short HEAD) \
  .venv/bin/uvicorn server.main:app \
  --app-dir "$PWD" --host 127.0.0.1 --port 7790 --loop asyncio --reload --reload-dir "$PWD/server"
```

Check it in a separate call, by its label rather than its commit (two worktrees fresh from `origin/main` report the same `build_commit`); the label is a checksum of the worktree path because the server keeps only 64 characters of it:

```bash
cd <worktree> && curl -s localhost:7790/v1/health | jq -e --arg l "iso:$(pwd | cksum | cut -d' ' -f1):7790" '.instance_label == $l and .status == "ok"'
```

A `false` means another server holds the port. `--app-dir "$PWD"` makes uvicorn serve this worktree's code; `build_commit` confirms it (a source run reports `unknown` without `LOOM_BUILD_COMMIT`). The label is read from the process environment, not `.env`: without it the server refuses to start.

## 6. Frontend dependencies

A worktree's `frontend/node_modules` may be a symlink into another checkout. `npm ci` through that link empties the other checkout's directory. Check first, and replace a link with a real install:

```bash
cd <worktree> && test -L frontend/node_modules && rm frontend/node_modules   # removes the link only
cd <worktree> && npm --prefix frontend ci
```

## 7. Integration tests

```bash
cd <worktree> && make test-integration
cd <worktree> && .venv/bin/python -m pytest tests/integration -m "not slow and not destructive" -q   # quick pass
```

Tests read `LOOM_CH_HOST` and `LOOM_BASE_URL` from the environment or from the `.env` the session loads (`LOOM_ENV_FILE=` loads none) and skip without them ([integration tests](../../../docs/development/testing.md#integration-tests)); never point them at a shared or production server. Tests that need self-signup skip in CI, so new tests use `mint_test_token`.

## Reference

- [Local development](../../../docs/development/local-development.md), [testing](../../../docs/development/testing.md)
