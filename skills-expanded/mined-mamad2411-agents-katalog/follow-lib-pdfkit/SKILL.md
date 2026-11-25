---
name: follow-lib-pdfkit
description: Use pdfkit to create PDFs server-side — layout, fonts, streams, images
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test

---

## Goal

Use pdfkit to create PDFs server-side — layout, fonts, streams, images

## Scope

Use when the task involves this library/tool — setup, usage, debugging, or best practices (lib pdfkit)

- Covers: programmatic server-side PDF generation — streaming output, text/vector/image layout, custom fonts, multi-page
- Not covered: HTML→PDF — use Playwright `page.pdf()` or a print pipeline instead; edge/workerd runtime — pdfkit requires Node
- No CLI — used via programmatic API only (thus none)
- Latest: `pdfkit@0.20.2` (verified 2026-09-13)
- References: [apis](references/apis.md) 
## Execute

### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Install `bun add pdfkit` and `bun add -D @types/pdfkit` for TypeScript
1. Create `new PDFDocument()` then pipe into a stream/response
1. Use `doc.text()`, `doc.moveTo()`, `doc.rect()` for layout — manual positioning
1. Register fonts with `doc.registerFont()` — mind font licensing
1. Finish with `doc.end()` — don't forget it or leave the stream hanging

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib pdfkit)

## Rules

- pdfkit requires the Node runtime — it doesn't run on edge/workerd (use a separate service or pre-render)
- Use `doc.bufferedPageRange()` for multi-page headers/footers
- Embed images with a buffer/path — compress before sending

- Use `/run-verify` if needed
- Use `/run-test` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib pdfkit)
- No known security/performance pitfalls (lib pdfkit)
- Lint, typecheck, tests pass
