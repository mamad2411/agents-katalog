---
name: daily-synthesis
description: Generate daily cross-domain synthesis from today's source notes. Use when user asks for daily synthesis or /daily-synthesis.
permissions:
  - vault.read
  - vault.write
---

# Daily Synthesis Skill

Lightweight cross-domain scan of today's curated source notes. Finds connections across domains, contradictions between sources, and the single most important cross-domain signal.

## Usage

```bash
python3 _scripts/daily_synthesis.py
```

## Output

`Sources/Daily Synthesis - YYYY-MM-DD.md` (cross-domain sparks from today's ArXiv, HN, Reddit, news, Twitter)

## Notes

- Requires at least 2 source notes from today to run
- Automatically runs after `/skill org-daily` when >=2 scripts succeed
- Skips synthesis/reflection notes to avoid self-referential loops
