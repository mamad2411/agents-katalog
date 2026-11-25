---
name: workspace-organization
description: "Use when creating, filing, moving, or archiving files in the agent workspace: which directory a file belongs in, how to date and attribute it, when to archive instead of delete, and how to keep the tree navigable over years."
---

# Workspace Organization

The workspace is the agent's own filesystem. Unlike a conversation, it persists; unlike memory, it holds whole documents. It is the only place where work too large for a message and too specific for a memory can live, and it is read far more often than it is written — usually months later, usually by an agent with no recollection of why the file exists.

That last point sets the standard. A file is well-filed when a future reader with no context can find it by guessing, and can tell what it is and when it was made without opening it. Everything below serves those two properties.

## The structure

Seven directories, each with one job. Resist adding more: a directory invented ahead of a real need stays empty and teaches readers that the structure is decorative.

**`notes/`** — Durable writing the agent or the user authored. Design documents, decisions, meeting notes, drafts, reference material written in-house. This is the default home for prose. Subdirectories by subject are encouraged once a topic exceeds a handful of files; `notes/drafts/` holds work not yet worth finding.

**`research/`** — Material gathered from outside. Fetched articles, downloaded specs, cloned repositories kept for study. The distinguishing test is authorship, not subject: if the agent wrote it, it is a note even when the topic is research; if it arrived from elsewhere, it is research even when it is prose.

**`projects/`** — Working directories scoped to a project, usually containing or shadowing a code checkout. Files here belong to the project's own conventions, not this skill's.

**`archive/`** — Superseded material retained deliberately. Anything moved here keeps its original relative path so the move is reversible. `archive/provenance/` holds manifests describing where imported files came from.

**`saved/`** — Files that arrived through a channel: attachments, screenshots, sent documents. This is a landing zone, not a home. Anything worth keeping gets filed into `notes/`, `research/`, or `projects/`; the rest is disposable.

**`ingest/`** — A pipeline, not storage. Files dropped here are read into memory and then removed. Never write anything here expecting to find it later, and never file anything here for organizational reasons.

**`skills/`** — Skills available to this agent. Managed by the skill tooling rather than by hand.

## Filing decisions

Choose the directory by asking two questions in order: *who wrote it* separates notes from research, and *is it current* separates either from archive. Subject matter never decides the top-level directory — it decides the subdirectory.

Files with no clear home usually mean one of two things. Either it belongs in `notes/` and simply lacks a topic yet, or it is a transient artifact that should not be filed at all. Prefer the first for anything a human wrote and the second for anything a tool emitted.

Do not create a new top-level directory. If the existing seven genuinely cannot hold something, that is a finding worth raising with the user, not a decision to make alone.

## Dating and attribution

Every file must answer "when was this made" without being opened, because filesystem timestamps do not survive being copied — a copied file gets a fresh creation time while keeping its old modification time. Timestamps are evidence that degrades; recorded dates do not.

Satisfy this one of two ways:

- **Date in the filename** for anything periodic or point-in-time: `2026-08-12-migration-plan.md`, `review-2026-08-12.md`. Use ISO order so names sort chronologically.
- **`created:` in frontmatter** for anything else. Markdown files carry it in a YAML block at the top, alongside `source_path:` when the file came from somewhere else.

Where a file's true creation date is unknown, record the best available evidence rather than today's date, and say which it is. A version-control add-date beats a filesystem timestamp; the earlier of birth and modification time beats either alone, since a copy keeps the old modification time while inventing a new birth time. Never stamp an imported file with the date it was imported — that erases exactly the fact the stamp exists to preserve.

When files arrive in bulk, write a manifest to `archive/provenance/` recording each file's destination, original path, resolved date, and how that date was determined. The manifest is what makes a reorganization reversible and an origin question answerable.

## Naming

Lowercase, hyphen-separated, descriptive of content rather than category: `transfer-engine-design.md`, not `doc1.md` or `important-notes.md`. The directory already encodes the category; repeating it in the filename wastes the part a reader actually scans.

Never leave a file named `Untitled`. A file worth keeping is worth thirty seconds of naming, and a file not worth naming should be deleted rather than filed.

## Archiving

Move, do not delete, anything that was ever referenced or acted upon. Deletion is correct only for genuine disposables: duplicates, transient tool output, files that were never meaningful.

Archiving preserves the original relative path — a file at `notes/planning/roadmap.md` becomes `archive/notes/planning/roadmap.md`. Do not flatten, and do not rename on the way in; a reader comparing archive to live should see the same shape twice.

When a document is superseded rather than abandoned, leave a line in the replacement naming what it replaced. A reader who finds the new file should not have to search the archive to learn there was an old one.

## Housekeeping

Periodically, and always after a bulk import: check `saved/` for files never filed, look for `Untitled` and other placeholder names, and confirm nothing has accumulated in `ingest/`. These are the three places disorder reliably starts.

Reorganizing an established tree is disruptive and should follow a stated plan rather than happening incrementally as a side effect of other work. Moving one misfiled file is housekeeping; moving twenty is a migration and deserves a manifest.

## Preferences

This section records how *this* user wants their workspace organized, beyond the defaults above. Edit it when a preference is stated or observed — a naming habit, a subdirectory convention, a rule about where a recurring kind of document goes. Keep entries short and concrete, and delete them when they stop being true.

Editing this skill is the correct way to record such preferences. Do not store them as memories: the skill is loaded exactly when the question arises, and a preference held in two places will eventually disagree with itself.

<!-- Add observed preferences below this line. -->
