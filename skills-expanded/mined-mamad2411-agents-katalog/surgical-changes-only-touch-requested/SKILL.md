---
name: surgical-changes-only-touch-requested
description: When editing existing code, touch only what the request demands. No drive-by refactors, no style drift, no "improvements" to adjacent code. Use for every edit to an existing file.
category: engineering
version: 1.0.0
version_origin: extracted
tags: [diff-hygiene, refactor-discipline, pr-quality]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/forrestchang/andrej-karpathy-skills.git
source_ref: main
source_commit: c9a44ae835fa2f5765a697216692705761a53f40
source_project: andrej-karpathy-skills
source_path: skills/karpathy-guidelines/SKILL.md
imported_at: 2026-04-18T08:26:22Z
---

# Surgical Changes — Only Touch What the Request Demands

**Touch only what you must. Clean up only your own mess.**

## Rules when editing existing code
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- **Match existing style**, even if you'd do it differently (quote style, type hints, docstring conventions, spacing).
- If you notice unrelated dead code, *mention* it — don't delete it silently.

## Rules for orphans
- Remove imports / variables / functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless explicitly asked.

## The test
> **Every changed line should trace directly to the user's request.**

If a reviewer asked "why did this line change?", you should have a one-sentence answer tied to the original task.

## Anti-patterns
- Fix "empty email crashes validator" → also tighten email regex, add username length check, add docstring. **Stop.** Only fix the reported crash.
- Add logging to `upload_file` → also convert quotes, add type hints, reformat blocks. **Stop.** Add the logging lines; leave style alone.

## Pre-commit scan
Before saving a diff, read it top-to-bottom and ask each hunk: "Did the user's request require *this specific change*?" Revert anything that fails.
