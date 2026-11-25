---
name: semgrep-setup
description: Install Semgrep, authenticate to the AppSec Platform when needed, and start the MCP server. Use when semgrep is missing, scans fail, or the MCP connection does not come up.
---

# Semgrep setup

## Install

```bash
brew install semgrep          # macOS
pipx install semgrep          # any platform with Python
pip install semgrep           # inside a project venv
semgrep --version
```

Docker alternative (no local install): `docker run --rm -v "$PWD:/src" semgrep/semgrep semgrep scan`.

## Accountless vs platform-connected

Semgrep works with no account: `semgrep scan --config p/security-audit` runs
entirely locally with registry rules. Connect to the Semgrep AppSec Platform
only when you want diff-aware CI scans, PR comments, org policies, or the
findings dashboard:

```bash
semgrep login                     # browser flow, stores a token locally
# or headless / CI:
export SEMGREP_APP_TOKEN=<token>  # create under Settings > Tokens in the platform
semgrep ci
```

Keep `SEMGREP_APP_TOKEN` in your CI secret store, never in the repo.

## MCP server

The MCP server ships inside the semgrep binary (the old standalone
`semgrep-mcp` package and repo are deprecated). This plugin starts it with:

```bash
semgrep mcp -t stdio
```

- Transports: `stdio` (default, what this plugin uses) and
  `streamable-http` (`-t streamable-http`, listens on 127.0.0.1:8000/mcp).
- Requires the `semgrep` binary on PATH; install it first (above).
- Platform-backed tools (fetching findings) need `SEMGREP_APP_TOKEN` in the
  environment; pure scanning tools work without any account.
- Semgrep also operates a hosted experimental endpoint at
  https://mcp.semgrep.ai/mcp; it is documented as unstable, so this plugin
  intentionally uses the local binary instead.

## Repo hygiene

- `.semgrepignore` at repo root for vendored and generated code.
- Commit custom rules under `rules/` and test them with `semgrep --test rules/`.
- Pin ruleset choices in CI config so scans are reproducible; avoid
  `--config auto` in offline or compliance-sensitive environments.

## Troubleshooting

- `command not found: semgrep`: install via brew/pipx; restart the MCP server.
- MCP server looks "hung" with no output: expected in stdio mode, it is
  waiting on stdin.
- `--config auto` fails offline: switch to explicit `p/<ruleset>` or local
  rule files.
- Slow scans on huge repos: scope to changed paths, exclude tests and
  vendored code, and prefer `semgrep ci` diff-aware scanning on PRs.
