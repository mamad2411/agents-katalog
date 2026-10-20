> ⚠️ PROJECT SCOPED: Read from .claude/ only.

Find where something lives AND its blast radius — both in one pass.

## Local Cache First

1. Read .claude/skills/_modules-index.md ← check index before anything else
   Cache hit: module listed with path → go directly to that file.
   Cache miss: fall through to full search.

## Find location

2. Read .claude/memory/dependencies.md if needed
3. Read relevant .claude/modules/ files
4. Search actual codebase

## Blast radius

5. Trace direct and indirect dependencies from the located thing

## Report

### Location

- Exact file paths and line numbers
- Which module owns it
- What imports it / what it exports to

### Impact if changed

- Risk: 🟢 Low / 🟡 Medium / 🔴 High
- Direct impact (files + paths)
- Indirect impact (files + paths)
- Tests to check
- Recommendation
