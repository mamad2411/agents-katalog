---
name: datasheet-extractor
description: Extract pinouts, voltages, registers, timing, and limits from user-supplied datasheet PDFs or excerpts. Use for lab and hardware prep. Never invent electrical specifications; label UNKNOWN when missing.
---

# Datasheet Extractor

Extraction stage only (ADR 0002). Do not calculate, interpret trends, or specify charts.

1. Bound the source (file/pages).
2. Extract requested fields with locators (page/section).
3. Mark missing fields UNKNOWN.
4. Hand off numbers needing math to deterministic calc tools, then `structured-data-evaluator`.

May call `source-inspector` in `document` or `dataset-metadata` mode.
