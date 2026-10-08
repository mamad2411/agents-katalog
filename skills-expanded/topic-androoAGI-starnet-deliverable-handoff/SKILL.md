---
name: deliverable-handoff
description: "Finish work as files the Commander can open: a format that previews, a clear name and place, the main file marked in DELIVERABLES, and a closing message that points to it."
license: MIT
metadata:
  title: "Deliverable Handoff"
  category: "Station"
  author: "StarNet"
---

Work the Commander cannot find did not happen. The station already records which files a run wrote; your job is to make those files the obvious, openable answer — named for what they are, in a format that previews, with the one that matters marked.

## Method
1. **Decide the deliverable before you write it.** One sentence: which file the Commander will open and what they will do with it — a report, a table, an image set, a patch.
2. **Pick formats that open where they look.** The DELIVERABLES library previews Markdown (.md), CSV (.csv) and images (.png, .jpg, .gif, .webp) right in the card. Use .md for documents, .csv for tables, an image format for pictures. Use another format only when the Commander asked for it or the next tool needs it.
3. **Know where files land.** fs.write writes into the current project folder when the session is anchored to one, otherwise into your private workspace. Studio tools default to `images/`, `audio/` and `edits/`. In a project, put deliverables where the project keeps such things; otherwise use one short folder named for the job.
4. **Name files for a human.** `2026-09-vendor-comparison.md`, not `output.md` or `final_v2_new.md`. Date-prefix anything periodic. Never overwrite a file the Commander already approved — write the new version beside it.
5. **Make the main file stand alone.** Its first lines say what it is, the date, and the sources used. It must make sense opened cold, weeks later, without this conversation.
6. **Keep supporting files beside it** and link them from the main file by relative path.
7. **Read back what you wrote (fs.read).** Confirm it saved, it is complete, and nothing is truncated or still a placeholder.
8. **Name the work once (deliverable_note),** at the end, and only if you created or changed files: `title` (a plain name, not a filename), `summary` (one sentence saying what it is), `kind` (doc, data, page, patch, image or files) and `main` (the path of the file that is the deliverable).
9. **Close with a pointer, not a recap.** Tell the Commander the title, the main path, and the one thing to look at first. If crew made files, point to them as "<workerId>'s workspace: <path>".

## Rules
- **Describe the work in the note; do not grade it.** Status, cost, crew and the file list are recorded by the station from the run itself, and anything you write about them is ignored.
- **Never claim a file exists that you did not see a tool confirm.**
- Skip the deliverable note when the Commander said to stop after the change or limited what you may do.
- Never put secrets in a deliverable; name the setting that holds them.

## Done means
The main file exists at the path you named, reads correctly on its own, previews or opens in the promised format, and the deliverable note names it as `main`.

## Output
The title, the main file path, the supporting files, and one line on what to read first.

*Needs the INTEL CAB (fs.write / fs.read). deliverable_note is available to every agent.*
