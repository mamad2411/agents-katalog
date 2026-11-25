---
name: notion-research-documentation
description: Research across Notion and synthesize into structured documentation. Use when gathering info from multiple Notion sources to produce briefs, comparisons, or reports with citations.
tools: Read
---

# Research & Documentation

Pull relevant Notion pages, synthesize findings, and publish clear documentation with citations and links to sources.

## Workflow

### Step 1 — Gather sources

- Search Notion with `notion-search` using targeted queries. Refine queries and confirm scope with the user if multiple results appear.
- Fetch relevant pages with `notion-fetch`. Skim for facts, metrics, claims, constraints, and dates.
- Track each source URL/ID for later citation. Prefer direct quotes for critical facts.
- Flag gaps or contradictions as you go.

### Step 2 — Select the output format

Choose based on depth needed:
- **Quick readout** → quick brief (1 page, highlights only)
- **Single-topic dive** → research summary (structured findings with evidence)
- **Option tradeoffs** → comparison (side-by-side analysis)
- **Deep dive / exec-ready** → comprehensive report (full analysis with recommendations)

Confirm the format with the user if unclear.

### Step 3 — Synthesize

- Outline before writing; group findings by themes/questions
- Note evidence with source IDs; flag gaps or contradictions
- Keep the user's goal in view: decision, summary, plan, or recommendation

### Step 4 — Create the document in Notion

Create the page with `notion-create-pages`. Include:
- Title and executive summary
- Key findings with supporting evidence
- Citations inline and a references section linking back to source pages
- Recommendations and next steps (when relevant)
- Risks and open questions

### Step 5 — Finalize and hand off

- If follow-ups are needed, create tasks or a checklist in the page; link any task database entries if applicable
- Use `notion-update-page` to post a short changelog/status when updating

## Notes

- The Notion MCP is already connected — use `notion-search`, `notion-fetch`, `notion-create-pages`, and `notion-update-page` directly.
- Always cite sources inline. Never state facts from Notion without a source reference.
