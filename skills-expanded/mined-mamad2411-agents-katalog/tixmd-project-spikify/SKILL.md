---
name: tixmd-project-spikify
description: Generate spike tickets from the project spec. Reads project.md and existing tickets, identifies areas needing exploration, and creates spike tickets after user review.
---

# /tixmd-project-spikify

Generate spike tickets from the project spec for areas that need exploration.

## Instructions

1. Read the project spec to understand the vision and scope:

```bash
cat .tixmd/project.md
```

2. Get all existing tickets to avoid duplicating spikes:

```bash
npx tixmd list
```

Also read existing spike tickets from `.tixmd/tixs/` to understand what's already being explored.

3. Note the project's **conventions** (ticket style, commit strategy, definition of done) from `project.md`. Use these to guide how spikes are scoped — e.g. if the ticket style is "vertical slices", each spike should explore a user-facing slice, not a horizontal layer.

4. Analyze the project spec and identify areas that need exploration — features, architectural decisions, integrations, or unknowns that don't yet have tickets. Consider:
   - Features mentioned in the spec that have no corresponding tickets
   - Architectural decisions that haven't been explored
   - Integration points that need investigation
   - Gaps between the current state (existing tickets) and the project vision

5. For each identified area, draft a spike with:
   - A concise **title** (e.g. "Explore authentication options")
   - A brief **description** of what needs exploring
   - **Open questions** that the spike should answer
   - Suggested **labels** (follow existing label conventions)

6. Present **all** generated spikes to the user in a numbered list. For each spike, show the title, description, and open questions.

7. Ask the user to review. For each spike, the user can:
   - **Approve** it as-is
   - **Edit** it (title, description, questions)
   - **Reject** it (skip creation)

8. For each approved spike, create it via the CLI:

```bash
npx tixmd new --title "<title>" --body "<body>" --labels "<labels>"
```

Use `\n` for newlines in `--body`. Structure the body as:

```
<description>\n\n## Questions to answer\n\n- <question 1>\n- <question 2>
```

9. After creating all approved spikes, show a summary of what was created.
