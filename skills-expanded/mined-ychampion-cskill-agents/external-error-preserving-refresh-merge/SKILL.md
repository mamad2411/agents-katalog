---
name: external-error-preserving-refresh-merge
description: "Merge fresh refresh diagnostics with externally owned errors so one subsystem reload does not erase valid adjacent failures."
metadata:
  author: ychampion
---

# SKILL: External Error Preserving Refresh Merge
**Domain:** plugin-installation
**Trigger:** Use when a refresh path recomputes its own errors but neighboring subsystems maintain related diagnostics that should survive the reload.
**Source Pattern:** Distilled from reviewed refresh-diagnostic ownership and merge implementations.

## Core Method
Treat refresh-time errors as one slice of the diagnostic picture rather than the whole state. Preserve errors owned by adjacent subsystems, merge in the freshly computed errors from the current reload, and deduplicate by a stable key so the result stays current without erasing still-relevant external failures. This lets a subsystem update what it owns while respecting error streams maintained elsewhere.

## Key Rules
- Preserve only the error sources the current refresh is not authoritative for.
- Build stable dedupe keys from error type and source, not from list position or timing.
- Merge preserved external errors with fresh refresh errors so users see one coherent diagnostic surface.
- Keep the ownership boundary explicit so future refactors know which subsystem may overwrite which errors.

## Example Application
If a plugin refresh recomputes loader failures while a language-server manager separately owns connection diagnostics, preserve the language-server errors and merge in the fresh loader errors so the UI retains the full current problem set.

## Anti-Patterns (What NOT to do)
- Do not replace the entire error array on every refresh; that silently drops failures from other live subsystems.
- Do not dedupe by array position or timestamp alone; equivalent errors need stable identity.
