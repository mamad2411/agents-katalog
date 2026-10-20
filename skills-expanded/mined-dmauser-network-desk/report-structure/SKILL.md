# Skill: Report Structure & Quality Bar

## Purpose

Define the standard skeleton and quality checklist for every network-desk deliverable, so reports are consistent, professional, and ready to render to HTML/PDF/DOCX/XLSX.

This skill governs **structure and quality**. The four renderer skills (`html-report`, `pdf-report`, `docx-report`, `xlsx-workbook`) govern **format conversion**.

## Standard report skeleton (Markdown)

Author the report as Markdown first — it is the source of truth that every renderer consumes.

Start with an optional **YAML front-matter** block — the DOCX/PDF/HTML renderers turn it
into a real **cover page** (title, subtitle, colored accent rule, metadata block). Cover
precedence is **front-matter → CLI flag (`--title`/`--subtitle`/`--classification`/`--version`/`--author`) → first `# H1`**. The `--specialist` value is never used as the title.

```markdown
---
title: <Topic>
subtitle: <Short descriptor, e.g. "Azure Firewall Rule Audit">
classification: Confidential
version: "1.0"
author: <Author or team>
---

# <Specialist> — <Topic>
<!-- e.g. "Firewall Engineering — Azure Firewall Rule Audit" -->

## Executive Summary
2–5 sentences a non-expert can act on: what was analyzed, the headline finding,
and the single most important recommendation. No jargon, no preamble.

## Scope & Assumptions
- What is in / out of scope
- Environment (cloud, region, subscription/account)
- Assumptions and the date of analysis (vendor limits/pricing change)

## Findings
Use a table for anything enumerable (rules, costs, gaps, risks). Rank by severity.

| # | Finding | Severity | Evidence | Impact |
|---|---------|----------|----------|--------|
| 1 | ...     | High     | ...      | ...    |

## Architecture / Topology
Embed at least one Mermaid diagram for any design or topology. (Use the
`cn_vnet` `network-diagram` skill to generate it.) Offer Excalidraw/draw.io on request.

The DOCX, PDF, and HTML renderers render ```` ```mermaid ```` fences to an **embedded
PNG** (centered, with a "Figure N." caption) using the **local Mermaid CLI** (`mmdc`,
falling back to `npx -y @mermaid-js/mermaid-cli`); the `.mmd`/`.png` are saved under
`network-desk/<specialist>/diagrams/`. If the CLI is unavailable the diagram is omitted
gracefully (caption + an appendix listing the source + the install command) — the source
is never dumped inline and no hosted service is called. Install with
`npm install -g @mermaid-js/mermaid-cli` to enable embedding.

## Recommendations
Numbered, prioritized, each with the concrete next step and the owner/effort.

## Appendix / References
- Vendor documentation links (with the product name)
- Raw data, calculations, or command output

> Analysis only — verify against vendor documentation before applying.
```

## Quality checklist (apply before rendering)

- [ ] **Executive summary leads** — reader gets the answer in the first paragraph.
- [ ] **Every number is sourced** — limits/quotas/prices cite a vendor doc and a date, or are labeled "illustrative — verify current values".
- [ ] **Findings are in a table**, ranked by severity, with evidence and impact columns.
- [ ] **At least one diagram** for any architecture/topology.
- [ ] **Recommendations are actionable** — numbered, prioritized, with next steps.
- [ ] **Headings are hierarchical** (`#` → `##` → `###`) — the DOCX/PDF TOC is built from them.
- [ ] **No secrets** — redact keys, tokens, connection strings, public IPs of real systems.
- [ ] **Footer present** — ends with the analysis-only line.

## Format selection — pick by purpose

| Format | Use when… | Renderer skill |
|--------|-----------|----------------|
| **Markdown** | Inline review, GitHub/PR, source of truth | (none — author directly) |
| **HTML** | Quick shareable, self-contained, opens in any browser | `html-report` |
| **PDF** | Stakeholder/exec hand-off, print, fixed layout | `pdf-report` |
| **DOCX** | Editable deliverable, corporate templates, tracked changes | `docx-report` |
| **XLSX** | Cost models, capacity plans, anything with **editable formulas** | `xlsx-workbook` |

When the user says "report" without a format, default to **Markdown + HTML** and offer PDF/DOCX/XLSX.

## Output location

Save the Markdown source and every rendered artifact under:

```
network-desk/<specialist>/reports/<kebab-topic>-<YYYYMMDD>.<ext>
```

`<specialist>` is the owning domain specialist's directory name (e.g. `firewall-engineer`, `pricing-analyst`, `vnet-architect`). Keep the `.md` source next to the rendered file so it can be regenerated.

## References

- Keep a Changelog (structure inspiration): https://keepachangelog.com/
- Microsoft Azure architecture docs: https://learn.microsoft.com/azure/architecture/networking/

**Analysis only — verify against vendor documentation before applying.**
