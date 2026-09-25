# Repo Referensi: akin-ozer/cc-devops-skills

Repo: https://github.com/akin-ozer/cc-devops-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/akin-ozer_cc-devops-skills
API: curl "localhost:27126/repos/readme?name=akin-ozer_cc-devops-skills"
Dibuat: 2026-09-16

## Cuplikan README
# akin-ozer/cc-devops-skills

Source: https://github.com/akin-ozer/cc-devops-skills
Fetched: 2026-09-16

## README
# DevOps skills for Claude Code and Codex

[![Mentioned in Awesome Claude Code](https://awesome.re/mentioned-badge-flat.svg)](https://github.com/hesreallyhim/awesome-claude-code)

A practical skill pack for DevOps work in Claude Code and Codex desktop.

This repository ships **31 skills**:
- **16 generators** for scaffolding production-ready configs
- **14 validators** for linting, security checks, and dry-run validation
- **1 debugger** (`k8s-debug`) for cluster troubleshooting

The goal is simple: make infra and pipeline work faster without skipping correctness checks.

## Quick Install

### Claude Code Plugin Marketplace

```bash
/plugin marketplace add akin-ozer/cc-devops-skills
/plugin install devops-skills@akin-ozer
```

### Codex Desktop

Skills only:

```bash
$skill-installer install https://github.com/akin-ozer/cc-devops-skills/tree/main/devops-skills-plugin/skills
```

Manual plugin install:

1. Clone the repo and link the packaged plugin into your local Codex plugin directory:

```bash
git clone https://github.com/akin-ozer/cc-devops-skills.git ~/.codex/devops-skills
mkdir -p ~/plugins ~/.agents/plugins
ln -s ~/.codex/devops-skills/devops-skills-plugin ~/plugins/devops-skills
```

2. Create or update `~/.agents/plugins/marketplace.json` so Codex can discover the plugin:

```json
{
  "name": "local-plugins",
  "interface": {
    "displayName": "Local Plugins"
  },
  "plugins": [
    {
      "name": "devops-skills",
      "source": {
        "source": "local",
        "path": "./plugins/devops-skills"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

If you already use `~/.agents/plugins/marketplace.json`, append the `devops-skills` entry instead of replacing the file.

The packaged Codex manifest lives at `devops-skills-plugin/.codex-plugin/plugin.json`. It exists alongside the Claude manifest and points at the same `skills/` directory.

### Team Rollout

Add this to project-level `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "devops-skills": {
      "source": {
        "source": "github",
        "repo": "akin-ozer/cc-devops-skills"
      }
    }
  }
}
```

## Drop-In GitHub Action Wrapper

This repository also publishes a **drop-in wrapper** around `anthropics/claude-code-action@v1`.

Replace:

```
