---
name: ctx-add-feature
description: Design and implement a new feature from scratch — product definition, engineering design, implementation, and validation. Use when building a feature that doesn't exist in the codebase yet.
metadata:
  author: nicolasse
  version: "2.0.0"
---

# New Feature

Creates a new feature end-to-end: product definition, technical design, implementation, and contract validation. Use this when the feature doesn't exist in the codebase yet.

## Input

The user describes what they want to build. Can be vague ("I need follow-up reminders") or specific ("A scheduled message system that sends WhatsApp messages N hours after a conversation ends").

## Workflow

### 1. Understand the Feature

Start a conversation to understand what the user wants. Ask about:

- What does it do? (the core behavior in one sentence)
- Who triggers it? (user action, cron, event, API call)
- What's the expected outcome? (message sent, data stored, UI updated)
- What are the main use cases? (happy paths)
- What's out of scope? (boundaries)

Keep it short. Don't interrogate — 2-3 questions max per round, stop when you have enough to write a first draft.

### 2. Create Feature Directory

Pick a kebab-case name for the feature. Confirm with the user.

Create `context/{feature}/` and copy the three template files from `context/_template/`.

### 3. Write product.md

From the conversation, write `product.md`. Follow the template — keep it minimal:

- Overview: 1-2 sentences
- Use cases: one line each
- Business rules: plain language
- Out of scope: plain language

Show it to the user. Iterate until they confirm. Write the file.

### 4. Design engineering.md

Now look at the existing codebase to inform the technical design. **Use an agent to explore the repos** — spawn a single agent to search across all repos for relevant patterns, interfaces, and conventions:

- List directories at the workspace root (skip `context/`) to understand what services exist
- Look at similar features to understand patterns, conventions, and how services communicate
- Identify which repos will need changes for the new feature
- Understand existing interfaces the new feature needs to integrate with

Then design the engineering contract with the user:

- Where does this feature live? (new service, existing service, multiple)
- What interfaces does it expose? (APIs, events, queues)
- What existing interfaces does it consume?
- What constraints apply?

Write `engineering.md`. Keep it minimal — only the contracts that matter. Show to user, iterate, write.

### 5. Implement

Use the contract-reviewer agent definition (if available) and implement the feature respecting the contracts defined in `product.md` and `engineering.md`.

**Use an agent for implementation** — when changes span multiple repos, spawn a single agent that has the full product and engineering context to implement across all affected repos.

If the feature is large, break it into multiple chunks — one per use case or logical piece. After each chunk, review before continuing.

### 6. Validate

After implementation, review the changes against both contracts:

**Product contract (`product.md`):**
- Do all use cases work as described?
- Are business rules enforced?

**Engineering contract (`engineering.md`):**
- Are all interfaces and contracts respected?
- Do naming conventions and patterns match?

If violations: fix them before proceeding.

### 7. Write implementation.md

Now that the code exists, write `implementation.md` describing what was just built:

- Key files created, organized by repo
- Flows for each use case
- Data model if any was created
- Known limitations (first version, so there will be some)
- Recent changes: today's date + "Initial implementation"

### 8. Handoff

Do NOT commit. Leave everything for the developer to review.

Provide a summary:
- What was designed (product + engineering decisions)
- What was implemented (files created/modified)
- Contract review result
- Any open questions or suggestions for next steps

The developer decides when and how to commit.
