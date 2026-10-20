---
name: follow-context-engineering
description: Manage AI agent context effectively — reduce context rot, improve work quality
argument-hint: "[scope]"
related:
  - follow-math-concepts
  - deep-validate
  - report
  - suggest-next-action
  - plan
  - loop-until-complete

---

## Goal

Manage the context of an AI coding agent effectively to preserve work quality across long-horizon tasks, using context engineering principles from Anthropic

## Scope

For AI coding assistants that run multi-step work, make many tool calls, or operate across sessions — to manage the context window systematically

## Execute

### 1. Curate System Context

> Goal: Curate the initial context with the fewest high-signal tokens necessary

1. Write clear system instructions — direct, unambiguous language
2. Organize instructions into clear sections (background, instructions, tool guidance, output description)
3. Use XML tags or Markdown headers to separate sections so the model distinguishes contexts clearly
4. If an `AGENTS.md` exists, read and follow it — it is the primary project-level context
5. Include only information essential to the current task — no irrelevant data

### 2. Optimize Tool Usage

> Goal: Use tools efficiently to reduce context consumption

1. Use tools that return concise output, not bloated output
2. Avoid tools with overlapping functionality
3. When similar tools exist, pick the most token-efficient one
4. Batch independent tool calls into parallel calls to cut rounds and context accumulation
5. Use `code_search` instead of reading files one by one to search
6. Use `offset` and `limit` to read only the needed parts of a file

### 3. Apply Compaction

> Goal: Use compaction when context nears full to preserve conversational flow

1. Summarize message history while preserving: architectural decisions, unresolved bugs, implementation details
2. Drop: redundant tool outputs, verbose error messages, irrelevant information
3. Use tool result clearing: remove old raw tool results that don't need re-inspection
4. After compaction, start fresh context with the summary + the 5 most relevant recent files
5. Review and score per `### 7. Review And Score Context Rot` when context degradation is detected

### 4. Use Structured Note-Taking

> Goal: Use agentic memory to maintain progress outside the context window

1. Create and update `progress.txt` or `NOTES.md` to track progress across sessions
2. Record: main goal, completed sub-tasks, key decisions, dependencies, problems encountered
3. Use the `create_memory` tool to save context needed across projects
4. Read the notes before resuming work to restore context quickly
5. Update notes after every significant sub-task is done

### 5. Decompose With Sub-Agent Pattern

> Goal: Break big work into sub-tasks to bound each part's context

1. Split a large task into sub-tasks with independent, separate contexts
2. Each sub-task runs in a clean context, accumulating no context from other sub-tasks
3. Each sub-task returns only a condensed summary (1,000-2,000 tokens), not raw context
4. Use `/plan` to lay out the sub-tasks before starting
5. Use `/loop-until-complete` for each sub-task

### 6. Manage Context Lifecycle

> Goal: Manage context across the whole conversation lifecycle

1. Start: curate the minimal context the task needs
2. During work: restate the goal every 5-10 tool calls to keep goal alignment
3. Before reset: summarize and preserve important context
4. After reset: read the notes and restore context quickly
5. Check for context rot signals every 10 tool calls
6. If context degradation is found, review and score per `### 7. Review And Score Context Rot`

### 7. Review And Score Context Rot

> Goal: Check context rot systematically and score it

1. Check context rot signals: repeated answers, forgetting earlier context, drifting from the goal, degraded answer quality
2. Check context preservation: summarize the main goal, current progress, and remaining tasks
3. Check context reset practices: recommend a reset when context gets too large
4. Check goal reminders: restate the main goal every 5-10 tool calls
5. Check task decomposition: sub-tasks stay within 10 tool calls
6. Check context window management: use `offset` `limit` `code_search`, batch parallel calls
7. Compute a health score from the 6 metrics per `### 6. Context Rot Review`
8. Rank findings by severity — per `deep-review-codebase/SKILL.md` Severity Classification
9. Report results with review score, severity, and action items

## Rules

### 1. Minimal High-Signal Context

Keep context as minimal as possible

- Curate only the high-signal tokens that maximize the chance of good results
- Avoid bloated tool outputs and verbose error messages
- Use `offset`, `limit` when reading large files
- Batch independent tool calls into parallel calls
- Don't re-read the same file multiple times

### 2. Compaction Strategy

Use compaction when context nears full

- Summarize while preserving: decisions, bugs, implementation details
- Drop: redundant tool outputs, verbose messages
- Use tool result clearing for the lightest compaction
- After compaction, start fresh context with the summary + recent files
- Review and score per `### 7. Review And Score Context Rot` when context degradation is detected

### 3. Persistent Memory

Use structured note-taking across sessions

- Record progress in `progress.txt` or `NOTES.md`
- Use `create_memory` for cross-project information
- Read notes before resuming work
- Update notes after significant sub-tasks
- Record: goal, progress, decisions, dependencies, problems

### 4. Task Decomposition

Split work to bound each part's context

- Each sub-task has its own independent context
- Return only a condensed summary, not raw context
- Use `/plan` to lay out sub-tasks
- Use `/loop-until-complete` for each sub-task

### 5. Goal Alignment

Keep goal alignment throughout the conversation

- Restate the main goal every 5-10 tool calls
- Verify output still matches the goal
- Adjust the goal if requirements change
- Use `/suggest-next-action` when the direction is unclear

### 6. Context Rot Review

Check and score context rot systematically

- Check context rot signals every 10 tool calls
- 6 core metrics: Context Rot Detection, Context Preservation, Context Reset Practices, Goal Reminder Usage, Task Decomposition, Context Window Management
- Score per metric: pass = 1, warning = 0.5, fail = 0
- Review score = (total score / 6) × 100%
- Grade: A (90+), B (80+), C (70+), D (60+), F (<60)
- Severity:
  - Critical: lost the main goal, forgot key decisions, redundant rework, major scope drift, wrong results
  - High: clearly degraded answer quality, no context preservation, no goal reminders
  - Medium: redundant or excessive file reads, unclear sub-tasks, no progress summary
  - Low: inconsistent goal-reminder wording, mediocre context window management
- Use `/report` for a findings table: Category, Finding, Severity, Location, Recommendation
- Run `/suggest-next-action` to recommend the next action

- Use /follow-math-concepts if needed
- Use /deep-validate if needed

## Expected Outcome

- The context window is used efficiently with reduced context rot
- High-signal tokens are complete, with no bloated context
- Progress is preserved across sessions via structured notes
- Long-horizon tasks are split into manageable sub-tasks
- Goal alignment is maintained throughout the conversation
- Context rot is detected, scored, and reported systematically
- Findings carry severity, review score, and action items
