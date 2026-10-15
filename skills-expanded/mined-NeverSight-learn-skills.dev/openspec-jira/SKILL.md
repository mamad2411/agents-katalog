---
name: openspec-jira
description: Wrapper for all OpenSpec change operations (new, propose, ff, continue) that ensures changes are prefixed with a Jira ticket number. Use this skill WHENEVER the user wants to create a new OpenSpec change, propose a feature, or fast-forward through artifact creation — especially when working in a Jira-tracked project. Triggers on phrases like "new openspec change", "propose a change", "/opsx:new", "/opsx:propose", "/opsx:ff", "create a spec change", "start a new change", or any request to begin an OpenSpec workflow.
---

# OpenSpec + Jira Convention

This skill ensures all OpenSpec changes are traceable to a Jira ticket by prefixing change names with the ticket number before invoking the underlying openspec workflow.

## Why this matters

Change directories under `openspec/changes/` and spec files under `openspec/specs/` are named after the change. Without a ticket prefix, it becomes hard to link a change back to its Jira story — especially after archiving. Prefixing with the ticket (e.g., `MLC-725-backend-ml-subpackage`) makes the connection explicit in the filesystem and git history.

## Steps

### 1. Ask for the Jira ticket

Before invoking any openspec command, ask the user for a Jira ticket number:

- **If available**, use a structured question tool (e.g., Claude: `AskUserQuestion`, Windsurf Cascade: `ask_user_question`) with:
  - Question: "What's the Jira ticket for this change?"
  - Option 1: Custom text input for ticket number
  - Option 2: "Skip (no ticket)"
- **Otherwise**, ask directly: "What's the Jira ticket for this change? (type the ticket number or 'skip')"
- If the user provides a ticket number (e.g., `MLC-725`), use it as the prefix
- If they skip, proceed without a prefix

**Format for prefixed names:** `<TICKET>-<change-name>` — all lowercase, hyphens between words.

Examples:
- Ticket `MLC-725`, change `backend ml subpackage` → `MLC-725-backend-ml-subpackage`
- Ticket `MLC-100`, change `add auth middleware` → `MLC-100-add-auth-middleware`
- No ticket, change `fix typo in prompts` → `fix-typo-in-prompts`

### 2. Proceed with the openspec operation

Once you have the final change name (with or without prefix), invoke the appropriate skill:

| User intent | Skill to invoke |
|-------------|-----------------|
| Start step-by-step | `openspec:new` with the prefixed name |
| Generate all artifacts at once | `openspec:propose` or `openspec:ff` with the prefixed name |

Pass the prefixed name as the argument so the underlying skill uses it as the change directory name.

### 3. Remind about the convention (first time only)

If this appears to be the user's first time using this workflow (no existing changes with ticket prefixes), briefly note:

> "All changes are prefixed with the Jira ticket number so they're easy to trace back to Jira. You can skip the prefix if there's no ticket."

Don't repeat this reminder on subsequent invocations — trust the user learned it.

## Naming rules

- Ticket number is uppercase: `MLC-725`, not `mlc-725`
- The rest of the name is lowercase with hyphens: `MLC-725-my-change-name`
- No spaces, underscores, or special characters in the change name portion
- Keep the descriptive part concise (3–5 words is ideal)

## When there's no ticket

If the user skips or says there's no ticket, proceed normally — no prefix. Don't block or warn repeatedly. The convention is a guideline, not a hard gate.