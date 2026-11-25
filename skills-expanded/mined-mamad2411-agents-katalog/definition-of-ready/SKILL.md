---
name: definition-of-ready
description: >
  Create or update a GitHub Project item of type 'docs' as the team's living
  Definition of Ready (DoR) reference checklist. This project item defines the
  minimum criteria a user story must meet before entering a sprint, and is
  consulted by /refine-story during the DoR compliance check at the end of every
  refinement session. Trigger when the user says "/definition-of-ready", "create
  definition of ready", "set up DoR", "update our definition of ready", "what is
  our DoR", or any variation of managing the team's Definition of Ready checklist.
---

# /definition-of-ready — Definition of Ready

Create or update the team's **Definition of Ready** as a **GitHub Project item**
of type `docs`. This item defines the minimum criteria a user story must meet before it can be
committed to a sprint. It is consulted by `/refine-story` at the end of every refinement session
to verify the story qualifies for "Ready for Implementation".

> **GitHub model:** Items created by this skill are **real GitHub Issues** in a private backing
> repository, added to the GitHub Project with `gh project item-add`. The backing repository is
> private so issues are never visible in any public repo. Resolve it from `AGENTS.md` / `CLAUDE.md`
> alongside the project number. Use `gh issue edit` and `gh issue comment` (with `--repo`) for
> content updates. Project fields (Type, Status, etc.) are set via GraphQL on the project item.

## Step 0 — Resolve the GitHub Project

Resolve before any operation:

1. Check `AGENTS.md` and `CLAUDE.md` for a configured project name/number and owner.
2. If not found, list available projects and ask:
   ```bash
   gh project list --owner <org-or-user> --format json | jq '.projects[] | select(.number==<project_id>)'
   ```

Read `references/github.md` for the exact commands.

---

## Step 1 — Check for an existing DoR item

Search for an existing DoR project item:

```bash
gh project item-list <project-number> --owner <org-or-user> --format json \
  | jq '.items[] | select(.title == "Definition of Ready")'
```

- If one exists: show it to the user and ask:
  - _"A Definition of Ready item already exists. Do you want to update it, view it, or create a new one?"_
  - **Update** → jump to Step 2 with the existing content pre-loaded; use `updateProjectV2DraftIssue`
  - **View** → print the item ID and stop
  - **Create new** → continue to Step 2 (the old item will remain; inform the user)
- If none exists: continue to Step 2.

---

## Step 2 — Compose the DoR checklist

Start from the base content in `docs/definition-of-ready.md`. Present the four minimum criteria plus any team-specific additions:

```markdown
## Definition of Ready

A Product Backlog item is Ready for a Sprint when it meets all of the following criteria:

### Minimum Criteria (non-negotiable)
- [ ] **Small** — can be completed by one developer within a single sprint
- [ ] **Sized** — has a relative effort estimate (Fibonacci: 1, 2, 3, 5, 8, 13...)
- [ ] **Just Enough Detail** — has acceptance criteria (Given/When/Then) sufficient to confirm the item functions as intended
- [ ] **Understood** — the Development Team has enough shared understanding to make a forecast in Sprint Planning

### Team-specific Criteria (optional additions)
<!-- Add any criteria specific to your team here -->
```

Ask the user:
- _"Do these criteria reflect your team's Definition of Ready? You can add team-specific criteria (e.g., 'has a technical spike completed', 'dependencies identified', 'designs approved') before we create the project item."_

Iterate until the user approves.

---

## Step 3 — Create or update the project item

Read `references/github.md` for the exact commands.

**If creating a new item:**
1. Create the project item with `gh project item-create`.
2. Set `Type = docs` on the item via `updateProjectV2ItemFieldValue`.

**If updating an existing item:**
1. Get the draft issue ID from the project item.
2. Update the body via `updateProjectV2DraftIssue`.

---

## Step 4 — Report

Tell the user:
- The project item ID of the created/updated item.
- That `/refine-story` will check this item at the end of every refinement session before moving a story to "Ready for Implementation".
- Suggest running `/definition-of-done` next if the team's DoD has not been set up yet.

---

## Rules

- Do not create the item until the user approves the checklist in Step 2.
- The item title must be exactly `Definition of Ready` — no suffixes.
- The four minimum criteria (Small, Sized, Just Enough Detail, Understood) are always included and cannot be removed — they are the non-negotiable baseline from Scrum.
- Team-specific criteria are additive only — they extend the minimum, never replace it.
- If the user asks to view the current DoR only, print the item ID and stop.
