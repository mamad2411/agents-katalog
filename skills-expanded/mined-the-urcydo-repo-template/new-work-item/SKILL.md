---
name: new-work-item
description: Creates and scopes a new work item in this repo's work/items/ folder. Use when asked to start, track, or plan a new piece of work, or when a request arrives in work/inbox/ that has no item yet.
---
# New work item

**Role:** orchestrator or planner. A builder with no item for the work creates it in `draft`, names the planner in `next_action`, and stops.

1. Choose the form. Under about an hour and no design questions: light item. Otherwise a full item.
   ```
   python3 tools/new_item.py <slug> --title "Human readable title"          # full
   python3 tools/new_item.py <slug> --title "Human readable title" --light  # one file
   ```
   The tool prints the path to `handoff.md` (or the single file). The id is `<date>-<slug>`.
2. Write the brief (full items, planner only; the orchestrator skips this and hands over): open `brief.md` in the item folder. Fill goal, why now, acceptance criteria, constraints, out of scope. Every acceptance criterion must be checkable by someone who was not there.
3. Check the repo already says nothing on it: skim `docs/INDEX.md` and `docs/decisions/` for related docs and ADRs. Link them in the brief.
4. Set the first move. Planner with a complete brief: `python3 tools/transition.py <id> planned --by planner --next "<what the builder does first>"`. Anyone else: leave it `draft` and name the planner: `python3 tools/transition.py <id> --next "Planner: write brief.md"`.
5. Confirm it shows on `work/ACTIVE.md` and run `python3 tools/check.py`.

Do not invent ids by hand; `new_item.py` handles dates and collisions. Do not create items for decisions that need the human; use `python3 tools/question.py ask`.
