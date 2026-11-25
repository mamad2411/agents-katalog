---
name: employment-discovery-summarizer
description: Condense personnel files, HR emails, performance reviews, and other employment records into a case-relevant summary organized around claim-relevant issues. Use whenever the user uploads or pastes personnel files, HR correspondence, performance reviews, or other employment documentation and wants them summarized or reviewed for issues relevant to a wrongful termination, discrimination, or wage claim.
---

# Employment Discovery Summarizer

Condenses personnel files and HR documentation into a summary organized around what matters for the claim, not a chronological restatement of every document.

## Workflow

1. **Build a timeline** of key employment events: hire date, promotions/reviews, any documented performance issues, the protected activity or protected characteristic at issue (if discrimination/retaliation), and the adverse action (termination, demotion, etc.) with its exact date.
2. **Flag temporal proximity** explicitly — how close in time the adverse action followed the protected activity (complaint, leave request, disclosure), since this is often central to retaliation claims.
3. **Flag inconsistencies**: employer's stated reason for the adverse action versus the documented performance history (e.g., termination "for performance" following years of strong reviews), or inconsistent treatment of similarly situated employees (comparators).
4. **Note comparator evidence** if present — other employees in similar roles/circumstances treated differently, with enough detail to identify what makes them comparable.
5. **Note anything favorable to the employee** explicitly (strong review history, employer admissions in emails, absence of prior documented issues) rather than only cataloguing neutral facts.

## Output format

```
## Discovery Summary — [Case name]

### Employment Timeline
| Date | Event |
|---|---|

### Protected activity / characteristic
[what it is, when it occurred/was disclosed]

### Adverse action
[what happened, date, employer's stated reason]

### Temporal proximity
[time gap between protected activity and adverse action]

### Inconsistencies flagged
- [stated reason vs. documented history]

### Comparator evidence
- [similarly situated employee(s), how treated differently]

### Favorable to employee
- [specific point]
```

## Document Output Format

If this summary is wanted as a standalone document, use the `docx` skill:

- **Header:** firm name/logo placeholder, case name, "Discovery Summary — Attorney Work Product" title, date.
- **Timeline table:** real Word table with header row shading, not markdown pipes.
- **Flags** (temporal proximity, inconsistencies, comparator evidence, favorable-to-employee): set apart visually from the neutral timeline, e.g., shaded callout boxes, so they're immediately findable.
- **Typography:** Calibri or Arial 11pt, 1" margins, page numbers if multi-page.

## Notes

- Flag pretext indicators neutrally ("stated reason is inconsistent with the review history") rather than concluding the claim will succeed — that's attorney judgment.
- Comparator quality matters a lot in these claims — be specific about what makes a comparator actually comparable (same supervisor, same conduct, same role) rather than asserting comparability loosely.
