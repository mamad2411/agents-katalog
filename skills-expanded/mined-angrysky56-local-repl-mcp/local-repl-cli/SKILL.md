---
name: local-repl-cli
description: "Use modern CLI tools (rg, fd, ast-grep, bat, sd, jq, yq, tokei, eza, dust, procs, delta, hyperfine, watchexec, just) through the LocalREPL shell bridge for efficient codebase analysis, structured data extraction, and reactive workflows. Trigger whenever the user wants to search code, inspect a repository, count or analyze files, compare diffs, benchmark commands, or orchestrate multi-step shell work — especially when they haven't specified which tool to use. This skill teaches token-efficient patterns (count-before-enumerate, structured --json output, progressive disclosure) and documents real execution-environment gotchas specific to MCP-launched subprocesses."
---

# local-repl-cli: efficient shell orchestration via LocalREPL

This skill turns the LocalREPL shell bridge into a disciplined CLI orchestration layer. The tools themselves (ripgrep, fd, ast-grep, jq, tokei, delta, hyperfine, watchexec, just) are widely known; the *value* of this skill is knowing **which one to reach for, what flags produce agent-friendly output, and which failure modes bite specifically in the MCP subprocess environment**.

Read one of the reference files when you need depth:
- `reference/recipes.md` — copy-paste multi-tool pipelines (codebase-first-touch, safe-refactor, benchmarking, reactive test loops)
- `reference/ast-grep-patterns.md` — correct pattern syntax with worked examples and anti-patterns
- `reference/gotchas.md` — environment quirks (sh vs bash, PATH inheritance, MCP JSON-string coercion, ripgrep stdin heuristic)

## Prerequisites

These tools must be on `$PATH`. If a verify fails, the tool is missing — stop and ask the user to install it per `~/Repositories/ai_workspace/local-repl-mcp/README.md`:

```
rg jq fd bat sd yq tokei eza dust procs delta hyperfine watchexec ast-grep just
```

Verify quickly: `run_shell("for c in rg jq fd bat sd yq tokei eza dust procs delta hyperfine watchexec ast-grep just; do command -v $c >/dev/null && echo OK: $c || echo MISS: $c; done", repl_id, use_shell=True)`. For a fuller report with per-tool install hints, run `bash scripts/check_tools.sh` from the skill directory.

## Core principles

### 1. Count before you enumerate

Before asking for contents, ask for a count. This is the single highest-leverage habit for token efficiency. A 30-second scan that dumps thousands of lines into context can almost always be replaced by a 20ms count that tells you whether the question is even worth pursuing.

**Example from a real session:** `rg -c "def " --type py` against a whole repo hung for 60 seconds and returned zero useful output. The scoped version `rg -c "def " --type py local_repl/` returned per-file counts in 20ms. Even better, `tokei --output json | jq '.Python.code'` returned the single aggregate number in 7ms.

Default progression:
1. `tokei --output json` for "how big is this codebase, by language" (always the first call on a new repo)
2. `rg -c PATTERN --type LANG SCOPE/` for "how often does this appear" — scoped, not whole-repo
3. `rg PATTERN --type LANG SCOPE/` only after the count justifies reading matches

### 2. Ask for structured output

Every tool in this stack has a `--json` (or `--output json`) flag. Use it. Text output forces regex extraction; JSON output allows deterministic `jq` pipelines.

| Tool | Flag |
|---|---|
| `rg` | `--json` (streaming, one JSON per line) |
| `fd` | `-x ... \;` or pipe through `jq -R` for structured |
| `ast-grep` | `--json=compact` or `--json=stream` |
| `tokei` | `--output json` |
| `hyperfine` | `--export-json FILE` |
| `jq` | native |

Always pipe through `jq` to extract *only* the fields that matter. Dumping raw JSON into context is worse than dumping raw text — same tokens, less human-readable.

### 3. Prefer structural matching over regex for code

When searching **code**, ast-grep beats ripgrep because it parses the language and matches AST nodes. Regex matches inside strings and comments and breaks on whitespace variations; ast-grep doesn't.

- `rg` for: freeform text, logs, configs, documentation, TODO markers
- `ast-grep` for: functions, classes, decorators, call sites, imports, type annotations — anything with syntactic structure

**Example:** Counting `@mcp.tool()` decorators across three Python files took ast-grep 7ms and returned exactly 15. A ripgrep `@mcp\.tool\(\)` pattern would've matched occurrences inside docstrings, comments, and string literals as well.

### 4. Use `just` recipes, not inline pipelines

If a multi-tool pipeline runs more than once, it belongs in a `justfile` in the project root — not reconstructed from scratch in each prompt. The skill's job is to *call* recipes, not to re-type them.

When you see a `justfile`, run `just --list` first and prefer recipes by name. When you don't see one and the user asks you to run the same pipeline twice, offer to add a recipe.

### 5. Reactive > polling

For anything that involves "run X when files change," use `watchexec` with its native file-watch. Polling loops (`while true; sleep`) waste cycles and miss fast edits. See `reference/recipes.md` for the reactive test-loop pattern.

## When to use this skill

Trigger this skill whenever the user's request involves any of:

- Exploring or summarizing a codebase ("how big is this repo", "what's in this project")
- Searching code ("find all calls to X", "where is Y defined")
- Counting or measuring things (files, functions, lines, commits)
- Comparing or diffing files or outputs
- Benchmarking command performance
- Setting up reactive workflows (run tests on save, rebuild on change)
- Extracting fields from JSON/YAML configs or API responses
- Running the same shell sequence repeatedly

Do NOT trigger this skill for:
- Pure Python work (use `run_python_in_repl` directly)
- Editing a single file (use `str_replace` or `edit_block`)
- Questions that don't involve the filesystem

## Isolated Virtual Environment Execution

When performing Python execution or testing against target projects that have their own virtual environments (such as `.venv`, `venv`, `env`), avoid running inside the default REPL unless the dependencies are installed globally. Instead, use the virtual environment execution tools:

- `run_python_in_venv(code, venv_path, repl_id=None)`: Runs Python code inside the context of the designated virtual environment or Python interpreter path.
- `find_venv(path=None)`: Automatically scans for virtual environments recursively from the given path to identify target environments.

This ensures dependency isolation and clean runs, preventing dependency conflicts or import errors.

## Standard workflow

1. **Establish context.** If the user is asking about a specific project, call `set_repl_cwd(repl_id, project_path)` first so subsequent shell calls land in the right directory.
2. **Count or survey.** Start with tokei or a scoped `rg -c` — don't dump contents until you know the shape.
3. **Choose the right tool.** rg for text, ast-grep for code structure, fd for paths, jq for JSON, tokei for size.
4. **Ask for JSON.** Pipe through jq to extract the specific fields you need.
5. **Scale up only if needed.** If a scoped query finds what you need, don't expand scope.
6. **Record learnings.** If a command failed in an interesting way, tag it: `tag_command(id, ["flaky", "known-issue"])`. Query `only_failures=True, since='1h'` when debugging.

## Critical environment notes

These gotchas are load-bearing. Skipping them causes silent failures that look like tool bugs. See `reference/gotchas.md` for depth.

- **`use_shell=True` invokes `/bin/sh`, not bash.** No brace expansion `{a,b}`, no `[[ ]]`, no process substitution `<(...)`. Use POSIX sh or invoke `bash -c '...'` explicitly.
- **Silent zero-match failures in ast-grep.** `def $NAME($$$): $$$` matches *nothing* because `$$$` only binds argument lists, not bodies. Use `def $NAME` to match by name only.
- **MCP serializer coerces JSON-looking strings to dicts**, which then fail Pydantic `str` validation on `stdin_input`. Workaround: pipe via `use_shell=True` with `echo '{...}' | jq ...`.
- **Scope broad searches.** Top-level `rg` without a path argument can hit pathological file trees (large `.venv`, symlink loops) and time out. Always scope: `rg PATTERN --type py src/`, never bare `rg PATTERN --type py`.
- **Commit before destructive edits.** Use `git show HEAD:file > file` for one-shot recovery if an edit goes sideways. This has already saved work in this codebase.

## Operational memory

The LocalREPL shell bridge logs every `run_shell` call to `evolution.db` automatically. Use this:

- `query_command_history(pattern='%rg%', only_failures=True, since='1h')` — what went wrong recently
- `command_stats(since='1d')` — success rate, slowest commands, top commands, top failures
- `tag_command(id, ['solved', 'fixed-v0.2.1'])` — annotate interesting rows so they're findable later

When a problem looks familiar, check history before re-running. When you solve something non-obvious, tag it.
