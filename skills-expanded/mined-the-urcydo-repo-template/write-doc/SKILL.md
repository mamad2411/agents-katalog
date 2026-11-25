---
name: write-doc
description: Creates or updates a documentation page in docs/ using the right Diataxis type, valid front matter and a one-sentence summary. Use whenever adding, changing, moving or deleting a doc.
---
# Write a doc

**Role:** the owner of the folder you are changing (see `agents/ROSTER.md`); usually the scribe. Docs in other roles' folders: hand the change to that role.

1. Pick exactly one type by the reader's need:
   - **tutorial**: a beginner learns by doing; the steps must work every time.
   - **how-to**: someone who knows the basics solves one task; a recipe.
   - **reference**: someone looks up a fact; accurate, complete, no opinions or instructions.
   - **explanation**: someone wants to understand why; context, trade-offs, history.
   If the page needs two types, write two pages and link them.
2. Check `docs/INDEX.md` first. Update an existing page rather than adding a near-duplicate.
3. Create it: `python3 tools/new_doc.py <type> "Title" --summary "One sentence a stranger can judge by."`
4. Fill it from the template. Keep it focused; split when it passes about 300 lines.
5. If it describes code, list the files under `related_code` in the front matter and set `last_verified` to today.
6. Delete or mark `deprecated` anything the change makes wrong. Stale docs are worse than none.
7. `python3 tools/sync_indexes.py && python3 tools/check.py`.

Do not link from core docs into optional module folders (the check will fail); use backticks. Do not hand-edit generated files such as `docs/INDEX.md`.
