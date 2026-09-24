# Repo Referensi: netresearch/docker-development-skill

Repo: https://github.com/netresearch/docker-development-skill
Ref lokal: /Users/chaali0324/.agents/repo-refs/netresearch_docker-development-skill
API: curl "localhost:27126/repos/readme?name=netresearch_docker-development-skill"
Dibuat: 2026-09-16

## Cuplikan README
# netresearch/docker-development-skill

Source: https://github.com/netresearch/docker-development-skill
Fetched: 2026-09-16

## README
# Docker Development Skill

[![License](https://img.shields.io/badge/License-MIT%20%2B%20CC--BY--SA--4.0-blue.svg)](#license)
[![Claude Code Compatible](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://claude.ai/claude-code)

Agent Skill for Docker image development - Dockerfile best practices, CI testing patterns, and Docker Compose orchestration.

## Features

- **Dockerfile Best Practices** - Multi-stage builds, layer optimization, security
- **CI Testing Patterns** - Test Docker images reliably in CI pipelines
- **Docker Compose** - Service orchestration, health checks, networking
- **Docker Bake** - Multi-platform builds with BuildKit
- **Security** - Vulnerability scanning, non-root users, secret management
- **Windows / WSL2** - Run docker through WSL when Docker Desktop uses the WSL2 backend (separate `docker-via-wsl` skill)

## Skills

This package bundles two skills:

- **`docker-development`** — Dockerfile, compose, bake, CI testing, and security patterns.
- **`docker-via-wsl`** — for AI agents running on a Windows host *outside* WSL: re-issue every `docker`/`docker compose` command inside WSL (via `wsl.exe`) so Docker Desktop's WSL2 backend does not corrupt bind-mount paths.

## Automatic Triggers

The `docker-development` skill activates automatically when working with:

| File Pattern | Description |
|--------------|-------------|
| `Dockerfile`, `Dockerfile.*`, `*.dockerfile` | Container image definitions |
| `docker-compose.yml`, `compose.yml` | Multi-container orchestration |
| `docker-bake.hcl` | BuildKit bake configurations |
| `.dockerignore` | Build context optimization |

The `docker-via-wsl` skill activates when an agent on a Windows shell (Git Bash/MSYS/PowerShell, *outside* WSL) is about to run any `docker` command.

## Installation

### Marketplace (Recommended)

Add the [Netresearch marketplace](https://github.com/netresearch/claude-code-marketplace) once, then browse and install skills:

```bash
# Claude Code
/plugin marketplace add netresearch/claude-code-marketplace
/plugin install docker-development@netresearch-claude-code-marketplace
```

### Without a marketplace

Since Claude Code 2.1.157 a plugin directory under your personal skills directory loads on its own:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/netresearch/docker-development-skill.git \
  ~/
