---
name: notion-preview
description: >-
  Draft or revise a Notion page as an HTML preview that looks like the real page, for review before
  anything is written into Notion. Covers the two modes (GENERATE a new page, UPDATE an existing one with
  a Previous / Proposed / Diff switch), the block vocabulary that makes a preview read as Notion, the
  two ways an approved page reaches Notion, and how to propose disposal. Triggers - "draft a Notion page
  for X", "preview this in Notion", "what will the page look like", "update the X specification", "show
  me the diff before I write it", "mock up the spec", "I can only read Notion now", "which pages should
  be archived".
---

# Notion previews

The preview stands in for the page during review, so wording is agreed before anything reaches Notion.
**Approval is the gate, not the writing** — once the owner has signed it off, write the page. A paste is
the fallback for a connector with no write path, not the normal ending.

**Check which, at the start of every session.** `get_tool_access` with `{}` returns the map; `create_pages`
and `update_page` present mean the direct route is open. Narrowing the call by `tool_names` needs the
underscored names from that map — hyphenated names return an empty map that reads exactly like a
revocation.

**Content rules are not here.** What a page says, which sections it has and in what order, the house voice
— all of that lives in `notion-specification` and the space's style-guide page. Load that skill and fetch
that page first. This skill owns presentation, review and handoff alone; `notion-editing` owns how a page
is changed, `notion-database` a schema or a view, and `notion-diagram` a figure.

## Before writing anything

1. **Read `notion-specification`** for the coordinates and the section skeleton, and fetch the style guide.
2. **Fetch the neighbours.** A page reads as house style by imitating live examples, not by following a
   list of rules — pull one or two sibling pages in the same database.
3. **Copy `reference/shell.html` and `assets/notion.css`** next to each other and fill the shell in. Never
   retype the toolbar or the diff script; the shell is the only copy that stays in step with the
   stylesheet.

**`reference/example.html` is the block vocabulary.** It is a filled specification page carrying every
block type — properties, callouts, toggles, mentions, an inline database, a Mermaid diagram, the diff
attributes — and all three diff states, plus a complete handoff panel. Copy markup from it rather than
inventing classes the stylesheet does not have.

## GENERATE

A page that does not exist yet. No diff exists, so drop `.n-switch` and `.n-tally` from the shell's bar and
leave the label; the bar still marks the file as a preview rather than the real thing.

Write the page as it should land, in full. A preview that stops at an outline cannot be reviewed for
wording, which is the whole point of showing it. Sections that are deliberately empty read **Not
applicable.** plus one clause of reason, exactly as they would in Notion.

## UPDATE

**Fetch the live page first and keep the returned text.** The Previous view must be the stored content,
never a reconstruction from memory or from an earlier preview — a reconstruction turns every incidental
rewording into a reviewable change and buries the real ones.

Then mark the diff **while writing**, block by block:

- a block only in the new version → `data-state="added"`
- a block only in the old version → `data-state="removed"`, kept in place
- a block whose wording moved → `data-state="changed"`, with `<del>` and `<ins>` around the runs that
  differ, plus a one-line `.n-note` saying why
- everything else → no attribute

**Do not compute the diff at runtime.** A DOM differ reports a re-wrap or a moved sentence as a change, has
no access to why an edit was made, and costs a dependency. The author of the edit already knows which
changes are real; marking them is the cheap path and the accurate one.

A changed block with no `.n-note` is a change nobody can review. Write the note or leave the block alone.

## Publishing

One preview file per Notion page, and the same file for the life of that page:

- Write it as a self-contained file — `docs/<section>/<page-slug>.preview.html` in the repo that owns the
  work, with `notion.css` beside it or inlined into a `<style>` block. It must render from `file://` with
  no build step, and any later session can read it back.
- **Title** — the Notion page title, unchanged. **Icon** — the page's Notion icon emoji in `.n-icon`.
- Iterating: edit the same file. Returning in a later session: read the existing file before overwriting
  it.

Once the approved page has landed in Notion, the baseline moves. Re-fetch the live page for the next
update rather than diffing against the last preview — otherwise edits made in the UI vanish from the diff.

## Handoff

The shell's handoff panel has three parts. Fill all three, even when the direct write route is open —
they are what the reviewer checks the write against.

1. **Paste the body** — the page as Notion-flavoured markdown in `#src`, Proposed state only.
2. **Rebuild by hand** — every block markdown cannot carry: the icon, callouts, toggles, inline database
   views, `@` mentions, tagline placement. With the direct route open, these become content in the
   `create-pages` / `update-page` call instead of instructions.
3. **Disposal** — pages this one supersedes, why, their inbound mention count, and the action. Nothing is
   deleted; see `notion-editing` for the Archive route and why mentions are counted first.

## Scope fence

The preview is a visual stand-in, not a Notion reimplementation. Out of scope, deliberately:

live database queries · filters, sorts and grouping · view switching · relations and rollups · comments
and suggestions · sidebar, breadcrumbs and backlinks · editing · search

Databases render as a static table of the rows that matter to the page, under a title row. If a page needs
a database view nobody can read as a table, that is a sign the page is leaning on Notion behaviour the
preview cannot carry — say so rather than approximating it.
