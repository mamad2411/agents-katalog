---
name: skill-content-audit
version: 1.0.0
description: Standardized content depth audit workflow for Hermes skill libraries — check frontmatter, related_skills, size
  limits, dead links, and CRLF hygiene across categories.
metadata:
  hermes:
    triggers:
    - content depth audit
    - skill audit
    - frontmatter check
    - related_skills audit
    - skill library audit
    - trigger check
    - size limit check
    tags:
    - curation
    - audit
    - frontmatter
    - triggers
    - related-skills
    - skill-library
    - quality
    related_skills:
    - github
    - skill-library-maintenance
author: Hermes Agent
license: MIT

---

# Skill Content Depth Audit

Standardized workflow for auditing a Hermes skill library's cross-reference health and frontmatter quality. Use when reviewing a category of skills for completeness, consistency, and structural integrity.

## When to Use

- Asked to "check the skill library", "audit skills", "triggers check", "frontmatter hygiene"
- Reviewing a new or existing category for quality (triggers, related_skills, tags)
- Before/after batch-importing skills from a hub
- As part of a Scribe / curation pulse

## Audit Checklist

For each skill in the target category, verify these 10 checks:

| # | Check | What to look for |
|---|-------|------------------|
| 1 | Triggers | `metadata.hermes.triggers` list present — NOT root-level `triggers:` |
| 2 | Tags | `metadata.hermes.tags` present (not root-level `tags:`) |
| 3 | Related Skills | `metadata.hermes.related_skills` — filled, not empty, no dead links |
| 4 | Root-level keys | Zero `triggers:`, `tags:`, `related_skills:` at YAML root |
| 5 | Size check | SKILL.md under 95KB (preemptive threshold) / 100KB (hard load limit) |
| 6 | Dead links | Every `related_skills` name resolves to an existing SKILL.md in the library |
| 7 | CRLF handling | Files with `\r\n` line endings — `patch()` works, `skill_manage(action='patch')` silently fails |
| 8 | Reference integrity | Every `references/*`, `scripts/*`, `templates/*` linked in body exists on disk |
| 9 | Content overlap | Two skills covering the same domain — flag for consolidation |
| 10 | Orphan detection | Skill referenced by zero peers — evaluate if intentional |

## Common Findings

- **Missing `related_skills`** — The single most common gap. Batch-imported skills almost always have zero cross-references. Add natural peers from the same category or adjacent categories (e.g., `imessage` → `[apple-notes, findmy, macos-computer-use]`).
- **Root-level `triggers:`** — YAML parses but inference engine ignores root-level keys when `metadata.hermes` block exists. Migrate under `metadata.hermes.triggers`.
- **CRLF silent failure** — `skill_manage(action='patch')` reports "1 replacement applied" success on `\r\n` files but never modifies them. Use the standalone `patch()` tool or Python byte-level replacement instead.
- **Dead `related_skills`** — References to consolidated or renamed skills that no longer exist. Grep the skill tree to verify every referenced name resolves.
- **Size threshold breached** — Skills over 100KB silently fail to load. Extract large sections (>15KB) to `references/` files.
- **Duplicated content in body** — Inline pitfalls repeated in reference files waste KB on skills approaching their limit. Replace with brief links to the reference file.

## Patching by File Type

| Line ending | Safe patching tool | Unsafe tool | Notes |
|-------------|-------------------|-------------|-------|
| LF (Unix) | `patch()` or `skill_manage(action='patch')` | — | Both work |
| CRLF (Windows) | `patch()` standalone tool | `skill_manage(action='patch')` | Standalone patch() handles CRLF correctly |
| Mixed/bulk | Python pathlib byte-level replacement | `sed -i` on MSYS | `sed -i` gets cross-device-link errors on MSYS |

### Python Byte-Level Replacement (Bulk CRLF)

```python
from pathlib import Path
for f in Path("skills/").rglob("SKILL.md"):
    text = f.read_bytes()
    old = b"old\r\ntext"
    new = b"new\r\ntext"
    if old in text:
        f.write_bytes(text.replace(old, new))
```

## Verification

After patching, verify with Python YAML parsing:

```python
import yaml
from pathlib import Path
errors = 0
for f in sorted(Path("skills/").rglob("SKILL.md")):
    parts = f.read_text(encoding="utf-8").split("---", 2)
    fm = yaml.safe_load(parts[1])
    hermes = fm.get("metadata", {}).get("hermes", {})
    if "triggers" not in hermes:
        print(f"❌ {f}: missing triggers")
        errors += 1
    if "tags" not in hermes:
        print(f"❌ {f}: missing tags")
        errors += 1
    if not hermes.get("related_skills"):
        print(f"⚠️  {f}: empty related_skills")
if errors == 0:
    print("✅ All skills pass frontmatter check")
```

Also CRLF-safe grep for counting:

```bash
grep -a "triggers:" skills/*/SKILL.md | wc -l
```

Regular `grep` (without `-a`) silently skips CRLF files it misidentifies as binary.

## Size Limit Extraction Pattern

When a SKILL.md approaches 95KB, extract its largest sections:

1. Identify the largest section (find with `grep -n "^## "` and measure byte ranges)
2. Move section content to `references/<section-slug>.md`
3. Replace inline content with a brief summary + link to the reference file
4. Verify frontmatter intact, section flow preserved, total size now under 85KB

## Pitfalls

- Don't rely on `skill_manage(action='patch')` for CRLF files — it silently no-ops.
- Don't use `grep` without `-a` on mixed CRLF trees — it misses CRLF files entirely.
- Don't trust "no warnings" or "1 replacement applied" as proof of correctness — always re-read the file post-patch.
- Don't use `sed -i` on MSYS/Windows — it frequently fails with cross-device-link errors.
- Don't append to PULSE.md by reading with offset/limit then writing back — the write silently truncates to the partial read. Read the full file first.
- Don't claim "all skills have triggers" without grepping with `-a` on a CRLF-containing tree — you will undercount by 60-93%.
- Don't dispatch more than 3 subagents per batch for content depth audits — the 3-project max_concurrent_children limit applies.
