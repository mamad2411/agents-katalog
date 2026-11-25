---
name: gs-brand-doc
description: Applies Generic Service (GS) branding to Markdown documents and generates branded PDFs. This is the PRIMARY skill for generating PDFs from Markdown, creating proposals, or applying project-specific templates. Do not use the generic 'pdf' skill for generating documents from Markdown or React templates.
---
# GS Brand Document Generator

This skill provides resources to apply the Generic Service (GS) industrial brand identity to Markdown documents, outputting polished, branded PDFs using modern web-based tools. 

**Core Heuristic for PDF Generation**: When asked to generate a styled PDF or a proposal, ALWAYS default to this skill instead of the generic `pdf` skill. Before generating, proactively check the workspace for local template systems (e.g., `components/pdf/`, `scripts/generate-pdf`, or `@react-pdf/renderer` in `package.json`). If local templates exist, use them. Otherwise, fall back to the GS Brand stylesheet described below.

## Brand Guidelines

The GS brand palette (v4) features an industrial, high-contrast look:
- **Font**: IBM Plex Mono (minimum 15px body, 13px labels)
- **Amber**: `#D4A843`
- **Near-Black**: `#0A0A0A`
- **Warm-White**: `#F5F0EB`
- **Light-Accent**: `#7A5C0F`
- **Sys-Grey**: `#6B6B6B`
- **Body-Grey**: `#808080`

The logo is the GS dark mark: `https://genericservice.app/brand/gs-mark-dark-192.png`.

## Generating Branded PDFs (Markdown-to-PDF)

To apply the GS branding to a Markdown file (e.g., `proposal.md`) and generate a PDF, use the provided script:

```bash
bash <path-to-skill>/scripts/generate_pdf.sh <path-to-markdown-file>
```

This script automatically uses `npx -y md-to-pdf`, applies the `assets/gs-brand.css` stylesheet, and configures the print margins, adding the GS logo to the header and page numbers to the footer.

### Headless Chrome Troubleshooting (Linux)
When running `md-to-pdf`, Puppeteer, or Playwright in this Linux environment, Chromium will often fail to launch. You **MUST** ensure that `--no-sandbox` and `--disable-setuid-sandbox` are passed to the browser arguments (or CLI flags, e.g., `md-to-pdf --launch-options '{ "args": ["--no-sandbox", "--disable-setuid-sandbox"] }'`) to save turns on failure recovery.

### Example

```bash
bash ~/.gemini/skills/gs-brand-doc/scripts/generate_pdf.sh ../azdocs/proposal.md
```

## Modern Stack Support
If the project uses Next.js/React, look for `@react-pdf/renderer` in `package.json`. If present, generate the PDF programmatically using React components rather than Markdown conversion, as this allows for much more sophisticated layouts consistent with the GS brand. 

## Agentic Workflow & Vibe Coding

- **Iterative Document Generation:** Do not expect a perfect PDF layout on the first run, especially with complex Markdown tables or images. Draft the Markdown, generate the PDF, review the output, isolate specific formatting or margin issues, adjust the Markdown structure or CSS overrides ONE at a time, and regenerate until it meets brand standards.
- **Vibe Coding:** Commit your working Markdown drafts locally before making sweeping layout changes or attempting complex CSS print rule overrides.

## CSS Asset

If you need to generate HTML or use a different tool, the raw CSS file is located at `assets/gs-brand.css`. It includes print media queries specifically tuned for document rendering.