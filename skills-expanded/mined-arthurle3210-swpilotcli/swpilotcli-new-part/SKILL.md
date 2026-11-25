---
name: swpilotcli-new-part
description: Create a new SolidWorks Part document using the user's configured default Part template. Reads `swDefaultTemplatePart` from user preferences and calls `NewDocument`. Use when the user asks to create a new part, start modeling from scratch, or needs a fresh `.sldprt` to host a subsequent sketch/feature workflow.
---

# SolidWorks New Part

Create a new empty Part document from the configured default Part template.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime**
- A valid default Part template configured in SolidWorks (Tools ▸ Options ▸ File Locations ▸ Document Templates)

## What this Skill does

- Makes SolidWorks visible (`swApp.Visible = true`)
- Reads `GetUserPreferenceStringValue(swDefaultTemplatePart)` to get the template path
- Fails with exit code 4 if the template path is empty
- Calls `NewDocument(template, 0, 0, 0)` and reports the new part's title

## When to use

- User asks "開一個新的零件" / "create a new part" / "start a new part"
- As the first step of an AI-driven part-modeling workflow before `sketch-on-face`, `sketch-draw`, `feature-extrude-boss`, etc.

## Quick start

```bash
dotnet run --project ./sup_tools/swpilotcli-new-part/scripts/NewPart/NewPart.csproj
```

## Return codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Cannot connect to SolidWorks |
| 4 | Default Part template path is empty — configure one in SolidWorks Options |
| 5 | `NewDocument` returned null (bad template path or template missing) |
