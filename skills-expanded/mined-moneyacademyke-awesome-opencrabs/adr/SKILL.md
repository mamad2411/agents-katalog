---
name: adr
description: Create, review, index, or supersede Architecture Decision Records for a repository using OpenCrabs-native file reads, plans, and verification.
---

# ADR Skill

Use this when the user asks for an ADR, architecture decision, decision log, or wants to capture why a technical direction was chosen.

Inspired by Ruflo's `ruflo-adr`, but rewritten for OpenCrabs.

## Workflow

1. Inspect project directives first: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursor/rules/*.mdc`, `.windsurfrules`, `.clinerules` if present.
2. Find existing ADR locations:
   - `docs/adrs/`
   - `docs/adr/`
   - `architecture/decisions/`
   - `specs/decisions/`
3. If none exists, create `docs/adrs/` unless project conventions say otherwise.
4. Use sequential numbering: `0001-title-kebab.md`.
5. ADR sections:
   - Title
   - Status: Proposed | Accepted | Superseded
   - Date
   - Context
   - Decision
   - Consequences
   - Alternatives considered
   - Verification / follow-up
6. If changing existing architecture, cross-link superseded ADRs instead of deleting them.
7. Validate by reading the written file and ensuring links/numbering are coherent.

## Tool routing

- Use `glob`/`grep`/`read_file` for discovery.
- Use `write_file` for new ADRs and `edit_file` for index updates.
- Use `plan` for multi-ADR or repo-wide architecture work.
- Do not commit or push unless explicitly approved.

## Output

Report the ADR path, status, and decision in one tight summary.
