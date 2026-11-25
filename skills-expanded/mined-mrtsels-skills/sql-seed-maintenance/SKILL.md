---
name: sql-seed-maintenance
description: Maintain monolithic SQL seed files (DDL+DML in one file). Verify column-value count consistency after schema changes, detect MySQL version incompatibilities, and regenerate compatible variants.
---

# SQL Seed File Maintenance

> 本技能为 SQL 种子文件维护类技能的伞(umbrella),已吸收 `mysql-init-sql-maintenance`(2026-08 合并)。
> 完整原文见 `references/absorbed-mysql-init-sql-maintenance.md`。

Pattern for maintaining a single-file SQL seed (e.g. `init.sql`) that combines DDL (CREATE TABLE) and DML (INSERT INTO) for demo/seed data.

## Trigger Conditions

- User asks you to add/remove a column from a table in `init.sql` or equivalent
- User reports "Column count doesn't match value count" error from MySQL
- User needs a MySQL 5.7 compatible version of a MySQL 8.0 seed file
- User asks you to verify a SQL seed file is valid

## Core Workflow

### 1. After any DDL change (add/remove column), verify INSERT VALUES

**The most common bug**: removing a column from CREATE TABLE but forgetting to remove the corresponding value from every INSERT row. Always verify immediately after schema changes.

### 2. Root-Cause Debugging for "Column count doesn't match value count"

When a colleague reports this error:

1. Find the offending line number from the error message
2. Grep for the matching INSERT statement and identify which table
3. Compare the CREATE TABLE column count against the VALUES count for each row of that INSERT
4. If they differ, check `git log` for recent commits that touched the table's DDL — the fix likely removed (or added) a column without updating the VALUES

### 3. Robust SQL Verification (handles escaped quotes and nested parentheses)

The naive approach of splitting by commas breaks when string values contain escaped single quotes or nested parentheses (JSON, URLs, Chinese text). Use a parser that tracks SQL string context:

```python
import re

with open("init.sql") as f:
    content = f.read()

tables = {}
for m in re.finditer(r"CREATE TABLE IF NOT EXISTS `(\w+)`\s*\((.*?)\)\s*ENGINE=", content, re.DOTALL):
    tbl = m.group(1)
    cols = re.findall(r"^\s*`(\w+)`", m.group(2), re.MULTILINE)
    tables[tbl] = {"n_cols": len(cols)}

for m in re.finditer(r"INSERT IGNORE INTO `(\w+)` VALUES\s*(.*?);", content, re.DOTALL):
    tbl = m.group(1)
    if tbl not in tables:
        continue
    values_block = m.group(2)
    n_cols = tables[tbl]["n_cols"]

    # Parse each row with proper quote tracking
    rows = []
    current = ""
    depth = 0
    in_q = False
    i = 0
    while i < len(values_block):
        ch = values_block[i]
        if in_q:
            if ch == '\\' and i+1 < len(values_block):  # escaped character
                current += values_block[i:i+2]; i += 2; continue
            elif ch == "'":
                if i+1 < len(values_block) and values_block[i+1] == "'":  # '' = escaped quote
                    current += "''"; i += 2; continue
                in_q = False
            current += ch; i += 1
        else:
            if ch == "'": in_q = True; current += ch; i += 1
            elif ch == '(':
                if depth == 0: current = ""
                depth += 1; current += ch; i += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    current += ch; rows.append(current); current = ""
                else: current += ch; i += 1
            else:
                if depth > 0: current += ch
                i += 1

    for ri, row in enumerate(rows):
        v = 1; q_in = False; bd = 0; j = 0
        while j < len(row):
            c = row[j]
            if q_in:
                if c == '\\' and j+1 < len(row): j += 2; continue
                elif c == "'":
                    if j+1 < len(row) and row[j+1] == "'": j += 2; continue
                    q_in = False
                j += 1
            else:
                if c == "'": q_in = True; j += 1
                elif c in ('[', '{'): bd += 1; j += 1
                elif c in (']', '}'): bd -= 1; j += 1
                elif c == ',' and bd == 0: v += 1; j += 1
                else: j += 1
        if v != n_cols:
            print(f"[{tbl}] row {ri+1}: {v} vals vs {n_cols} cols")
```

### 4. MySQL Version Compatibility

When the seed file targets MySQL 8.0 but needs to run on MySQL 5.7:

| Issue | MySQL 8.0 | MySQL 5.7 | Fix |
|-------|-----------|-----------|-----|
| Collation | `utf8mb4_0900_ai_ci` | Not supported | Replace with `utf8mb4_general_ci` |
| bit(1)=true | `_binary '\x01'` (literal byte 0x01) | May not work | Use `b'1'` |
| bit(1)=false | `_binary '\0'` | Works but fragile | Use `b'0'` |
| datetime precision | `datetime(6)` | Supported since 5.6.4 | OK |

**Note on `_binary` introducers**: MySQL 5.7 and 8.0 treat `_binary '\\u0001'` differently. In MySQL 8.0.19+, `\u` is a Unicode escape. In MySQL 5.7, `\u` is literal 'u'. Always use `b'0'`/`b'1'` for bit(1) values — they work in all versions.

### 5. Generating a MySQL 5.7 compatible copy

Work at the byte level (not text) if the file contains literal binary bytes:

```python
with open("init_compatible.sql", "rb") as f:
    data = f.read()

data = data.replace(b"utf8mb4_0900_ai_ci", b"utf8mb4_general_ci")   # collation
data = data.replace(b"_binary '\\0'", b"b'0'")                      # bit false
data = data.replace(b"_binary '\x01'", b"b'1'")                    # bit true (literal byte)

with open("init_compatible.sql", "wb") as f:
    f.write(data)
```

### 6. Handling Multi-Megabyte Single-Line INSERTs

Some seed files contain huge text blobs (e.g. AI analysis content in policy rows) as a single-line multi-row INSERT. This can exceed the MySQL 5.7 client's line buffer on Windows (~64KB), causing `Unknown command '...'` errors.

**Fix**: Split the multi-row `INSERT INTO table VALUES (row1),(row2),...;` into individual `INSERT INTO table VALUES (row1); INSERT INTO table VALUES (row2); ...` statements. This keeps each line short.

Parse the multi-row body with the robust string-aware parser from step 3, rebuild as individual statements:

```python
rows = [...]  # from step 3 parser
new_block = "\n".join(
    f"INSERT IGNORE INTO `{table}` VALUES {row};"
    for row in rows
)
```

### 7. Verification after fix

- Run the column-count comparison script (step 3)
- Confirm `_binary` patterns are gone: `grep -c "_binary " init_compatible.sql` → 0
- Confirm collation updated: `grep -c "utf8mb4_0900" init_compatible.sql` → 0
- Verify longest line is reasonable: `awk '{print length}' init.sql | sort -rn | head -1` — should be under 64KB
- Verify parentheses balanced: all CREATE TABLE and INSERT blocks have matching `(` and `)`

## Pitfalls

- **INSERT without column list**: When `INSERT INTO table VALUES (...)` omits column names, the VALUES must match ALL columns in the exact CREATE TABLE order. Removing a column from DDL without adjusting every VALUES row causes "Column count doesn't match value count" (ERROR 1136).
- **Literal byte 0x01 in SQL files**: If the file contains literal byte 0x01 (SOH character) for bit(1) true values, text editors may corrupt it. Work at the byte level (open with `open(..., "rb")`) when editing such files.
- **Flyway vs monolithic approach**: If using a single `init.sql` (not Flyway), migration scripts become dead weight. Either use migrations OR a single seed file, not both.
- **Multiple INSERT IGNORE INTO for same table**: Some tables have multiple INSERT statements. Check ALL of them, not just the first.
- **`_binary` introducer and MySQL version**: `_binary` is valid MySQL syntax in all versions, but the content after it (especially `\u` and literal binary bytes) behaves differently across versions.
- **MySQL client line buffer**: The mysql.exe client on Windows has a ~64KB line buffer. Lines exceeding this are split at the buffer boundary, and the fragment may be misinterpreted as a client command (e.g. `Unknown command '\"'`). Always split long lines.
- **Verification parser must handle real SQL**: SQL strings can contain escaped single quotes (`\'`), doubled single quotes (`''`), and nested parentheses (URLs, JSON inside strings). The verification parser MUST track string context, not just count characters.
- **Trace through git history for root cause**: When a column-count mismatch appears, the root cause is often a recent commit that changed the DDL without updating the DML. Check `git log --oneline -- init.sql` to find the offending change.
