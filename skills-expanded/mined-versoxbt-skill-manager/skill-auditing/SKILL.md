---
name: skill-auditing
description: >
  Activates when the user wants to see their installed skills, mentions
  "skill manager", "check my skills", "skill audit", "what skills do I have",
  "skill updates", "newer version", "outdated plugins", or wants to know
  what's installed and where it comes from.
version: 0.3.0
---

# Skill Auditing

## Quick Start

See all your installed skills:

```
/skill-check
```

Fix structural issues (user-owned skills only):

```
/skill-check --fix
```

## What It Shows

- **Full inventory** of every skill with description, source, repo link, and token count
- **GitHub repo links** for every skill — resolved from plugin.json, skill-lock, or marketplace git remote
- **Structure issues** — missing frontmatter fields (name, description, version)
- **Available updates** — checks GitHub for newer versions of plugins and standalone skills

## Options

| Flag | Effect |
|------|--------|
| `--fix` | Fix structural issues (with confirmation, user-owned skills only) |
| `--json` | Output machine-readable JSON |
| `--no-update` | Skip GitHub update checks (offline mode) |
