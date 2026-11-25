---
name: pdf-viewer
description: >
  Interactive PDF viewer skill. Use when user wants to open, view, annotate,
  highlight, stamp, fill form fields, or sign a PDF with live visual feedback.
  Trigger phrases: "open this PDF", "show me this contract", "highlight the key
  terms", "help me fill out this form", "sign this", "stamp it APPROVED",
  "mark this CONFIDENTIAL", "add initials to each page", "walk me through this
  document". Also trigger when user provides a PDF path or arXiv URL alongside
  any visual/interactive intent. Do NOT trigger for pure summarization or text
  extraction (use native Read tool instead).
---

# pdf-viewer

You have access to a local PDF server that renders documents in a live viewer
and supports annotation, form-filling, and signature placement with real-time
visual feedback.

## Reference files

Load on demand — do not load all eagerly:

| File                      | What's in it                                                                   | When to read                                              |
| ------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------- |
| `references/view-pdf.md`  | Full tool API (`display_pdf`, `interact`), annotation types, coordinate system | Always read on activation — core reference                |
| `references/open.md`      | Opening workflow, supported sources, when NOT to use viewer                    | When user just wants to open/view a document              |
| `references/annotate.md`  | Collaborative annotation workflow, batch patterns, tips                        | When user wants to annotate, highlight, stamp, or mark up |
| `references/fill-form.md` | Form-filling workflows (user-driven vs AI-assisted), unnamed field handling    | When user wants to fill a form                            |
| `references/sign.md`      | Signature/initials placement workflow, coordinate tips                         | When user wants to sign or add initials                   |

## Quick decision guide

| User intent                                    | Action                                             |
| ---------------------------------------------- | -------------------------------------------------- |
| "open" / "show" / "view"                       | `display_pdf` → offer next steps based on doc type |
| "annotate" / "highlight" / "stamp" / "mark up" | Read `annotate.md`                                 |
| "fill" / "form" / "complete this form"         | Read `fill-form.md`                                |
| "sign" / "initials" / "signature"              | Read `sign.md`                                     |
| "summarize" / "what does it say" / "extract"   | **Stop** — use native Read tool, not viewer        |

## Core tools (summary)

- **`list_pdfs`** — list available local PDFs. Call when no path given.
- **`display_pdf(url, page?, elicit_form_inputs?)`** — open document. Returns `viewUUID` (required for all `interact` calls) and `formFields` if PDF has fillable fields.
- **`interact(viewUUID, commands[])`** — all follow-up actions. Batch commands; end with `get_screenshot` to verify.

Full API detail in `references/view-pdf.md`.

## Always

- Call `display_pdf` once per document. Reuse `viewUUID` for all `interact` calls.
- Batch related commands in one `interact` call.
- End annotation/form/sign batches with `get_screenshot` — show result to user.
- Remind user they can download annotated PDF from viewer toolbar when done.
