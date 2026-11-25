---
name: rw-crm-components-planner
description: Create a read-only initial implementation plan from relevant RW CRM UI context.
---

# RW CRM Components Planner

Discover the relevant Figma, UI-library, CRM-code, test, accessibility, and recursive Confluence context for the task. Consult the approved learning ledger. Return a bounded initial plan with scope, files, interfaces, risks, verification, and any UI-library-over-Figma decision. For target-repository test verification, follow [references/testing-policy.md](../../references/testing-policy.md) and specify direct Jest commands only.

This skill is read-only. It never approves a plan, proposes code edits, or invokes implementation. Missing or ambiguous context is recorded as a risk rather than guessed.
Planner output must identify the task-scoped context snapshot, source gaps, and library decisions. Discover and retrieve relevant sources on demand through the approved allowlist; do not imply permanent retention of every Figma or Confluence file.

Return the structured plan as the approval source of truth and a `planArtifact` descriptor with `kind: implementation-plan`, `mediaType: text/markdown`, a readable title, a safe `.md` filename, revision, plan ID, and Markdown content. Accept optional `ticketKey` and `artifactRevision` inputs; default the initial artifact to revision 1. Attach the descriptor as a conversation Markdown artifact without modifying the target repository. Keep previous revisions available. Never use a SHA-256 value as the artifact title, filename, or content.

If the host cannot attach the artifact, state that the attachment is unavailable and render the Markdown inline under the intended filename. Do not replace it with a hash-named artifact.
