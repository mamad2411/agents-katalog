---
name: decompose-epic
description: Decompose a PRD or epic into vertically-sliced user stories using a Jeff Patton-style user story map; produces docs/maps/<slug>.md. Story slices, not an engineering WBS (work-breakdown).
---

# decompose-epic

> Break a PRD or epic into a Jeff Patton-style user story map. Slices are vertical (shippable), not horizontal (layer-by-layer).

## When to use

- A PRD describes more than one user activity or release.
- The user says "break this down", "what's the smallest slice?", "user story map".
- A workflow needs an ordered list of stories before implementation.

## Inputs

- PRD path (required).
- Optional: number of intended releases (default 2: walking skeleton + next).

## Procedure

1. Read [`User-story-map.md`](../../templates/User-story-map.md).
2. Read the PRD's **Problem**, **Goals**, **Requirements**, **Acceptance criteria**.
3. Identify 2–5 high-level user activities (the **backbone**, left to right).
4. For each activity, list the user tasks vertically. Order by frequency or sequence.
5. Group tasks into releases:
   - **Walking skeleton** — minimum set that proves the journey end-to-end.
   - **Subsequent releases** — themed slices.
6. Write `docs/maps/<slug>.md` from the template.

## Quality bar

- Each story is shippable on its own; no "build the database, then the API, then the UI" decomposition.
- Each story is a user-observable behavior.
- Walking skeleton ≤ 5 stories.

## Output

- File: `docs/maps/<slug>.md`.
- Summary listing backbone activities and walking-skeleton story count.
