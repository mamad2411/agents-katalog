---
name: react-pdf
description: Generates PDF documents using the React-PDF library (@react-pdf/renderer) with TypeScript and JSX.
allowed-tools:
- Bash
- Read
- Write
- Grep
- Glob
metadata:
  version: 0.2.0
  category: trail-of-bits
---
# Generating PDFs with React-PDF

## Quick Start
```bash
# Install dependencies
npm install react @react-pdf/renderer
npm install -D tsx

# Run your PDF script
npx tsx my-document.tsx
```

## Workflow
1. **Setup**: Install `react`, `@react-pdf/renderer`, and `tsx`.
2. **Design**: Create a document using `Document`, `Page`, `View`, and `Text` components.
3. **Styling**: Define styles using `StyleSheet.create()` following Flexbox patterns.
4. **Fonts**: Download and register local TrueType fonts if custom typography is needed.
5. **Rendering**: Wrap `renderToFile` in an async IIFE to generate the PDF.
6. **Validation**: Preview the PDF using `pdftoppm` or `PyMuPDF` to verify layout.

## Rules & Constraints
- **RULE-1**: Fonts MUST be local files; remote URLs (http/https) do NOT work.
- **RULE-2**: Wrap async rendering code in an IIFE to avoid top-level await errors.
- **RULE-3**: Disable hyphenation for custom fonts to prevent crashes.
- **RULE-4**: Use `tsx` to run TypeScript/JSX files directly without complex config.

## When to Use
- Generating reports, invoices, resumes, or forms with complex layouts.
- Need for Flexbox-based layout rather than absolute coordinate math.
- Integrating inline SVG graphics or custom Google Fonts.

## When NOT to Use
- Extracting text from existing PDFs (use `pdfplumber`).
- Filling existing PDF forms (use `pypdf`).
- Simple one-off text PDFs with no layout requirements.

## References
- [Skill Manual](references/react-pdf-manual.md)
- [Component API](references/components.md)
- [Example Template](assets/example-template.tsx)
