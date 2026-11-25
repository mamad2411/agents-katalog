---
name: word-uiux-review
description: 'Evaluate generated Word document UX quality. Use for readability, hierarchy, style consistency, and export output checks.'
argument-hint: 'Document goal and UX quality concerns'
user-invocable: true
---

# Word UIUX Review

## When to Use
- You need quality checks on generated `.docx` output.
- You need better visual hierarchy or readability.
- You want to validate output images from export flow.

## Focus Areas
- Heading and section hierarchy
- Paragraph rhythm and list scanability
- Table legibility and density
- Theme/style consistency
- Exported page image quality

## Procedure
1. Review generation logic in `docx_components/components/`, `docx_components/theme.py`, and `docx_components/template.py`.
2. Inspect export workflow in `docx_components/export.py` for rendering constraints.
3. Produce issue list ordered by user impact.
4. Recommend minimal style/systemic changes with acceptance checks.

## Export CLI
`docx_components/export.py` ships a CLI. Two equivalent invocations:

```bash
# After pip install -e .
docx-export <file.docx> -o <out_dir> --dpi 200 --prefix page

# Without install
python -m docx_components.export <file.docx> -o <out_dir> --dpi 200 --prefix page
```

Arguments:
| Flag | Default | Description |
|------|---------|-------------|
| `docx` | required | Path to `.docx` file |
| `-o / --output` | `<stem>_pages/` | Output directory for PNG files |
| `--dpi` | `150` | Rasterization DPI |
| `--prefix` | `page` | Filename prefix for each PNG |

## Verification
1. Export the target `.docx` to PNGs using the CLI above.
2. View the resulting `page_001.png`, `page_002.png`, ... files.
3. Confirm readability, hierarchy, and table clarity at the chosen DPI.
