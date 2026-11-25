---
name: engineering-memory
description: Use the SolidWorks MCP memory tools on every CAD task when memory_* tools are listed, including a new part or assembly from scratch. After the first save, call memory_overview so the new project is stored. Note only constraints, decisions, findings, and failed attempts.
---

# Engineering memory

Memory is a cache of the model and of notes the engineer approved. The live model is the truth for a write. The engineer says what they want in plain words. You choose the tool, the page, the token budget, the units, and which thing a note attaches to. When `memory_overview` says Approve for me, you save ordinary notes and you mark only a very critical note so the host asks once.

## The loop

1. For a saved project, call `memory_overview` at the start of CAD work. A new part or assembly follows New project. Do not call memory before the first save.
2. Call `memory_find` to get ids from the engineer's words, or from the current selection when an id is not known yet.
3. Call `memory_look` and `memory_impact` before a change. Tell the engineer about constraints and warnings.
4. Read the live SolidWorks value before a write. Use the action address. The API number on that line is what gets written. Lengths are meters and angles are radians. The write of that named dimension or feature is `model` change, using the meter number on the line. Memory is not re-read as proof the write landed.
5. Call `memory_note` once at the end: constraints the engineer stated (author engineer), findings, failed attempts with the reason, and decisions. Skip this call when the turn has none of those.

When a footer says `more: page=2`, call that tool again with `page` or a higher `max_tokens`. `max_tokens` stops at 6000. `memory_overview` stays at 1000 by default. There is no setting for paging or budgets.

## New project

A project is new when the part or assembly has just been created, or when `memory_overview` shows no files.

1. Model and save with the SolidWorks tools first. An unsaved part has no path, and `memory_overview` cannot create a project for it.
2. Call `memory_overview` once, with no project argument. That call creates the project from the saved file's folder and stores the model: features, sketches, dimensions, mates, and material. Do not copy those into notes.
3. Call `memory_note` only when this turn has something the model cannot say: a constraint the engineer just stated, a decision that is not geometry, a finding, or a failed attempt and why. One call, one fact per note, attached to the dimension or feature. If none of those happened, stop after the overview.
4. If the job workspace has `design_state.json` and the overview shows no notes, follow First use of a project in that same `memory_note` call.
5. On the next edit of this project, use the loop above.

## Rules

- `PROPOSED` notes are hints. They are not approved facts.
- Quote a stale note with the old value and the new value, and ask the engineer before relying on it.
- Say coverage limits out loud. Drawings that are not open, and lightweight components, are named. "None known" does not mean there are none.
- One fact per note, on the most specific thing (a dimension, not the whole part). At most 10 notes in the one `memory_note` call.
- Values, mates, and structure are already in memory. Note constraints, findings, failed attempts, and decisions.
- Re-attach an orphaned note with `replaces`.

## Approve for me

When `memory_overview` contains `Approve for me`, omit `critical` on an ordinary note. The host saves it approved and does not show a dialog.

Set `critical` true only when the note is very critical, and put those notes in their own `memory_note` call. The host then asks once for that call. Very critical means one of these:

- it refutes an approved note
- it replaces an approved constraint or decision the engineer did not ask to change
- it states a safety, regulatory, or do-not-change limit the engineer did not say in this turn

A constraint or decision the engineer just stated, a finding, a failed attempt, and a warning about a rebuild or coverage are not critical. Do not ask in the chat as well. The dialog is the only ask, and only for that call.

When the overview has no `Approve for me` line, omit `critical`. Ask each time already shows a dialog. Save as hints keeps the notes as proposals.

## First use of a project

On the first overview of a project that has no notes, if the job workspace has `design_state.json`, propose its simplifications as warnings and its recorded decisions (DEC entries) and stated requirements as decisions and constraints, in one `memory_note` call. `bridge_facts` belong in skills, not memory.

## Examples

The engineer says "model a 100 x 50 x 10 mm plate" and no file is saved yet.

1. Create and save the part. Do not call memory before that save.
2. `memory_overview` with no project argument. That stores the plate. Do not note 100, 50, or 10.
3. Nothing in the turn is a constraint, a decision that is not geometry, a finding, or a failed attempt, so do not call `memory_note`.

The project is ENC-000. The engineer says "D7 on the lid stays 12 mm."

1. `memory_overview`.
2. `memory_find` for "lid D7", or the current selection.
3. `memory_look` and `memory_impact` on that dimension. Tell the engineer about any constraint or warning on it.
4. Read the live dimension. The line shows `12 mm (0.012 m)`. A later write uses `0.012`.
5. One `memory_note`: kind constraint, text "D7 stays 12 mm", author engineer, attached to that dimension.

Before changing D7, call `memory_impact` again. If a note on that line is `PROPOSED`, tell the engineer it is a hint. If it is stale, quote the old value and the new value and ask before using it. If the footer says drawings were not open, say that.

A mate attempt fails. At the end, one `memory_note` of kind attempt records the reason, attached to the mate that failed. The mate's geometry stays in memory; the note is only the failed attempt.
