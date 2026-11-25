---
name: blueprint-publish
description: Curate a working blueprint and scratchpad into a team-ready Notion page with collaborative review of every section before publishing. Use when user wants to publish the blueprint, push to Notion, or share the blueprint with the team.
---

# Blueprint Publish

Curate working docs (blueprint + scratchpad) into a team-ready Notion page. Every section is reviewed before publishing. Nothing goes to Notion without explicit approval.

## Process

### 1. Pre-flight

1. Ask for the blueprint and scratchpad locations if not already known.
2. Read both working docs.
3. Verify all blueprint sections are populated.
4. Flag sections with hedging language or unresolved items.
5. If issues found: "Fix now or publish as-is with them in Risks/Open Questions?"

### 2. Curation pass — blueprint (above the fold)

For each section:
1. Present the section as it would appear in Notion.
2. Ask: "Does this read right for the team? Anything to tighten up?"
3. User approves or revises.

See [curation-checklist.md](curation-checklist.md) for what to watch for.

### 3. Curation pass — scratchpad (below the fold)

For each major thread (spike findings, rejected alternatives, code exploration, open threads):
1. "Should this go into the Notion scratchpad, stay private, or get dropped?"
2. For items going to Notion, ask if wording needs cleanup for a team audience.

### 4. Notion publishing

1. Show a final summary of what will be published. Wait for confirmation.
2. Find the org's Projects database in Notion (search by name, or ask user for URL).
3. Create the blueprint page.
4. Populate above-the-fold sections from curated blueprint.
5. Populate collapsible scratchpad from curated selections.
6. Link Linear tickets referenced in estimates.
7. Return the Notion page URL.

### 5. Post-publish

Suggest next steps:
- "Share this in the project channel for manager review before concept review."
- If testing plan hasn't been created: "You'll also need a testing plan — use `write-a-test-plan`."

Does not auto-trigger any other skills.

## Conventions

- No writes to Notion without explicit approval.
- Writing tone: factual, concise. No emoji. No cheerful AI filler.
