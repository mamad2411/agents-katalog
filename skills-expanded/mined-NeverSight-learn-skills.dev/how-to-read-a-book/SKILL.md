---
name: how-to-read-a-book
description: |
  Trigger this skill whenever the user wants to process an EPUB book file and upload it to NotebookLM
  for deep analytical reading. Activate when: the user mentions "NotebookLM" or "notebook" along with
  "book", "ebook", "epub", or a book title; when they want to convert/split an EPUB into chapters;
  when they mention uploading a book to NotebookLM; when they want to create a reading companion
  or use "How To Read a Book" methodology with NotebookLM. Also trigger for phrases like
  "analyze this book", "deep read this book", "upload chapters to notebooklm", "epub to notebooklm",
  or any mention of analytical reading with NotebookLM.
---

# How To Read a Book — NotebookLM Reading Companion

## Overview

Transform EPUB-formatted ebooks into chapter-level Markdown sources for NotebookLM, paired with a custom "How To Read a Book" analytical reading persona. This skill orchestrates the complete workflow: parsing EPUB structure, splitting by chapters, creating a NotebookLM notebook, injecting the reading companion persona, and uploading all sources.

## When to Use

Use this skill when the user wants to:
- Upload an EPUB book to NotebookLM for deep reading
- Create a structured reading companion for non-fiction books
- Split an EPUB into chapters and upload them as separate sources
- Apply analytical reading methodology to a book in NotebookLM
- Transform ebooks into NLP-friendly chapter format for AI analysis

## Prerequisites

Before running this skill, ensure:
1. The user has `notebooklm-py` installed: `pip install notebooklm-py playwright`
2. Playwright installed: `playwright install chromium`
3. User is authenticated: `notebooklm login`
4. User has an EPUB file locally available

## How to Use

### Step 1: Verify Environment

Check if dependencies are installed and user is authenticated:

```bash
which notebooklm
notebooklm list  # Should succeed if authenticated
```

If not installed, guide user through setup or run `./install.sh` if it exists.

### Step 2: Get EPUB Path

Ask the user for the path to their EPUB file, or confirm the path if they provided it.

User prompts that indicate EPUB path:
- "I have a book at /path/to/book.epub"
- "Process this EPUB: ~/Downloads/mybook.epub"
- "Upload this book to NotebookLM" (ask for path)

### Step 3: Run the Skill

Execute the main script with the EPUB path:

```bash
python3 /Users/jarodise/.claude/skills/how-to-read-a-book/scripts/run.py <path-to-epub>
```

### Step 4: Report Results

The script will output:
- Progress indicators for each phase (📖 Parsing → ✍️ Converting → 📤 Uploading → ✅ Complete)
- JSON result with `notebook_id`, `notebook_url`, `book_title`, `chapter_count`, `sources_uploaded`
- Human-readable summary with NotebookLM link

### Step 5: Guide the User

Once complete, tell the user:
- How many chapters were uploaded
- The NotebookLM notebook URL
- That the reading companion persona is now active
- Suggest starting questions like "What is the main problem this book is trying to solve?" or "Summarize Chapter 1's key argument"

## What the Skill Does

1. **Parse EPUB**: Extract book metadata and chapter structure using TOC-first with heading-based fallback
2. **Split into Chapters**: Convert each chapter to Markdown with frontmatter (number, title, source book)
3. **Create Notebook**: Create new notebook titled `<Book Title> — Reading Companion`
4. **Configure Persona**: Inject "How To Read a Book" analytical reading methodology as system prompt
5. **Upload Sources**: Upload all chapter Markdown files as individual sources
6. **Cleanup**: Remove temporary files after successful upload

## Error Handling

| Error | Response |
|-------|----------|
| EPUB file not found | "I couldn't find that EPUB file. Please check the path: `<path>`" |
| Invalid/corrupt EPUB | "This EPUB appears to be damaged or in an unsupported format." |
| NotebookLM not installed | "Please install dependencies first: `pip install notebooklm-py playwright && playwright install chromium`" |
| Not authenticated | "Please authenticate with NotebookLM first: `notebooklm login`" |
| Upload fails | Report partial success, preserve temp files for retry |

## Expected Output Format

The script outputs JSON after `---JSON_OUTPUT---` delimiter:

```json
{
  "notebook_id": "uuid-here",
  "notebook_url": "https://notebooklm.google.com/notebook/uuid-here",
  "book_title": "Book Title Here",
  "chapter_count": 12,
  "sources_uploaded": 12
}
```

## Limitations

- EPUB format only (not PDF, MOBI, or AZW)
- Local files only (no URL downloading)
- Single universal reading companion persona (no book-type variations)
- Post-upload conversation happens in NotebookLM interface, not via this skill

## Reference

- Pattern based on: `/Users/jarodise/Documents/GitHub/CNinfo2Notebookllm`
- EPUB parsing: `ebooklib` Python library
- NotebookLM CLI: `notebooklm-py`
