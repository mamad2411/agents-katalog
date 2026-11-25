---
name: update-wiki
description: Publish the repo-root wiki/ specification tree to the HW-OpenClaw GitHub Wiki on demand. Use when the user asks to sync, publish, update, or refresh the GitHub Wiki from the version-controlled wiki/ directory.
---

# Update Wiki

Use this skill to publish the version-controlled `wiki/` tree to the GitHub Wiki.

The source of truth is always the repo-root `wiki/` directory. The GitHub Wiki is only a generated mirror for web browsing.

## Workflow

1. Make sure the local branch contains the intended `wiki/` content.
1. Run a dry run first:

```sh
python3 .codex/skills/update-wiki/scripts/update-wiki.py --dry-run --output /tmp/hw-openclaw-wiki-preview
```

1. Inspect the generated preview if the change is non-trivial.
1. Publish:

```sh
python3 .codex/skills/update-wiki/scripts/update-wiki.py
```

## Behavior

- clones `https://github.com/<owner>/<repo>.wiki.git` into a temporary local directory
- replaces the clone content with the local `wiki/` tree
- preserves the `wiki/` directory structure and file names as much as possible
- copies Markdown pages and supported assets exactly as they live under `wiki/`
- commits and pushes only when generated wiki content changed
- removes the temporary local wiki clone before the script exits

## Authentication

The script uses normal Git commands.

If pushing fails, fix the local Git credential setup the same way you would for any other `git push` to GitHub.

## Rules

- Do not edit the GitHub Wiki web UI as the source of truth.
- Do not publish unreviewed wiki changes.
- Do not keep the local wiki clone after publishing.
- If generated wiki output looks wrong, fix the versioned `wiki/` source or the script, not the generated Wiki repo by hand.
