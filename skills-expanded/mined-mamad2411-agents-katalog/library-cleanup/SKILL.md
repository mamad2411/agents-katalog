---
name: "library-cleanup"
description: "Organizes files in a document library so people and AI can find them easily. Scans all files, summarizes issues (duplicates, empty folders, bad names), recommends a clean structure with a visual before/after comparison, reads file content to propose meaningful rename suggestions, then executes with a TODO checklist the user can follow along with. Triggered when someone says \"clean up file demo\"."
---
# Library Cleanup

When the user says **"clean up file demo"**, follow these steps to organize the current document library.

---

## Phase 1: Scan & Summarize Issues

- Identify the current document library using get_current_list_or_library.
- Get the library schema using get_list_schema.
- List all files and folders recursively using list_items with recursive=true, retrieving FileLeafRef, FileRef, FileDirRef, File_x0020_Size, FSObjType, and Modified.
- Analyze with execute_code and present a **high-level summary** of what's wrong. Keep it brief and scannable — no exhaustive item-by-item lists. Cover:
  - **Duplicate files**: Same filename appearing in multiple folders (note count and examples).
  - **Empty or near-empty folders**: Folders with 0 files, or only 1-2 files and no subfolders — they add clutter without value.
  - **Bad names**: Vague or unhelpful folder/file names like "Stuff", "Misc", "Random", "Junk Drawer", "temp", "New Folder", "DO NOT USE", "Why Is This Here", "drafts maybe", "asdfghjkl", "doc1", "thing", "final_FINAL_v3 (2)", "Copy of Copy of...", "idk", "zzzzz", "untitled", "aaa", "test123", "file (1)", "hmm what is this", "New Document", "IMPORTANT maybe", etc.
  - **Excessive nesting**: Folders buried 3+ levels deep that make browsing painful.
- Present this as a short, punchy summary — think executive briefing, not audit report.
- **Store the "before" metrics** for later use: total folders, duplicate file count, files with bad names count, empty folders count, max nesting depth. Calculate an initial **Organization Score** from 0–100 based on a weighted formula (penalize duplicates, bad names, empty folders, excessive depth).

---

## Phase 2: Recommend a Clean Structure (with Visualization)

This phase combines the plan AND the visualization into one cohesive recommendation. The user should see the full picture — proposed structure, rename plan, and before/after comparison — all at once before approving.

### Step A: Design the new folder structure

- Based on the scan, propose a **new folder structure** that is:
  - **Very simple**: Minimize folder count. Flat is better than deep.
  - **Grouped by similarity**: Files about the same topic or type go together.
  - **Clearly named**: Every folder name should tell you exactly what's inside.
  - **Easy for both humans and AI**: Logical grouping, no ambiguity, no junk drawers.
- To design the structure:
  - Read a sample of files (use cat_file on a representative set) to understand what content exists.
  - Group files by theme/purpose based on their names and content.
  - Propose new folder names that are descriptive and professional.

### Step B: Content-based rename plan (CRITICAL)

- Identify all files with bad, vague, or unclear names.
- **Read the actual content of every badly-named file** using cat_file. Do NOT skip this step. Do NOT guess names from the old filename alone.
- For each file, propose a new name **derived from the file's actual content** — use the document title, subject matter, client name, project name, or primary topic found inside the file. Names should be specific and descriptive enough that someone can understand what the file is without opening it.
  - Example: "asdfghjkl.pdf" containing a kitchen inspection report → "Grand Gastronomy Hall Kitchen Inspection.pdf"
  - Example: "doc1.docx" containing a construction bid → "Solara Energy - AI Research Facility Bid.docx"
  - Example: "thing.pdf" containing a solar array bid → "Quantum Solar Array Initiative Bid.pdf"
- **Never use generic placeholder names** like "Unnamed Document.pdf", "Unknown Document.docx", "Miscellaneous.pdf", "Document 1.docx", etc. These are no better than the original bad names. Always base the name on what the file actually says.
- If reading a file's content reveals it belongs in a different category folder than initially planned, note this as a **recategorization** in the plan.
- If a file is empty or unreadable, note that to the user and ask them what to name it.

### Step C: Present the full plan with visualization

Present everything together in one cohesive recommendation:

1. **Tree-style text visualization** of the recommended folder structure showing each proposed folder with its files listed underneath (using the NEW proposed names for renamed files) and file counts per folder.

2. **Content-based rename table** with columns: Current Name | Proposed Name | Content Summary | Destination Folder. This shows the user exactly what each file contains and why you chose that name.

3. **Before vs. after comparison table** showing key metrics side by side: total folders, max depth, empty folders, bad names, Organization Score.

4. **Grouped bar chart** (using create_chart) comparing "Before" vs. "After" across those metrics. Use red for the current state and green for the recommended state.

5. **Folders to delete** — list all folders that will be removed.

Then ask: **"Do you approve this plan?"**

---

## Phase 3: Execute with TODO Checklist

Once the user approves the plan, immediately present a **TODO checklist** of every discrete action you will perform. Format it as a numbered checklist using empty checkboxes. Group items logically.

Example format:
```
## Cleanup TODO

### Create new folders
- [ ] Create "Construction Bids" folder
- [ ] Create "Inspection Reports" folder
- [ ] Create "Engineering Manuals" folder

### Remove duplicates
- [ ] Delete duplicate "report.docx" from Stuff/ (keeping copy in Reports/)

### Move files to new folders
- [ ] Move construction_bids_T7_F1.pdf → Construction Bids/
- [ ] Move inspection_reports_T1_F1.docx → Inspection Reports/
- ... (list every move)

### Rename files (content-based)
- [ ] asdfghjkl.pdf → Grand Gastronomy Hall Kitchen Inspection.pdf
- [ ] doc1.docx → Solara Energy - AI Research Facility Bid.docx
- ... (list every rename)

### Delete empty old folders
- [ ] Delete "Stuff" folder
- [ ] Delete "Misc" folder
- ... (list every folder deletion)

### Generate impact report
- [ ] Create cleanup-impact-report.html
```

After presenting the checklist, begin executing. As you complete each group of actions, **re-display the full checklist with completed items checked off** using `[x]` and remaining items still unchecked `[ ]`. This gives the user a running progress view.

**Execution order:**
1. Create new folders → update checklist
2. Remove duplicates (if any) → update checklist
3. Move all files to new locations → update checklist
4. Rename files using content-based names + move any recategorized files → update checklist
5. Delete empty old folders → update checklist
6. Generate impact dashboard → update checklist

**After each group**, re-display the updated checklist and ask: "Want me to continue?" Wait for a response before proceeding.

---

## Phase 4: Impact Dashboard

After all cleanup actions are done, generate a polished **HTML impact dashboard** file and save it to the document library using create_text_file.

### Collecting "After" Metrics
- Re-scan the library (list_items recursive) to get the actual post-cleanup state.
- Calculate the "after" metrics: total folders, duplicate files, files with bad names, empty folders, max depth.
- Recalculate the **Organization Score** (0–100) using the same formula as Phase 1.

### Dashboard Requirements

Use execute_code with outputDataRef to generate the full HTML content. The dashboard must be a single self-contained HTML file (inline CSS, no external dependencies) with a clean, modern design. It should include:
- **Header**: Library name, date of cleanup, title like "Library Cleanup Impact Report".
- **Four metric cards** in a row, each card showing:
  - **Organization Score**: Large number with green upward arrow and improvement text (e.g., "+62 points").
  - **Total Folders**: Large number with green downward arrow and reduction text.
  - **Files with Bad Names**: Large number with green downward arrow and reduction text.
  - **Duplicate Files**: Large number with green downward arrow and reduction text.
- **Styling**: White cards with subtle shadow, light gray background (#f8fafc), professional sans-serif font, green (#22c55e) for improvements, responsive flexbox layout, max-width ~1000px.

Save the file as cleanup-impact-report.html in the library root. Present the link to the user. Mark the final TODO item as complete and show the fully checked-off list.

---

## Scale and resilience

The skill must handle large libraries and partial failures gracefully — the consumer should never be left with a half-cleaned library and no idea what went wrong.

### Large libraries (> 1000 items)

- **Initial scan**: `list_items recursive=true` may exceed the response size limit on libraries with > 1000 items. If the call returns a truncated or paged response, fall back to **per-folder scanning**: enumerate top-level folders first, then walk each one in turn, aggregating the results in `execute_code`.
- **Content reads in Phase 2**: do not call `cat_file` on every file. Read content **only for files with bad/vague names** (the rename candidates). For a 5000-file library this is typically < 100 reads.
- **Batch the execution in Phase 3**: cap each move/rename batch at ~50 operations. After each batch, re-display the checklist and pause for the user's *"continue"* before starting the next batch. This keeps each step recoverable and visible.
- **Throttling**: if the tenant returns a throttling error (HTTP 429 or equivalent), back off and retry the single operation once. If it fails again, mark the item as failed in the checklist and continue with the rest of the batch.

### Partial failures during execution (Phase 3)

Moves, renames, and folder deletions can fail for individual items — file locked, permission denied, name conflict, throttling. The run **must not abort** on a single-item failure.

- **Continue the batch.** Capture the error against the failed checklist item, mark it `[✗]` (instead of `[x]` or `[ ]`), and move on. Do not roll back items already completed.
- **One retry, then mark failed.** For transient errors (throttling, timeout), retry the single operation once. If it fails again, leave the `[✗]` and record the reason.
- **End-of-batch summary.** After each batch, the re-displayed checklist must show counts: e.g. `42 succeeded, 3 failed, 5 remaining`.
- **Final report.** The Phase 4 impact dashboard must include a **"Items that need attention"** section listing every `[✗]` item with its failure reason. If this section is empty, omit it.
- **Never silently drop an action.** Every item from the approved plan must end the run as either `[x]` (done), `[✗]` (failed, with reason), or `[ ]` (skipped by the user) — never simply missing.

### Phase 4 dashboard fallback

`execute_code` and `create_text_file` may be unavailable, may fail to render the HTML, or may be blocked from writing to the library root.

- **If `execute_code` fails**: skip the HTML generation and present the same content as a Markdown report inline in the chat — header, four metric cards as a Markdown table, before/after comparison, list of `[✗]` items. The cleanup itself is still considered successful; only the dashboard format degrades.
- **If `create_text_file` fails to write to the library root**: try writing to a `Cleanup Reports` subfolder. If that also fails, return the HTML inline in the chat as a fenced code block and tell the user where they can paste it.
- **Always surface the score change.** Even with no dashboard, the chat reply must include the before/after Organization Score and the count of completed vs failed actions.

---

## Constraints

- **Never delete, move, or rename files without explicit user approval of the overall plan.**
- Always confirm the full plan in Phase 2 before executing anything in Phase 3.
- **Never propose generic/placeholder rename names.** Always read the file content and derive a meaningful name from it.
- Focus on making the library easy to browse for both humans and AI — clear naming, logical grouping, minimal nesting.
- For large libraries or partial failures, follow the rules in **Scale and resilience** above. A single-item failure must not abort the run.
- The Organization Score formula should be consistent between Phase 1 and Phase 4 so the comparison is fair. Suggested formula: start at 100, subtract points for each duplicate (-3), each bad name (-3), each empty folder (-2), each level of nesting beyond 2 (-5), and each folder beyond a reasonable count (-1 per excess folder). Clamp to 0–100.