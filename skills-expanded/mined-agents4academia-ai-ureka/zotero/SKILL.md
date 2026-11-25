---
description: Ingest a Zotero PDF (with annotations) into a clean source file + a consolidated annotation note
argument-hint: <PDF path or search query> (e.g. "/path/to/react.pdf" or "ReAct reasoning acting")
allowed-tools: Read, Write(sources/**), Write(notes/**), Write(.mcp.json), Glob, Bash(date:*), Bash(python3:*), Bash(sh .claude/src/pyrun:*), AskUserQuestion, mcp__zotero__zotero_search_items, mcp__zotero__zotero_get_item_metadata, mcp__zotero__zotero_get_item_children, mcp__zotero__zotero_get_attachment_path, mcp__zotero__zotero_get_pdf_outline, mcp__zotero__zotero_read_pdf_pages, mcp__zotero__zotero_get_annotations, mcp__pdf-tools__extract_pdf_text, mcp__pdf-tools__extract_ink_annotations
---

**Do not read existing files in `notes/` or `sources/` to infer style. Follow only
the instructions in this skill. Existing files may use a different format.**

Ingest a Zotero-annotated PDF given by **$ARGUMENTS** and write two kinds of output:

- **`sources/zotero_<slug>.md`** — objective paper text, clean and impersonal (`type: zotero_source`)
- **`notes/zotero_<paper_slug>/annotations.md`** — all annotations consolidated in reading
  order, each with a location description and verbatim content; ink crops alongside (`type: zotero_annotation`)

If **$ARGUMENTS** is empty, use `AskUserQuestion` to ask:
- Question: "What PDF or paper do you want to ingest?"
- Options: "A file path (e.g. /path/to/react.pdf)", "A search query (e.g. ReAct reasoning acting)"
Do not proceed until the user answers.

## Root

- Sources: `sources/`. Template: `.claude/Templates/source.md`.
- Notes: `notes/zotero_<paper_slug>/`. Template: `.claude/Templates/note.md`.
- Ink crops: saved directly into `notes/zotero_<paper_slug>/` by `extract_ink_annotations`.

---

## Step 1 — Route input and resolve all paths

**This step produces three variables that must ALL be settled before Step 2 begins:
`abs_path`, `item_key`, and `zotero_path`. Execute the phases below in strict
order. Do not call any Step 2 tools until Phase 1-C is complete.**

---

### Phase 1-A — Establish `abs_path`

Determine whether **$ARGUMENTS** is a **path** or a **search query**.

It is a **path** if any of these are true:
- ends with `.pdf`
- starts with `/`, `./`, `..\`, a Windows drive letter (`C:\`), or `~`
- contains `/` or `\`

**If PATH:** expand to absolute path:
```
python3 -c "import os,sys; print(os.path.abspath('$ARGUMENTS'))"
```
→ `abs_path`. Check whether it exists on disk.

**If QUERY:** `abs_path` is absent. Proceed to Phase 1-B.

---

### Phase 1-B — Find `item_key`

**If PATH and on disk:** extract the title from the first page, then search Zotero
using both the basename (without extension) and the extracted title:
```
sh .claude/src/pyrun --need fitz -c "
import fitz, sys
doc = fitz.open(sys.argv[1])
text = doc[0].get_text()[:500]
doc.close()
sys.stdout.buffer.write(text.encode('utf-8'))
sys.stdout.buffer.write(b'\n')
" "<abs_path>"
```
`zotero_search_items(query="<basename>")` and `zotero_search_items(query="<pdf_title>")`.
Pick the best candidate → `item_key`. If no match: `item_key` is absent.

**If PATH and not on disk:** `zotero_search_items(query="<basename>")` → `item_key`.
If no match: stop and report.

**If QUERY:** `zotero_search_items(query="$ARGUMENTS")` → `item_key`.
If no match: stop and report.

**Do not proceed to Phase 1-C until `item_key` is settled (found or confirmed absent).**

---

### Phase 1-C — Resolve `zotero_path`

**If `item_key` is absent:** `zotero_path` is absent. Go to Phase 1-D.

**If `item_key` is known:** call `zotero_get_item_children(item_key)` to get the
PDF attachment. Then call `zotero_get_attachment_path(attachment_key)`.

Three outcomes — handle each, never skip:

**A — Path returned and exists on disk:**
`zotero_path` = that path. Done.

**B — Path returned but does not exist on disk** (e.g. `attachments:` prefix):
Strip the placeholder prefix. Get `zotero_base_dir` (see below), then:
```
python3 -c "import os,sys; print(os.path.abspath(os.path.join(sys.argv[1], sys.argv[2])))" "<zotero_base_dir>" "<stripped_path>"
```
→ `zotero_path`.

**C — No path returned at all:**
Use the `filename` field from the children response. Get `zotero_base_dir` (see
below), then:
```
python3 -c "import os,sys; print(os.path.abspath(os.path.join(sys.argv[1], sys.argv[2])))" "<zotero_base_dir>" "<filename>"
```
→ `zotero_path`.

**Getting `zotero_base_dir`** (cases B and C):
1. Read `.mcp.json` — check `ZOTERO_BASE_ATTACHMENT_PATH` in the `zotero` env block.
   If present, use immediately.
2. If absent — use `AskUserQuestion`:
   - Question: "Zotero could not resolve the local path for `<filename>`. What is your Zotero linked-file base directory?"
   - Options: one example per platform + "Other"
   Do not call any further tools until the user answers.
3. Persist to `.mcp.json`:
   `"env": { "ZOTERO_LOCAL": "true", "ZOTERO_BASE_ATTACHMENT_PATH": "<zotero_base_dir>" }`
   Skip if already set to the same value.

**Do not proceed to Phase 1-D until `zotero_path` is settled (resolved or confirmed absent).**

---

### Phase 1-D — Compare paths and decide ingestion mode

With `abs_path` and `zotero_path` both settled, determine what to ingest:

| `abs_path` | `item_key` | `zotero_path` on disk? | Mode |
|---|---|---|---|
| Present | Present | Same as `abs_path` | Single file — use Zotero metadata + annotations |
| Present | Present | Different from `abs_path` | Two distinct files — merge both |
| Present | Absent | — | Local file only; no Zotero entry |
| Absent | Present | Yes | Zotero file only |
| Absent | Present | No | Zotero read-only (no ink extraction) |

**Step 1 is now complete. Proceed to Step 2.**

---

## Step 2 — Gather metadata and annotations (when Zotero entry exists)

**Do not begin this step until Step 1 is fully complete** — all of the following
must be settled before any tool call here:
- `abs_path` — expanded absolute input path (or absent if no local file)
- `item_key` — Zotero entry key (or confirmed absent)
- `zotero_path` — resolved local path of the Zotero attachment (or confirmed absent;
  the "Resolving a Zotero attachment path" procedure must have run to completion,
  including any user prompt for the base directory)

Do **not** call `extract_ink_annotations` on `abs_path` before `zotero_path` is
known — all ink extraction happens after both paths are resolved.

When `item_key` is known, call:

- `zotero_get_item_metadata(item_key)` → title, authors, year, abstract
- `zotero_get_annotations(item_key)` → highlights + typed notes + area annotations

Derive the **paper slug** from the title now (snake_case, e.g. `attention_is_all_you_need`)
— you need it for the note folder path and for `extract_ink_annotations`.

With both `abs_path` and `zotero_path` now known, run `extract_ink_annotations` on
**each path that is accessible on disk**. If `zotero_path` == `abs_path`, run once only:

```
extract_ink_annotations("<path>", output_dir="notes/zotero_<paper_slug>")
```

Crops are saved as `notes/zotero_<paper_slug>/crop_<stem>_p<N>_c<M>.png`.

---

## Step 3 — Read body text from all sources

Run `extract_pdf_text` on **every PDF path that is accessible on disk**. Never use
`zotero_read_pdf_pages` for body text.

| Condition | Action |
|---|---|
| `zotero_path` on disk | `extract_pdf_text("<zotero_path>")` |
| `abs_path` on disk AND distinct from `zotero_path` | `extract_pdf_text("<abs_path>")` |
| No `item_key`, `abs_path` on disk | `extract_pdf_text("<abs_path>")` only |

Label each result by its source path. Carry all labelled texts forward to Step 5a.

---

## Step 4 — Describe annotations by location

For every annotation, produce a **record**. Each record has three fields:

1. **`topic`** — a 3–5 word snake_case slug.
2. **`concepts`** — concepts touched (short list).
3. **`description`** — two parts, written as plain prose:

   **Part 1 — Location.** Describe WHERE the annotation is using content landmarks,
   not coordinates or percentages. Use natural language:
   - Page number and PDF source (if multiple)
   - Margin position: "left margin", "right margin", or "inline with text"
   - Vertical position: "top of page", "upper section", "mid-page", "lower section",
     "bottom of page" — use these terms only; never use percentages or pixel values
   - Content anchor: the nearest section heading, figure number, formula, or key phrase
     (e.g. "alongside §3.2.2", "next to Figure 2", "above the attention formula")

   **Part 2 — What was marked.** Describe exactly what the annotation consists of:
   - For underlines: which specific words or phrases are underlined
   - For circles/boxes: which specific element is enclosed (a word, a diagram block,
     a formula, a figure label)
   - For arrows: what the arrow points from and to
   - For handwriting: the transcribed text verbatim
   - For whole-page crops: enumerate each distinct mark visible — do not collapse
     multiple marks into "various annotations"; describe each one separately

   End with the verbatim content in **[brackets]**.

   Examples:
   > "Page 4, right margin, mid-page, alongside §3.2.2 Multi-Head Attention. A
   > handwritten question in the margin next to the sentence describing learned linear
   > projections of queries, keys, and values.
   > [Handwritten: "learned linear projection?"]"

   > "Page 3, inline, lower section, alongside §3.1 Decoder. An ink underline under
   > the phrase describing causal masking.
   > [Handwritten: ink underline under "prevent positions from attending to subsequent positions"]"

**Ink annotations** (from `extract_ink_annotations`):

For **every** ink crop (whether `whole_page: false` or `true`), the mandatory
first action is to `Read` the image and produce a **raw mark inventory** in your
internal reasoning — before writing any description. The inventory is a numbered
list of every ink mark visible in the image, top-to-bottom, left-to-right. Do not
skip any mark. **This inventory is a working step only — never write it to any
output file.**

Inventory format (internal only):
```
1. [type] on/under/around "[exact text or element]" — [location on page]
2. [type] on/under/around "[exact text or element]" — [location on page]
...
```

Types: `underline` / `circle` / `box` / `bracket` / `arc or curve` / `arrow` /
`freehand stroke` / `handwriting`.

**Do not use `surrounding_ctx` to infer what is marked.** The inventory must come
entirely from visual observation of the image. `surrounding_ctx` may only be used
afterwards to identify which section/figure/formula a mark is adjacent to.

Once the inventory is complete:
- For `whole_page: false`: the inventory typically has one entry → one record.
- For `whole_page: true`: each inventory entry (or tight cluster) → one record.
  Never combine multiple entries into one record. A page with 5 marks → 5 records.

For each record:
- Verbatim: `[Handwritten: "transcribed text"]` for handwriting, or
  `[Handwritten: <type> under/around "<exact text>"]` for marks.
- If `label` non-empty: append `— label: "label"` inside the brackets.
- Embed the crop: `![](./crop_<stem>_p<N>_c<M>.png)` (single crop) or
  `![](./page_<stem>_p<N>.png)` (first record for a whole-page only; omit in
  subsequent records for the same page) — immediately before the verbatim.
- Use `bbox`/`page_width`/`page_height` only for margin vs inline and coarse
  vertical zone — never report raw numbers.

**Highlights** (`annotationType: "highlight"`):
- Describe exactly which phrase is highlighted.
- Verbatim: `[Highlight: "annotationText"]`
- If `annotationComment` non-empty: `[Highlight: "annotationText" — Note: "annotationComment"]`

**Typed notes / area annotations** (other `annotationType` values):
- Verbatim: `[Note: "annotationComment"]`

Collect all records in reading order (by page and position).

---

## Step 5a — Write the source file

1. Read `.claude/Templates/source.md`.
2. Fill in:
   - `type: zotero_source`
   - `title`: from metadata, or inferred from the first page of body text
   - `concepts_mentioned`: key concepts as a YAML inline list
   - `source_links`: one entry per ingested file. Each entry is a structured object:
     - Plain local file (no Zotero match):
       `- path: <abs_path>`
     - Zotero-linked file:
       `- zotero: {item_key: <item_key>, linked_path: <zotero_path>}`
     - Both (distinct files merged):
       `- path: <abs_path>`
       `- zotero: {item_key: <item_key>, linked_path: <zotero_path>}`
   - `## Content`: write the extracted body text verbatim, with no rewriting, no summarisation, and no omissions:
     - **Single source, or all sources identical** (compare after stripping leading/trailing whitespace): paste the text once.
     - **Sources differ**: write each version under its own `### <source_path>` subheading, verbatim.
3. Get today's date: `date +%F`
4. Slugify the title → snake_case. Target: `sources/zotero_<slug>.md`.
   If the file already exists, use `AskUserQuestion`:
   - Question: "`sources/zotero_<slug>.md` already exists. Overwrite?"
   - Options: "Yes, overwrite", "No, keep existing"
   Do not write or call any further tools until the user answers.

---

## Step 5b — Write annotation files and merge

Skip this step entirely (and report) if the PDF had no annotations.

1. Create `notes/zotero_<paper_slug>/` if it doesn't exist:
   ```
   python3 -c "import os; os.makedirs('notes/zotero_<paper_slug>', exist_ok=True)"
   ```

2. **Write one temporary file per record** from Step 4, in reading order.
   For each record, write `notes/zotero_<paper_slug>/_note_<NN>_<topic>.md`
   (underscore prefix marks it as temporary) containing:
   ```
   ### <topic>

   <description from Step 4>

   ![](./crop_or_page_filename.png)   ← ink annotations only

   [verbatim content]
   ```
   Complete each file fully before moving to the next. Do not batch or summarise.

3. **Merge all temporary files** into `notes/zotero_<paper_slug>/annotations.md`.
   Read `.claude/Templates/note.md` for the frontmatter shape:
   - `type: zotero_annotation`
   - `title`: `<paper title> — Annotations`
   - `concepts_mentioned`: union of all concept lists from Step 4 records
   - `source_links`: list of all PDF paths ingested (raw source paths, not the
     derived source file) — one entry per PDF used

   `## Content` = concatenation of all `_note_*.md` files in reading order,
   separated by `---`.

   If `annotations.md` already exists, use `AskUserQuestion`:
   - Question: "`notes/zotero_<paper_slug>/annotations.md` already exists. Overwrite?"
   - Options: "Yes, overwrite", "No, keep existing"
   Do not write or call any further tools until the user answers.

4. **Delete the temporary files** after `annotations.md` is written:
   ```
   python3 -c "
   import os, glob
   for f in glob.glob('notes/zotero_<paper_slug>/_note_*.md'):
       os.remove(f)
   "
   ```

---

## Wrap up

Report:
- Source file written: `sources/zotero_<slug>.md`
- Annotation note written: `notes/zotero_<paper_slug>/annotations.md` (N annotations)
- Ink crops written: list any `notes/zotero_<paper_slug>/crop_*.png` and `page_*.png`
- Zotero match status (item_key or "no match")
- Annotation counts: N highlights, N typed notes, N ink annotations
- Anything skipped (one-line reason each)

Then ask the user:
- Run `/retrieve <topic>` to find related sources and existing pages.
- Run `/collate <topic>` to synthesise a paper or concept page from this note together with other sources on the same topic.
