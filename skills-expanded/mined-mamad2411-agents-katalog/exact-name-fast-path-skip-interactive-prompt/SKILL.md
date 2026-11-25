---
name: exact-name-fast-path-skip-interactive-prompt
description: When a search keyword matches exactly one catalog entry's `name` field, skip the numbered-list picker and resolve directly. A UX pattern for CLIs with a "search + pick" flow that saves a round-trip for the common script/demo/exact-slug case.
category: cli
tags: [cli-ux, argparse, interactive-prompt, fast-path, catalog-search]
triggers:
  - "exact name match skip prompt"
  - "catalog search fast path"
  - "single-result picker"
  - "interactive flag opt-in"
  - "--interactive opt out"
source_project: skills-hub-v2.6.3
version: 0.1.0-draft
---
