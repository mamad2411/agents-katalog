---
name: scriptorium-overview
description: >-
  Guide for the scriptorium multi-agent framework for writing technical books about open-source 
  source code. Use when: starting a new book writing project, understanding the system architecture,
  asking what scriptorium is or does, deciding which agent or phase to use, getting a quick-start
  setup guide, or understanding the hub-spoke design and file pointer mechanism.
license: MIT
---

# Tech-Editorial: Multi-Agent Book Writing Framework

## Core Philosophy
> **Agents are stateless; the file system is stateful.**

Each agent is a one-time worker with no memory of past calls. All cross-agent state lives in shared files on the file system. The Orchestrator (#0) controls information flow via **File Pointers** — explicit file path lists injected into each agent's context.

## Architecture: Hub-Spoke

```
              ┌─────────────┐
              │  Orchestrator │  ← Hub (sole coordinator)
              │     #0        │
              └──────┬───────┘
       ┌─────────────┼─────────────┐
       │             │             │
  ┌────▼────┐   ┌────▼────┐   ┌───▼─────┐
  │ Agent A │   │ Agent B │   │ Agent C │  ← Spokes (no direct inter-agent talk)
  └─────────┘   └─────────┘   └─────────┘
```

- Sub-agents NEVER communicate with each other directly
- All state passes through shared files
- Orchestrator is the only entity that reads all files and issues next instructions

## The 12-Agent Team

| # | Agent | Analogy | Phase | Key Output |
|---|-------|---------|-------|------------|
| #0 | Orchestrator | Film Director | All | Task scheduling, file pointer injection |
| #1 | Architect | Tech Director | 1 | `outline-draft.md`, `source-map.md` |
| #2 | Reader Advocate | Product Manager | 1 | `outline-reader-feedback.md` |
| #3 | Researcher | Code Archaeologist | 3 | `research/chXX-research.md` |
| #4 | Writer | Technical Author | 3 | `drafts/chXX-draft.md` |
| R1 | Code Reviewer | Principal Engineer | 3,4 | `reviews/chXX-r1-code.md` |
| R2 | Consistency Reviewer | Memory Curator | 3,4 | `reviews/chXX-r2-consistency.md` |
| R3 | Content Reviewer | Senior Editor | 1,3,4 | `reviews/chXX-r3-content.md` |
| RS | Student Reader | CS Junior | 3 | `reader-feedback/chXX-rs.md` |
| RE | Engineer Reader | 8yr Engineer | 3 | `reader-feedback/chXX-re.md` |
| RH | Hobbyist Reader | Tech Enthusiast | 3 | `reader-feedback/chXX-rh.md` |
| #11 | Bookbinder | Layout Designer | 5 | `publish/*.html` |

## 5-Phase Pipeline

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
大纲定稿   共享资源   逐章写作   统稿审计   HTML发布
           构建      ×N章
```

## Quick-Start (4 Steps)

1. Copy `agents/`, `framework/`, `templates/` into your book project directory
2. Fill in templates: `source-map.md` (target codebase map), `outline.md` (chapter structure), `style-guide.md` (writing rules), `glossary.md` (initial terms)
3. Configure Orchestrator with: project name, source repo path, total chapters, parallel batch size, target audience
4. Execute Phase 1: Invoke Architect (#1) → Reader Advocate (#2) → R3 review → human approval of `outline-final.md`

## File Pointer Protocol

Every agent invocation includes explicit file lists:
- 📥 **Must-read files**: injected as context before the task
- 📤 **Must-write files**: the agent's sole output targets  
- 🚫 **Forbidden files**: explicitly listed as read-only

This prevents context overload and accidental overwrites.

## Completion Marker System

Each agent appends an HTML comment as the last line of its output:
```
<!-- RESEARCH_COMPLETE -->
<!-- DRAFT_COMPLETE -->
<!-- R1_CODE_REVIEW_COMPLETE -->
<!-- R2_CONSISTENCY_REVIEW_COMPLETE -->
<!-- R3_CONTENT_REVIEW_COMPLETE -->
<!-- REVIEW_COMPLETE -->
<!-- READER_PANEL_COMPLETE -->
<!-- CHAPTER_FINAL -->
<!-- HTML_COMPLETE -->
```

The Orchestrator uses these markers (not SQL alone) to detect true completion.

## For detailed specs, use the other skills:
- `/scriptorium-workflow` — full phase-by-phase execution guide
- `/scriptorium-agents` — all 12 agent specifications with example prompts
- `/scriptorium-templates` — how to fill each of the 8 project templates
