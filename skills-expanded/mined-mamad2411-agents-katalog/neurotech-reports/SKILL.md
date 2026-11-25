---
name: neurotech_reports
description: Read and present NeuroTech intelligence briefings when the user asks about neurotech, BCI news, or recent reports.
---

# NeuroTech Reports — Skill Specification

This skill gives you access to the output of the **NeuroTech NewsHound** pipeline,
which runs nightly and produces intelligence briefings on implantable brain-computer
interfaces, ECoG/sEEG, microstimulation, and enabling technologies.

## When to use this skill

Activate when the user asks about:
- Neurotech news, BCI updates, or recent research
- The latest report, briefing, or alerts
- Specific companies (Neuralink, Paradromics, Synchron, Precision Neuroscience, etc.)
- Regulatory milestones (FDA approvals, IDEs, clinical trials)
- What the NewsHound found, discovered, or flagged

## File layout

All files live in this skill's directory (`neurotech_reports/`).

### Reports (by date)

Each run produces four files with the naming pattern `YYYY-MM-DD.*`:

| Pattern | Contents |
|---------|----------|
| `YYYY-MM-DD.md` | Full Markdown report: executive brief, themes, scored items, reviewer notes |
| `YYYY-MM-DD.html` | Styled HTML version of the same report |
| `YYYY-MM-DD.alerts.json` | JSON array of high-priority items (scored 9-10) |
| `YYYY-MM-DD.full.json` | Complete pipeline output: all scored items, themes, errors, metadata |

**To find the latest report:** sort the `.md` files by date in the filename and read the most recent one.

### Aggregate files

| File | Contents |
|------|----------|
| `dashboard.html` | Cross-run summary dashboard |
| `discoveries.yaml` | New companies/entities discovered by the pipeline, pending human review |
| `meta_actions.yaml` | Trace of the meta-agent's self-improvement actions (vocabulary updates, source health checks, coverage assessments) |
| `cron.log` | Raw log of nightly pipeline runs |

### Configuration and memory

| File | Contents |
|------|----------|
| `config.yaml` | Pipeline configuration: sources, watchlist, models, scoring parameters |
| `vocabulary.yaml` | Domain vocabulary (130+ terms) used for PubMed queries and regex filtering |
| `discovery_memory.json` | Persistent entity tracker: companies, labs, technologies seen across runs |
| `editorial_memory.json` | Story-level memory: what has been reported before (for dedup and novelty classification) |

## How to answer questions

### "What's the latest?" / "Any news?"
1. Find the most recent `.md` file by date
2. Read it and present the **TL;DR** and **Themes** sections
3. Mention the number of alerts and offer to show them

### "Tell me about [company/topic]"
1. Read the most recent `.md` or `.full.json`
2. Search for the company/topic in scored items
3. Also check `discoveries.yaml` and `discovery_memory.json` for tracked entities

### "What alerts came in?"
1. Read the most recent `.alerts.json`
2. Present each alert with its score, title, category, and source URL

### "What has the agent been doing?" / "How is the pipeline?"
1. Read `meta_actions.yaml` for the latest self-improvement trace
2. Check `cron.log` tail for run health (duration, token cost, item counts)
3. Mention any source health issues or vocabulary updates

## Formatting

- When presenting reports in chat (Telegram/WhatsApp), use plain text with bold for emphasis — no markdown tables
- Keep summaries concise; offer to go deeper on specific themes or items
- Always cite the report date so the user knows how current the information is
