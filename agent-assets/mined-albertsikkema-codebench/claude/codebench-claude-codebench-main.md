# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A YAML-driven multi-step pipeline runner for `claude-safe` and `claude-server`. Each step launches a fresh container — i.e. fresh Claude context — so a "pipeline" is a way to chain prompts that hand off artifacts (files on disk) without sharing conversation history. Steps run either locally (`runner: safe` → `claude-safe`) or remotely on a dev VM (`runner: server` → `claude-server`). A step can also be a plain shell `command:` that runs on the host regardless of the pipeline's runner — useful for deterministic Python setup before the LLM steps.

The product is `.claude/pipelines/pipeline.py`, the helper scripts under `.claude/pipelines/scripts/`, and the YAML files under `.claude/pipelines/`. The `examples/` tree contains reference repos (`claude-safe`, `claude-setup`, `sandcastle`, `project-server-main`) that this code is built on top of — read them for context, but they are not part of the product.

## Common commands

```bash
./.claude/pipelines/pipeline.py .claude/pipelines/research-plan.yaml "your topic"     # run a pipeline
./.claude/pipelines/pipeline.py .claude/pipelines/research-plan.yaml --model sonnet "topic"
./.claude/pipelines/pipeline.py .claude/pipelines/build.yaml --runner safe "plans/foo.md"   # override server→safe
CLAUDE_MODEL=sonnet ./.claude/pipelines/pipeline.py .claude/pipelines/research-plan.yaml "topic"
```

`.claude/pipelines/pipeline.py` is a `uv run --script` shebang with PEP 723 inline metadata — no separate venv or `pip install` needed, `uv` resolves `pyyaml` on first run. There are no tests, linters, or CI.

## Architecture

- **`.claude/pipelines/pipeline.py`** — single-file runner. Loads the YAML, renders templates, dispatches each step:
  - `command:` step → `run_shell()` (always on host, `bash -c`).
  - `prompt:` step with `runner: safe` → `run_claude_safe`/`run_claude_interactive` (stream-json or TTY).
  - `prompt:` step with `runner: server` → `run_claude_server` (`claude-server -p ... --follow`, captures session ID from `==> Session: <id>`, then `claude-server --sync <id>` rsyncs the remote workspace back). The `interactive` flag is ignored in server mode — there is no local TTY.
- **`CLAUDE_SAFE_CMD = ["claude-safe", "--no-firewall", "--"]`** at the top of `.claude/pipelines/pipeline.py` is the fixed prefix for local steps. The `--` is required so `claude-safe` treats the rest as Claude args, not its own flags.
- **`.claude/pipelines/scripts/`** — helper Python scripts called from `command:` steps (e.g. `build_setup.py` does branch + PR creation in pure Python before the server LLM steps run). Each is a `uv run --script` PEP 723 shebang.
- **One container per step.** Steps don't share conversation state — they communicate by writing files (typically into `.claude/memories/`) and referencing those paths in the next step's prompt via `{{ steps.<id>.output }}`. The `setup` shell step in `build.yaml` is the canonical example.
- **Session context auto-injected on every `prompt:` step.** Before invoking claude(-safe|-server), `.claude/pipelines/pipeline.py` shells out to `.claude/helpers/get_metadata.sh` (single source of truth for date/time, repo, branch, commit) and appends a `GitHub owner/repo:` line derived from `origin`. The result is passed via `--append-system-prompt`. Step prompts can reference owner/repo/date directly without `gh repo view` or `date`. Recomputed per step, so post-`setup` steps see the new branch.

## YAML schema

```yaml
name: <pipeline name>            # required
description: <one-liner>         # optional
runner: safe|server              # optional, default `safe` — applies to prompt: steps
runner_args: ["--github", ...]   # optional, default [] — extra args passed to claude-server

steps:
  - id: <step id>                # required, used in {{ steps.<id>.output }}
    interactive: true|false      # required — must be set explicitly per step
                                 # (ignored when runner is `server` or step is `command:`)
    output: <path template>      # optional, exposed as {{ output }} inside this step
    # Exactly one of `prompt:` or `command:` per step:
    prompt: |                    # LLM step; runner-dispatched (safe/server)
      ...
    command: |                   # Shell step on host; supports template variables
      ...
```

**Template variables** resolved by `render()`:
- `{{ input }}` — the positional CLI input (joined args)
- `{{ timestamp }}` — pipeline start time, formatted `%Y-%m-%dT%H-%M-%S`
- `{{ pipeline_dir }}` — absolute path to the directory containing the pipeline YAML; use this to invoke helper scripts via `{{ pipeline_dir }}/scripts/foo.py` so the pipeline works regardless of the caller's cwd
- `{{ output }}` — only inside a step's body, equal to the rendered `output` field of that same step
- `{{ steps.<id>.output }}` — the rendered `output` of a previous step

Unknown variables raise `ValueError`. Steps that omit `interactive`, or that set both/neither of `prompt:`/`command:`, are rejected at load time.

## Editing rules specific to this repo

- **`interactive` is mandatory on every step**, even server / command steps where it is ignored. `load_pipeline` errors out if it's missing — don't paper over this with a default.
- **Exactly one of `prompt:` or `command:` per step.** `command:` steps always run on the host via `bash -c`, regardless of the pipeline's `runner`.
- **Don't strip `--no-firewall` from `CLAUDE_SAFE_CMD`.** Pipelines run on the user's machine and the firewall is opt-in for individual sessions, not the default for orchestrated runs.
- **Server steps auto-sync.** After every `prompt:` step in `runner: server` mode, `.claude/pipelines/pipeline.py` calls `claude-server --sync <session>` to rsync the remote workspace back. Don't add a manual sync step.
- **Don't add a slash command that runs `.claude/pipelines/pipeline.py`.** It would invoke `claude-safe` from inside a container, which doesn't work.
- **Stream-json formatter lives in `.claude/pipelines/pipeline.py`.** `format_event` / `_format_tool_call` are the local source of truth — edit them in place.
- **Step output paths are templates, not promises.** `.claude/pipelines/pipeline.py` renders `output` and exposes it as `{{ output }}` inside the body, but doesn't itself create or verify the file. The prompt or command has to write there.
- **`build.yaml` setup runs locally even in server mode.** The setup script creates the branch + PR on the host's repo, then `claude-server` rsyncs that branch state to the VM for the build/review/triage steps.
