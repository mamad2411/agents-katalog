---
name: folder-organizer
description: >
  Use when a user wants to scan, audit, analyze, or tidy up a folder or collection of files — whether uploaded directly to the conversation, specified by local path, or described verbally. Trigger on requests like 整理檔案、掃描資料夾、幫我分類檔案、檔案整理計畫、資料夾結構建議、file organization, folder audit, help me sort my files, clean up my downloads, rename and categorize files, suggest a folder structure. Always follow a plan-first, execute-later pattern — never rename, move, or delete anything before the user confirms the full plan.
---

# Folder Organizer

A skill for scanning, analyzing, and organizing files — producing a complete reorganization plan before touching anything.

---

## Core Principle: Plan First, Execute Later

**Never rename, move, copy, or delete any file before the user explicitly confirms the full plan.**

Always present the complete plan and wait for an affirmative response.

---

## Phase 1 — Scan & Inventory

Determine where the files are:

| Source | How to access |
|--------|---------------|
| Uploaded to conversation | Check `/mnt/user-data/uploads/` |
| Local path given by user | Use `bash_tool` to `ls -lah <path>` |
| Described verbally | Ask the user to upload or provide a path |

Run a scan and report:

```bash
# Count files and get basic stats
find <target_dir> -type f | wc -l
find <target_dir> -type f -name "*" | sort
ls -lah <target_dir>
```

Present a simple summary:
- 📁 Total file count
- File types found (extensions breakdown)
- Any immediately obvious duplicates or empty files

---

## Phase 2 — Per-File Analysis

For each file, determine:

| Field | What to provide |
|-------|----------------|
| 📌 Content | What the file contains or represents (read text files; infer from name/extension for binaries) |
| 🏷 Suggested filename | Clear, descriptive, lowercase-with-hyphens or underscores, include date if relevant |
| 📂 Suggested folder | Logical category group name |
| 🗑 Deletable? | Flag if file appears redundant, empty, temp, or duplicate |

**Filename conventions:**
- Lowercase, use `-` or `_` as separators
- Include context: `2024-q3-sales-report.xlsx` not `report.xlsx`
- Keep extensions unchanged

**Folder naming conventions:**
- Short, noun-based: `reports/`, `assets/`, `drafts/`, `archives/`
- Avoid deep nesting beyond 2 levels unless necessary

---

## Phase 3 — Grouping & Structure Proposal

After analyzing all files, produce:

1. **Grouped clusters** — files that belong together by topic, project, or type
2. **Proposed folder tree** — show as a tree diagram, e.g.:
   ```
   📁 organized/
   ├── 📁 reports/
   │   ├── 2024-q1-sales.xlsx
   │   └── 2024-q3-forecast.pdf
   ├── 📁 assets/
   │   ├── logo-primary.png
   │   └── banner-homepage.jpg
   └── 📁 drafts/
       └── proposal-v2.docx
   ```
3. **Files to delete** — list separately with reason
4. **Files to bundle** — groups that could be zipped together (e.g., all assets for a project)

---

## Phase 4 — Confirmation Gate

Present the full plan and ask:

> 「以上是完整的整理計畫，請確認後我再執行。如需調整任何分類、檔名或資料夾名稱，請直接告訴我。」
> 
> (English: "Above is the complete reorganization plan. Please confirm before I proceed. Let me know if you'd like to adjust any category, filename, or folder name.")

**Do not proceed until the user says yes / 確認 / 執行 or equivalent.**

---

## Phase 5 — Execution (only after confirmation)

Once confirmed, execute the plan:

```bash
# Example: create folders and move files
mkdir -p <output_dir>/reports
mv "<source>/old-name.xlsx" "<output_dir>/reports/2024-q3-sales.xlsx"
# ... etc
```

After execution:
- Show a final file tree of the result
- Confirm completion with file count moved/renamed

---

## Edge Cases

| Situation | Behavior |
|-----------|----------|
| File content unreadable (binary, encrypted) | Infer from filename/extension; flag as "manual review needed" |
| Duplicate filenames after renaming | Append `-2`, `-3` suffix |
| User uploads a ZIP | Extract first, then analyze contents |
| No files found | Ask user to re-upload or verify path |
| Very large folder (100+ files) | Summarize by type clusters first; ask if user wants per-file detail |

---

## Output Language

Match the user's language. If the user writes in Traditional Chinese (繁體中文), respond in Traditional Chinese. If in English, respond in English.
