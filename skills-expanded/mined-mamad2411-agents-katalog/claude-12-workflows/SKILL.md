---
name: claude-12-workflows
description: Twelve things you can do with Claude (build CLI tools, spin up an MCP server, personal RAG over your notes, learn a codebase in an hour, mock interviews, browser automation, tailor a resume, scheduled cloud routines, landing pages and pitch decks without Figma, parallel multi-agent code reviews, Auto Mode, build your own skills) with the steps, the feature each uses, and the matching command or skill in this repo. Use when the user asks what Claude can do or how to start one of these workflows. Source @shiva.bytes (Sivasankar Natarajan) 11-second video "12 Insane Things That You Can Do with Claude" (Batch 103). A different infographic from the Anna Bilan "12 Insane Things" already mapped in Batch 99.
---

# 12 workflows (Sivasankar Natarajan)

| # | Workflow | Steps on the card | Feature | In this repo |
|---|---|---|---|---|
| 1 | Build CLI tools in minutes | Describe it in plain English; Claude builds, codes and tests it; get a ready-to-run binary | Claude Code | `tdd-workflow`, `python-scaffold` |
| 2 | Spin up your own MCP server | Choose the tool; define endpoints + auth; Claude builds server + config | Claude Code, MCP protocol | `mcp-builder`, `mcp-server-patterns` |
| 3 | Personal RAG over your notes | Connect your apps; ask your question; get cited answers | Connectors, Memory | `ai-second-brain`, `rag-implementation` |
| 4 | Learn any codebase in an hour | Drop a GitHub repo into Claude; ask it to map the architecture; get a guided walkthrough, file by file | Claude Code, Projects | `/map-codebase`, `codebase-onboarding` |
| 5 | Mock interview practice on demand | Tell Claude the role and round type; it role-plays as the interviewer; get live feedback after each answer | Skills (/interview) | `/mockinterview`, `/interview` |
| 6 | Automate the browser | Install Claude in Chrome; say "find me the cheapest flight under 6 hours" | Claude in Chrome | `computer-use`, `playwright-skill` (supervise; see `web-task-scoping`) |
| 7 | Tailor your resume per job | Paste the JD and your resume; Claude rewrites for ATS keywords; exports a clean PDF | Skills (/resume) | `/dream-job`, `/resume-review` |
| 8 | Schedule cloud Routines that run while you sleep | Set prompt + schedule; connect your tools; get results anytime | Routines, Connectors | `scheduled-routine` command |
| 9 | Design landing pages and pitch decks without Figma | Describe what you need; Claude designs it live; export or hand off | Claude Design | `design-templates`, `premium-html-presentation` |
| 10 | Run parallel multi-agent code reviews | Drop /ultrareview on your open PR; agents scan for bugs; get labeled results (critical / high / medium / low) | /ultrareview, sub-agents | `/multi-agent-review`, `/team-review`, `/prod-bug-check` |
| 11 | Let Auto Mode ship code end to end | Give a spec or bug; Claude builds and tests; opens a PR for review | Claude Code, Auto Mode | `/feature-dev`, `/prp-pr` |
| 12 | Build your own Skills with /commands | The card repeats the Auto Mode steps (spec or bug, build and test, open PR) under this heading | Skills 2.0 (/commands) | `/write-a-skill`, `skill-creator` |

## Cautions
- Card 12's three bullets are a copy of card 11's, so the "build your own skills" steps are not actually shown. Use `/write-a-skill` instead of the card.
- `/ultrareview` and "Skills 2.0" are named on the card; I could not verify either as current product features. Treat them as the author's labels and check your Claude Code version's `/help`.
- Auto Mode and browser automation act on your behalf. Review the PR before merging, and supervise any browser task that logs in or pays.
- Item 8 routines run with the connectors you grant; grant the minimum.
