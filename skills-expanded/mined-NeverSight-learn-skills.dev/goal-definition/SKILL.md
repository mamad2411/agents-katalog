---
name: goal-definition
description: Use when you have a raw idea or request and need to define a clear goal with success criteria before exploring solutions. Use when requirements are vague, when "what does done look like" is unclear, or when assumptions need surfacing.
---

# Goal Definition

Take a raw idea or request and turn it into a clear, actionable goal with explicit success criteria, assumptions, and constraints.

## When to Use

- You have a vague idea or user request that needs sharpening
- Before brainstorming approaches — define the "what" before the "how"
- Requirements are ambiguous or incomplete
- You need to align on success criteria before investing in design
- Assumptions are lurking but haven't been stated

**When NOT to use:** The goal is already crystal clear with written success criteria, or a `goal-definition.md` already exists and is still accurate.

## Input

- Raw idea or request from the user
- `context-map.md` from the artifact folder (recommended but not required)
- See `references/context-sources.md` for additional project documentation that may provide context

## Output

- `goal-definition.md` saved to the artifact folder (see `references/formats.md` for template)

## The Process

### Step 1: Locate Artifact Folder

If `context-map.md` exists in a known artifact folder, use that same folder. Otherwise, ask the user for the artifact folder path (same as `research` Step 1).

### Step 2: Restate as "How Might We"

Take the raw idea and reframe it as a crisp problem statement:

> **Raw:** "We need better search"
> **Reframed:** "How might we help users find the content they need in under 3 seconds?"

This forces clarity on what's actually being solved. Present the reframed statement and confirm with the user before proceeding.

### Step 3: Ask Sharpening Questions

Ask 3-5 targeted questions — no more. One question per message. Focus on:

1. **Who is this for?** — The specific user and their situation
2. **What does success look like?** — Concrete, observable outcomes
3. **What are the real constraints?** — Time, tech, resources, compatibility
4. **What's been tried before?** — Prior attempts, why they failed or didn't happen
5. **Why now?** — What changed that makes this important

Use structured options where possible:

```
What is the primary user for this feature?
  A. New users during onboarding
  B. Power users with large datasets
  C. All users equally
  D. Internal team / admin users
```

Do NOT proceed until you understand who this is for and what success looks like. These two answers shape everything downstream.

### Step 4: Surface Assumptions

Before writing the goal document, list every assumption you're making:

```
ASSUMPTIONS I'M MAKING:
1. The existing search index can handle the new query patterns
2. Users primarily search by title, not content
3. We can add a new API endpoint without breaking existing clients
4. Response time under 500ms is achievable with current infrastructure
→ Correct me now or I'll proceed with these.
```

Wait for confirmation. Unvalidated assumptions are the #1 source of wasted work downstream.

### Step 5: Reframe as Testable Success Criteria

Turn vague goals into concrete, testable conditions:

> **Vague:** "Make search better"
> **Testable:**
> - Search returns relevant results for 90% of common queries
> - Results appear within 500ms
> - Users can filter by date, type, and author
> - Zero-results page suggests alternative queries

Present and confirm with the user.

### Step 6: Define Scope Boundaries

State explicitly what is NOT included and why:

- **Not Doing:** [Thing] — [Reason]
- **Not Doing:** [Thing] — [Reason]

The "Not Doing" list is arguably the most valuable part. Focus is about saying no to good ideas.

### Step 7: Write Goal Definition

Write `goal-definition.md` to the artifact folder using the template from `references/formats.md`. Include all findings from Steps 2-6.

Announce the saved path:

> "Goal definition saved to `[path]/goal-definition.md`."

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The goal is obvious" | Obvious goals have hidden assumptions. Write them down — it takes 5 minutes. |
| "We'll figure out success criteria later" | Without success criteria, you can't know when you're done. Define them now. |
| "I don't want to constrain the solution" | Goal definition constrains the problem, not the solution. Brainstorming handles solutions. |
| "The user already told me what they want" | Users describe solutions. Your job is to uncover the underlying problem. |
| "Assumptions are too early to surface" | The earlier you surface assumptions, the cheaper they are to correct. |

## Red Flags

- Jumping to solutions before defining the problem
- No "who is this for" answer
- Success criteria that say "works correctly" or "is fast"
- No assumptions listed
- Empty "Not Doing" list — everything has scope boundaries
- Proceeding without user confirmation on reframed problem

## Verification

Before handing off, confirm:

- [ ] Problem restated as "How Might We" and confirmed by user
- [ ] 3-5 sharpening questions asked and answered
- [ ] Assumptions listed and confirmed
- [ ] Success criteria are specific and testable
- [ ] "Not Doing" list has at least 2 items
- [ ] `goal-definition.md` saved to artifact folder

## Next

> "Goal defined. Next recommended skill: **brainstorming** — explore approaches to achieve this goal."
