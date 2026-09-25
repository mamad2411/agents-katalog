# Repo Referensi: claude-office-skills/skills

Repo: https://github.com/claude-office-skills/skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/claude-office-skills_skills
API: curl "localhost:27126/repos/readme?name=claude-office-skills_skills"
Dibuat: 2026-09-16

## Cuplikan README
# claude-office-skills/skills

Source: https://github.com/claude-office-skills/skills
Fetched: 2026-09-16

## README
# Claude Office Skills

> A curated collection of practical Claude Skills for real-world office tasks. Zero setup required.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Skills](https://img.shields.io/badge/Skills-136+-blue.svg)](#skills)
[![MCP Tools](https://img.shields.io/badge/MCP_Tools-39-green.svg)](#office-mcp-server)

---

## 🚀 NEW: Office MCP Server

**39 fully-implemented tools** for Office document operations via MCP (Model Context Protocol).

| Module | Tools | Capabilities |
|--------|-------|--------------|
| **PDF** | 10 | Extract, merge, split, compress, watermark, forms, **OCR** |
| **Spreadsheet** | 7 | Read/write Excel, analyze, formulas, pivot tables |
| **Document** | 6 | Create/edit Word, templates, merge documents |
| **Conversion** | 9 | xlsx⇔csv, docx⇔md, json→xlsx, batch convert |
| **Presentation** | 7 | Create PPT, extract, Markdown→slides, HTML export |

**Quick Start:**
```bash
cd mcp-servers/office-mcp && npm install && npm run build
```

[📖 Full MCP Documentation](./office-mcp/SKILL.md) | [💻 MCP Source Code](./mcp-servers/office-mcp/)

---

## 📚 NEW: Extensible Knowledge Base

**Domain knowledge as structured data** - customize Claude's expertise for your jurisdiction and industry.

| Layer | Description | Customizable |
|-------|-------------|--------------|
| **Base** | Universal risk patterns, completeness checklists | Core team |
| **Jurisdictions** | US, China, EU, California... | Community |
| **Domain** | Healthcare, Finance, Government... | Community |
| **Custom** | Your company rules, private knowledge | You |

**Available Knowledge:**
- 15+ risk patterns (liability, IP, termination, confidentiality...)
- 19 completeness check items
- 4 jurisdictions (US Federal, California, China, EU)

**Quick Start:**
```yaml
# In your SKILL.md
knowledge:
  base:
    - mcp-servers/office-mcp/knowledge/base/risk_patterns.json
  jurisdictions:
    - mcp-servers/office-mcp/knowledge/base/jurisdictions/california.json
```

[📖 Knowledge Index](./KNOWLEDGE_INDEX.md) | [🤝 Contribute Knowledge](./CONTRIBUTING_KNOWLEDGE.md)

---

## 🤖 NEW: Pre-built Agents

**5 ready-to-deploy AI personas** with curated ski
