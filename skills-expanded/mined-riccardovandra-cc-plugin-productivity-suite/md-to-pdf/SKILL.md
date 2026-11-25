---
name: md-to-pdf
description: Converts Markdown files to clean, professional PDFs. Use when creating PDF reports, proposals, or documents from markdown. Supports tables, headers, lists, and custom styling.
---

# Markdown to PDF

Convert markdown documents to clean, professional PDFs.

## Quick Start

```bash
# Basic conversion
uv run scripts/convert.py input.md output.pdf

# With custom title
uv run scripts/convert.py input.md output.pdf --title "ROI Analysis"

# Use brand styling (if configured)
uv run scripts/convert.py input.md output.pdf --style brand
```

## Features

- Clean, professional output
- Tables with proper formatting
- Headers (H1-H3)
- Bullet and numbered lists
- Bold and italic text
- Code blocks
- Page numbers
- Custom styling support

## Available Operations

| Operation | Description | Usage |
|-----------|-------------|-------|
| Convert | Markdown to PDF | `convert.py input.md output.pdf` |

## Script Usage

```bash
uv run scripts/convert.py <input.md> <output.pdf> [options]
```

**Arguments:**
- `input.md`: Path to markdown file
- `output.pdf`: Path for output PDF

**Options:**
- `--title`: Document title (overrides H1)
- `--style`: Style preset (`default`, `brand`, `minimal`)
- `--no-page-numbers`: Disable page numbers

## Styling

### Default Style
- Clean white background
- Professional typography
- Blue headers
- Gray table headers

### Brand Style (Future)
Configure in `context/business/brand-style.json`:
```json
{
  "primary_color": "#2c3e50",
  "accent_color": "#3498db",
  "font_family": "Helvetica"
}
```

## Examples

```bash
# Convert ROI analysis
uv run scripts/convert.py "workspace/docs/2025-12-17 - Herbox ROI/roi-analysis.md" "ROI-Analysis.pdf"

# With title override
uv run scripts/convert.py proposal.md proposal.pdf --title "Project Proposal"
```

## Output Location

PDFs are saved to the specified output path, or same directory as input if only filename given.

## Activation Triggers

- "convert to PDF", "make a PDF"
- "export as PDF", "PDF from markdown"
- "create PDF report"
