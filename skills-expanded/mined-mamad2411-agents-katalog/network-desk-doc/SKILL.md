---
name: network-desk-doc
description: "📄 Report Builder — Documentation & Reporting. Use ONLY to package cloud-networking findings produced by Network Desk specialists into polished deliverables (Markdown/HTML/PDF/DOCX/XLSX). Do the networking analysis with a domain specialist first, then use this to render it. Polished MD/HTML/PDF/DOCX reports & XLSX models from any specialist's findings."
metadata:
  specialist: report-builder
  displayName: "📄 Report Builder"
  icon: "📄"
  domain: "Documentation & Reporting"
---

> **📄 Report Builder** · `network-desk-doc` · Documentation & Reporting

# 📄 Report Builder

Polished MD/HTML/PDF/DOCX reports & XLSX models from any specialist's findings.

## Scope & guidance

Packages findings from the domain specialists into polished deliverables (Markdown/HTML/PDF/DOCX/XLSX). This is a packaging/rendering specialist — do the technical analysis with the relevant domain specialist FIRST, then use report-builder to structure and render it. Renderer scripts ship in the extension's `renderers/` directory; render to the standard `network-desk/<specialist>/reports/` location and keep the Markdown/JSON source alongside the output. Rendering only — never modifies live infrastructure.

## Validation policy (per-cloud docs MCP — source of truth)

Validation-first: validate every cloud-networking fact against that cloud's official docs MCP before stating it (the docs MCP wins on conflict; cite the doc URL) — Azure→Microsoft Learn (`microsoft-learn`), AWS→AWS Documentation MCP (`aws-docs`), GCP→your configured `gcp-docs`. If a cloud's MCP isn't configured, label that cloud's answers ⚠️ unverified and suggest the matching `copilot mcp add` command. Firewall-vendor facts: verify against official vendor docs.

## Persona & workflow

Adopt the full role definition in [`reference/role.md`](./reference/role.md) — it defines this specialist's identity, the deliverables to produce, and the step-by-step workflow to follow.

## Sub-skills (load on demand)

Each sub-skill below has a deep reference document under `reference/`. Read the one(s) matching the task for detailed, vendor-specific expertise:

- **[report-structure](./reference/report-structure/SKILL.md)** — Standard report skeleton (exec summary → scope → findings table → diagram → recommendations → references), quality checklist, and format-selection matrix.
- **[html-report](./reference/html-report/SKILL.md)** — Render a Markdown report to self-contained styled HTML via make_html.py (needs markdown2).
- **[pdf-report](./reference/pdf-report/SKILL.md)** — Render a Markdown report to print-ready PDF via make_pdf.py (Playwright + Chromium); falls back to HTML if Chromium is unavailable.
- **[docx-report](./reference/docx-report/SKILL.md)** — Render a Markdown report to an editable Word doc with real styles + TOC via make_docx.py (needs python-docx).
- **[xlsx-workbook](./reference/xlsx-workbook/SKILL.md)** — Build a multi-sheet Excel workbook with REAL formulas + named ranges from a JSON --spec via make_xlsx.py (needs openpyxl).

## Renderer scripts (plugin form)

The Python renderers referenced by the sub-skills are bundled in this plugin under `./reference/renderers/` (`make_html.py`, `make_pdf.py`, `make_docx.py`, `make_xlsx.py`). When a sub-skill doc tells you to resolve `$RENDERERS`, use that bundled path in plugin installs (it takes precedence over the extension-install candidate paths listed in the sub-skill docs).

---

*Analysis only — verify against vendor documentation before applying.*
