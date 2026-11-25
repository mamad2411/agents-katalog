---
name: plan
description: "Use when the user asks to plan a project, initiative, event, engagement or any multi-step effort before non-trivial work. Produces a structured plan with owners, milestones and binary done-criteria."
allowed-tools: Read, Glob, Grep
argument-hint: "[what to plan]"
---

# Plan

Create a clear, actionable plan. Not a strategy deck. A plan someone can execute this week.

## Step 1: Clarify scope

If the scope is unclear, ask max 3 questions:
- What's the desired outcome?
- What's the deadline or timeline?
- Any constraints (budget, people, dependencies)?

If the user already provided enough context, skip straight to the plan.

## Step 2: Check existing context

Read relevant files before planning. Wherever the workspace keeps them, that means:
- the active and pipeline project folders — is there already work in progress?
- the services-and-pricing sheet — if pricing or services are involved
- the engagement tracker — current commitments and pipeline

If none of those exist, ask once where they live rather than guessing at a path.

## Step 3: Build the plan

### Format

**Goal:** [1 sentence — what success looks like]

**Timeline:** [start → end, or phases]

**Steps:**

| # | What | Owner | By when | Depends on |
|---|------|-------|---------|------------|
| 1 | ... | the owner / a named delegate / other | date | — |
| 2 | ... | ... | date | Step 1 |
| ... | | | | |

**Risks:**
- [risk 1] → [mitigation]
- [risk 2] → [mitigation]

**Open questions:**
- [anything that needs answering before execution]

### Rules

- Max 10 steps. If it needs more, break into phases.
- Every step has an owner and a deadline. "Sometime next week" is not a deadline.
- Flag dependencies explicitly. What blocks what.
- Be realistic about the founder's time — assume a solo operator running several business lines at
  once unless the workspace says otherwise, and check the plan against the hours actually free.
- If the plan involves other people (named delegates, contractors, partners), note who needs to be
  looped in.
- Answer in whatever language the user is writing in, and stay in it

## Step 4: Offer to persist

After the owner approves the plan:
- "Want me to save this as a project file alongside the other active projects?"
- "Want me to update the tracker?"
- "Want me to create calendar blocks or draft emails to loop people in?"
