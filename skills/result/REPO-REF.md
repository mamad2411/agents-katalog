# Repo Referensi: parallel-web/parallel-agent-skills

Repo: https://github.com/parallel-web/parallel-agent-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/parallel-web_parallel-agent-skills
API: curl "localhost:27126/repos/readme?name=parallel-web_parallel-agent-skills"
Dibuat: 2026-09-16

## Cuplikan README
# parallel-web/parallel-agent-skills

Source: https://github.com/parallel-web/parallel-agent-skills
Fetched: 2026-09-16

## README
# Parallel Agent Skills

[Agent Skills](https://agentskills.io/specification) for [Parallel](https://parallel.ai) — web search, content extraction, deep research, and data enrichment for AI coding agents.

## Prerequisites

Most execution skills require `parallel-cli` (installed, authenticated, and funded). The [`parallel-cli-setup`](skills/parallel-cli-setup/SKILL.md) skill walks an agent through install, auth, balance, and skills install end-to-end — install the plugin/skills below, then run `/parallel:parallel-cli-setup` from your agent.

`migrate-to-parallel` updates an application's own web-data integration. It uses the appropriate Parallel API or SDK and needs `PARALLEL_API_KEY` only for an explicitly authorized live smoke test.

## Installation

### Agent Skills

Use `parallel-cli` to install skills into Cursor, Cline, GitHub Copilot, and other compatible agents.

```bash
# Install all Parallel skills
parallel-cli skills install
```

### Claude Code

Available as a [Claude Code Plugin Marketplace](https://code.claude.com/docs/en/discover-plugins).

```bash
/plugin marketplace add parallel-web/parallel-agent-skills
/plugin install parallel
# restart Claude Code before continuing!

# this will install/update CLI and authenticate if not done already
/parallel:parallel-cli-setup
```

### OpenAI Codex

Install skills using the built-in skill installer (run inside Codex):

```text
$skill-installer parallel-web/parallel-agent-skills
```

Then run the setup skill to install/auth the CLI:

```text
/parallel:parallel-cli-setup
```

## CDN and discovery

A human + machine-readable catalog is published at [skills.parallel.ai](https://skills.parallel.ai).

Useful endpoints:

- [skills.parallel.ai](https://skills.parallel.ai) — human-friendly catalog and install instructions
- [skills.parallel.ai/index.json](https://skills.parallel.ai/index.json) — machine-readable skill index
- `https://skills.parallel.ai/<skill>/SKILL.md` — live raw skill file
- `https://skills.parallel.ai/<skill>/manifest.json` — file manifest + checksums
- `https://skills.parallel.ai/<skill>/versions.json` — release history for that skill
- `https://skills.parallel.ai/archives/<skill>/<version>.zip` — immutable GitHub Release archive via CDN redirect

## Skills

Skills follow the [Agent Skills](https://agentskills.io/specification) specification and double as Clau
