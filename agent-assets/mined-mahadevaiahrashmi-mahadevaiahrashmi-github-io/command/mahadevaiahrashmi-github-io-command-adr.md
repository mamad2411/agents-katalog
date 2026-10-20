<!-- agent-notes: { ctx: "create new ADR from template", deps: [docs/adrs/template.md], state: active, last: "archie@2026-02-12" } -->
Create a new Architecture Decision Record for: $ARGUMENTS

Steps:
1. Determine the next ADR number by checking existing files in `docs/adrs/`.
2. Use the template at `docs/adrs/template.md`.
3. Fill in the context, decision, and consequences based on the topic provided.
4. Save as `docs/adrs/NNNN-<slug>.md` where NNNN is the zero-padded number and slug is a kebab-case title.
5. Add agent-notes frontmatter per `docs/methodology/agent-notes.md`.
