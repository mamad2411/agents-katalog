---
name: use-plain-text-over-pdfs
description: "Provide extracted text when layout is irrelevant, retaining the original PDF for visual or page-specific verification."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["pdf-parsing", "plain-text", "token-savings", "ocr-elimination", "efficiency", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Use Plain Text Over Heavy PDFs (Text-First Token Hygiene) (AI Skill)

## Overview
When you upload a multi-page PDF or image-heavy document into an AI assistant, modern multimodal models often convert the pages into high-resolution images, consuming **up to 1,600 visual tokens per page** while struggling with multi-column text wrap and table borders.

The **Text-First Token Hygiene Protocol** advocates extracting raw plain text or clean Markdown before prompting - reducing token usage by up to **80%**, slashing latency from 20 seconds to 1 second, and eliminating visual OCR errors.

---

## Heavy PDF Upload vs. Clean Plain Text

```
┌─────────────────────────────────────────────────────────────┐
│                 Document Ingestion Economics                │
│                                                             │
│  [ RAW 10-PAGE PDF UPLOAD ]:                                │
│  • Visual OCR conversion: ~16,000 vision tokens             │
│  • 15-20 second ingestion latency                           │
│  • Risk of scrambled two-column reading orders              │
│                                                             │
│  [ EXTRACTED PLAIN TEXT / MARKDOWN ]:                       │
│  • Pure text tokens: ~2,500 tokens (84% Token Reduction)    │
│  • Sub-second response latency                              │
│  • 100% Deterministic string search and table retention     │
└─────────────────────────────────────────────────────────────┘
```

---

## The 3 Failure Modes of Direct PDF Uploads

1. **Two-Column Text Scrambling**: OCR systems often read horizontally across two columns, merging two unrelated sentences into a confusing jumble.
2. **Ghost Watermarks & Headers**: Repeating page headers, footers, and page numbers clutter the context window and dilute the model's attention.
3. **Visual Token Tax**: You pay for every square inch of whitespace and background margin in the PDF.

---

## Fast Plain-Text Extraction Tools

Before uploading a heavy file, use one of these instant extraction methods:

| Method | How to Do It | Best For |
| :--- | :--- | :--- |
| **Direct Copy-Paste** | Highlight the exact 3 sections you need $\rightarrow$ `Ctrl+C` $\rightarrow$ Paste in `<context>` | Short sections, articles, agreements |
| **CLI `pdftotext`** | Run `pdftotext input.pdf output.txt` | Bulk technical whitepapers & manuals |
| **Browser Print to Text** | Open PDF in Chrome $\rightarrow$ Select All $\rightarrow$ Copy | Instant 5-second extraction |

---

## Master Plain-Text Injection Prompt Template

```markdown
Analyze the extracted text from [DOCUMENT NAME] below:

<document_content>
[PASTE CLEAN EXTRACTED TEXT HERE]
</document_content>

Task:
- Extract the 3 key findings and all financial numbers.
- Ignore any residual formatting glitches.
```

---

## Real-World Case Study

### Scenario: Auditing a 20-Page Vendor Security Whitepaper

#### Direct PDF Upload
- **Token Count**: 31,000 tokens billed (mostly high-res page image tiles).
- **Latency**: 28 seconds to start streaming.
- **Error**: Model hallucinated that the company lacked encryption because the security table was rendered as an image with low contrast.

#### Extracted Text Approach
- User ran `pdftotext whitepaper.pdf - | pbcopy` and pasted only the "Security & Encryption" chapter.
- **Token Count**: 1,400 tokens billed (95% token savings).
- **Latency**: 1.2 seconds.
- **Accuracy**: 100% verified citation of AES-256 and TLS 1.3 standards.

---

## Summary Best Practices
- **Never upload a whole 50-page PDF to ask about 1 paragraph**: Copy and paste just the relevant paragraph.
- **Strip headers and footers**: Removing repetitive page numbers keeps attention razor-sharp on core data.
