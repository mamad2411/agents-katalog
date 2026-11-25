---
name: org
description: Run all automation scripts in this Obsidian vault. Use when the user asks to organize the vault, run scripts, execute automation, or run /org.
---

# Organization Skill

Runs all automation scripts in parallel and reflects on the process. Use sub-skills for daily/weekly subsets.

## Quick Start

```bash
python3 _scripts/org_skill.py
```

## Sub-Skills

| Skill | Command | Purpose |
|-------|---------|---------|
| `org-list` | `--list` | List all available scripts |
| `org-daily` | `--daily` | ArXiv, HN, Reddit, news, Twitter |
| `org-weekly` | `--weekly` | Weekly synthesis + self-reflection |
| `org-status` | `--status` | Check execution status and recent runs |
| `org-logs` | `--logs` | View recent execution logs |

## Options

- `-s, --skip s1,s2`: Skip specific scripts
- `-v, --verbose`: Stream each script's output (runs sequentially)

## Examples

```bash
python3 _scripts/org_skill.py --list
python3 _scripts/org_skill.py --daily
python3 _scripts/org_skill.py --skip arxiv_digest.py,twitter_capture.py
python3 _scripts/org_skill.py --daily -v
```

## Scripts Executed (default)

- arxiv_digest.py, hn_newsletter.py, reddit_digest.py, tophub_news_simple.py, twitter_capture.py
- weekly_synthesis.py

## Output

- Log: `_logs/org_skill_YYYYMMDD_HHMMSS.log`
