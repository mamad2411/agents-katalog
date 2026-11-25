---
name: codex-update-spec
description: "Update durable project specs/docs when implementation changes architecture, workflow, conventions, or recurring lessons."
---

# Update Spec

Use this when a change creates durable behavior or a recurring rule.

1. Identify the affected spec layer:
   - project-level behavior -> `.codex/spec/project/`
   - shared development guidance -> `.codex/spec/guides/`
   - harness lifecycle behavior -> `AGENTS.md`, `README.md`, `PRD.md`, `global/AGENTS.md`, or `templates/workflow.md`

2. Update the smallest relevant spec/doc.

3. If the active task changes durable harness behavior, update the relevant
   spec/doc and mention the update in verification. If no spec update is
   needed, state why in the verification summary.

4. Re-run focused verification.
