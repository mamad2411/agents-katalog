---
name: sandbox-setup
description: Set up and configure the agent-sandbox development environment
---

# Agent Sandbox Setup

This skill helps configure the agent-sandbox Docker development environment.

## Available Tools
The sandbox includes: bat, eza, fd, dust, procs, btm, xh, mcfly, fzf, zoxide, starship, micro, lazygit, gitui, tokei, yq, delta, gping, duf, ripgrep, jq, tmux, pre-commit, gitleaks, hadolint, shellcheck.

## Common Tasks

### Initialize pre-commit in a project
```bash
cp ~/.pre-commit-config.yaml.template .pre-commit-config.yaml
pre-commit install
pre-commit run --all-files
```

### Check Docker access
```bash
docker version
docker compose version
```

### Verify tool availability
```bash
for tool in claude codex gemini opencode bat eza fd dust procs btm xh mcfly fzf delta rg jq yq; do
  command -v "$tool" && echo "OK: $tool" || echo "MISSING: $tool"
done
```
