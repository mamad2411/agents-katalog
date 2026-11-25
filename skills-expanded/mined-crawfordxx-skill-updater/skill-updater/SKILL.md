---
name: skill-updater
description: "Scan all installed Claude Code skills, check if they originate from open-source GitHub repos, and detect available updates. Use this skill when the user mentions updating skills, checking skill versions, auditing installed skills, skill freshness, or wants to know which skills are from GitHub and whether newer versions exist. Also trigger when the user says 'check my skills', 'update skills', 'skill status', or anything about skill maintenance."
---

# Skill Updater

Scan installed Claude Code skills, identify their GitHub origins, and check for available updates using `gh` CLI.

## How It Works

Skills can come from two places:
1. **GitHub repos** — tracked in `skills-lock.json` with `source`, `sourceType`, and `computedHash`
2. **Local/custom** — created by the user, no upstream source

This skill scans both project-level (`<project>/.claude/skills/`) and global (`~/.claude/skills/`) skill directories, cross-references with `skills-lock.json`, and uses `gh` CLI to check if upstream repos have newer versions.

## Usage

Run the scanner script:

```bash
python3 <skill-dir>/scripts/scan_skills.py [options]
```

### Options

| Flag | Description |
|------|-------------|
| `--project-dir PATH` | Project root (default: current working directory) |
| `--global-dir PATH` | Global skills dir (default: `~/.claude/skills`) |
| `--lock-file PATH` | Path to skills-lock.json (default: `<project-dir>/skills-lock.json`) |
| `--check-updates` | Actually query GitHub for updates (slower, requires `gh` CLI) |
| `--json` | Output as JSON instead of table |
| `--outdated-only` | Only show skills that have updates available |

### Examples

**Quick overview** — list all skills and their sources:
```bash
python3 scripts/scan_skills.py --project-dir /Users/crawford/workspace
```

**Check for updates** — compare local hashes against GitHub:
```bash
python3 scripts/scan_skills.py --project-dir /Users/crawford/workspace --check-updates
```

**Show only outdated** — filter to skills needing updates:
```bash
python3 scripts/scan_skills.py --project-dir /Users/crawford/workspace --check-updates --outdated-only
```

**JSON output** — for programmatic use:
```bash
python3 scripts/scan_skills.py --project-dir /Users/crawford/workspace --check-updates --json
```

## Workflow

1. Run the script to get a status overview
2. Review which skills have updates available
3. For skills you want to update, the script prints the `claude skill install` command
4. For local skills, it checks if a matching GitHub repo exists (by searching skill name)

## Interpreting Results

| Status | Meaning |
|--------|---------|
| `up-to-date` | Local hash matches upstream — no action needed |
| `update-available` | Upstream has changed since last install |
| `local` | Not from GitHub, user-created skill |
| `unknown` | In lock file but couldn't check upstream |
| `not-tracked` | On disk but not in skills-lock.json |

## Requirements

- `gh` CLI installed and authenticated (`gh auth status`)
- Python 3.8+
- `skills-lock.json` in the project root (created by `claude skill install`)
