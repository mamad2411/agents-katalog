---
name: microcopy
description: "The small words that shape big experiences. Button labels, tooltips, confirmations, placeholders, and the 3-word strings that determine whether a product feels polished or half-finished. Use during any copy audit pass."
---

# Microcopy

The small words that shape big experiences.

## How to use

- `/microcopy` Apply microcopy constraints to this conversation.

## Constraints

### Buttons
- MUST describe the action outcome, not the mechanical action
- "Create project" not "Submit". "Send invite" not "Confirm".
- Destructive actions: name what's being destroyed ("Delete project" not "Delete")
- MUST use sentence case, not Title Case or ALL CAPS
- Loading state: show progress ("Saving..." not "Please wait")

### Confirmations and Dialogs
- Title: what's about to happen
- Body: what it means and whether it's reversible
- Primary button: the action being confirmed
- Secondary button: "Cancel" (not "No" or "Go back")
- NEVER use "Are you sure?" without explaining the consequence

### Tooltips and Help Text
- MUST add information the user doesn't already have
- Keep under 15 words. If it needs more, use a help page.
- SHOULD answer "why" not just "what" (why this field exists, not just what to put in it)
- NEVER use tooltips as the only way to explain essential functionality

### Empty and Placeholder Text
- Input placeholders: show the expected format, not the label ("name@company.com")
- MUST NOT use placeholders as labels (they disappear on focus)
- Empty search: suggest search terms or show popular queries
- NEVER use "N/A", "null", "undefined", or "—" where a human-readable message belongs

### Error Micro-Copy
- MUST say what went wrong in plain language
- MUST say how to fix it
- Place error text adjacent to the field that caused it
- Use red for errors, but don't rely on color alone (add an icon or text prefix)
