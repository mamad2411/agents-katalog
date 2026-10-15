---
name: snap-issues
description: >
  Turn current context, source references, and repo understanding into
  independently grabbable GitHub issues. Use when the user wants to break down a
  PRD, plan, spec, idea discussion, or implementation conversation into vertical
  issues agents can pick up.
---

Take conversation/PRD/spec context and codebase understanding and produce independently grabbable GitHub issues.

## Process

1. Gather context:

Work from whatever is already in the conversation context. If the user passes an issue reference, PR, URL, or path as an argument, fetch it recursively and read the relevant body, comments, and linked context.

2. Explore the codebase:

If you have not already explored the codebase, do so to understand the current state of the code. Issue titles and descriptions should use the project's domain vocabulary, and respect ADRs, tests, interfaces, and prior art in the area you're touching.

3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every relevant layer (schema, API, UI, tests), with enough public contract detail to implement the user-facing behavior
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices, if any, must complete first
- **User stories covered**: which user stories this addresses, if the source material has them

Ask the user:

- Does the granularity feel right? Too coarse or too fine?
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

5. Publish the issues to GitHub

For each approved slice, publish a new issue to GitHub using `references/issue-template.md`.
Assign every created issue to the invoking GitHub user (`--assignee @me` when using `gh issue create`).

Publish issues in dependency order, blockers first, so later issues can reference real GitHub issue identifiers in the `Blocked by` field.

Do not close or modify any parent issue.

6. Post the breakdown (optional)

If the source context includes a GitHub issue, post the final breakdown as a comment on that issue using `references/breakdown-template.md`.
