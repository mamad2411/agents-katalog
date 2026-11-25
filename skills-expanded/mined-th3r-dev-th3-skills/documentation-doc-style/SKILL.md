---
name: documentation-doc-style
description: >-
  Write and build documentation for any work product (an API, a deploy or update, a system, a feature, a
  release, a test round) in one consistent house style, and output a matching PDF + DOCX from a single
  Markdown source. Use whenever the user wants to document, write up, report on, or hand over something:
  "write an API spec", "เขียนเอกสาร", "ทำรายงานอัปเดต", "document this endpoint", "make a user guide",
  "write the README", "changelog for this release", "system overview for onboarding", "report for the
  client", "export as PDF and Word", or asks to make an existing document match the house style. Covers
  seven document types (report/change record, API reference, user guide/quickstart, FAQ,
  architecture/onboarding, README, changelog) with fixed skeletons, and a theme of TH Sarabun fonts, a
  plain black/grey palette, and green/yellow/red change highlighting. Thai-first headings; English works
  the same way.
---

# Doc Style Builder

One method, seven skeletons, one theme. The value is **consistency**: a reader who has seen one document
of a type can find what they need in the next one without reading it, and a revision shows exactly what
changed.

## Work like this: gather → ground → summarize → confirm → build

The usual failure is a document that looks right and describes the system wrongly. Avoid it in this order:

1. **Gather.** Collect what the user points at: code, an OpenAPI file, logs, screenshots, notes, an older version of the document.
2. **Ground.** Check each fact against the real thing before writing it: the controller and DTO for an API,
   the server's own output for a deploy, the running screen for a guide. When the user's notes and the
   system disagree, the system wins. Tell the user about the conflict.
3. **Pick the reader and the type.** Decide who reads it (end user, integrator, operator, developer,
   approver outside the team), then pick the type from `references/doc-types.md`. The reader decides
   what to leave out.
4. **Summarize.** List the sections, the tables, and what changed since the last version, as a short
   scannable list.
5. **Confirm.** Show the summary and wait for a go-ahead, unless the user said to just build it.
6. **Build.** Write the Markdown to the skeleton, then run the builder (below).

## House rules

- **Short and finished.** A document says what was done, where, and what the result was. Leave out the
  working: raw logs, dead ends, the tools you happened to use.
- **Every claim has evidence.** A result row points to a screenshot, a response, or a command output. A check
  with no evidence stays in the table as `ยังไม่มีหลักฐาน` / "no evidence yet". It is never dropped and never
  marked as passed.
- **Screenshots prove where they were taken.** The address bar or the shell prompt is visible.
  Keep at most about four per target.
- **Readers outside the team see nothing internal.** No internal paths, config-section names, ticket
  shorthand or chat handles. Use real usernames only when the reader needs them to log in, and name issue
  owners by role ("IT ของลูกค้า", "ทีมพัฒนา").
- **Unknown is `-`, never invented.** A production URL that does not exist yet is `-`.
- **Blank is not zero.** An empty value stays empty or `-`. Never write `0` for "not measured".
- **Revisions are visible.** Add a revision-history row (`Version | วันที่ | ผู้เขียน | รายละเอียด`), mark
  changed table rows `[+]` / `[~]` / `[-]`, and include the legend once (see `references/theme.md`).
  Keep removed rows in the table, struck through; do not delete them.
- **Dates.** Thai readers get Buddhist-era `dd/mm/yyyy+543` (`13/10/2569`). Follow whatever an existing
  document already uses.
- **Thai prose.** Headings and fixed labels stay Thai as in the skeleton. Field names, types, commands and
  JSON stay as they are. For paragraphs of Thai, use a Thai-writing skill such as `kien-thai` if one is
  installed. Keep technical terms that practitioners say in English (`deploy`, `schema`, `endpoint`).
- **Never hand-edit the output.** Fix the Markdown (or the theme) and rebuild.

## Build

```bash
uv run scripts/build_doc.py doc.md                         # -> "doc - Update <ddmmyyyy>.pdf" + ".docx"
uv run scripts/build_doc.py doc.md --prefix ACME --out dist --formats html,pdf,docx
uv run scripts/build_doc.py doc.md --no-date               # -> "doc.pdf" + "doc.docx"
uv run scripts/build_doc.py doc.md --css layout.css        # a layout stylesheet after the theme (HTML/PDF), e.g. software-engineer/release-docs
```

Needs `pandoc` on PATH. The PDF needs Chromium for playwright once:
`uv run --with playwright playwright install chromium`. Run the script from this skill's folder or give its
full path; it finds `assets/theme.css` relative to itself.

The Markdown is pandoc Markdown:
- Front matter sets `title`, `subtitle`, `author` and `date`.
- Pipe tables take their column widths from the separator dashes.
- A table with an empty header row becomes a key/value table, with the key column shaded.
- `![caption](img.png)` gives a captioned figure.
- A first cell that starts with `[+]`, `[~]` or `[-]` marks the row as added, edited or removed.

`references/example.md` exercises all of it. Build it once to check the setup.

File names follow `[<PREFIX>_]<name> - Update <ddmmyyyy>.<ext>`, so a folder groups documents by topic and
a rebuild on the same day replaces the earlier file.

## Theme

`assets/theme.css` is the only place fonts, sizes and colors are defined. The builder reads its tokens for the
DOCX and applies the stylesheet to the HTML/PDF. `references/theme.md` explains each token.
To re-brand, edit the tokens and keep the rule that color carries meaning (pass/fail, change state) and
nothing else.

## Check before handing over

1. Open the PDF and the DOCX. Check that headings, tables and code blocks look the same in both, that header
   rows repeat across pages, and that no row is cut in half.
2. Re-read the result and issue tables against the evidence: every result row should trace to something
   the reader can see.
3. For an outside reader, search the Markdown for internal paths, hostnames, config labels and handles
   before sending.
