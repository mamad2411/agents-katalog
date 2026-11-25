---
name: bootstrap-index
description: Build or refresh a docs index.md (single project or multi-project repo)
---

# Bootstrap Index

Builds or refreshes an `index.md` that points to every useful documentation file, for either a single project or a multi-project docs repo — detect which one this is before doing anything.

## Detect the repo shape

1. Check for `projects/` (or `@/projects/`) at the repo root, containing multiple subfolders that each look like an independent project (their own `docs/` or `index.md`).
2. If that structure exists: this is a **multi-project meta-repo**. Follow "Multi-project mode" below.
3. Otherwise: this is a **single project** (the normal CoDriDe shape — `docs/business-context/`, `docs/technical-context/` at the root). Follow "Single-project mode" below.

If it's genuinely ambiguous (e.g., a `projects/` folder exists but only has one entry, or doesn't look like independent projects), ask the human which mode applies instead of guessing.

## Single-project mode

Build or refresh `docs/index.md`, pointing to every useful resource in this project's own docs: `docs/business-context/` and its files (master docs, `features/`, `brainstorm/`), `docs/technical-context/` and its files (`project-briefing.md`, `adr/`, `briefing/`), and the root `README.md`.

Go through the actual folder structure — don't assume standard file names exist — and list what's really there, each with a one-line description of what it covers.

If the user's request names a specific subfolder to focus on (e.g., only `docs/technical-context/`), treat that as the scope of the refresh rather than rebuilding the entire index.

## Multi-project mode

Each project has its own folder under `projects/`. Inside each of these folders, there's meant to be an `index.md` file that points to all other useful resources for that project.

### If no project is named: rebuild the root index

Build the root `projects/index.md` file. For each project folder, include:
- name, with a link to its folder
- short description
- repository url
- GitHub issues/project board url (if used for tracking)

This information is usually available inside the project's own main files (its `index.md`, or an equivalent overview file). Don't add anything beyond the above to the root index.

### If the user names a specific project: rebuild that project's index

Used to rebuild one project's index after its directory/file structure changed. Go through that project's folder structure, understand what files and folders exist, and refine its `index.md` to match — create it if it doesn't exist yet, edit it if it does. The index should point to every other useful resource in that project's folder.
