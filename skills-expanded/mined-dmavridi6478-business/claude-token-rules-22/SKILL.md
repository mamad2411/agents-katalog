---
name: claude-token-rules-22
description: The "22 Claude Rules to stop hitting token limits" turned into an auditable checklist — non-negotiables (effort, model, cache, scheduled tasks, screenshots) and basics (one message, one topic per chat, Projects, short instructions, /clear in Claude Code). Audits a CLAUDE.md, a connector list and a workflow against the rules and reports measured savings candidates. Use when usage limits are hit early, before building scheduled tasks, or when reviewing CLAUDE.md size. Run via /token-audit.
---

# 22 Claude rules to stop hitting token limits

Source: infographic by how-to-ai.guide. These are one creator's heuristics. Several figures (for example "$5,725 of work a month on Opus vs $1,273 on Fable", "4,784 tokens full screenshot vs under 100 cropped") are the author's own numbers — do not repeat them as facts. Rule 10 ("Paste Anthropic's two sentences") names no sentences on the card; do not invent them.

## I. Non-negotiables
1. Medium effort, never Max.
2. Save the free reset for a bad day, not Monday morning.
3. One model per chat; the card recommends Opus 5.5 over Fable (author's cost claim).
4. Never change model between turns: each model has its own cache.
5. Never return to an old chat; the cache expires. Summarise in 10 lines, start new.
6. End quick questions with "No web search."
7. Plan in text, ask for the file last.
8. Highlight; never ask for a full redo.
9. Load connectors on demand; switch off apps the chat does not need.
10. (Unspecified on the card — see note above.)
11. Crop every screenshot; convert PDFs to Markdown.
12. Pause every scheduled task you do not read (an hourly task is 24 runs a day).

## II. Basics
13. Start every task with "ask me questions." 14. One message with all asks. 15. Speak instead of typing. 16. Never correct; edit the prompt and restart. 17. One topic per chat. 18. Keep standing instructions under 2,000 words. 19. Put reused files in a Project. 20. In Claude Code: one task, then /clear; CLAUDE.md under 200 lines; /usage weekly. 21. Split the day into three sessions; check Usage first. 22. Ask for images rarely.

## Audit procedure (what can be measured)
1. CLAUDE.md: `wc -w` and `wc -l`. Pass = ≤ 2,000 words and ≤ 200 lines (rules 18 and 20). Report the margin.
2. Connectors enabled in the session (rule 9): list them; flag those unused by the task.
3. Scheduled tasks/routines (rule 12): list triggers; flag any that fire more than daily or whose output is never read.
4. Attached images/PDFs (rule 11): flag uncropped screenshots and PDFs not converted.
5. Chat hygiene (rules 5, 14, 16, 17): can only be assessed from what the user describes.
Report PASS / FAIL / CANNOT MEASURE per rule. Never invent token counts.
