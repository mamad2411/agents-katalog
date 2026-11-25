---
name: minimum-viable-parser
description: Decide the cheapest, lightest, accurate acquisition and parsing path before reading, scraping, parsing, transforming, downloading, OCRing, or browser-automating any webpage, app page, local file, screenshot, PDF, document, dataset, or software UI. Use before web/app/page inspection, JS-heavy page decisions, screenshot/file parsing, scraping workflows, browser or Playwright alternatives, data extraction, and agent efficiency routing.
---

# Minimum Viable Parser

## Purpose

Choose the minimum viable acquisition path that preserves the accuracy required by the task. Run this decision before reading, scraping, parsing, transforming, downloading, OCRing, screenshotting, or browser-automating a source.

Optimize for speed, low setup cost, and high-fidelity parsing. The cheapest path is valid only when it can satisfy the requested output and evidence quality.

## First Decision

Before touching the source, infer:

- Target type: URL, app page, local file, image, screenshot, PDF, document, spreadsheet, dataset, media, software UI, or mixed input.
- Required output: summary, exact quote, structured JSON, table, screenshot finding, code-oriented inspection, transformed file, or task-specific artifact.
- Fidelity requirement: text-only, structure-preserving, layout-sensitive, visual, interactive, authenticated/local state, or behavior-sensitive.
- Available context: pasted content, attached files, local project files, current browser/app state, existing screenshots, caches, or known APIs.
- Constraints: no paid services, no sign-in-only services, avoid first-time installs unless accuracy requires them.

Make the decision internally by default. State the selected path in one short sentence only when it helps the user understand cost, delay, or tool choice.

## Acquisition Ladder

Use the first rung that can meet the task's fidelity requirement.

1. **Existing context**: Use pasted text, provided screenshots, attached files, local files, current app/browser state, or prior command output.
2. **Cheap metadata probe**: Inspect path, extension, MIME type, headers, file size, modified time, or a small sample before full parsing.
3. **Structured source**: Prefer JSON, CSV, XML, RSS/Atom, sitemaps, manifests, embedded JSON-LD, OpenGraph metadata, APIs, exports, or database/query access when available.
4. **Static text/HTML**: Use direct HTTP/file reads and lightweight DOM/table extraction for pages whose meaningful content is present without rendering.
5. **Format-native parser**: Use the relevant parser or skill for PDFs, DOCX, XLSX, PPTX, images, audio/video, archives, or source-code projects.
6. **Visual extraction**: Use screenshot analysis or OCR only when the content is rasterized, visual, canvas-based, inaccessible as text, or layout fidelity matters.
7. **Local browser automation**: Use Playwright or an available browser skill when JavaScript rendering, interaction, viewport layout, canvas, login state already present locally, or app behavior is required.
8. **Install a lightweight dependency**: Install only when the current environment cannot parse accurately and the dependency is established, free, and task-appropriate.

Do not use paid, sign-in-only, or hosted browser services such as Browserbase-style infrastructure unless the user explicitly asks for them.

## Escalation Rules

Escalate to a heavier rung when evidence shows the current rung is incomplete or unreliable:

- Static HTML is empty, skeletal, blocked, or hydration-dependent.
- The target data appears in rendered DOM but not source HTML.
- User asks about layout, responsive behavior, screenshots, charts, canvas, maps, animations, or interactions.
- The file is scanned, image-only, encrypted, malformed, or needs layout-preserving extraction.
- OCR confidence is low, tables are misaligned, or exact text matters.
- A transformation risks corrupting a structured file without a format-native library.
- The task requires verifying extracted data against visible UI or rendered output.

Prefer one targeted escalation over trying many tools. Stop escalating once the output is accurate enough for the task.

## Notification Rules

Notify the user before:

- Installing any dependency or downloading browser binaries.
- Starting browser automation when cheaper parsing might reasonably be expected.
- Downloading large files or large sets of assets.
- Using any third-party service.
- Doing anything slow, network-heavy, stateful, or likely to affect user accounts, sessions, or remote systems.

Do not notify solely because the task requires crawling multiple pages. Keep crawls bounded by the user's request or by a conservative inferred scope, and summarize the scope used in the final answer.

## Tool Selection Guidance

- Use local files and already available tools first.
- Use `rg`, file metadata, and small samples before full project or corpus reads.
- Use direct HTTP for static pages when source content is sufficient.
- Use a DOM parser for HTML structure instead of brittle string scraping when available.
- Use format-aware tooling for PDFs, Office documents, spreadsheets, images, archives, and media.
- Load another skill only after the selected path clearly matches that skill.
- Load a Playwright/browser skill only after deciding that browser automation is required.
- Prefer spinning up an already available tool over downloading or installing a new one.
- If installing is required, choose the smallest established dependency that solves the accuracy problem.

## Validation

Validate the acquisition result before relying on it:

- Check that the expected content is present, not just that a command succeeded.
- Compare counts, headings, titles, table headers, visible labels, or known anchors against the request.
- For structured extraction, verify schema shape and a few representative rows/items.
- For visual tasks, verify that the screenshot or image region actually contains the target.
- For transformed files, verify the output opens or parses and preserves required content.

If validation fails, escalate one rung and retry. If all free/local paths fail, explain the blocker and the lightest viable next option.

## Output Behavior

Return whatever the user requested. Do not produce a separate parsing report unless useful.

When the path matters, include a compact note such as:

`Acquisition path: static HTML parse; escalated to Playwright because the table was rendered client-side.`

Keep that note short and omit it when it adds no value.
