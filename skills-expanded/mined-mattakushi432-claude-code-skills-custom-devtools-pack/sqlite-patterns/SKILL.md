---
name: sqlite-patterns
description: "When to activate: SQLite, WAL, FTS5, JSON1, pragma, in-memory database, embedded, WASM, SQLite3"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: databases
  language: sql
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# SQLite Patterns

## WAL Mode and Pragmas

```sql
-- Enable WAL for concurrent reads + single writer
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;       -- safe with WAL, faster than FULL
PRAGMA cache_size = -64000;        -- 64MB page cache (negative = KB)
PRAGMA temp_store = MEMORY;
PRAGMA mmap_size = 268435456;      -- 256MB memory-mapped I/O
PRAGMA foreign_keys = ON;          -- disabled by default!
PRAGMA busy_timeout = 5000;        -- 5s retry on locked db

-- Check DB integrity
PRAGMA integrity_check;
PRAGMA quick_check;                 -- faster, less thorough
```

## FTS5 Full-Text Search

```sql
-- Create FTS5 virtual table
CREATE VIRTUAL TABLE articles_fts USING fts5(
  title, body,
  content='articles',              -- external content table
  content_rowid='id',
  tokenize='unicode61 remove_diacritics 2'
);

-- Populate and keep in sync
INSERT INTO articles_fts(rowid, title, body)
  SELECT id, title, body FROM articles;

-- Triggers to keep FTS in sync
CREATE TRIGGER articles_ai AFTER INSERT ON articles BEGIN
  INSERT INTO articles_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;
CREATE TRIGGER articles_ad AFTER DELETE ON articles BEGIN
  INSERT INTO articles_fts(articles_fts, rowid, title, body) VALUES ('delete', old.id, old.title, old.body);
END;
CREATE TRIGGER articles_au AFTER UPDATE ON articles BEGIN
  INSERT INTO articles_fts(articles_fts, rowid, title, body) VALUES ('delete', old.id, old.title, old.body);
  INSERT INTO articles_fts(rowid, title, body) VALUES (new.id, new.title, new.body);
END;

-- Search with ranking
SELECT a.id, a.title, rank
FROM articles_fts
JOIN articles a ON a.id = articles_fts.rowid
WHERE articles_fts MATCH 'sqlite patterns'
ORDER BY rank;

-- Phrase and prefix search
SELECT * FROM articles_fts WHERE articles_fts MATCH '"exact phrase"';
SELECT * FROM articles_fts WHERE articles_fts MATCH 'sqlit*';
```

## JSON1 Extension

```sql
-- JSON functions
SELECT
  json_extract(data, '$.name')          AS name,
  json_extract(data, '$.tags[0]')       AS first_tag,
  json_array_length(data, '$.tags')     AS tag_count
FROM items;

-- json_each — shred array to rows
SELECT item.value AS tag
FROM items, json_each(items.data, '$.tags') AS item
WHERE items.id = 1;

-- json_patch — merge objects
UPDATE items SET data = json_patch(data, '{"status":"active"}') WHERE id = 1;

-- Index on JSON value
CREATE INDEX idx_name ON items (json_extract(data, '$.name'));
```

## Window Functions

```sql
SELECT
  date,
  revenue,
  SUM(revenue) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING) AS cumulative,
  AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d,
  ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank
FROM daily_revenue;
```

## Python Usage

```python
import sqlite3

# Thread-safe connection with WAL
con = sqlite3.connect("app.db", check_same_thread=False)
con.execute("PRAGMA journal_mode=WAL")
con.execute("PRAGMA foreign_keys=ON")
con.row_factory = sqlite3.Row  # dict-like rows

# Context manager for transactions
with con:
    con.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "a@b.com"))

# In-memory database for tests
mem_con = sqlite3.connect(":memory:")

# Parameterized queries (always — never f-strings)
users = con.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()

# Batch insert
con.executemany("INSERT INTO events VALUES (?, ?, ?)", event_tuples)
```

## WASM / Browser

```javascript
// sql.js — SQLite compiled to WebAssembly
import initSqlJs from 'sql.js';
const SQL = await initSqlJs({ locateFile: f => `/wasm/${f}` });
const db = new SQL.Database();
db.run("CREATE TABLE t (a, b)");
db.run("INSERT INTO t VALUES (?,?)", [1, "hello"]);
const results = db.exec("SELECT * FROM t");
// Persist: db.export() returns Uint8Array
```

## Tips

- One write connection + many read connections with WAL = high concurrency
- Use `WITHOUT ROWID` tables for lookup tables with natural primary keys
- `VACUUM` periodically or after bulk deletes to reclaim space
- `ATTACH DATABASE` to query multiple SQLite files in one session
- SQLite is great for: desktop apps, CLI tools, test fixtures, edge/embedded
