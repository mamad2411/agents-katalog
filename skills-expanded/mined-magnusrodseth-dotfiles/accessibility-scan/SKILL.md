---
name: accessibility-scan
description: "Locates accessibility violations in a selected page and source. Use when auditing a live frontend or a configured accessibility target."
---

# Accessibility scan

Read AGENTS.md and the repository's docs for the browser tool, scan command,
accesslint configuration, target URLs and source maps. Discover actual tools in
the active harness. Personal MCP names, browser profiles and global skills are
not prerequisites. Follow the user's browser and credential policy.

1. Confirm the requested target, viewport, authentication state and test data.
   Verify that a local listener belongs to this checkout. Record unavailable
   setup rather than scanning a different app silently.
2. Run the configured scan or supported accessibility engine. Use local target
   configuration rather than a hardcoded port. Capture rule, impact, affected
   element, accessible name, selector and relevant DOM evidence.
3. Resolve each concrete violation to its owning component/style with source
   maps, selectors and actual code. Report exact source locations and explain
   the user impact. Engine warnings and automated passes do not establish full
   accessibility; note keyboard, focus, reading-order and visual checks needed.
4. Return deduplicated findings, coverage and limits. Preserve existing baseline
   violations separately from new ones when comparison evidence exists. A scan
   request grants no automatic fix, baseline suppression or tracker mutation.
