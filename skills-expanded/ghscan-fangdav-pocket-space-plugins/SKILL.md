---
name: contribution-guidelines
description: >
  This skill should be used whenever creating, editing, moving, or deleting files
  in the Pocket Space shared drive. Trigger with "create a document", "add a file",
  "write a new doc", "update this file", "where should I put this", or any request
  that modifies the folder contents. Ensures all contributions follow Pocket Space
  conventions for file formats, naming, README maintenance, and folder structure.
---

# Pocket Space Contribution Guidelines

Rules for keeping the shared drive consistent, organized, and AI-readable.

## Authorship

- **Include your name at the top of any file you create** (e.g., `Author: David, Feb 2026`).
- When making significant edits to an existing file, add your name if it isn't already there.
- Do NOT include the author's name in the file name.

## File Format Rules

1. **Markdown (.md)** and **Excel (.xlsx)** for all planning files — brainstorming, research, meeting notes, roadmaps, open questions, ideation, and any working/in-progress documents. Use `.md` for files that do not require input from multiple users.
2. **Word (.docx)** only for final deliverables — polished reports, formal letters, or documents that **require** ongoing collaboration or input from multiple users. Do **not** use `.docx` for planning or research. **Do not make .docx files unless explicitly asked.**
3. **Excel (.xlsx)** for tabular data and spreadsheets.
4. **Allowed formats**: `.md`, `.docx`, `.xlsx`, `.csv`, `.json` — nothing else.
5. **Do not use Google Docs** — all documents must be stored as local files (`.md`, `.docx`, etc.) in this shared drive, not as Google Docs links or files.

## Naming Conventions

- Use underscores instead of spaces: `My_Document.md` not `My Document.md`
- Use descriptive names: `SocialFi_Market_Analysis.xlsx` not `Analysis.xlsx`
- For versioned docs, use `_Current` suffix for the canonical version: `FRD_Current.md`
- Date-prefixed for chronological files: `2025-01-29_Meeting_Notes.md`

## Before Making Changes

1. **Always read the README.md** in a folder before making any changes to it.
2. README files contain important context about what exists and its purpose.
3. Check if a file already exists before creating a new one.

## After Making Changes

1. **Update the relevant README.md** to reflect any new, modified, or deleted files.
2. If creating a new folder, add a README.md to it.

## README Writing Guidelines

- **Be parsimonious.** Keep content high-level and concise — say only what is needed to orient the reader.
- **Focus on what the folder is about**, not what individual files it contains. Do not list or reference specific files.
- **Describe subfolders.** After explaining the folder's purpose, list any subfolders and briefly state what each one is for.

## Research Folder Rule for .docx Deliverables

Every `.docx` deliverable must live inside a **dedicated topic folder** alongside a `Research/` subfolder containing all the `.md` source files used to generate it.

**Required structure:**
```
[Department_Folder]/
└── [Topic_of_Research]/
    ├── [Topic_of_Research].docx       ← The deliverable
    └── Research/                       ← All source .md files
        ├── README.md                   ← Describes contents of this research folder
        ├── Landscape_Research.md
        ├── Comparison_Matrix.md
        ├── Segment_A/                  ← Can be deeply nested
        │   ├── Segment_A_Deep_Dive.md
        │   └── Sub_Topic/
        │       └── Sub_Topic_Research.md
        ├── Segment_B/
        │   └── Segment_B_Deep_Dive.md
        └── ...
```

**Rules:**
- The topic folder and .docx share the same name (e.g., `SocialFi_Market_Analysis/SocialFi_Market_Analysis.docx`)
- The `Research/` subfolder must contain a `README.md` describing its contents
- All .md files referenced in the .docx must live inside `Research/` or its subfolders
- The `Research/` folder can be deeply nested — use subfolders to organize by segment, topic, or phase
- The .docx must hyperlink to files inside its `Research/` folder
- If research files already exist elsewhere in the drive, copy or move them into `Research/` so the deliverable and its sources are self-contained

## Folder Placement Rules

- `_Active/` — Only current, relevant documents
- `_Archive/` — Historical documents, organized by era/pivot
- `_Meeting_Notes/` — Organized by `YYYY-MM` subfolders
- Never place files at the root level unless they are project-wide (like README.md)
