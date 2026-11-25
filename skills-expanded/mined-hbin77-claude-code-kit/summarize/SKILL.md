---
name: summarize
description: Generate concise summaries of code, PRs, files, or sessions.
---

# Summarize Skill

Generate concise summaries of code, PRs, files, or sessions.

## Modes

### Code Summary
Analyze a file or directory and produce:
- Purpose and responsibilities
- Key functions/classes and what they do
- Dependencies and integrations
- Entry points

### PR Summary
Analyze git changes and produce:
- What changed and why
- Files modified with brief descriptions
- Risk assessment
- Testing recommendations

### Session Summary
Summarize the current work session:
- Tasks completed
- Files modified
- Decisions made
- Open items / next steps

## Output Format

```
## Summary: [Subject]

### Overview
[1-2 sentences]

### Key Points
- [Point 1]
- [Point 2]
- [Point 3]

### Details
[Expanded information if needed]

### Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]
```
