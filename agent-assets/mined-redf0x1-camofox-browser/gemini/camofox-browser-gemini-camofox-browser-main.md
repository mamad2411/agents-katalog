# GEMINI.md — CamoFox Quick Rules

Essential pattern: snapshot-first, ref-driven browser automation with explicit user scope.

## Key Rules
- Start with tab open/create, then run snapshot before interacting.
- Use refs (`eN`) for click/type/fill/press; selector usage is fallback only.
- Re-run snapshot after navigation or major DOM mutation.
- Prefer structured output (`--format json`) for automation pipelines.
- Use encrypted auth vault injection; never print or persist plaintext secrets.

## Context
- Base URL: `http://localhost:9377`
- Core entities: `userId`, `tabId`, `sessionKey`
- Common loop: navigate -> snapshot -> act -> snapshot

For complete details and authoritative project guidance, see `AGENTS.md`.
