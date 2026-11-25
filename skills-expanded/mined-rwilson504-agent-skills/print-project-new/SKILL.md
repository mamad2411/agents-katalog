---
name: print-project-new
description: 'Scaffold a new 3D print project folder — README, a first material-and-orientation decision record, and an optional session log. Adapts to whatever folder layout the repository already uses. USE FOR: new print project, scaffold print project, start a 3D print project, create print project folder.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["3d-printing","scaffolding","project-setup","decision-records"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/3dprint", "emoji": "🖨️" } }
---

# Scaffold a new 3D print project

You are creating a new project folder for a 3D-printed item. Work through
this checklist, adapting it to the conventions the repository already uses.
The one part worth insisting on is the decision record — material and
orientation choices are the ones people forget and then re-litigate.

## Inputs to confirm

Before creating files, confirm with the user:

1. **Where project folders live** — if the repo already groups projects
   (`printing/`, `projects/`, one folder per part at the root), follow that.
   Only ask if there is no existing pattern to copy.
2. **Project slug** — lowercase, hyphenated, no spaces (e.g.
   `desk-organizer`, `battery-holder-aa8`). Reject anything else.
3. **One-line purpose** — what is this print and who/what is it for?
4. **Source model** — does it already exist (path or link), is a CAD
   workflow producing it (the `cad-builder` agent *(separate plugin)* is one
   such), or is it a third-party download (MakerWorld / Printables)?
5. **Initial material guess** — PLA / PETG / ABS / TPU / other. Just a
   starting point; the first decision file will lock it in.
6. **Printer and slicer** — default to Bambu Lab P2S + Bambu Studio, which
   the rest of this plugin assumes. Record whatever the user actually has.

If any answer is missing, ask for it before proceeding.

## Files to create

Create the following inside the project folder:

### 1. `README.md`

```markdown
# <Project Title>

**Slug:** `<project-slug>`
**Status:** in-progress
**Started:** YYYY-MM-DD
**Agent:** 3D Print Operator

## Purpose
<one-line description of what the part is and who or what it is for>

## Source Model
<link / path to STL/STEP/.3mf, or note which CAD workflow is producing it>

## Target Print Settings (initial — see decisions/ for final)
- **Material:** <initial guess>
- **Printer:** <printer from inputs>
- **Slicer:** <slicer from inputs>

## Decisions
See [`decisions/`](decisions/) for the chronological record of every
non-trivial choice made on this project.

## Files
- `*.stl` / `*.step` — source models
- `*.3mf` — slicer project files
- `profiles/` — exported slicer profiles (optional)
- `photos/` — build-plate photos, failure photos, finished prints
```

### 2. `decisions/0001-material-and-orientation.md`

This is the **first decision** for every print project. Pre-fill it as a
template that the user fills in during the first real conversation:

```markdown
# 0001. Material and Print Orientation

- **Date:** YYYY-MM-DD
- **Status:** proposed
- **Project:** <project-slug>

## Context
What's the part for? What loads will it see? What environment (indoor,
outdoor, hot, wet, UV)? What aesthetic matters?

## Options Considered
1. **<material A>** — pros / cons for this part
2. **<material B>** — pros / cons for this part
3. **<material C>** — pros / cons for this part

For orientation, consider:
- Layer line direction vs. load direction (layers are weakest in Z)
- Which face is cosmetic and should be top/visible
- Which features need supports and where supports leave scars
- Bridge spans and overhang angles

## Decision
**Material:** <chosen>
**Orientation:** <described or with sketch reference>
**Why:** <one paragraph>

## Consequences
- Print time estimate: <>
- Material cost estimate: <>
- Trade-offs accepted: <>

## Lessons (filled in after first print)
<empty until the print runs>
```

### 3. A session log — only if the repository keeps one

Some repositories track time per project. **If one already exists elsewhere
in the repo, copy its format exactly** and seed a row for this session. If
there is no such convention, skip this file entirely rather than inventing
one.

## After creating files

1. Commit, so the scaffold is recorded before any real work starts:
   ```
   git add <project-folder>
   git commit -m "scaffold: new print project <project-slug>"
   ```
2. Ask the user the first real question (usually about the part's purpose,
   loads, or environment) so you can help them fill in
   `0001-material-and-orientation.md`.
3. Hand control back to the **3D Print Operator** agent for the actual
   slicing / printing work.

## Reminders

- **Always create `decisions/`.** Even if the user says "it's just a quick
  print", create the folder and the 0001 file. They can leave it as
  "default profile, no decisions to record" — but the structure exists
  for when something IS worth recording.
- **Slug must be lowercase-hyphenated.** Reject `MyProject`, `my project`,
  `My_Project`. Accept `my-project`.
- **Don't pre-fill the decision** with your guesses. Lay out the options,
  let the user choose. The whole point of a decision file is the human
  made the call deliberately.
