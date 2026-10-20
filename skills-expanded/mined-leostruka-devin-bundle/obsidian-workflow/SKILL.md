---
name: obsidian-workflow
description: Use when the user wants to build or update a local codebase wiki in Obsidian with architecture diagrams, source-linked documentation, hierarchical pages, auto-refresh, effort levels (low/medium/high), Deep Research pass (architecture critique, anti-patterns, tech debt), and conversational Q&A via deep-mode; or reorganize, refactor, or restructure an Obsidian vault, knowledge base, or documentation folder; or audit, validate, or fix Obsidian project wikis (broken wikilinks, source citations, diagrams, sensitive info, language); or compare wiki knowledge by source session or source type to surface cross-session blind spots.
triggers: [user]
---
# obsidian-workflow

A unified skill covering the full Obsidian knowledge lifecycle: **build** a codebase wiki, **reorganize** a vault, **audit** wiki quality, and **compare** knowledge across sessions to surface blind spots. Each mode is independent — invoke the one matching the user's request. Full detail lives in `modes/<mode>.md` — read it when you enter that mode.

## Mode selector

| Mode | Trigger | What it does | Detail |
|------|---------|--------------|--------|
| Build Wiki | "Document this codebase / project", "Build a local wiki for this repo", "Create architecture diagrams with source links", "Map all modules, functions, and dependencies with code references", "Visualize the system with Mermaid diagrams", updating an existing engineering wiki after code changes | Scaffolds and fills a meticulous, SRS/ISO-style local codebase wiki in an Obsidian vault with source-linked documentation, hierarchical pages, Mermaid diagrams, a re-index workflow, and a project page + MOC linked into the parent context map. Capture cross-session insights with `memory-management`. | `modes/build-wiki.md` |
| Reorganize Vault | "Reorganize my vault", "This vault is a mess, help me structure it", "Plan a refactoring of my documentation", "My projects are scattered, organize them", "Audit my knowledge base structure", after a merger/acquisition that combined knowledge bases, when a vault has grown organically and needs structural correction | Diagnoses organizational problems in a knowledge base, selects adaptive methodologies that fit the content, plans a safe refactoring, and executes with wikilink validation | `modes/reorganize-vault.md` |
| Audit Wiki | "Audit my wikis", "Check for broken links in the vault", "Validate source citations across all project wikis", "Find sensitive information in the vault", "Fix template broken links", before committing/syncing the vault, after bulk updates to wiki content | Audits and validates Obsidian project wikis against established standards — broken wikilinks, missing source citations, missing diagrams, sensitive information, language inconsistencies; can fix common template issues | `modes/audit-wiki.md` |
| Cross-session Comparison | "Compare wiki knowledge by source session", "Show me what devin_session knows vs manual", "Surface cross-session blind spots", browsing/filtering wiki pages by source provenance | Browses and compares Obsidian wiki knowledge filtered by source provenance, surfacing cross-session blind spots via diff/map views built from `.manifest.json` | `modes/cross-session-comparison.md` |
