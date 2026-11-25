---
name: generic-claudemd-authoring
description: Apply when editing CLAUDE.md or any other .claude/ context file. Keeps the file small and Claude-focused.
metadata:
  stack: [generic]
---

# CLAUDE.md authoring

CLAUDE.md is Claude-only context, not human documentation. Minimise size ruthlessly — every byte burns token budget on every turn.

## Rules

- If a convention is enforced by a hook, do NOT document it in CLAUDE.md. The hook is the source of truth.
- If a procedural behaviour is defined in a skill, do NOT restate it in CLAUDE.md. Link to the skill by name.
- If the `dev-team` plugin already covers a workflow (orchestrator, three-phase, code-review, gates, memory), do NOT duplicate. Point at the plugin entry.
- Only include things Claude needs *proactively* on every turn: stack manifest, entry point, project identity, repo layout, tech-stack table, naming conventions.
- Prefer terse bullets and tables over prose. No motivational language. No "this codebase is awesome" intros.
- No code comments saying "see CLAUDE.md" either — that breeds duplication.

## Anti-patterns

- Repeating the gate definitions inline (they live in `generic-gate-pipeline`).
- Repeating per-stack standards inline (they live in `dotnet-*`, `nextjs-*`, `expo-*` skills).
- "Don't do X" rules with no enforcing hook — write the hook instead.
- Project history, decision narratives, or vendor research summaries — those go in `docs/`.

## Target shape

A useful CLAUDE.md has roughly these sections in this order:

1. Entry point and orchestrator routing
2. Stack manifest (fenced YAML)
3. Project overview (3–5 lines)
4. Partners & vendors table
5. Repository layout
6. Tech-stack table
7. Architecture summary with pointers to per-stack skills
8. Naming conventions
9. Pointer back to this skill ("see generic-claudemd-authoring")

Target ~115 lines. Past 150, a skill is missing.
