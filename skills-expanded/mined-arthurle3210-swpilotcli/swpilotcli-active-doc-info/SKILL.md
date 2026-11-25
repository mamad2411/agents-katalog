---
name: swpilotcli-active-doc-info
description: Get information about the currently open SolidWorks document (part, assembly, or drawing). Use when you need to check document properties, file path, document type, or current state without modifying it.
---

# SolidWorks Active Document Info

Get metadata and properties of the currently active SolidWorks document.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- **Active SolidWorks document** must be open

## What this Skill does

Retrieves detailed information about the active SolidWorks document, including:
- File path and name
- Document type (Part, Assembly, Drawing)
- Document state (saved, modified, read-only)
- Configuration information
- Feature tree and component details (for assemblies)

## When to use

- **Check document properties** before modifying
- **Verify file location** and state
- **List components** in an assembly
- **Analyze document structure** for workflow planning

## Quick start

Run the tool:

```bash
dotnet run --project ./scripts/ActiveDocInfo.csproj
```

Expected output:

```
[Document Info]
File: C:\SolidWorks\Part001.sldprt
Type: Part
State: Saved
Modified: false
...
```

## Examples

### Example 1: Get basic document info
```
User: What file is currently open in SolidWorks?
Claude: I'll check the active document for you.
```
Run the tool and report back to user.

### Example 2: Verify before operations
```
User: Is the current part saved before I modify it?
Claude: I'll check the document state using this tool.
```

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for detailed output schema and return values.

## Notes

- Requires an active SolidWorks instance
- Returns read-only information; does not modify documents
- Execution time: typically < 500ms
