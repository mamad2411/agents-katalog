---
name: Task Decomposer
slug: task-decomposer
description: "Use when the user has a large, complex, or ambiguous request that needs to be broken down into smaller, actionable steps for AI assistance. Helps users structure prompts, manage context window limits, plan multi-session work, and get better results from AI coding agents. Also for 'too complex', 'where do I start', 'break this down', 'step by step', 'context too large', 'multi-step task', 'prompt structure', 'AI workflow', 'organize my request'."
license: MIT
compatibility: opencode, claude-code, cursor, windsurf, copilot
metadata:
  category: development
  audience: developers
---

# Task Decomposer

Help users decompose complex requests into structured, AI-friendly task sequences. Optimizes for context window efficiency, clear dependency ordering, and measurable progress — so the user gets better results from fewer, more focused interactions.

## Philosophy

Most AI frustration comes from one root cause: **asking for too much at once**. A single vague prompt produces a shallow result. Task decomposition reverses this — it teaches users (and guides the assistant) to think in atomic, dependency-ordered units.

The model: **Plan → Slice → Prompt → Verify → Next**

---

## User-Facing Framework

When a user says something large or vague, walk them through this decomposition framework:

### Step 1: Goal Articulation

Ask the user clarifying questions to define the **true objective**:

- "What is the single outcome you want when this is done?"
- "What constraints matter? (deadlines, tech stack, standards)"
- "What does success look like? How will you verify it?"
- "What are you *not* trying to do? (anti-goals)"

**Output:** A one-paragraph goal statement. If it takes more than 3 sentences, keep refining.

### Step 2: Dependency Map

Help the user identify the natural order of work:

```
Level 1 — Foundation   (setup, config, data model)
Level 2 — Core Logic   (business logic, API, main feature)
Level 3 — Polish       (UI, error handling, edge cases)
Level 4 — Verify       (tests, review, deploy)
```

Ask: "Which of these must exist before the next can start?"

**Output:** A numbered list of 3-7 phases with dependencies marked.

### Step 3: Slice into Atomic Prompts

Each prompt the user will give to the AI should be:

| Property | Description |
|---|---|
| **Atomic** | One logical change — one file, one concern |
| **Standalone** | Has enough context to execute without history |
| **Verifiable** | Clear accept/reject criteria |
| **Window-fit** | Fits comfortably in context window (under ~40K tokens of instruction) |

Template for each slice:

```
## Task: [short name]
## Context
[2-3 sentences: what exists, what doesn't, relevant files]
## Requirements
- [bullet list of what the AI should do]
- [specific files to create/modify]
## Acceptance Criteria
- [how to verify this is done correctly]
## Constraints
- [patterns to follow, things to avoid]
```

**Output:** 3-7 prompt cards the user can paste one at a time.

### Step 4: Context Budget Plan

Warn the user about context window limits and plan accordingly:

- **Session 1** (Foundation + Core): ~3 prompts, start fresh
- **Session 2** (Polish + Verify): ~3 prompts, start fresh
- **Cross-session handoff**: End each session with a `CONTEXT.md` summary

Generate a `CONTEXT.md` at each milestone:

```markdown
# Context Handoff — [Milestone Name]

## Completed
- [x] Done item 1 — /path/to/file
- [x] Done item 2 — /path/to/file

## Decisions
- Chose X over Y because Z
- API returns shape: { ... }

## Next session
- Remaining tasks with dependencies
- Files the next agent needs to read first

## State
- Branch: feature/xyz
- Migrations applied: 3
- Environment variables added: DATABASE_URL, API_KEY
```

### Step 5: Execution Order

Present the final plan to the user:

```markdown
## Execution Plan

Phase 1 — Foundation (Session 1)
  Prompt 1: Set up project scaffolding and config
  Prompt 2: Create database schema and models
  Prompt 3: Implement auth middleware
  └─ Verify: run `npm run dev`, confirm login page loads

Phase 2 — Core Logic (Session 1 cont.)
  Prompt 4: Build user CRUD API
  Prompt 5: Implement business logic service
  └─ Verify: run tests, confirm API responds

Phase 3 — Polish (Session 2)
  Prompt 6: Add error handling and validation
  Prompt 7: Style UI components
  └─ Verify: manual QA flow

Phase 4 — Verify (Session 2 cont.)
  Prompt 8: Write missing tests
  └─ Verify: coverage >= 80%, all tests pass
```

---

## Assistant Behavior

### When the user asks something large

1. **Do NOT** start implementing immediately
2. Instead, respond with the Goal Articulation questions (Step 1)
3. Once the goal is clear, present a Dependency Map for confirmation
4. After user approves, generate the Execution Plan with prompt cards
5. Offer to execute Prompt 1 immediately, or let the user drive

### When context is getting full

Monitor the conversation size. If approaching context limits:

1. Summarize decisions and state into a `CONTEXT.md`
2. Advise the user to start a new session
3. Tell them to include the `CONTEXT.md` in the new session's first prompt

### When the user is unsure how to prompt

Offer templates:

```
"I need you to [action] on [file/area]. 
Specifically:
- [requirement 1]
- [requirement 2]
Don't: [what to avoid]
Verify by: [criteria]"
```

---

## Anti-Patterns to Avoid

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| "Build the whole app" | Context overflow, shallow everywhere | Decompose into 5-10 atomic prompts |
| Mid-session context switch | Previous context wastes tokens | Finish prompt → CONTEXT.md → new session |
| No acceptance criteria | AI stops early or over-engineers | Write 1-3 specific checks per prompt |
| Implicit dependencies | AI makes wrong assumptions | State "X must exist before Y" explicitly |
| Vague success criteria | Can't tell when done | "API returns 200 with { id } on POST /users" |

---

## Examples

### Example 1: Full-stack feature plan

User: "I need to add a payment page"

Agent response uses the framework:

1. **Goal clarification**: "What payment provider? Single product or variable amounts? Save payment methods? Any compliance requirements?"
2. **Dependency Map**: `Stripe setup → Checkout API → Payment form UI → Success/failure pages → Tests`
3. **Prompt cards**:
   - Prompt 1: "Set up Stripe SDK, create `/api/create-payment-intent` endpoint"
   - Prompt 2: "Build React checkout form with Stripe Elements"
   - Prompt 3: "Add payment success/failure pages with error handling"
   - Prompt 4: "Write tests for payment flow edge cases"
4. **Context budget**: Session 1 (Prompt 1-2), Session 2 (Prompt 3-4)

### Example 2: Context recovery

User starts a new session: "I was working on the payment page last time"

Agent: "Let me check for a CONTEXT.md file in the project root..."

If found: Read it and continue from where it left off.
If not found: Ask "What was the last thing that was working? Do you remember the key decisions?"

### Example 3: Rescuing a stuck user

User: "My prompt is getting ignored, the AI keeps going off track"

Agent: "Your prompt may be too broad. Let me help restructure it. What are you trying to accomplish?"

Walk through Steps 1-3 and produce a focused single-prompt card.

---

## Reference: When to use which approach

| User says | Approach |
|---|---|
| "Add a login page" | Small → just do it (no decomposition needed) |
| "Build an e-commerce site" | Large → use full framework |
| "It keeps forgetting what we did" | Context full → generate CONTEXT.md handoff |
| "I don't know where to start" | Ambiguous → Goal Articulation first |
| "I have this PR, write tests" | Specific → just do it, no decomposition |
| "My prompt is too long and AI ignores parts" | Bloated → slice into atomic prompts |
