---
name: syncfusion-dotnet-word
description: Create, edit, format, and convert Word (.docx) documents using Syncfusion DocIO for .NET. Use this skill for Word processing and DOCX automation when the user asks to generate Word files, modify document content, insert tables or images, apply formatting, automate document workflows, or convert Word to PDF using C# code or CSX execution.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Word (DOCX) Document Processing

## Overview

Create, edit, and convert Word (.docx, .doc) files using the Syncfusion Word Library.
This skill supports two operational modes — generating C# code for the user's project or executing tasks directly through a CSX script.

## Key Capabilities

- **Create & Edit:** Documents (.docx, .doc, .rtf, .txt, .xml), paragraphs, headings, styles, lists, tables, charts, shapes, images, hyperlinks, bookmarks, watermarks, headers/footers, form fields, content controls, SmartArt, OLE objects
- **Advanced Features:** Mail merge (DataTable, JSON, XML, custom objects), track changes, comments, mathematical equations (LaTeX), compare/split/merge documents, table of contents
- **Conversion:** Word to PDF (font embedding, PDF/A, accessibility), Word to Image (PNG, JPEG, BMP, TIFF), HTML ↔ DOCX, RTF ↔ DOCX, Text ↔ DOCX, XML ↔ DOCX
- **Security:** Password encryption/decryption, document protection with editable ranges, macro management

## Prerequisites

- .NET SDK 8+ and `dotnet-script`: `dotnet tool install -g dotnet-script`
- Syncfusion License: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Generate Code (Mode 1)
**User:** "Show me how to create a Word document with a table"

**Result:** C# code snippet displayed (no files created)

### Example 2: Execute Task (Mode 2)
**User:** "Create a Word document with a table at output/report.docx"

**Result:** Physical file created at specified path

## Two Modes — Choose Based on User Intent

Before choosing a mode, infer what the user wants to accomplish:

### Mode 1: Generate C# Code for the User's Project *(default)*

Use this mode when the user wants to view, write, review, refactor, or modify C# code related to Word processing.

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

### Mode 2: Execute via CSX Script *(does not touch project files)*

Use this mode only when the user explicitly requests execution, file generation, or a fully produced output (such as a completed Docx file).

**Trigger keywords:** "create a word document", "make a document", "generate a document", "open", "edit", "modify", "change" a `.docx` file, "without modifying my project", "run a csx script", or when the user provides a file path (e.g., `output/report.docx`).

**Workflow:**

#### Step 1 — Create Temp CSX Script

- Start with `references/template.csx` as the base
- Create at: `{skill-root}/syncfusion-dotnet-word/scripts/temp-{uniqueId}.csx` (e.g., `skill-root` = `.codestudio/skills`)
- Use random GUID for unique filename (e.g., `temp-a3f7b2c1.csx`); never create in workspace root

#### Step 2 — Build Script from Reference Files

- Do NOT invent APIs/methods not in reference files
- Read relevant `references/*.md` file(s) and extract code snippets
- Replace all placeholders: file paths, document properties, data values, field names, etc.

#### Step 3 — Execute Script

- Run: `dotnet script {skill-root}/syncfusion-dotnet-word/scripts/temp-{uniqueId}.csx`
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
| **document-structure.md** | Create/load document, add sections, page setup, save to file or stream, supported formats |
| **styles-and-formats.md** | Paragraphs, headings, bullet & numbered lists |
| **paragraph-and-styles.md** | Add paragraphs, paragraph formatting, styles (built-in/custom), text formatting, tab stops, breaks, symbols, text boxes |
| **tables.md** | Create tables, cell formatting, merge cells |
| **bookmarks.md** | Create bookmarks, navigate, retrieve, insert, replace, delete content |
| **charts.md** | Create charts from scratch/Excel, modify data, refresh, customize elements, 3D formatting, convert to image |
| **shapes.md** | Add shapes, format, rotate, group, ungroup shapes |
| **mail-merge.md** | Simple field merge, merge with regions (groups), nested merge, DataTable, dynamic objects, business objects, DataView, XML, JSON, image merge fields, merge events (MergeField, MergeImageField, BeforeClearField, BeforeClearGroupField), field mapping, retrieve merge field names, remove empty paragraphs, clear fields option |
| **form-fields.md** | Add checkboxes, dropdowns, text input fields, modify properties |
| **macros.md** | Load/save macro-enabled documents (DOTM, DOCM), check for macros, remove macros, preserve macros through conversion |
| **mathematical-equation.md** | Create equations (fraction, radical, matrix, N-array, etc.), modify existing equations, LaTeX support, equation formatting |
| **split-word-documents.md** | Split documents by sections, headings, bookmarks, placeholder text |
| **merge-word-documents.md** | Merge documents in new page, same page, maintain imported list styles |
| **table-of-contents.md** | Add TOC, update, apply switches, custom styles, table of figures, remove TOC |
| **compare-word-documents.md** | Compare two Word documents, set author and date, comparison options, ignore format changes |
| **html-conversions.md** | Convert HTML to DOCX, convert DOCX to HTML, XHTML validation, customize images (import/export), CSS selectors, export options, headers/footers export |
| **rtf-conversions.md** | Convert RTF to DOCX, convert DOCX to RTF, preserve formatting and content |
| **markdown-conversion.md** | Convert Markdown to DOCX, convert DOCX to Markdown, customize images, CommonMark and GitHub-flavored syntax support |
| **text-conversions.md** | Convert Text to DOCX, convert DOCX to Text, extract plain text, preserve text content |
| **xml-conversions.md** | Convert Word to XML (WordML), convert XML to Word, Word Processing XML format (2007+) |
| **word-to-pdf.md** | Convert DOCX to PDF, embed fonts, PDF/A conformance, accessible PDF, preserve form fields, font substitution, fallback fonts by script type and Unicode ranges |
| **word-to-image.md** | Convert DOCX to Image | Convert specific page to image | Convert Page range to image |
| **word-to-odt.md** | Convert Word to ODT, preserve formatting and content, supported document elements, text formatting |
| **encryption.md** | Encrypt with password, open encrypted doc, remove encryption, protect from editing, editable ranges |
| **watermark.md** | Text and picture watermarks, watermark layout, scaling, washout effect, remove watermark |
| **find-and-replace.md** | Find/FindAll/FindNext, Replace (string/regex), ReplaceSingleLine, and FindItem* APIs |
| **footnotes-and-endnotes.md** | Add footnotes and endnotes, set positions (bottom of page/end of section), numbering formats, separators, modify content, remove notes |
| **track-changes.md** | Enable/disable track changes, accept/reject changes, filter by reviewer, revision information |
| **comments.md** | Add/modify/remove comments, insert on specific text, access parent comments, retrieve commented items |
| **content-controls.md** | Block and inline content controls, types (rich text, plain text, checkbox, date, dropdown, picture), properties, protection, form filling, XML mapping |
| **header-footer.md** | Add/remove headers and footers, page numbers with fields (date, time), odd/even pages, first page different, borders, images, link to previous |
| **hyperlinks.md** | Web hyperlink, email hyperlink, file hyperlink, bookmark hyperlink, image hyperlink, modify hyperlink |
| **ole-object.md** | Add embedded OLE objects, extract OLE objects to file, remove OLE objects, object types |
| **smartarts.md** | Create SmartArt layouts, add/modify nodes, change appearance, assistant nodes, remove SmartArt |

---

## Rules

- Output files go in `./output/` directory
- Temp `.csx` scripts must be created inside `{skill-root}/syncfusion-dotnet-word/scripts/` — never in the workspace root or customer `scripts/` folder
- Use license key from `SyncfusionLicense.txt` at workspace root or env var `SYNCFUSION_LICENSE_KEY`
- Never use Python libraries (e.g., python-docx)
- Never leave temp `.csx` files after execution