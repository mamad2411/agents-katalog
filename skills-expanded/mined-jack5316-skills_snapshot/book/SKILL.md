---
name: book
description: Manage and generate book notes. Use when user asks for book notes, Kindle highlights, or /book.
---

# Book Notes Skill

Creates structured book notes from AI knowledge or Kindle clippings.

## Usage

**From title (AI-generated):**
```bash
python3 _scripts/book_notes.py title "Book Title" [--author X]
```

**From Kindle clippings:**
```bash
python3 _scripts/book_notes.py kindle path/Clippings.txt [--book X]
```

- `--book`: Filter to specific book when Clippings.txt has multiple

## Output

`Sources/` or `Atlas/` with structured notes (Overview, Key Ideas, Quotes, [[wikilinks]])
