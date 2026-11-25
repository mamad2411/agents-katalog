---
name: claude-50-use-cases
description: Index of 50 Claude use cases in 2026 grouped into ten areas (writing, research, coding, MCP and integrations, personal productivity, image analysis, business uses, Microsoft 365, productivity and workflow, education), with the prompt pattern to start each group and which installed skills cover it. Use when the user asks what Claude can do for their role or wants ideas by category. Source infographic "50 Claude Use Cases - Everything Claude can do for you in 2026" (Batch 102). Items marked (Assist) on the slide mean Claude supports a human rather than owning the task.
---

# 50 Claude use cases (2026)

| Area | Use cases on the slide (numbers as printed) | Start here in this repo |
|---|---|---|
| Writing and content | 1 long-form writing; 2 copywriting and marketing copy; 3 LinkedIn and social content; 4 email drafting; 5 creative writing; 6 technical writing and documentation | `copywriting`, `article-writing`, `linkedin-strategy`, `email-drafter`, `tech-docs-generator` |
| Research and analysis | 7 deep research with web search; 8 document analysis and summarisation; 9 competitive intelligence; 10 academic and scientific research (assist); 11 data interpretation and pattern analysis; 12 legal document review (assist) | `deep-research`, `competitor-analysis`, `claude-data-use-cases`, `contract-review` |
| Coding and development | 13 code generation; 14 debugging; 15 code review and refactoring; 16 autonomous agentic coding with Claude Code (assist); 17 automated test writing; 18 database queries; 19 API integration and boilerplate; 20 security vulnerability identification (assist) | `code-review`, `tdd-workflow`, `sql-optimization-patterns`, `security-review` |
| MCP and integrations | 21 MCP app integrations; 22 support-ticket triage and automation; 23 Google Workspace integration | `mcp-builder`, `mcp-dev-team-6`, `os-support` agent, `google-workspace-ops` |
| Personal productivity | 24 thinking partner and second brain; 25 summarising long content; 26 planning and scheduling | `claude-thinking-partner`, `ai-second-brain`, `weekly-planning-workflow` |
| Education and learning | 27 study material creation; 28 language learning and translation; 29 tutoring and concept explanation | `/learn-faster`, `learn-feynman`, `translate-preserve-tone` |
| Productivity and workflow | 30 Projects for persistent context; 31 Artifacts for runnable outputs; 32 memory across conversations (when available); 33 Cowork for desktop file automation; 34 computer use for UI automation (assist); 35 Skills for custom workflow automation; 36 extended thinking for hard problems; 37 adaptive reasoning for agentic tasks | `claude-six-levels`, `skill-creator`, `computer-use` |
| Microsoft 365 | 38 Claude in Excel; 39 in PowerPoint; 40 in Word; 41 in Microsoft 365 Copilot Researcher | `xlsx`, `pptx`, `docx`, `ms365-free-alternatives` |
| Business and professional | 42 strategic planning and brainstorming; 43 meeting summaries and action items; 44 HR and talent workflows (assist); 45 legal research and case analysis (assist); 46 financial analysis and modelling (assist); 47 brand voice consistency at scale | `business-decision-frameworks`, `meeting-notes-processor`, `hr` , `brand-voice`, `startup-financial-modeling` |
| Image and visual analysis | 48 image analysis; 49 chart interpretation; 50 document OCR | `image`, `pdf-to-markdown`, `invoice-receipt-processor` |

Cautions (added here): the "(Assist)" items are the high-stakes ones (legal, HR, finance, security, science); a human must verify the output. Items 41 and 38-40 depend on the user's Microsoft 365 licence and are not available through this repo. Item 32 is labelled "when available" on the slide; do not assume memory exists in a given surface.
