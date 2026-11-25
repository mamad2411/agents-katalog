---
name: canonical-root-marketplace-path-normalization
description: "Normalize relative extension source paths against a canonical repo root so shared marketplace records stay stable across worktrees."
metadata:
  author: ychampion
---

# SKILL: Canonical-Root Marketplace Path Normalization
**Domain:** extensions-mcp
**Trigger:** Use when project settings declare relative extension paths but the shared registry spans multiple worktrees or checkouts.
**Source Pattern:** Distilled from reviewed shared-registry path normalization logic.

## Core Method
Resolve relative local source paths against the repository's canonical root rather than the current worktree directory before comparing them to shared registry entries. This produces one stable identity for a shared record, prevents worktrees from overwriting each other with checkout-specific paths, and avoids dead paths when temporary worktrees disappear. Normalize before diffing so equivalent repo-relative settings are treated as the same source.

## Key Rules
- Normalize shared local paths against the canonical repo root, not the active worktree.
- Run normalization before diff comparison so equivalent sources do not look like drift.
- Preserve a valid existing entry when a transient worktree path is missing but the canonical source is still the same.

## Example Application
If a repo declares `./plugins/internal`, normalize it against the canonical checkout root so every worktree resolves to the same shared registry path.

## Anti-Patterns (What NOT to do)
- Do not stamp worktree-specific absolute paths into a user-global registry.
- Do not treat equivalent repo-relative paths as true source changes.
- Do not overwrite a valid shared entry with a dead temporary path.
