# Install and use Easyskillz 0.5.1

Requires Node.js 22+.

```bash
npm install --global easyskillz@0.5.1
easyskillz --version
```

Easyskillz exposes a CLI-only public API. Use canonical domain commands in scripts and agent instructions.

## Existing project

```bash
easyskillz project doctor
easyskillz skill validate
easyskillz project migrate --dry-run
easyskillz project sync --dry-run
```

Review each plan. Apply a legacy migration with `project migrate --write`; apply ordinary project sync non-interactively with the explicit apply option shown by its help.

## Add a skill

```bash
easyskillz skill add review-pr --dry-run
easyskillz skill add review-pr --confirm
```

Edit `.easyskillz/skills/review-pr/`. Keep `SKILL.md`, scripts, references, and assets together; native hosts receive the complete directory.

Codex, Copilot, Gemini CLI, Antigravity, Cursor, and Devin consume the shared `.agents/skills` output. Claude Code consumes `.claude/skills`. Configuring several shared consumers still creates one physical artifact.

## Adopt instructions explicitly

```bash
easyskillz docs adopt docs/AGENTS.source.md --target AGENTS.md --dry-run
easyskillz docs adopt docs/AGENTS.source.md --target AGENTS.md --write
easyskillz docs sync --dry-run
easyskillz docs sync --write
```

`project sync` never claims instruction ownership. Adoption refuses unmarked user content and competing owners.

## Automation

Use `--json` for one success or error object. Use `--dry-run` for every mutation before applying. Usage failures exit 2; operational failures exit 1.

The aliases `sync`, `doctor`, and `add` remain deprecated through 0.5.x and are removed no earlier than 0.6.0. Do not put them in new automation.

Support is `conformant` unless dated activation evidence names a tested host version; installation alone does not make a surface verified.
