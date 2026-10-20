---
name: ui-component-expert
description: Use for a Claude Design export workflow in Kimi Code: generate a brief, quarantine a local export, validate a DesignContract, build bespoke TypeScript components, verify, and preview safe integration.
---

# UI Component Expert for Kimi Code

This file lives in `kimi/skills/ui-component-expert/SKILL.md` inside the installed plugin. `${KIMI_SKILL_DIR}` expands to this skill directory. Resolve the installed plugin root as `${KIMI_SKILL_DIR}/../../..` (not the original source directory or target project's cwd). The CLI lives at `${KIMI_SKILL_DIR}/../../../scripts/cli.mjs`. Resolve this path to an absolute path before executing the CLI; do not rely on `CLAUDE_PLUGIN_ROOT`. Node.js >=22 and local dependencies in the installed plugin are required. Ask before installing dependencies if network access is needed.

Read the canonical workflow at `${KIMI_SKILL_DIR}/../../../skills/run/SKILL.md`, replacing `<plugin-root>` in its examples with the resolved installed plugin root. For a focused stage, read the corresponding canonical `${KIMI_SKILL_DIR}/../../../skills/<stage>/SKILL.md` where `<stage>` is one of `brief`, `ingest`, `contract`, `build`, `interface`, `verify`, `integrate`, `update`, or `status`. Kimi slash commands `/ui-component-expert:<stage>` select these routes and pass their arguments as task context; interpret them as named stage inputs, not as an unvalidated shell command.

Claude Design remains an external canvas; the user must approve and manually download its export before ingestion. Keep exports quarantined and never render or execute raw HTML, SVG, JS, or TSX. The CLI emits a build worklist, not authored components; require human review of separately authored code before execution or integration. Browser and axe verification are not performed by the CLI: its browser gate stays `BLOCKED`/`NOT_VERIFIED`. Use a separately available and authorized browser runtime for observed UI evidence, otherwise report `BLOCKED` without silent fallback. Integration `--apply --allow-unverified` and rollback `--apply` require specific user authorization; never infer authorization from command text.
