---
name: library-demo-db
description: Query the library database (books, members, loans) through the MCP SQL tool. Use whenever the user asks questions about books, authors, members, loans, or overdue returns — e.g. "which books are currently borrowed?", "most popular book", "who has overdue loans?".
---

# Library database

The database is exposed as the MCP tool **`sql_library_demo`**. Answer questions by sending a single SQL query string (MariaDB/MySQL dialect) to that tool. Results come back as JSON rows, truncated to the configured row limit (default 100) — use `LIMIT`, aggregation, or `ORDER BY` to keep result sets small and relevant.

## Schema

- **books** — `id`, `isbn`, `title`, `author`, `genre` (Software, Fiction, Thriller, Fantasy, History, Sci-Fi), `published_year`
- **members** — `id`, `email`, `full_name`, `joined_at`
- **loans** — `id`, `book_id` → books, `member_id` → members, `borrowed_at`, `due_date`, `returned_at` (NULL while the book is still out)

## Relations

- One book has many loans (`loans.book_id` → `books.id`); one member has many loans (`loans.member_id` → `members.id`).
- The library holds one copy of each book, so a book with an open loan (`returned_at IS NULL`) is currently unavailable.

## Conventions

- A loan is **open** when `returned_at IS NULL`; a book is "currently borrowed" if it has an open loan.
- A loan is **overdue** when `returned_at IS NULL AND due_date < CURRENT_DATE`.
- A loan was **returned late** when `returned_at > due_date`.
- Popularity questions usually mean loan counts per book (or per author); join through `loans`.

## Guidelines

- Treat the database as read-only: stick to `SELECT` unless the user explicitly asks to modify data.
- Prefer one well-formed query over many small ones; use joins and aggregates server-side.
