---
name: syncfusion-dotnet-pdf-to-image
description: Convert PDF files to images with customization options (output format, DPI, pages, scaling, and image quality). Supports one mode — generate C# code for the user's project.
compatibility: Requires .NET SDK 8+ and dotnet-script global tool. Designed for Windows, macOS, and Linux.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Pdf To Image Converter Using Syncfusion .NET PDF Library
## Overview
This PDF to image converter library allows converting PDF documents to images without opening the document in the PDF Viewer control. It allows you to selectively export pages as a stream by utilizing the ‘Convert’ method, facilitating the transformation of PDF files into images.

## Quick Start Examples

### Example 1: Generate Code
**User:** "Show me the C# code to convert pdf to image."
**Result:** C# code snippet displayed (no files created)

## One Modes

### Mode 1: Generate C# Code for the User's Project *(default)*
Use this mode when the user wants to view, write, review, refactor, or modify C# code related to pdf to image conversion processing.

**Trigger keywords:** "show me how", "how to", "how can I", "how do I", "provide code", "provide an example", "give an example", "demonstrate", "code snippet", "sample code", "example", "sample", "give me", "show me", "Program.cs", "example code", "generate code for", "codesnippet".

**Workflow:**

#### Step 1 — Detect Application Type and Suggest Required NuGet Packages
- Inspect the workspace project files (`.csproj`, `web.config`, `App.config`, `Startup.cs`, `Program.cs`, etc.) and use the detection signals table in `references/nuget-packages.md` to determine the application type.

- Based on the detected application type, identify the correct NuGet package(s) from references/nuget-packages.md and instruct the user to install them before generating any code.

#### Step 2 — Generate Code from Reference Files Only

> **Do NOT invent, guess, or suggest any API, method, property, class, or namespace not explicitly present in the reference files.**

- Read the relevant `references/*.md` file(s) for the requested feature
- Build C# code **strictly** from the APIs and snippets found in those files
- Do **not** create or run any `.csx` script
---

## API Summary

| API / Property | Purpose |
|---|---|
| `new PdfToImageConverter(stream)` | Loads a PDF document from a stream via constructor |
| `new PdfToImageConverter(stream, password)` | Loads an encrypted PDF document from a stream via constructor |
| `imageConverter.Load(stream)` | Loads a PDF document from a stream using the Load method |
| `imageConverter.Load(stream, password)` | Loads an encrypted PDF document from a stream using the Load method |
| `imageConverter.Convert(pageIndex, keepTransparency, isSkipAnnotations)` | Converts a single PDF page to an image stream |
| `imageConverter.Convert(startPage, endPage, keepTransparency, isSkipAnnotations)` | Converts a range of PDF pages to an array of image streams |
| `imageConverter.Convert(pageIndex, SizeF, keepAspectRatio, keepTransparency, isSkipAnnotations)` | Converts a PDF page to an image with a custom width and height |
| `imageConverter.Convert(startPage, endPage, dpiX, dpiY, keepTransparency, isSkipAnnotations)` | Converts a range of PDF pages to images at a custom DPI resolution (MVC / WinForms / WPF) |
| `imageConverter.Convert(pageIndex, zoomFactor, tileXCount, tileYCount, tileX, tileY)` | Converts a PDF page to an image using zoom factor and tile matrix coordinates (ASP.NET Core / Blazor) |
| `imageConverter.PageCount` | Gets the total number of pages in the loaded PDF document |
| `imageConverter.ScaleFactor` | Sets the scale factor to enhance output image quality (default: `1.5f`) |
| `imageConverter.ReferencePath` | Sets a custom folder path for PDFium binary extraction in restricted-access environments |

---

## Code References

All templates and snippets are in the `references/` folder:

| File | Contents |
|---|---|
| `nuget-packages.md` | Lists the required NuGet packages for PDFToImageConverter per target platform, with application-type detection signals |
| `load.md` | Loads a PDF document (plain or encrypted) as stream into PdfToImageConverter using constructor or Load method |
| `customizing-conversion.md` | Converts PDF pages to images — single page, page range, custom size, custom DPI, and zoom/tile resolution |
| `multithreading-pdf-to-image.md` | Converts PDF pages to images using multithreading — via Task-based async and Parallel.For patterns |

---

## Rules

- Output files go in `./output/` directory
- Use license key from `SyncfusionLicense.txt` at workspace root
- Don't use any API which is not in reference

## Prerequisites

- Install required runtime and library packages from NuGet before running recognition.
- .NET SDK 8+ and `dotnet-script`: `dotnet tool install -g dotnet-script`
- Syncfusion License: `SyncfusionLicense.txt` or env var `SYNCFUSION_LICENSE_KEY`
- Free license: https://www.syncfusion.com/products/communitylicense
