---
name: ctx-add-use-case
description: Implement a new use case for an existing feature, maintaining consistency with product definitions and engineering contracts. Use when adding behavior to an already-mapped feature.
metadata:
  author: nicolasse
  version: "2.0.0"
---

# Add Use Case

Implements a new use case for an existing feature, maintaining consistency with product definitions and engineering contracts.

## Workflow

### 1. Feature Resolution

List all directories under `context/`.
Match the user's request to the most likely feature directory based on semantic understanding. Examples:
- "follow up", "followUps", "seguimiento" → `follow-up/`
- "booking", "reservas", "citas" → `booking/`

**If you are confident in the match** (single obvious candidate), confirm to the user which feature you matched and proceed.
**If ambiguous** (multiple plausible matches or no clear match), list the available features and ask the user to pick one before continuing.

Never guess. Never create a new feature directory in this command.

### 2. Duplicate Check

Read `context/{feature}/product.md`.
Check if the requested use case already exists — consider semantic equivalence, not just exact text match. A use case described differently but covering the same behavior counts as existing.

- If it exists: inform the user and stop.
- If it partially overlaps: inform the user and ask how to proceed.
- If it's new: continue.

### 3. Implementation

Implement the new use case respecting:
- The three context files: `product.md`, `engineering.md`, `implementation.md`
- Existing code patterns and conventions
- The engineering contracts (interfaces, schemas, constraints)

Stay scoped. Only modify files related to the feature. If the change requires touching shared code or other features, stop and report.

### 4. Contract Validation

After implementation, validate the changes against both contracts:

**Product contract (`product.md`):**
- Do all previously defined use cases still work as described?
- Does the new use case behave as requested?
- Are there contradictions with existing product definitions?

**Engineering contract (`engineering.md`):**
- Are all interfaces and contracts respected?
- Do naming conventions and patterns match?
- Are there breaking changes to APIs or data models?

**If validation fails:** revert code changes and report what broke.
**If validation passes:** proceed to context update.

### 5. Context Update

Only after successful validation:

1. **`product.md`** — Add the new use case to the use cases section, following the existing format and level of detail.
2. **`implementation.md`** — Update if the implementation introduced new components, flows, or changed existing ones.
3. **`engineering.md`** — Update only if new interfaces, contracts, or technical constraints were introduced.

### 6. Handoff

Do NOT commit changes. Leave all changes (code + context files) staged or unstaged for the developer to review.

Provide a summary of:
- What was implemented
- What context files were updated and why
- The contract review result
- Any warnings or suggestions

The developer decides when and how to commit.
