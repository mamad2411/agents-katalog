---
name: nomos
description: Thin binary bootstrapper for Nomos (zero-token AST & Git guardrails across 11 languages). Use when asked to audit AI technical debt, prevent test deletion or reward-hacking (t.Skip, hollow stubs, swallowed errors), lock main, baseline a legacy brownfield repo, or set up deterministic PreToolUse and pre-commit guardrails.
---

# Nomos Thin Binary Bootstrapper (Zero Prompt-Pack Rules)

Nomos is a compiled `~20 MB` `CGO_ENABLED=0` static Go binary (`Apache-2.0`, `0` LLM tokens) that sits between any coding agent and Git. This skill is strictly a **one-time bootstrapper** - never simulate AST gates in Markdown prompts or DIY shell scripts.

## 1. Ensure `nomos` Binary Is Installed

Check `command -v nomos`. If missing, install the SHA-256 verified binary:

```bash
# Linux, macOS, and WSL2:
curl -fsSL https://sophialabs.ca/install | bash

# Alternatives when shell-pipe policy restricts curl | bash:
# brew install --cask mgantlett/tap/nomos
# npx --yes @mgantlett/nomos xray .
# uvx nomos-cli xray .
# GOTOOLCHAIN=auto CGO_ENABLED=0 go install github.com/mgantlett/nomos/substrate/cmd/nomos@latest
# Optional zero-install remote MCP tools & resources (nomos://capabilities/catalog):
# claude mcp add --transport http nomos https://sophialabs.ca/mcp
```

## 2. Run Read-Only Day-0 Audit (`0` Repository Writes)

```bash
nomos xray .
```

Report the repository's `AI Hangover Score` (`0-100`, `Grade A-F`) and top 3 structural hotspots to the user.

## 3. Initialize Non-Breaking Branch Guard & Hand Off to Compiled Hooks

```bash
nomos init
# Or run a zero-git-status stealth trial tracked only in .git/info/exclude:
# nomos init --local
```

- `nomos init` freezes existing legacy debt in `nomos.baseline.json` so **zero untouched legacy files fail**, locks `main`, scaffolds a compact `~13`-line `AGENTS.md`, and wires `~4ms` native agent + Git `pre-commit` / `post-commit` hooks.
- **Never run `nomos init --worktrees` on Day 0** unless explicitly requested by the user.
- **Invisible Stewardship:** Once `nomos init` completes, compiled Go hooks govern tool calls and commits automatically. Resolve any `nomos verify` rejections yourself without weakening tests (`t.Skip`, deleted assertions, `// TODO` stubs) and never ask the human operator to run `nomos` commands manually.

## 4. Complete Capabilities & Subsystem Map (Page 0 SSoT)

- **Local CLI Introspection (`66` Capabilities, `42` Gate `ProbeID`s, `16` Directives):** Run `nomos capabilities [<probe_id>] [--json]` or `nomos --help-agent`.
- **Zero-Install Agent Markdown Reference:** Fetch `https://sophialabs.ca/docs/specs/capabilities.md` (or read MCP resource `nomos://capabilities/catalog` on `https://sophialabs.ca/mcp` / `nomos mcp`).
