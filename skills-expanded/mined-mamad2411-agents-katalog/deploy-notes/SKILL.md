---
name: deploy-notes
description: Preview release notes for an Infiquetra tag-promotion deployment candidate.
---

# Deploy Notes

Preview deployment notes before promotion.

## Procedure

1. Read `../deploy-state/SKILL.md`.
2. Use `../../scripts/preview_release_notes.py` to inspect the commit range.
3. Include issue links, PR links, deployment tags, checks, and risk notes when available.
4. Do not create GitHub releases unless the user explicitly asks for that mutation.

```bash
python3 plugins/deploy/scripts/preview_release_notes.py \
  --repo infiquetra/example \
  --base staging-v1.2.2 \
  --head v1.2.3
```
