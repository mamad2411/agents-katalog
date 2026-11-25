---
name: reflect
description: Generate self-reflection report and save as Obsidian note. Use when user asks for reflection, system analysis, or /reflect.
---

# Self-Reflection Skill

Analyzes system behavior and effectiveness via SystemBehaviorTracker. Generates actionable improvement recommendations.

## Usage

```bash
python3 _scripts/self_reflection.py reflect [--days N] [--save]
python3 _scripts/self_reflection.py analyze [--days N]
python3 _scripts/self_reflection.py improve [--days N] [--apply]
```

- `reflect`: Generate reflection report (--save writes to vault)
- `analyze`: Analyze behavior patterns
- `improve`: Generate improvement plan (--apply to implement)

## Output

`_logs/reflection_log.json` — performance tracking
