---
name: asking-user-next-steps
description: IMPORTANT for GitHub Copilot — especially after completing a task, always use ask_user to wait for the user's next instruction instead of going silent.
---

# Asking User for Next Steps

## Overview

When you need to find out what the user wants to work on next, **always prefer the `ask_user` tool over plain text questions** — it provides a structured form, captures responses reliably, and delivers a significantly better UX than asking in free text.

This skill is critical to keeping conversations productive. GitHub Copilot should **never go silent** after completing a task — always close the loop by prompting the user for their next instruction.

## Core Pattern

```
At session start OR after every completed task:
  If ask_user tool is available → use ask_user tool (REQUIRED)
  Otherwise → ask in plain text as a fallback
```

**Rule: Never end a turn silently after finishing a task.** Completing work without asking what's next leaves the user waiting and breaks the conversational flow.

## How to Detect GitHub Copilot Environment

You are running inside GitHub Copilot CLI if **any** of the following are true:
- The `ask_user` tool is listed among your available tools
- Your system prompt explicitly mentions "GitHub Copilot CLI"
- The `report_intent` tool is available (it is GitHub Copilot-specific)

## Implementation

```
// ✅ CORRECT: Use ask_user tool in GitHub Copilot
ask_user(
  message: "Task complete! What would you like to work on next?",
  requestedSchema: {
    properties: {
      task: {
        type: "string",
        title: "Next task",
        description: "Describe what you'd like to do next"
      }
    },
    required: ["task"]
  }
)

// ❌ WRONG: Plain text question when ask_user is available
"What would you like to work on next?"

// ❌ WRONG: Going silent after task completion
(no follow-up at all)
```

## When to Use

- **Session just started** with no clear task provided
- **A task just completed** — immediately follow up with `ask_user`; do NOT end the turn silently
- **Instructions are ambiguous** and you need the user to clarify direction before proceeding

## Important Rules

- **Always use `ask_user` when available** — plain text questions are only acceptable if the tool is unavailable
- **Always include a schema** — a schema-less `ask_user` call loses the structured input benefit entirely
- **Keep forms focused** — one topic per form; do not combine unrelated questions in a single call
- **Acknowledge completion first** — briefly summarize what was done before asking for next steps, so the user has clear context

## For Persistent Enforcement (Recommended)

Skills are **opt-in** — they must be explicitly invoked via the `skill` tool. For this rule to apply automatically in every session without manual invocation, also add it to your global instructions file:

**`~/.copilot/copilot-instructions.md`**:

```markdown
## Task Completion

Always follow the `asking-user-next-steps` skill requirements:
- After completing any task, **never go silent**
- Always use the `ask_user` tool (with a schema) to prompt for the next instruction
- Only fall back to plain text if `ask_user` is unavailable
```

This ensures the rule is always active, while the skill provides the detailed implementation reference.

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---|---|---|
| Asking in plain text when `ask_user` is available | Worse UX, response not captured reliably | Use `ask_user` tool |
| Calling `ask_user` with no schema | Loses structured input; just like plain text | Always define `requestedSchema` |
| Mixing multiple unrelated questions in one form | Confusing and hard to answer | Split into separate calls |
| Going silent after task completion | User doesn't know GitHub Copilot is done and waiting | Always prompt for next steps |
