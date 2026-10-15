---
name: project-tool-allowlist
description: Scan a repo's stack and tooling plus installed helper tools (package managers, build/test/lint commands, make, git, rtk) and generate a project-local permission allowlist for the current agent/client so those commands run without prompting. Use when the user wants fewer permission prompts, to pre-approve a project's dev tools, or to set up an agent config for a repo's stack.
---

# Project Tool Allowlist

Generate a project-local permission allowlist from a repo's detected tooling so the
running agent can run its dev commands without prompting each time.

## Workflow

1. Identify the target folder (default: current working directory) and the git
   scope the user wants (`read-only`, `safe`, or `all`; default `safe`).
2. Identify the current client — **do not assume Claude**. The detector
   auto-detects from inherited env (`--client auto`, the default): `CLAUDECODE`/
   `CLAUDE_CODE_*` → Claude, `CODEX_*` → Codex, else unknown. It prints the
   resolved client on stderr. Each client has a different target:
   - **Claude Code** → write `.claude/settings.local.json` (or `.claude/settings.json` with `--shared`).
   - **Codex** → project-trust block the **user** appends to `~/.codex/config.toml` (agent can't write it).
   - **Anything else** → see "Unknown client" below.

   If you are running under Codex, you must use the Codex path — never write a
   `.claude/` settings file for a Codex session.
3. Run the detector to preview what it found (auto-detects the client):

   ```bash
   python3 scripts/detect_tools.py <folder> --git <scope>
   ```

4. Show the user the detected stack, installed tools, and the allow patterns.
5. Apply.

## Apply per client

**Claude Code** — merge into the settings file (idempotent union, never clobbers
existing entries):

```bash
python3 scripts/detect_tools.py <folder> --client claude --git safe --apply
# add --shared to target the committed .claude/settings.json
```

**Codex** — trust is **global by design**, not repo-committed. Codex's `projects`
trust map lives only in the global `~/.codex/config.toml`, keyed by absolute path;
Codex reads no per-project `config.toml` (the sole repo-local file it loads is
`AGENTS.md`, which is instructions, not permissions). This is deliberate — if a
repo could ship a file trusting itself, cloning a hostile repo would auto-trust
it. So there is no project-local alternative; the trust must be applied to the
global config by the user.

Codex's sandbox also cannot write its own global `~/.codex/config.toml`
(it lives outside the project workspace), so the agent cannot apply this itself.
The detector prints a ready-to-run `printf >> ~/.codex/config.toml` command plus
the trust block it writes. Show both, then have the **user** run the command
(e.g. paste it with the `!` prefix). It trusts the whole project — Codex has no
per-command allowlist. Re-running is safe: the detector skips and reports if the
project's trust block is already present — use this to verify it applied. Do
**not** rely on `codex doctor`'s exit code: it can exit nonzero for reasons
unrelated to config (e.g. a corrupt `~/.codex/logs_*.sqlite`), so a nonzero exit
does not mean the trust block failed.

**Unknown client** — run with `--client list --json` to get the raw `Bash(...)`
command prefixes, then look up how *your own* client stores project-local
permissions/allow rules and write that config with the equivalent entries.

## What it allows

- Project file access: `Read(**)`, `Edit(**)`, `Write(**)` — gitignore-style
  patterns relative to the settings file's project root, so file ops anywhere in
  the project run without prompting, nothing outside it. Pass `--no-files` to
  skip. Claude-only; Codex project trust already covers file read/write.
- Stack commands: package-manager scripts (npm/bun/pnpm/yarn), `make` targets,
  `cargo`/`go`/`pytest`/`mvn`/`gradle` build+test, linters/formatters.
- Installed safe helper tools on PATH (`gh`, `jq`, `rg`, `fd`, `just`, ...).
- Network/infra tools (`curl`, `wget`, `docker`, `kubectl`, `aws`, `gcloud`,
  `terraform`, `ansible`, ...) and `rtk gain` are **gated** — not allowed unless
  you pass `--include-infra`. Blanket-approving them is an exfil/mutation risk, so
  they keep prompting by default. The detector prints which gated tools it found.
- `git` per chosen scope: `safe` allows status/diff/log/add/commit/checkout/
  branch/fetch/stash; it never allows `push`, `reset`, or `clean` — those keep
  prompting. `read-only` allows only non-mutating git; `all` allows `Bash(git:*)`.
- If `rtk` is installed, every prefix is mirrored as `rtk <prefix>` so the same
  scope (including git safety) holds when commands run through the rtk proxy.
- MCP servers: one whole-server `mcp__<server>` entry per detected server (allows
  every tool that server exposes). Servers are found via `claude mcp list`, the
  project's `.mcp.json`, and `~/.claude.json` (global + this project's
  `mcpServers`). Pass `--no-mcp` to skip. Codex covers MCP via project trust, so
  the `mcp__` entries only matter for Claude/unknown clients.

## Notes

- Re-running is safe: the Claude merge **unions** with the existing
  `permissions.allow` and preserves every other key in the file — existing
  config is extended, never overwritten.
- The merge also **simplifies**: a narrower entry is dropped when a broader one
  already covers it (`Bash(git:*)` subsumes `Bash(git status:*)`; `mcp__srv`
  subsumes `mcp__srv__tool`). Apply reports `+N new, -M redundant collapsed`.
- Review before applying `--git all`; it removes the push/reset/clean guardrail.
