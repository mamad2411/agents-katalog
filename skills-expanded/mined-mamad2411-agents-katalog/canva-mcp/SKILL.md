---
name: canva-mcp
description: Guide for using the Canva MCP server integration. Use when creating, importing, exporting, or managing designs in the user's Canva account via MCP. Covers recommended workflows, import limits, template constraints, available tools, and critical pitfalls to avoid.
---

# Canva MCP Skill

Read this skill before using the Canva MCP server.

## When to Use Canva vs Alternatives

Only use the Canva connector when the user specifically needs Canva features — such as using an existing Canva template, accessing their Canva brand kit, organizing Canva folders, or exporting from Canva. If the user just needs slides, social media graphics, or visual content without Canva-specific requirements, prefer creating designs directly (e.g. Google Slides for presentations, or generating images with other tools) — these produce better results and are far more reliable. Ask the user if they really need Canva.

## Design Creation — Recommended Workflow

1. Build the design locally as a PPTX file (editable text, shapes, layout), then use `import-design-from-url` to upload it to Canva. This is the most reliable path to editable Canva designs.
2. AVOID `generate-design` — it relies on Canva's AI to generate the design, Manus can only control the input query. Do not use it unless the user explicitly requests it and understands that Canva's AI creates the final content, not Manus.
3. If you must use `generate-design`, ALWAYS specify `design_type` (e.g. `"presentation"`, `"social_media_post"`). Check the MCP for the supported design types. Without it, the API almost always returns "document type is not supported".

## Import Limits (import-design-from-url)

- **PPTX is the best format** — produces editable Canva designs with text, shapes, and layout intact.
- PDF imports have broken spacing and layout issues — avoid for multi-element designs.
- Image-based content (PNG, JPG, or any rasterized format) becomes a static, non-editable image in Canva regardless of the import format used.
- The `url` parameter must be a publicly accessible URL. Upload assets first with `upload-asset-from-url` if needed.

## Available Tools

Strictly adhere to the available tools in the Canva MCP server.  Do not hallucinate new tools or promise the user functionalities that the Canva MCP server does not provide.
Instead, inform the user that the functionality is not exposed by Canva and they have either:
1. Use the Canva Web App instead, or
2. Let Manus create their slides without using Canva (Google Slides, Nanobanana, etc), or
3. Think of and offer a workaround using existing Canva MCP tools. For example, if the brand kit is not directly fetchable, you may instead choose to fetch a design that uses that template and reference that instead. When using a workaround plan, inform the user of it AND ALWAYS ASK FOR APPROVAL OR FEEDBACK.

## Export Workflow

Always call `get-export-formats` before `export-design` to discover valid format options for the design.

## Important Constraints

- `generate-design` has a free quota. Extensive usage requires a paid Canva subscription. Most users don't have one.
- If any Canva tool fails 3 times consecutively, STOP retrying and inform the user of the issue.
- If a tool call returns an error, do NOT tell the user it succeeded. Report the actual error.
- Design editing is currently NOT supported — you cannot modify elements within an existing Canva design programmatically.
- `create-design` creates a blank design with given dimensions. It does NOT generate content.
- `create-design-from-candidate` requires a `candidate_id` from a prior `generate-design` call.
