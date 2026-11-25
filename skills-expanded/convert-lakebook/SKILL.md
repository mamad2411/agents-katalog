---
name: convert-lakebook
description: |
  Convert Yuque .lakebook exports to Markdown files. Use when the user has a .lakebook file
  and wants to extract all documents as individual .md files. Supports batch conversion with
  an auto-generated index file.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# convert-lakebook

Convert Yuque `.lakebook` export files to clean Markdown documents.

## What This Skill Does

1. Extracts the `.lakebook` tar archive
2. Parses `$meta.json` for document metadata (titles, ordering, dates)
3. Converts each document's HTML body to clean Markdown using `html2text`
4. Outputs individual `.md` files named by document title
5. Generates an `_index.md` with a table of all documents

## Prerequisites

```bash
pip install beautifulsoup4 html2text
```

## Usage

When the user provides a `.lakebook` file path, run the conversion script:

```bash
python3 ~/Desktop/lakebook-converter/convert.py "<lakebook_file_path>" --output "<output_dir>"
```

### Parameters

- `<lakebook_file_path>`: Path to the `.lakebook` file (required)
- `<output_dir>`: Output directory for Markdown files (optional, defaults to `~/Desktop/lakebook-converter/output/`)

### Default Behavior

If the user just says `/convert-lakebook` with no arguments:

1. Ask the user for the `.lakebook` file path
2. Ask where they want the output (suggest `~/Desktop/lakebook-converter/output/`)
3. Run the conversion
4. Report results: how many docs converted, where they are, and show the index

### Example Invocations

```
/convert-lakebook ~/Desktop/export.lakebook
/convert-lakebook ~/Downloads/my-notes.lakebook --output ~/Documents/notes/
```

## Output Format

Each document becomes a Markdown file:

```markdown
# Document Title

[converted content...]
```

An `_index.md` file is generated with:

```markdown
# Document Index

Total: N documents

| # | Title | Words | Created |
|---|-------|-------|---------|
| 1 | [Title](filename.md) | 1234 | 2024-01-01 |
```

## Error Handling

- If dependencies are missing, prompt the user to install them
- If the file doesn't exist, report the error clearly
- If some documents fail to convert, report them but continue with the rest

## Post-Conversion Tips

After conversion, suggest the user can:
1. Use `/extract-memory <output_dir>` to analyze their writing style
2. Read specific documents with the Read tool
3. Search across documents with Grep
