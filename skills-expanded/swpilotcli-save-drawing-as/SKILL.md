---
name: swpilotcli-save-drawing-as
description: Save the active SolidWorks drawing to a different format. Exports to the same directory as the drawing file with the same filename and a new extension. Supported formats: pdf, png, jpg, tif, dwg, dxf, ai, psd, edrw, html, slddrw. Default format is pdf if no argument is given. Optionally accepts a second argument to override the output file path. Use when you need to export or convert the current drawing to another format.
---

# SolidWorks Save Drawing As

Export the active SolidWorks drawing to another format. Output is saved in the same directory as the source drawing.

## Prerequisites

- **SolidWorks 2024+** with SwpilotCLI add-in installed
- **.NET 8+ Runtime** on the system
- An active `.slddrw` drawing document open in SolidWorks
- The drawing must be saved (have a file path) before exporting

## What this Skill does

1. Reads the active drawing's file path to determine the output directory and filename
2. Builds the output path: same directory, same name, new extension
3. For PDF: creates an `ExportPdfData` object to export all sheets silently
4. Calls `SaveAs3` with the target format
5. Reports output path and file size on success

## When to use

- Export drawing to PDF for sharing or printing
- Convert drawing to DWG/DXF for CAD exchange
- Save a copy in PNG/JPG/TIF for image use
- Any format conversion from the current drawing

## Quick start

```bash
# Export as PDF (default)
dotnet run --project ./sup_tools/swpilotcli-save-drawing-as/scripts/SaveDrawingAs/SaveDrawingAs.csproj

# Specify format
dotnet run --project ./sup_tools/swpilotcli-save-drawing-as/scripts/SaveDrawingAs/SaveDrawingAs.csproj -- dwg
dotnet run --project ./sup_tools/swpilotcli-save-drawing-as/scripts/SaveDrawingAs/SaveDrawingAs.csproj -- png

# Override output path
dotnet run --project ./sup_tools/swpilotcli-save-drawing-as/scripts/SaveDrawingAs/SaveDrawingAs.csproj -- pdf "C:\output\myfile.pdf"
```

Expected output:

```
Active document: D:\Projects\AA-NDE-R.SLDDRW
工程圖 : AA-NDE-R.SLDDRW
格式   : PDF
輸出   : D:\Projects\AA-NDE-R.pdf
✓ 匯出成功
  大小: 359 KB
Task completed successfully.
```

## Supported formats

| Argument | Extension | Description |
|----------|-----------|-------------|
| `pdf` | .pdf | Adobe PDF (default) |
| `png` | .png | PNG image |
| `jpg` / `jpeg` | .jpg | JPEG image |
| `tif` / `tiff` | .tif | TIFF image |
| `dwg` | .dwg | AutoCAD DWG |
| `dxf` | .dxf | AutoCAD DXF |
| `ai` | .ai | Adobe Illustrator |
| `psd` | .psd | Adobe Photoshop |
| `edrw` | .edrw | eDrawings |
| `html` | .html | eDrawings Web HTML |
| `slddrw` | .slddrw | SolidWorks Drawing copy |

## Reference

See [API_REFERENCE.md](API_REFERENCE.md) for arguments, exit codes, and APIs used.

## Notes

- Output file is saved in the **same directory** as the drawing, with the same filename
- If a file with the same name already exists, it will be overwritten
- PDF export uses `ExportPdfData` with all sheets enabled and silent mode (no preview)
