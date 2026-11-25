---
name: productivity-category-pointer
description: "Pointer to a library of 33 specialized Productivity skills. Use when working on productivity-related tasks."
risk: none
---

# Productivity Capability Library 🎯

This is a **pointer skill**. The 33 specialized Productivity skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **anywrite** — Compiled CLI covering all 52 endpoints of the Anytype local API — objects, properties, tags, search, chat, files — one binary, no MCP server needed.
- **ask-matt** — Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **box-automation** — Automate Box operations including file upload/download, content search, folder management, collaboration, metadata queries, and sign requests through Composio's Box toolkit.
- **brain-to-docs** — Interview the user to turn project vision and decisions into README and ADR documentation.
- **cal-com-automation** — Automate Cal.com tasks via Rube MCP (Composio): manage bookings, check availability, configure webhooks, and handle teams. Always search tools first for current schemas.
- **calendly-automation** — Automate Calendly scheduling, event management, invitee tracking, availability checks, and organization administration via Rube MCP (Composio). Always search tools first for current schemas.
- **codex-profiles** — Use codex-profiles to run Codex CLI or Codex Desktop with isolated CODEX_HOME profiles for separate accounts, projects, and local state.
- **compile-knowledge** — Compile durable, non-obvious findings into an interlinked markdown knowledge store — atomic files, [[wiki-links]], a maintained index — so an agent gets smarter across sessions instead of relearning the same facts.
- **context-kit** — Evaluate, adapt, and safely install Context Kit personal context artifacts for Claude Code or adjacent agent workflows.
- **daily-gift** — Relationship-aware daily gift engine with five-stage creative pipeline — editorial judgment, synthesis, concept generation, visual strategy, and rendering in H5, image, or video
- **docusign-automation** — Automate DocuSign tasks via Rube MCP (Composio): templates, envelopes, signatures, document management. Always search tools first for current schemas.
- **dropbox-automation** — Automate Dropbox file management, sharing, search, uploads, downloads, and folder operations via Rube MCP (Composio). Always search tools first for current schemas.
- **faf-wizard** — Done-for-you .faf generator. One-click AI context for any project - new, legacy, or famous. Auto-detects stack, scores readiness, works everywhere.
- **file-organizer** — 6. Reduces Clutter: Identifies old files you probably don't need anymore
- **gmail-automation** — Lightweight Gmail integration with standalone OAuth authentication. No MCP server required.
- **google-calendar-automation** — Lightweight Google Calendar integration with standalone OAuth authentication. No MCP server required.
- **grill-me** — A relentless interview to sharpen a plan or design.
- **grill-with-docs** — A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- **grilling** — Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
- **handoff** — Compact the current conversation into a handoff document for another agent to pick up.
- **interview-coach** — Full job search coaching system — JD decoding, resume, storybank, mock interviews, transcript analysis, comp negotiation. 23 commands, persistent state.
- **interview-style-doc-building** — Build structured strategy documents by asking one question at a time and patching the file.
- **markdown-rendering** — Open Markdown reliably in cmux panes and recover from blank rendered surfaces.
- **mdpr-skill** — Review MDPR Markdown presentation workflows with semantic hints, visual checks, and deterministic renderer boundaries.
- **office-productivity** — Office productivity workflow covering document creation, spreadsheet automation, presentation generation, and integration with LibreOffice and Microsoft Office formats.
- **one-drive-automation** — Automate OneDrive file management, search, uploads, downloads, sharing, permissions, and folder operations via Rube MCP (Composio). Always search tools first for current schemas.
- **read-all-adrs** — Read every ADR in a project before summarizing architectural context or decisions.
- **rich-elicitation** — Asks clarifying questions in multiple rounds before starting ambiguous tasks. Fires when 2+ task dimensions each have 3+ viable answers.
- **setup-help** — Walk a user through setup or installation one step at a time with the remaining steps visible.
- **telegram-bot-messaging** — Send Telegram messages, files, and alerts via bot API; ask questions with inline buttons and wait for the answer. Supports multiple bots, named chat targets, and CI/cron/hook notifications.
- **time-ledger** — Natural-language time tracking: parse what the user says they did into Activity/Minutes/Date rows in their own Notion database — asking instead of guessing when unsure.
- **trading-ledger** — A trading journal that captures the decision, not just the fill: thesis, plan, and emotion at the moment of entry, written to the user's own Notion database; reviews grade decisions, not P&L.
- **workorai** — WorkorAI talent-marketplace skill: candidates search jobs and manage applications; employers run the job lifecycle and get ranked candidate matches with white-box fit explanations.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/productivity/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/productivity`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
