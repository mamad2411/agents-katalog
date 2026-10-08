---
name: notes-vault
description: "Read, search, create and edit notes in the Commander's local Markdown notes vault (for example an Obsidian vault) with the station's file tools, linking notes with [[wikilinks]]."
license: MIT
metadata:
  title: "Notes Vault"
  category: "Productivity"
  author: "Teknium"
---

# Notes Vault

Use this skill for filesystem-first work in a Markdown notes vault: a folder of `.md` notes such as an Obsidian vault. It covers reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Resolve a concrete vault path before calling any file tool.

- Check `notebook.read` for a saved vault path first. If there is none, ask the Commander where the vault lives, then save it with `notebook.write` (for example "Notes vault: <absolute path>") so later sessions reuse it.
- If the Commander is unsure, a common default is `Documents/Obsidian Vault` in their home folder. A folder that contains a hidden `.obsidian/` directory is a vault root.
- File tools take a concrete absolute path. Never pass `~` or an environment-variable reference as a path; resolve it first.
- The vault lives outside your workspace, so the first file-tool call on it asks the Commander to trust that folder. After they approve, the file tools work there directly. An unattended routine can only use a vault folder that was already trusted.
- Vault paths often contain spaces. That is another reason to prefer the file tools over shell commands.

## Read a note

Use `fs.read` with the absolute path to the note. Pass `numbered: true` when you need to cite or edit exact lines; use `offset` and `limit` to page long notes.

## List notes

Use `fs.search` with `target: "files"`, `query: "*.md"`, and `path` set to the vault (or a subfolder) path. For a small vault, `fs.list` with `recursive: true` also works. Prefer these over shell `dir`, `ls`, or `find`.

## Search

Use `fs.search` for both filename and content searches.

- Filenames: `target: "files"` with a filename glob as `query`.
- Note contents: `target: "content"` with the text as `query` and `file_glob: "*.md"`. Add `regex: true` for a regular expression, `ignoreCase: true` to ignore case, and `output_mode: "files_only"` when you only need which notes match.
- Hidden folders such as `.obsidian/` (the vault's app settings) are skipped, which is what you want.

## Create a note

Use `fs.write` with the absolute path and the full Markdown content. First check with `fs.search` (`target: "files"`) that a note with that name does not already exist, because `fs.write` replaces a file's contents.

## Append to a note

- For a plain append at the end, use `fs.append`.
- For an anchored insert (for example new content after an existing heading), `fs.read` the note, then use `fs.edit` to replace the anchor with the anchor plus the new content.
- When rewriting the whole note is clearer than constructing a fragile edit, use `fs.write`.

## Targeted edits

Use `fs.edit` for focused changes when the current content gives you a stable, unique anchor (`fs.edit` requires that you `fs.read` the note first in this run). Use `fs.patch` for multi-hunk changes. Prefer both over shell text rewriting.

## Wikilinks

Notes link to each other with `[[Note Name]]` syntax (`[[Note Name|shown text]]` for an alias, `[[Note Name#Heading]]` for a section, `![[image.png]]` to embed). When creating notes, use wikilinks to connect related content.

*Needs the CABINET (file tools); the NOTEBOOK remembers the vault path.*

Adapted for StarNet from obsidian (Teknium), MIT.
