---
name: dn-summarize
description: >
  Deep, non-obvious summarization of any content — URLs, documents, text, images, PDFs, or files.
  Use when the user says "summarize", "dn-summarize", "/dn-summarize", "break this down",
  "what's important here", or asks for analysis of a URL, article, document, image, screenshot,
  or pasted text. NOT a standard summary — extracts hidden insights, tensions, and actionable
  implications instead of restating what the content already says.
---

# DN-Summarize

Analyze the provided content (URL, document, image, text, or file) using the framework below.
Do NOT produce a conventional summary that restates the author's main points. Instead, extract
what a smart reader would miss on a first pass.

## Input Handling

- **URL**: Use WebFetch to retrieve content, then analyze
- **Image/screenshot**: Read the image file directly, then analyze
- **PDF**: Read with the Read tool (specify pages if large), then analyze
- **File**: Read the file, then analyze
- **Pasted text**: Analyze directly

## Analysis Framework

After reading the content carefully, produce exactly these four sections:

### 1. Non-Obvious Insights (3-5)

Identify things that aren't stated explicitly but can be inferred from the content.
Skip anything the author already highlights as a key point.

### 2. Tensions & Contradictions

Where does the argument conflict with itself, or with conventional wisdom?
What's left unresolved?

### 3. The "So What"

If a smart, busy person could only take away one actionable implication from this,
what would it be and why?

### 4. What's Missing

What question does this content raise but never answer?
What would you want to know next?
