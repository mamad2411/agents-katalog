---
name: syncfusion-dotnet-markdown
description: Create, edit, and convert Markdown documents (.md) using Syncfusion Markdown. Supports two modes — generate C# code for the user's project or execute a task via CSX script. Use when the user mentions markdown, .md files, markdown generation, Syncfusion Markdown.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Markdown Document Processing

## Overview

Create, edit, and convert Markdown (.md) files using the Syncfusion Markdown Library.
This skill supports two operational modes — generating C# code for the user's project or executing tasks directly through a CSX script.

## Key Capabilities

- **Create & Edit:** paragraphs, headings, lists, tables, images, hyperlinks, code blocks, blockquotes, task lists
- **Parse & Modify:** load from files/streams, iterate and update blocks and inlines
- **Serialization:** convert Markdown document models back to plain Markdown text and write to files
- **Advanced Features:** custom parsing events, image loading handlers, nested lists, task list support

## Prerequisites

- .NET SDK 8+ and `dotnet-script`: `dotnet tool install -g dotnet-script`
- Syncfusion License: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Generate Code (Mode 1)
**User:** "Show me how to create a Markdown document with a table"

**Result:** C# code snippet displayed (no files created)

### Example 2: Execute Task (Mode 2)
**User:** "Create a Markdown file at output/report.md"

**Result:** Physical file created at specified path (via temporary CSX script)

## Two Modes — Choose Based on User Intent

Before choosing a mode, infer what the user wants to accomplish:

### Mode 1: Generate C# Code for the User's Project *(default)*

Use this mode when the user wants to view, write, review, refactor, or modify C# code related to Markdown processing.

**Trigger keywords:** "show me how", "how to", "how can I", "how do I", "provide code", "provide an example", "give an example", "demonstrate", "code snippet", "sample code", "example", "sample", "give me", "show me", "Program.cs", "example code", "generate code for", "codesnippet"

**Workflow:**

#### Step 1 — Detect the Application Type and Suggest the Correct NuGet Package(s)

- Inspect the workspace project files (`.csproj`, `web.config`, `App.config`, `Startup.cs`, `Program.cs`, etc.) and use the detection signals table in `references/nuget-packages.md` to identify the application type.
- Look up the correct package(s) from `references/nuget-packages.md` based on the detected app type and tell the user to install them **before** generating any code.

#### Step 2 — Generate Code from Reference Files Only

Do NOT invent, guess, or suggest any API, method, property, class, or namespace not explicitly present in the reference files.

- Read the relevant `references/*.md` file(s) for the requested feature
- Build C# code **strictly** from the APIs and snippets found in those files
- Select the correct snippet variant based on the app type detected in Step 1:
  - **Windows-specific apps** (WinForms, WPF, .NET Framework Console, ASP.NET MVC4/5, UWP) → use Windows-specific snippets
  - **Cross-platform apps** (ASP.NET Core, .NET Core/.NET 5+ Console, Blazor, MAUI, Xamarin) → use cross-platform / `.Net.Core` snippets
- Do **not** create or run any `.csx` script

---

### Mode 2: Execute via CSX Script *(does not modify project files)*

Use this mode only when the user explicitly requests execution, file generation, or a fully produced output (such as a completed md file).

**Trigger keywords:** "create a markdown document", "make a markdown file", "generate markdown", "parse markdown", "convert markdown to HTML", "open", "edit", "modify", "change" a `.md` file, "without modifying my project", "run a csx script", or when the user provides a file path (e.g., `output/report.md`).

**Workflow:**

#### Step 1 — Create Temp CSX Script

- Start with `references/template.csx` as the base
- Create at: `{skill-root}/syncfusion-dotnet-markdown/scripts/temp-{uniqueId}.csx` (e.g., `skill-root` = `.codestudio/skills`)
- Use random GUID for unique filename (e.g., `temp-a3f7b2c1.csx`); never create in workspace root

#### Step 2 — Build Script from Reference Files

- Do NOT invent APIs/methods not in reference files
- Read relevant `references/*.md` file(s) and extract code snippets
- Replace all placeholders: file paths, document properties, data values, field names, etc.

#### Step 3 — Execute Script

- Run: `dotnet script {skill-root}/syncfusion-dotnet-markdown/scripts/temp-{uniqueId}.csx`
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
| **document-structure.md** | Create/load/save markdown documents, DOM structure, block and inline elements |
| **create-markdown.md** | Create markdown documents from scratch, add paragraphs, headings, formatting |
| **parse-markdown.md** | Parse markdown from files/streams, process blocks, iterate content, modify parsed documents |
| **text-formatting.md** | Apply bold, italic, strikethrough, code span, subscript, superscript formatting |
| **headings-styles.md** | Apply heading styles (H1-H6), paragraph styles, blockquotes |
| **lists.md** | Create numbered and bulleted lists, nested lists (up to 8 levels), list formatting |
| **tables.md** | Create tables with column alignments (left, center, right), add rows and cells |
| **hyperlinks.md** | Add hyperlinks with display text, URLs, and screen tips |
| **images.md** | Insert images from URLs or bytes, alt text, image formats, base64 encoding |
| **code-blocks.md** | Create fenced and indented code blocks, language specification |
| **blockquotes.md** | Create blockquotes with nesting levels |
| **task-lists.md** | Create task lists with checked/unchecked checkboxes (GitHub-style) |
| **advanced-features.md** | Advanced markdown features, custom parsing, events |


## Rules

- Output files go in `./output/` directory
- Temp `.csx` scripts must be created inside `{skill-root}/syncfusion-dotnet-markdown/scripts/` — never in the workspace root or customer `scripts/` folder
- Use license key from `SyncfusionLicense.txt` at workspace root or env var `SYNCFUSION_LICENSE_KEY`
- Never use Python libraries (e.g., python-markdown)
- Never leave temp `.csx` files after execution