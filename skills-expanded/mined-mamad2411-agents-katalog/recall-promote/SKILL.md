---
name: recall-promote
description: "Use when recurring themes need promotion to permanent MEMORY.md entries, or when the user mentions 'promote', 'recurrence', or 'recurring themes'."
---

# Recall Promote

Review `~/.tandem/state/recurrence.json` and the project MEMORY.md.

For each theme with count >= 3:
1. Check if MEMORY.md already covers it
2. If not, draft a [P1] entry with (observed: first_seen_date) capturing the theme's meaning
3. Present proposed entries for user approval
4. After approval, append to MEMORY.md

## Output format

For each theme that needs promotion:
```
Theme: <slug> (count: N, first seen: YYYY-MM-DD)
Status: [already covered | needs promotion]
Proposed entry: [P1] <description> (observed: YYYY-MM-DD)
```

If all themes are already covered, report: "All recurring themes are represented in MEMORY.md."

## Notes

- Only promote themes, never demote existing [P1] entries
- Use the theme slug's natural language form in the entry (e.g., "error-handling" becomes "error handling")
- The (observed: date) should use the theme's first_seen date from recurrence.json
