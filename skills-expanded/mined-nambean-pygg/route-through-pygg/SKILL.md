---
name: route-through-pygg
description: Set up Claude Code, Codex CLI or OpenCode to send their model requests through Pygg's local gateway, and read what each launch cost. Use when the user asks to route their coding agent through Pygg, use cheaper or local models in Claude Code, or see what a session cost.
---

# Route a coding agent through Pygg

Pygg is a local gateway on `127.0.0.1:8741`. It sends each request to a model the user connected (API keys, coding plans, a local Ollama), falls back when one fails, and records what every request cost. These steps are the user's to run in their own terminal: they start new sessions of the agent, so do not run them from inside this one.

## Check that Pygg is there

```bash
pygg doctor        # finds the store and the running gateway
pygg providers     # the connections, and whether they answer
```

No `pygg` command: `npm install -g @pygg/cli@dev`. On Windows, the Pygg app (from the project's GitHub releases) is the gateway; on macOS and Linux, `pygg gateway serve` runs it in a terminal.

## Claude Code

The user keeps their Claude sign-in; Pygg starts Claude Code through the gateway one launch at a time and changes no file.

```bash
pygg setup claude                 # a Pygg key of its own, kept in the credential store
pygg run claude                   # this launch through Pygg, model auto; a receipt when it exits
pygg run --statusline claude      # the same, with the launch's cost in the status line
```

## Codex CLI and OpenCode

```bash
pygg setup codex     # adds a `pygg` provider and profile, after a backup
pygg run codex       # or: codex --profile pygg -m auto/cheap
pygg setup opencode  # a Pygg provider with the auto aliases and the enabled models
pygg run opencode
```

## See what it cost

```bash
pygg launches --by-repo   # each launch's receipt, by repository
pygg usage                # requests, tokens and cost
```

Models: `auto` picks by the request; `auto/cheap` prefers the cheapest model that fits. A subscription or web-session model has no per-request price, so its cost shows as unknown, not $0.
