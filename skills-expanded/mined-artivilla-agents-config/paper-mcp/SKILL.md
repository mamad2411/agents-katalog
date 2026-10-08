---
name: paper-mcp
description: Use the Paper MCP server to fetch paper metadata, sections, figures, citations, and full-text context, then translate that context into structured outputs such as summaries, extraction tables, and implementation-ready notes. Trigger when a task involves paper links/DOIs/arXiv IDs, literature review, citation extraction, or Paper MCP setup and troubleshooting.
---

# Paper MCP

Use the Paper MCP server for paper-driven research and implementation tasks. For setup and debugging details (env vars, config, verification), see `references/paper-mcp-config.md`.

## Paper MCP integration rules
These rules define how to translate paper inputs into reliable outputs and must be followed for every paper-driven change.

### Required flow (do not skip)
1. Resolve the paper first (URL/DOI/arXiv/PMID) and fetch high-level metadata before requesting full text.
2. If the full response is large or truncated, fetch section-level context and work section-by-section.
3. Fetch a stable citation list before drafting any claims that depend on references.
4. If figures/tables are relevant, fetch those assets and capture captions prior to synthesis.
5. Only after metadata plus content context are collected, generate the user output (summary/table/notes/code-facing plan).
6. Validate all key claims against source excerpts before marking complete.

### Tool mapping rule
- Paper MCP deployments may expose different tool names.
- Start by listing available paper MCP tools, then map this workflow to equivalent tools in the current server.
- If a required capability is missing (for example, no section fetch or no citation endpoint), note the limitation and continue with the best available fallback.

### Implementation rules
- Treat paper MCP responses as source context, not final prose.
- Keep outputs traceable: tie each important claim to a section, figure, or citation.
- Distinguish evidence from inference clearly.
- Preserve units, metrics, and dataset/task names exactly as written in source context.
- Prefer concise structured output (tables/checklists) when comparing multiple papers.
- For code-facing tasks, extract actionable constraints (input shapes, evaluation metrics, baseline numbers, reproducibility requirements).

### Quality rules
- Do not invent citations, metrics, or section names.
- Call out uncertainty when context is partial, truncated, or conflicting.
- If two sources disagree, present both with scope and date/context differences.
- Keep quoted text short and use paraphrasing for long passages.

## References
- `references/paper-mcp-config.md` - setup, verification, troubleshooting, and input ID guidance.
- `references/paper-tools-and-prompts.md` - tool mapping checklist and prompt templates for common paper workflows.
