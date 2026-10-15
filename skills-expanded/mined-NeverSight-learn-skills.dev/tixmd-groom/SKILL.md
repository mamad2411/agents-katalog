---
name: tixmd-groom
description: Groom and refine a tixmd ticket. Converts spikes into actionable tickets with acceptance criteria, or improves existing tickets. Use when the user wants to refine, elaborate, or improve a ticket.
---

# /tixmd-groom

Refine any ticket — elaborate spikes into actionable tickets, or improve criteria on existing ones.

## Instructions

1. **Detect the target ticket** using the first match:
   - If args were passed (e.g. `/tixmd-groom spike-cli`), use that as the ticket ID
   - Otherwise, run `npx tixmd list` to get all tickets, then identify **groomable** tickets — spikes (no acceptance criteria) and tickets that could benefit from refinement. Present the groomable tickets as a numbered list and ask the user to pick one

2. **Read the ticket file** from `.tixmd/tixs/<ticket-id>.md` to understand its current state.

3. **Read `.tixmd/project.md`** for project context and conventions (ticket style, commit strategy, definition of done). Apply these conventions when refining the ticket.

4. **Branch based on ticket type:**

### For spikes (no acceptance criteria)

- Ask the user exploratory questions to understand what this spike is about:
  - What are the options or approaches?
  - What constraints or requirements exist?
  - What are the key tradeoffs?
- Recommend an approach, but present alternatives with enough context for the user to decide
- Once the direction is clear, propose acceptance criteria that define "done"
- Present the refined ticket (title, description, criteria) for user review
- After approval, create a new actionable ticket file at `.tixmd/tixs/<new-ticket-id>.md`:
  - Use a descriptive kebab-case ID (not `spike-*`)
  - Include appropriate frontmatter (labels, dependencies, created)
  - Write the refined description and acceptance criteria in the body
- **Mark the spike as resolved** by adding `groomed_tickets: [<new-ticket-id>]` to its frontmatter — this changes its status to `resolved` and preserves the trail from spike to actionable ticket

### For actionable tickets (has acceptance criteria)

- Discuss with the user what needs refinement:
  - Are criteria clear and verifiable?
  - Is anything missing?
  - Should the scope be adjusted?
- Propose changes and get user approval
- Edit the ticket file directly, preserving existing frontmatter

5. **When editing the ticket file**, always preserve existing YAML frontmatter fields. Only modify the markdown body (title, description, criteria).

6. Confirm the changes and show the updated ticket.
