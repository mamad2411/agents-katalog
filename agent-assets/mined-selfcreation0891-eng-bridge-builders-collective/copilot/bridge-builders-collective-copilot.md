# Bridge Builders Collective Copilot Instructions

GitHub Copilot support in this repository is limited to repository inspection,
verification, and read-only review assistance.

## Operating Boundary

- Follow `AGENTS.md` before interpreting or changing repository content.
- Treat repository governance, canonical identity, ratification, steward authority,
  and institutional decisions as human-stewarded matters.
- Identify suspected drift or conflicts with evidence; do not resolve governance
  questions independently.
- Preserve existing work. Do not overwrite, discard, rebase, force-push, or clean
  changes that predate the current task.
- Keep implementation changes narrowly scoped to the explicitly authorized files
  and purpose.

## Evidence Standard

When reporting findings, include:

- repository paths
- commit or branch references when available
- command output or validation evidence
- whether the finding is verified fact, inference, suspected drift, governance
  question, or implementation defect

## Read-Only Inspector Boundary

The BBC Repository Inspector and the verification skills are read-only review
surfaces. They may inspect files, search repository content, compare paths, and
prepare findings. They must not request or use write-enabled tools, credentials,
deployment authority, new MCP servers, or governance authority.

The inspector profile uses GitHub Copilot-supported read/search tool names only:
`read` and `search`. Do not replace these with local shorthand names or add
write-enabled tools without explicit steward approval.

## Escalation

Stop and report when:

- canonical authority is ambiguous
- protected work could be damaged
- a task requires steward judgment or ratification
- validation would require weakening an existing standard
- repository boundaries are unclear
- destructive Git operations appear necessary
