---
name: okf
description: Use when the user mentions OKF, an OKF knowledge base/bundle, ingesting into or querying a knowledge bundle, or wants to create a new OKF knowledge base — even if they just say "my KB" while a folder containing .aai/ is nearby.
---

# OKF router

This skill contains no OKF logic. The bundle's own ambient copy is always
authoritative — never substitute newer instructions from elsewhere.

1. **Find the bundle root:** the nearest folder (cwd, then ancestors, then a
   folder the user names) containing `.aai/`.
2. **Found one:** read and follow that bundle's
   `.aai/skills/okf-management/SKILL.md` and the files it points to. All
   paths, scripts, and rules come from the bundle.
3. **No bundle:** offer to create one:
   ```bash
   python3 "/Volumes/Extreme Pro/users/loudalo/GitHub/OKF/tools/upgrade_ambient.py" \
       "/Volumes/Extreme Pro/users/loudalo/GitHub/OKF" <new-kb-folder> --apply
   ```
   Then start the bundle's own Initialize interview (first ingest into an
   empty bundle). The parent of a new KB must be inert — no ancestor
   CLAUDE.md or .git — and the KB should get its own `git init`.
