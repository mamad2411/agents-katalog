---
name: fallback-source-presence-sufficiency
description: "When a declared source is only a fallback default, treat any existing materialized source as satisfying the contract instead of forcing a replacement."
metadata:
  author: ychampion
---

# SKILL: Fallback Source Presence Sufficiency
**Domain:** extensions-mcp  
**Trigger:** Apply when a configuration entry represents a fallback source and existing materialized state from another source should be preserved if it already satisfies presence.
**Source Pattern:** Distilled from reviewed extension lifecycle and source-reconciliation patterns.

## Core Method
Distinguish fallback intent from authoritative source declarations. If the declared source exists only to satisfy the missing case, then the presence of any already-materialized source is enough and should be treated as up to date. This prevents the reconciler from overwriting valid state merely because the default source differs from the source that actually materialized the resource.

## Key Rules
- Carry a flag that distinguishes fallback/default declarations from authoritative source directives.
- For fallback entries, compare on presence first and skip source-equality enforcement once materialized state exists.
- Preserve seeded, mirrored, or previously installed sources when they already satisfy the resource contract.
- Restrict this relaxation to fallback intent only; authoritative declarations should still drive updates when the source changes.
- Document why fallback entries are special so future maintainers do not "simplify" the logic back into destructive churn.

## Example Application
If a package manager uses an official registry as a fallback only when no mirror is installed, leave an already-seeded internal mirror alone. The fallback declaration should not force a re-download from the official registry just because the source URLs differ.

## Anti-Patterns (What NOT to do)
- Do not compare fallback declarations against materialized sources as if they were hard directives; you will overwrite healthy state unnecessarily.
- Do not erase the distinction between "default if missing" and "must come from here"; they drive very different reconcile behavior.
