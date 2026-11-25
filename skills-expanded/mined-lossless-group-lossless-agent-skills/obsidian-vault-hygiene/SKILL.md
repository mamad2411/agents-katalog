---
name: obsidian-vault-hygiene
description: How to promote loose notes in the operator's Obsidian vault (content-md/lossless) into their proper typed folders with standard frontmatter — back up, classify, merge duplicates, verify the URL, OG-fetch, tag, move, and repair wikilinks. Use whenever the user points at a note sitting at the vault root "waiting for metadata love", asks to "tag it and move it to the right folder", "run OG fetch", "clean up the root", "these VCs are in the root", or whenever an agent is about to create a note and finds an empty or thin root stub with the same name; also when clicking a bare [[link]] in Obsidian has created empty root files. Encodes the vault-is-symlinks layout (root not under git, typed folders are), the backup-first rule, the high/medium/low classification gate, merge-don't-duplicate, fill-only-empty OG fetching, line-wise frontmatter edits that preserve key order, and the post-move link-uniqueness check.
---

# Obsidian Vault Hygiene

> **Status: draft (2026-10-14).** Written from one run: 74 venture-firm notes promoted from
> the vault root into `vertical-toolkits/Venture-Capital-Firms/` (68 moved, 6 merged, all
> 126 inbound links still resolving). Generalize carefully as more note types go through it.

## The layout you're working in

- The vault is `/Users/mpstaton/content-md/lossless`. Most top-level folders (`Sources`,
  `vertical-toolkits`, `organizations`, `concepts`, `moc`, …) are **symlinks** into the git-tracked
  `lossless-monorepo/content/`.
- The **vault root itself is not under git.** Loose root notes have no history. A bad
  edit or move there can't be undone, so back up first.
- Wikilinks use **vault paths**: `Sources/…` (capital S) even though the repo folder is
  `content/sources/`.
- Clicking a bare `[[Name]]` that resolves to nothing makes Obsidian create an **empty note at
  the root**. Many root files are 0-byte stubs created that way.

## Procedure

1. **Back up.** `cp -p` every root `.md` you might touch (simplest: all of them) into
   `/Users/mpstaton/content-md/_backups/<YYYY-MM-DD>-<task>/`. Check the count matches.
2. **Classify.** Find candidates by name pattern and body keywords, then confirm the type against
   the CRM (`orgType` in the Lossless Twenty, read-only) and any event rosters. Sort into
   **high / medium / low** with a reason for each, and **migrate only high**. Hand medium to the
   operator (LPs, asset managers, accelerators and people with firm-like names live here).
3. **Collision check.** Search the whole vault, following symlinks: exact basename, the name
   with "Ventures/Capital/VC/Partners" stripped, and `aliases:` in frontmatter. If a typed note
   already exists, **merge** into it: carry over aliases, append any non-empty body under
   `***`, then delete the root file. Never drop non-empty content.
4. **Verify the URL.** Take it from the CRM domain, an event roster, or a search confirmed
   against the firm's own site. If the name is ambiguous (several firms share it) or the site
   is dead, set no `url` and list the note.
5. **OG fetch.** Fetch the site directly. Fill only empty or missing `og_*` fields, drop
   placeholder values ("Home", `"[]"`, a CMS default image), and set `og_last_fetch`.
   Add `linkedin_url` only when the firm's own site links it and the slug matches the firm.
   (The `tidyverse/observers` OpenGraph service does the same through opengraph.io when its
   API key is available.)
6. **Frontmatter.** Edit line by line so key order, quoting style and the body survive. Add
   only the missing standard keys for the type (see below). Keep any existing `publish`
   value; when it's absent, use `false`.
7. **Move**, then check that each moved basename is still unique in the vault. Bare links keep
   resolving only if it is. Rewrite to full vault paths: links to a name that's now ambiguous,
   links to a note renamed by a merge, and any path-qualified link to the old location.
   Escape the pipe (`\|`) inside table rows.
8. **Verify and record.** Re-scan every link to an affected name for breakage, and write a
   manifest (old path, new path, action, url, OG fetched yes/no) to the scratchpad.

## Standard frontmatter by type

| Type | Folder | Keys |
|---|---|---|
| Venture firm (incl. fund-of-funds) | `vertical-toolkits/Venture-Capital-Firms/` | `url`, `linkedin_url`?, `date_created`, `date_modified`, `og_title`, `og_description`, `og_image`, `og_favicon`, `og_last_fetch`, `tags: [Venture-Capital-Firms]` (+ `Fund-of-Funds`), `site_uuid`, `publish`, `title`, `slug`, `at_semantic_version: 0.0.0.1` |
| Person | `Sources/People/` | `date_created`, `date_modified`, `tags` (`Venture-Investors` for GPs/LPs), `site_uuid`, `publish`, `title`, `slug`, `at_semantic_version`, verified `url`/`linkedin_url`, `aliases`? |

Other types (operating companies, LPs that aren't fund-of-funds, tools) have no settled folder
yet. Ask before inventing one.

## Anti-patterns

- Moving root notes without a backup.
- Creating a second note when a typed one exists under a slightly different name.
- Overwriting existing OG values, or keeping junk ones because "a field is a field".
- Guessing a domain from a firm name.
- Rewriting a whole frontmatter block, which reorders keys and changes quoting across files.
- Bulk-normalizing unrelated drift you notice along the way (mixed `tags` styles, typo'd keys).
  Note it and leave it.
