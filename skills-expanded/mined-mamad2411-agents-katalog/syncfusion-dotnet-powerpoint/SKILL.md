---
name: syncfusion-dotnet-powerpoint
description: Create, edit, format, and convert PowerPoint (.pptx) presentations using Syncfusion Presentation for .NET. Use this skill for PowerPoint processing and presentation automation when the user asks to generate slides, modify PPTX content, insert text or images, build presentations programmatically, or convert PowerPoint to PDF using C# code or CSX execution.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# PowerPoint (PPTX) Presentation Processing
## Overview

Create, edit and convert PowerPoint (.pptx) files using the Syncfusion Presentation Library.
This skill supports two operational modes — generating C# code for the user’s project or executing tasks directly through a CSX script.
## Key Capabilities

- **Create & Edit:** Presentations (.pptx), slides (clone and merge), paragraphs, text boxes, tables, shapes, images, lists, connectors, hyperlinks, headers/footers, comments, document properties, sections
- **Advanced Features:** Custom animations and slide transitions, master slide layouts, speaker notes, SmartArt, OLE objects, find and replace, macros, chart creation and editing, chart-to-image conversion
- **Conversion:** PowerPoint to PDF; PowerPoint to images (PNG, JPEG)
- **Security:** Encrypt and decrypt presentations; set and remove write protection

## Prerequisites

- .NET SDK 8+ and `dotnet-script`: `dotnet tool install -g dotnet-script`
- Syncfusion License: `SyncfusionLicense.txt` or env var `SYNCFUSION_LICENSE_KEY`
- Free license: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Generate Code (Mode 1)
**User:** "Show me how to create a PowerPoint presentation with a simple bar chart"

**Result:** C# code snippet displayed (no files created)

### Example 2: Execute Task (Mode 2)
**User:** "Create a PowerPoint presentation with a simple bar chart at output/SalesChart.pptx"

**Result:** Physical file created at `output/SalesChart.pptx` with the chart embedded

## Two Modes — Select Based on User Intent

### Mode 1: Generate C# Code for the User's Project *(default)*
Use this mode when the user wants to view, write, review, refactor, or modify C# code related to PowerPoint processing.

**Trigger keywords:** "show me how", "how to", "how can I", "how do I", "provide code", "provide an example", "give an example", "demonstrate", "code snippet", "sample code", "example", "sample", "give me", "show me", "Program.cs", "example code", "generate code for", "codesnippet" .

**Workflow:**
 
#### Step 1 — Detect Application Type and Suggest Required NuGet Packages
- Inspect the workspace project files (`.csproj`, `web.config`, `App.config`, `Startup.cs`, `Program.cs`, etc.) and use the detection signals table in `references/nuget-packages.md` to determine the application type.
- Based on the detected application type, identify the correct NuGet package(s) from references/nuget-packages.md and instruct the user to install them before generating any code.
 
#### Step 2 — Generate Code from Reference Files Only
Do NOT invent, guess, or suggest any API, method, property, class, or namespace not explicitly present in the reference files.
 
- Read the relevant `references/*.md` file(s) for the requested feature
- Build C# code **strictly** from the APIs and snippets found in those files
- Select the correct snippet variant based on the app type detected in Step 1:
  - **Windows-specific apps** (WinForms, WPF, .NET Framework Console, ASP.NET MVC4/5 ) → use Windows-specific snippets
  - **Cross-platform apps** (ASP.NET Core, .NET Core/.NET 5+ Console, Blazor, MAUI) → use cross-platform / `.Net.Core` snippets
- Do **not** create or run any `.csx` script
---

### Mode 2: Execute via CSX Script *(does not touch project files)*
Use this mode only when the user explicitly requests execution, file generation, or a fully produced output (such as a completed PPTX file).

**Trigger keywords:** "create a presentation", "make a presentation", "generate a presentation", "open", "edit", "modify", "change" a `.pptx` file, "without modifying my project", "run a csx script", or when the user provides a file path (e.g., `output/report.pptx`).

**Workflow:**

#### Step 1 — Create Temp CSX Script
- Start with `references/template.csx` as the base
- Create at: `{skill-root}/syncfusion-dotnet-powerpoint/scripts/temp-{uniqueId}.csx` (e.g., `skill-root` = `.codestudio/skills`)
- Use random GUID for unique filename (e.g., `temp-a3f7b2c1.csx`); never create in workspace root

#### Step 2 — Build Script from Reference Files
- Do NOT invent APIs/methods not in reference files
- Read relevant `references/*.md` file(s) and extract code snippets
- Replace all placeholders: file paths, document properties, data values, field names, etc.

#### Step 3 — Execute Script
- Run: `dotnet script {skill-root}/syncfusion-dotnet-powerpoint/scripts/temp-{uniqueId}.csx`
- Verify successful execution and capture any errors

#### Step 4 — Clean Up and Report
- Delete the temp `.csx` file after execution
- Report SUCCESS/ERROR with output file path(s) and any error messages with fixes
---

## Code References

All templates and snippets are in the `references/` folder:

| File | Contents |
|---|---|
| **template.csx** | Base CSX script structure (Mode 2 only) |
| **presentation-structure.md** | Create/save/close presentation, slide layout, page size, document properties |
| **slides.md**| Add, remove, resize, and customize PowerPoint slides, print slides |
| **layout.md** | Access, customize, and create master slides and layout slides |
| **paragraph.md** | Add, format, and manage paragraphs in textboxes and shapes |
| **sections.md** | Create and Modify Sections in presentation |
| **tables.md** | Create and modify tables in presentation |
| **shapes.md** |  Add, iterate, format, and remove shapes (AutoShapes, pictures, text boxes, group shapes) in a presentation |
| **connectors.md** | Add, edit, update, and remove connectors between shapes |
| **image.md** | Add, replace, crop, and remove images including SVG support |
| **list.md** | Create numbered, bulleted, picture, and multi-level lists |
| **chart.md** | Create and edit chart in presentation |
| **animation-transition.md** | Add, modify slide transition and annimation effect in presentation |
| **comments.md** | Add, Reply, Modify, Delete commments in presentation |
| **header-footer.md** | Add, edit, and remove headers and footers including slide numbers and dates |
| **notes.md** | Add, edit, format, and remove speaker notes in presentations |
| **ole-objects.md** | Insert, extract, and manage OLE objects (Excel, Word, Visio) in slides |
| **conversions.md** | Convert Presentation to image and Pdf |
| **encrypt-decrypt.md** | Security: Protect, encrypt, and decrypt during read or write access in presentations |
| **find-and-replace.md** | Find and Replace, Find and highlight in specific slide or in presentation |
| **smartart.md** |  Create a SmartArt, Add, Edit, Remove nodes in SmartArt in a PowerPoint Presentation|
| **hyperlinks.md** | Add or Modify Web, Email, Bookmark, File, Image hyperlinks |
| **macros.md** | Load, Save, Remove and manage macros in presentations |
---

## Rules

- Output files go in `./output/` directory
- Temp `.csx` scripts must be created inside `{skill-root}/syncfusion-dotnet-powerpoint/scripts/` — never in the workspace root or customer `scripts/` folder
- Use license key from `SyncfusionLicense.txt` at workspace root or env var `SYNCFUSION_LICENSE_KEY`
- Never use Python libraries (e.g., python-pptx)
- Never leave temp `.csx` files after execution