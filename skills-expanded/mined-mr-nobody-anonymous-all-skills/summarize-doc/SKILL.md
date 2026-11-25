---
name: summarize-doc
description: "Converts a document into a summary. Use when the user asks about the document thing."
category: skill-governance
domain: skill-governance
subdomain: general
version: 1.0.0
license: Apache-2.0
risk: low
source:
  repository: "product-on-purpose/agent-skills-toolkit"
  commit: "333810d901"
  imported_at: "2026-09-20"
  license: "Apache-2.0"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# summarize-doc

Read the document, then write the summary. A worked example lives in
[the basic example](examples/basic.md).

## Steps

1. Read the document.
2. Write the summary.
