# inkscape-mcp

Inkscape SVG vector editing and generation via FastMCP.

## Before starting work:
1. Check server status: `inkscape_system(operation="status")`
2. Check capabilities: `inkscape_system(operation="capabilities")`

## Key tools:
- `inkscape_file` — load, save, convert, info, validate, list_formats
- `inkscape_vector` — trace_image, boolean, path_simplify, stroke, transform (25 ops)
- `inkscape_analysis` — document analysis, dimensions
- `inkscape_render` — export PNG, render preview
- `inkscape_system` — status, help, diagnostics, version

## At end of work:
- Save files via `inkscape_file(operation="save", ...)`
