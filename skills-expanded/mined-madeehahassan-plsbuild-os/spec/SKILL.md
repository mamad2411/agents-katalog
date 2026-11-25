---
name: Spec
description: Write or update a project spec. Use when starting a new product, after a meaningful build session, or when something changed and you want to capture it. Adapts to Claude Code, claude.ai, and Cowork.
---

# /spec

Use this when starting a new project, after a meaningful build session, when something changed and you want to capture it, or when starting a new Claude session and need to get oriented quickly.

---

## Which surface are you on?

**Claude Code**
You have access to the files. Read `project/spec.md` and any existing `project/specs/*/shape.md` folders before writing anything. Write updates to disk directly. Create new dated folders under `project/specs/` when a session deserves one.

**claude.ai chat**
You can't touch files. Ask the user to paste the current `spec.md`, or describe what's there. Return updates as copy-ready markdown blocks labeled by filename so the user knows what goes where. For new dated folders, return the folder name and the full `shape.md` content as one block.

**Cowork**
You have access to the workspace folder. Read the spec and any existing dated folders first. Write updates back to disk. Confirm with the user before overwriting an existing `spec.md` that has recent content.

---

## Before you write anything

This skill shapes a spec. That's thinking work, not building work.

**In Claude Code:** enter plan mode first (Shift+Tab until you see "plan mode"). Don't write files or run commands while shaping. Exit plan mode only once the user has approved the content.

**In chat or Cowork:** confirm out loud that you're shaping, not executing. If the user just wants to ship something, run `/build` instead.

If the request is ambiguous, stop and ask: "Are we shaping a spec, or are we building?" Do not proceed until the user confirms.

---

## Why this matters

Claude has no memory between sessions. The spec is the memory. Keep it alive.

---

## Two places the spec lives

plsBuild OS splits specs into two:

1. **`project/spec.md`** — the **living spec**. What's true right now. One file. Gets updated every session.
2. **`project/specs/`** — the **frozen history**. One folder per decision, dated, named, left alone after it ships.

When someone asks "what did we decide three weeks ago?", you open the matching folder in `specs/` and read the `shape.md` inside. The living spec has moved on. The folder preserves the thinking at the time.

Both matter. Update the living spec every session. Create a new frozen folder when the work deserves one.

---

## When to create a new frozen folder

Every time you shape something meaningful. Signals:
- Starting a new feature
- Making a decision worth remembering
- Changing direction on something already live
- A session produced a real answer

Skip for tiny fixes and work already captured in another folder.

### How to create one

1. Get the current date and time: `YYYY-MM-DD-HHMM`
2. Pick a short slug: `onboarding-flow`, `alert-banner`, `signals-tab`
3. Create `project/specs/YYYY-MM-DD-HHMM-slug/`
4. Copy `project/specs/_template/shape.md` into it
5. Fill in the four sections: what we're building, why this approach, what we ruled out, notes/visuals

Drop any mockups or screenshots in the same folder.

---

## Updating the living spec

After every meaningful session, touch `project/spec.md`:
1. Update Status and Current focus
2. Move completed items from What's Next to Core Features
3. Add new Known Issues
4. Update Last Updated

5 minutes. Saves an hour next session.

---

## Living spec template

Copy this for every new product. Fill it in. On Chat, paste it into the product's Project. On Cowork / Code, save it at `project/spec.md` in the product repo.

```
# [Product Name]

## What it is
One paragraph. What does it do, who is it for, what problem does it solve?

## Status
[ ] Idea
[ ] Building MVP
[ ] MVP done, testing
[ ] Live
[ ] Growing

Current focus: [one sentence on what you're working on right now]

## Stack
Frontend:
Backend/DB:
Auth:
Deploy:
AI:
Payments:
Other:

## Live URLs
Production:
Repo:

## Core Features
What actually exists today. Not planned.

1.
2.
3.

## What's Next
Prioritized. Top item is current focus.

1. [in progress]
2. [next]
3. [after that]

## Known Issues

## Design Direction
3 words. Colors. Fonts. Reference products.

## Key Decisions Made

## Decisions Still Open

## Last Updated
[Date and what changed]
```

---

## Frozen folder template

Use `project/specs/_template/shape.md` as the starting point. Four sections:

1. **What we're building** — one or two paragraphs on the thing itself
2. **Why this approach** — the reasoning, the constraints, why this beat alternatives
3. **What we ruled out** — other options considered, one line each on why they lost
4. **Notes / visuals** — links, mockups, sketches, anything that belongs with the decision

Keep it short. A shape.md is 5 minutes of writing, not an hour.

---

## Workflow layer (once you graduate)

When one product becomes three and a flat spec stops being enough, the same split moves to Notion (or Linear, or whatever you use):

- `spec.md` → a "Product Hub" page in Notion
- `specs/YYYY-MM-DD-HHMM-slug/` → dated subpages under the hub

Same pattern. Different surface.
