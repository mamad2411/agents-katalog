---
name: company-product-signals
description: Infer product areas and goals from job postings, Reddit, and app-store signals. Use when the user asks for "product signals", "job postings", or "product goals" for a company.
---

# Company Product Signals

Research public product signals and infer what a company is building toward.

## What to use

- Company job postings and LinkedIn Jobs
- Reddit threads and relevant product discussions
- App Store / Google Play descriptions, release notes, and reviews when relevant

## Output format

- `Product features (from job postings):` bullet list
- `Product goals (from job postings):` bullet list, clearly labeled as inferred
- `Reddit / app signal:` 1-2 sentences only if it adds signal
- `Source hints:` short list of sources used

## Rules

- Ground product features and goals in evidence from role descriptions whenever possible.
- Keep inferred items labeled as inference.
- Stay concise and factual.
