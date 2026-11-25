---
name: syncfusion-dotnet-smart-data-extraction
description: Extract tables, form fields, and document layout from PDFs or images (scanned PDFs, PNG/JPG) using Syncfusion Smart Data Extractor. Trigger when users ask to parse/extract/convert document data (invoices, receipts, KYC/forms) into structured output and want C#/.NET integration code using the extractor. 
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Smart Data Extractor — Syncfusion
## Overview

Extracts complete document structures from PDFs and images files using the Syncfusion SmartDataExtractor Library.
This skill supports one operational mode — generating C# code for the user's project.

## Key Capabilities

- **Document structure extraction**: Identify text elements, images, headers, footers, and tables (including regions, header rows, columns, cell boundaries, and merged cells).
- **File format support**: Works with PDF documents and common image formats such as JPEG and PNG.
- **Table extraction**: Specialized capability to extract tabular data.
- **Form recognition**: Detects and processes structured form data.
- **Page-level control**: Extract data from specific pages or defined page ranges.
- **Confidence threshold**: Results are filtered based on a configurable confidence score (0.0–1.0).

## Prerequisites

- Install required runtime and library packages from NuGet before running extraction.
- Syncfusion License: `LICENSE.txt` or env var `SYNCFUSION_LICENSE_KEY`

## Quick Start Examples


### Example : Generate Code
**User:** "Write Program.cs code to extract the data from pdf and save as JSON."
**Result:** C# code snippet displayed (no files created)

## Mode 

### Mode 1: Generate C# Code for the User's Project *(default)*

Use this mode when the user wants to view, write, review, refactor, or modify C# code related to Smart Data Extractor processing.
**Trigger keywords:** "show me how", "how to", "how can I", "how do I", "provide code", "provide an example", "give an example", "demonstrate", "code snippet", "sample code", "example", "sample", "give me", "show me", "Program.cs", "example code", "generate code for", "codesnippet" .

**Workflow:**
#### Step 1 — Detect Application Type and Suggest Required NuGet Packages
- Inspect the workspace project files (`.csproj`, `web.config`, `App.config`, `Startup.cs`, `Program.cs`, etc.) and use the detection signals table in `references/nuget-packages.md` to determine the application type.
- Based on the detected application type, identify the correct NuGet package(s) from `references/nuget-packages.md` and instruct the user to install them before generating any code. ONLY use package IDs and versions listed in `references/nuget-packages.md` — do not suggest, look up, or infer package names from external sources or common naming conventions.
- Note: If the user's request is explicitly table-only (asks only to extract table data), recommend only the Table Extractor package listed in `references/nuget-packages.md` and review the ExtractTable section for the detected application type. Do not recommend or add the broader `SmartDataExtractor` package unless the user requests non-table extraction or JSON conversion features.
#### Step 2 — Generate Code from Reference Files Only
Do NOT invent, guess, or suggest any API, method, property, class, or namespace not explicitly present in the reference files.
 
- Read the relevant `references/*.md` file(s) for the requested feature
- Build C# code **strictly** from the APIs and snippets found in those files
- Select the correct snippet variant based on the app type detected in Step 1:
  - **Windows-specific apps** (WinForms, WPF, .NET Framework Console) → use Windows-specific snippets
  - **Cross-platform apps** (ASP.NET Core, .NET Core/.NET 5+ Console, Blazor, MAUI) → use cross-platform / `.Net.Core` snippets
  - After the `using` / namespace lines at the top of the generated code, always insert the license registration block from the **Register License** section in `references/nuget-packages.md`
  - Do **not** create or run any `.csx` script
---

---

## Code References

All templates and snippets are in the `references/` folder:

| File | Contents |
|---|---|
| **document-structure.md** | Quick extractor setup and usage snippets |
| **extract-data.md** | Examples: ExtractDataAsJson, ExtractDataAsPdfStream,ExtractDataAsPdfDocument, async variants |
| **extract-table.md** | Table extraction examples (ExtractTableAsJson)|
| **recognize-forms.md** | recognize form fields examples : FormRecognizeOptions, RecognizeFormAsPdfDocument,RecognizeFormAsPdfStream, RecognizeFormAsJson async variants |
| **data-options.md** | Explanation of `TableExtractionOptions`, `FormRecognizeOptions`, `ConfidenceThreshold` , `PageRange`|

---


## Rules

- Output files go in `./output/` directory
- Use license key from `LICENSE.txt` at workspace root
- Don't use any API which is not in reference
 - Only use NuGet package IDs and versions defined in `references/nuget-packages.md` when recommending or adding packages.
 - For table-only extraction requests, recommend/install only the table extractor package from `references/nuget-packages.md` for the detected application type.

