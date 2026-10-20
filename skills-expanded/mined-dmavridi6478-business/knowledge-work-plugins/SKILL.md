# Knowledge Work Plugins — Role-Specific Claude Plugin Library

Open-source plugin collection that turns Claude into a specialist for specific job functions. Built for [Claude Cowork](https://claude.com/product/cowork), also compatible with Claude Code.

**Source:** `anthropics/knowledge-work-plugins` (public)
**Local clone:** `/home/user/anthropics/knowledge-work-plugins`
**Marketplace:** [claude.com/plugins](https://claude.com/plugins/)

---

## 11 Plugins

| Plugin | What it does | Key connectors |
|--------|-------------|----------------|
| **productivity** | Tasks, calendars, daily workflows, personal context | Slack, Notion, Asana, Linear, Jira, Monday, ClickUp, Microsoft 365 |
| **sales** | Prospect research, call prep, pipeline review, outreach, battlecards | Slack, HubSpot, Close, Clay, ZoomInfo, Notion, Fireflies |
| **customer-support** | Ticket triage, response drafting, escalation packaging, KB articles | Slack, Intercom, HubSpot, Guru, Jira, Notion |
| **product-management** | Specs, roadmaps, user research synthesis, stakeholder updates | Slack, Linear, Jira, Figma, Amplitude, Pendo, Intercom, Fireflies |
| **marketing** | Content, campaigns, brand voice, competitive briefs, channel reporting | Slack, Canva, Figma, HubSpot, Amplitude, Ahrefs, Klaviyo |
| **legal** | Contract review, NDA triage, compliance, risk assessment, templated responses | Slack, Box, Egnyte, Jira, Microsoft 365 |
| **finance** | Journal entries, reconciliation, financial statements, variance analysis, close, audits | Snowflake, Databricks, BigQuery, Slack, Microsoft 365 |
| **data** | SQL, statistical analysis, dashboards, visualizations, data validation | Snowflake, Databricks, BigQuery, Definite, Hex, Amplitude |
| **enterprise-search** | Find anything across email, chat, docs, wikis in one query | Slack, Notion, Guru, Jira, Asana, Microsoft 365 |
| **bio-research** | Preclinical R&D: literature, genomics, target prioritization, single-cell RNA | PubMed, bioRxiv, ClinicalTrials.gov, ChEMBL, Benchling, Open Targets |
| **cowork-plugin-management** | Create or customize plugins for your org's tools and workflows | — |

---

## Plugin Structure

Every plugin follows the same layout — markdown and JSON, no code, no build steps:

```
plugin-name/
├── CONNECTORS.md                # Connector setup guide
├── README.md                    # Plugin overview
└── skills/                      # Domain knowledge Claude draws on automatically
    └── <skill-name>/
        └── SKILL.md
```

`product-management` also has `commands/` with explicit slash commands (e.g. `/product-management:write-spec`).

---

## Skills per Plugin

### productivity
`memory-management` · `start` · `task-management` · `update`

### sales (35 skills)
`account-context` · `account-plan` · `account-research` · `account-tiering` · `call-prep` · `call-summary` · `close-plan` · `competitive-intelligence` · `create-an-asset` · `crm-hygiene-check` · `customer-health` · `customer-voice` · `daily-briefing` · `deal-advance-gap` · `deal-review` · `deal-signals` · `deal-slip-scenario` · `draft-outreach` · `end-of-day` · `expansion-whitespace` · `forecast` · `handle-objection` · `inbox-sweep` · `lead-triage` · `log-activity` · `pipeline-review` · `renewal-radar` · `rep-context` · `route-lead` · `schedule-meeting` · `setup` · `stakeholder-map` · `team-pipeline` · `update-opportunity` · `weekly-wrap` · `win-loss-review`

### customer-support
`customer-escalation` · `customer-research` · `draft-response` · `kb-article` · `ticket-triage`

### product-management
`competitive-brief` · `metrics-review` · `product-brainstorming` · `roadmap-update` · `sprint-planning` · `stakeholder-update` · `synthesize-research` · `write-spec`

### marketing
`brand-review` · `campaign-plan` · `competitive-brief` · `content-creation` · `draft-content` · `email-sequence` · `performance-report` · `seo-audit`

### legal
`brief` · `compliance-check` · `legal-response` · `legal-risk-assessment` · `meeting-briefing` · `review-contract` · `signature-request` · `triage-nda` · `vendor-check`

### finance
`audit-support` · `close-management` · `financial-statements` · `journal-entry` · `journal-entry-prep` · `reconciliation` · `sox-testing` · `variance-analysis`

### data
`analyze` · `build-dashboard` · `create-viz` · `data-context-extractor` · `data-visualization` · `explore-data` · `sql-queries` · `statistical-analysis` · `validate-data` · `write-query`

### enterprise-search
`digest` · `knowledge-synthesis` · `search` · `search-strategy` · `source-management`

### bio-research
`instrument-data-to-allotrope` · `nextflow-development` · `scientific-problem-selection` · `scvi-tools` · `single-cell-rna-qc` · `start`

---

## Installation

### Claude Code

```bash
# Add the marketplace
claude plugin marketplace add anthropics/knowledge-work-plugins

# Install a specific plugin
claude plugin install sales@knowledge-work-plugins
claude plugin install data@knowledge-work-plugins
```

Once installed, skills activate automatically; slash commands are available in your session (e.g., `/sales:call-prep`, `/data:write-query`).

### Cowork

Install directly from [claude.com/plugins](https://claude.com/plugins/).

---

## Customization

Plugins are generic starting points. Make them yours by:

- **Swap connectors** — Edit `.mcp.json` to point at your tool stack
- **Add company context** — Drop terminology, org structure, and processes into skill files
- **Adjust workflows** — Modify skill instructions to match how your team works
- **Build new plugins** — Use `cowork-plugin-management` or follow the structure above

---

## Prompts

### Load a sales plugin skill

```
Using /home/user/anthropics/knowledge-work-plugins/sales:
Read skills/call-prep/SKILL.md.
Run the call-prep workflow for a meeting with [company name] about [topic].
```

### Customize a plugin for your org

```
Using /home/user/anthropics/knowledge-work-plugins/[plugin]:
Read README.md and CONNECTORS.md.
Customize the skills to use [your CRM/tool] and reflect [your company's] terminology and processes.
```

### Build a new plugin from scratch

```
Using /home/user/anthropics/knowledge-work-plugins/cowork-plugin-management:
Read skills/ to understand the plugin authoring process.
Create a new plugin for [role/function] with skills for [workflow 1], [workflow 2], and [workflow 3].
```

### Run the finance close workflow

```
Using /home/user/anthropics/knowledge-work-plugins/finance:
Read skills/close-management/SKILL.md and skills/journal-entry/SKILL.md.
Walk through the month-end close checklist for [company/period].
```
