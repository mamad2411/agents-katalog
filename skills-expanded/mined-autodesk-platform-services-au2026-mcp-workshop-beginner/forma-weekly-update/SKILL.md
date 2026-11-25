---
name: forma-weekly-update
description: Generates a summary of file changes in a given Forma project for the last 7 days, or for a specific date range if provided.
---

Generate a summary of recent changes in a Forma project using the available MCP tools.

## Instructions

1. If the user has not specified a project, use `list-hubs-projects` to show available projects and ask which one to summarise.
2. Use `list-folder-contents` to recursively browse the project's folder structure.
3. Filter items to those modified within the requested time range:
   - Default: last 7 days from today
   - If the user provides a date range (e.g. "between May 1 and May 15"), use that range instead
4. Group results by folder. For each modified item, include:
   - File name
   - Who modified it
   - When it was modified
5. Present the output as a readable summary, for example:

```
## Weekly Update — [Project Name]
Period: [start date] to [end date]

### [Folder Name]
- **[File Name]** — modified by [User] on [Date]
- ...

### [Another Folder]
- ...
```

If no changes were found in the period, say so clearly.
