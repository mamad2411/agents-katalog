---
name: lean
description: Use when the user invokes /lean, says "save tokens", "token efficient", "don't drain my tokens", "watch the budget", "cheap mode", or at the start of any large multi-step task where token cost matters. Also use when about to do bulk reads, spawn subagents, or process large files/MCP data and cost discipline is needed.
---

# Lean Mode

**Core principle: quality stays, waste goes.** Token efficiency means eliminating redundant work, never cutting corners. A wrong guess, a skipped verification, or a sloppy edit costs more tokens to fix than it saved.

**First action on invocation:** read `LEARNINGS.md` in this skill's folder and apply every entry. It is short by design.

## The Protocol (execute in this order)

### 1. Plan first
Write a numbered plan (7 steps max) before any multi-step work. Execute chronologically. Re-plan only when blocked, not when curious.

### 2. Ask, never guess
If anything is ambiguous, ask BEFORE starting: one batched AskUserQuestion with multiple-choice options covering ALL open questions. One round trip. A wrong assumption doubles the job.

### 3. Intake discipline (input tokens)
- Grep/glob before Read. Read line ranges, never whole large files.
- Never re-read a file you just edited or already have in context.
- Big command output: pipe through `head`/`tail`/`grep`/`jq`, or redirect to a scratch file and grep that.
- MCP pulls (Notion, Gmail, Drive, project trackers): fetch the specific page/thread/record. Never dump whole databases or unfiltered search results.
- ToolSearch: load every tool you'll need in ONE call.
- Browser work: prefer text extraction over screenshots. Images cost far more tokens than text.
- Notes and memory files are leads: use them to skip broad discovery, then verify only the specific fact live.

### 4. Delegation policy
- NEVER spawn a subagent on your most expensive model tier. Set an explicit cheaper model on every Agent call: a mid-tier model by default, the cheapest tier for mechanical work (bulk reads, copy transforms, scraping, formatting).
- Every subagent gets a complete plan: exact file paths, exact output format, no exploration budget.
- Don't delegate what one grep answers. Do delegate bulk surface work so the expensive main model stays the orchestrator.

### 5. Output discipline (output tokens cost ~5x input)
- Edit with diffs. Never rewrite a whole file for a partial change.
- Never echo file contents or code back into chat. Reference paths as `file:line`.
- Final summary: 5 sentences or fewer unless the task genuinely needs more. No restating the plan or the diff.
- Build only what was asked. No speculative extras, no unrequested refactors.

### 6. Verify proportionally
Run the ONE test or command that covers the change. Never claim "done" without proof (quality floor), never run full suites or builds "just to be safe" (waste ceiling).

### 7. Session hygiene
Long contexts re-bill everything on every message (softened by prompt caching, but never free). Concrete triggers, checked at task boundaries only (never mid-task):
- Past roughly 45% of the context window (tunable: check LEARNINGS.md for the current number), or any low-context system warning appears: suggest writing a handoff note + starting a fresh session before the next task.
- Topic switch to unrelated work: suggest a fresh session regardless of context size.
- Never let auto-compact fire mid-task; it burns tokens summarizing and loses detail you didn't choose to lose.

## Self-improvement loop
When the user corrects a token-wasting behavior, or you catch yourself violating this protocol: append ONE line to `LEARNINGS.md` (`YYYY-MM-DD | pattern | rule`). Cap the file at 20 entries; when it exceeds that, consolidate duplicates into the strongest single rule. This is how the skill gets smarter without getting heavier.

## Rationalizations vs reality

| Excuse | Reality |
|---|---|
| "Reading the whole file gives better context" | Grep found the section. Read those lines. |
| "A quick default-model subagent is fine here" | Hard rule. Cheaper model with a plan, always. |
| "Guessing saves a round trip" | Wrong guess = full redo. Ask once, batched. |
| "Full suite is safer" | The scoped test covers the change. Suites are for CI. |
| "A longer summary is more helpful" | Unread text is pure cost. Five sentences. |
| "They'd probably want this extra piece too" | Unrequested work is waste. Ask or skip. |
| "I'll re-check the file to be sure my edit landed" | Edit errors on failure. It landed. |

## Red flags — STOP before the tool call
- Read with no line range and no prior grep on a file over ~200 lines
- Agent call with no `model` param
- A second AskUserQuestion in the same task (you failed to batch)
- Write replacing a file when Edit would do
- Fetching data the conversation already contains
- Screenshot when page text would answer the question

## Measuring your savings
`scan-sessions.sh` (in this folder) scores your past Claude Code sessions from the local transcripts: weighted token units per session and per message. Run it before adopting lean to capture a baseline, then again after a couple of weeks and compare. See README.md.
