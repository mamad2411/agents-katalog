---
name: readable-arxiv
description: Fetches an arXiv paper — metadata (title, authors, abstract) via WebFetch on the abs page, plus the full PDF via curl on arxiv.org/pdf and structured extraction by pdfvision. Use when the URL is in the form arxiv.org/abs/{paper_id}.
---

# arXiv Paper Reader

## Steps

### 1. Fetch metadata with WebFetch

Use WebFetch to load the arXiv page and extract paper information.

- Title
- Authors
- Abstract

### 2. Download the PDF

```bash
curl -L -o /tmp/paper.pdf "https://arxiv.org/pdf/{paper_id}.pdf"
```

### 3. Extract the PDF contents

Prefer [pdfvision](https://github.com/yamadashy/pdfvision) — it reports per-page density and works in any agent runtime that can spawn a CLI:

```bash
npx pdfvision /tmp/paper.pdf
```

If only a Claude Code-style multimodal Read tool is available, `Read /tmp/paper.pdf` also works.
