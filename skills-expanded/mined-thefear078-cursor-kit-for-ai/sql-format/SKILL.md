---
name: sql-format
description: Prettify, format, validate, and lint SQL queries. Use when cleaning up messy queries, reviewing migrations, standardizing team SQL style, or debugging syntax errors.
---

# SQL Format & Lint

Prettify, validate, and standardize SQL with consistent style. **Parse before format** — report syntax errors with line context. Never execute SQL against production without explicit user request.

## When to Use This Skill

| Trigger | Example request |
|---------|-----------------|
| Readability | "Format this nested SELECT" |
| Syntax check | "Why does this query fail to parse?" |
| Style standardization | "Apply 2-space indent, uppercase keywords" |
| Migration review | "Lint this CREATE TABLE statement" |
| Dialect conversion | "Convert MySQL LIMIT to PostgreSQL" |

## Phase Checklist

```
[ ] 1. Identify SQL dialect (PostgreSQL, MySQL, SQLite, SQL Server, etc.)
[ ] 2. Parse query — report syntax errors with line/column
[ ] 3. Apply formatting rules (indent, keywords, commas)
[ ] 4. Lint for common issues (SELECT *, missing WHERE on UPDATE)
[ ] 5. Present formatted output with change summary
[ ] 6. Never execute against live DB unless explicitly requested
```

---

## Supported Dialects

| Dialect | Parser tool | Notes |
|---------|-------------|-------|
| PostgreSQL | `pg_format`, `sqlfluff` | Default if unspecified |
| MySQL / MariaDB | `sqlfluff --dialect mysql` | Backtick identifiers |
| SQLite | `sqlfluff --dialect sqlite` | Limited ALTER support |
| SQL Server (T-SQL) | `sqlfluff --dialect tsql` | Bracket identifiers |
| Standard SQL | Generic formatting rules | May miss dialect specifics |
| BigQuery | `sqlfluff --dialect bigquery` | Backtick tables, STRUCT |

**Always ask or infer dialect** — formatting and lint rules differ significantly.

---

## Formatting with sqlfluff

```bash
# Install
pip install sqlfluff -q

# Format file (PostgreSQL dialect)
sqlfluff format query.sql --dialect postgres

# Lint with rules
sqlfluff lint query.sql --dialect postgres

# Fix auto-fixable issues
sqlfluff fix query.sql --dialect postgres

# Parse only (syntax check)
sqlfluff parse query.sql --dialect postgres
```

### Common sqlfluff Rules

| Rule | Description |
|------|-------------|
| L003 | Indentation consistent |
| L016 | Long lines wrapped |
| L031 | Avoid table aliases in GROUP BY |
| L034 | Wildcard then simple targets in SELECT |
| L042 | JOIN/WHERE subqueries require alias |
| L044 | Lowercase keywords (configurable) |
| L047 | Missing DISTINCT with COUNT |

---

## Formatting with pg_format (PostgreSQL)

```bash
# Install (Debian/Ubuntu)
# apt install pgformatter

# Format query
echo "SELECT a,b FROM t WHERE x=1" | pg_format -

# Options
pg_format --keyword-case 2 --spaces 2 query.sql
# --keyword-case 1=unchanged, 2=uppercase, 3=lowercase
# --spaces 2=indent width
```

---

## Python Formatting (sqlparse)

```bash
pip install sqlparse -q
```

```python
import sqlparse

sql = "SELECT id,name,email FROM users WHERE active=1 ORDER BY created_at DESC"
formatted = sqlparse.format(
    sql,
    reindent=True,
    keyword_case="upper",
    indent_width=2,
    comma_first=False,
)
print(formatted)
```

```python
# Split multiple statements
import sqlparse
statements = sqlparse.split(open("migration.sql").read())
for i, stmt in enumerate(statements, 1):
    print(f"-- Statement {i}")
    print(sqlparse.format(stmt, reindent=True, keyword_case="upper"))
```

---

## Style Guide (Default)

| Element | Convention |
|---------|------------|
| Keywords | UPPERCASE (`SELECT`, `FROM`, `WHERE`) |
| Identifiers | lowercase_snake (`user_id`, `created_at`) |
| Indent | 2 spaces per level |
| Commas | Trailing comma in multiline lists |
| Line length | Wrap at 100 chars |
| Strings | Single quotes `'value'` |
| Aliases | Explicit `AS` keyword |

### Before / After Example

```sql
-- Before (minified)
select u.id,u.name,o.total from users u join orders o on u.id=o.user_id where o.status='completed' order by o.total desc limit 10

-- After (formatted)
SELECT
  u.id,
  u.name,
  o.total
FROM users AS u
INNER JOIN orders AS o
  ON u.id = o.user_id
WHERE
  o.status = 'completed'
ORDER BY
  o.total DESC
LIMIT 10;
```

---

## Lint Checks (Manual Rubric)

| Severity | Check | Message |
|----------|-------|---------|
| Error | Unbalanced parentheses | Missing closing `)` |
| Error | Missing semicolon (multi-stmt) | Statement boundary unclear |
| Warning | `SELECT *` in production query | Specify columns explicitly |
| Warning | UPDATE/DELETE without WHERE | Risk of full-table modification |
| Warning | Implicit cross join | Missing JOIN condition |
| Warning | Non-sargable predicate | `WHERE YEAR(date) = 2024` → range |
| Info | VARCHAR without length | Specify max length |
| Info | Missing index hint on FK | Consider index on foreign key column |

```python
import re

def basic_sql_lint(sql: str) -> list[dict]:
    issues = []
    upper = sql.upper()

    if re.search(r"\bSELECT\s+\*", upper):
        issues.append({"severity": "warning", "rule": "no-select-star",
                        "message": "SELECT * — specify columns explicitly"})

    if re.search(r"\b(DELETE|UPDATE)\b", upper) and not re.search(r"\bWHERE\b", upper):
        issues.append({"severity": "warning", "rule": "dml-needs-where",
                        "message": "UPDATE/DELETE without WHERE clause"})

    if upper.count("(") != upper.count(")"):
        issues.append({"severity": "error", "rule": "unbalanced-parens",
                        "message": "Unbalanced parentheses"})

    return issues

sql = "DELETE FROM sessions"
for issue in basic_sql_lint(sql):
    print(f"[{issue['severity']}] {issue['rule']}: {issue['message']}")
```

---

## Dialect-Specific Notes

### PostgreSQL

```sql
-- Array syntax
SELECT tags[1] FROM posts;

-- JSON operators
SELECT data->>'name' FROM users;

-- RETURNING clause
INSERT INTO logs (msg) VALUES ('done') RETURNING id;

-- ILIKE for case-insensitive
SELECT * FROM users WHERE email ILIKE '%@example.com';
```

### MySQL

```sql
-- Backtick identifiers
SELECT `order`, `group` FROM `table`;

-- LIMIT offset
SELECT * FROM t LIMIT 10 OFFSET 20;

-- ON DUPLICATE KEY UPDATE
INSERT INTO t (id, v) VALUES (1, 'a') ON DUPLICATE KEY UPDATE v = 'a';
```

### SQLite

```sql
-- Limited ALTER TABLE
-- Use table rebuild pattern for column changes

-- AUTOINCREMENT
INTEGER PRIMARY KEY AUTOINCREMENT

-- Date functions
SELECT date('now'), datetime('now');
```

---

## Parameter Placeholder Conventions

| Dialect | Placeholder | Example |
|---------|-------------|---------|
| PostgreSQL (psycopg2) | `%s` or `%(name)s` | `WHERE id = %s` |
| PostgreSQL (asyncpg) | `$1, $2` | `WHERE id = $1` |
| MySQL (mysqlclient) | `%s` | `WHERE id = %s` |
| SQLite | `?` | `WHERE id = ?` |
| SQLAlchemy | `:name` | `WHERE id = :id` |

When formatting parameterized queries, preserve placeholders exactly — do not quote or modify them.

---

## Worked Examples

### Example 1: CTE formatting

```sql
-- Input
WITH active_users AS (SELECT id,name FROM users WHERE active=true)
SELECT au.name,count(o.id) FROM active_users au LEFT JOIN orders o ON au.id=o.user_id GROUP BY au.name

-- Output
WITH active_users AS (
  SELECT
    id,
    name
  FROM users
  WHERE active = TRUE
)
SELECT
  au.name,
  COUNT(o.id)
FROM active_users AS au
LEFT JOIN orders AS o
  ON au.id = o.user_id
GROUP BY
  au.name;
```

### Example 2: Lint catches dangerous DELETE

```
Query:  DELETE FROM audit_log
Lint:   [warning] dml-needs-where: UPDATE/DELETE without WHERE clause
Action: Add WHERE created_at < '2023-01-01' or confirm intentional truncate
```

### Example 3: Escape string literals

```
Input:  WHERE name = 'O'Brien'
Fix:    WHERE name = 'O''Brien'  (double single-quotes)
See:    encode-decode for general escaping patterns
```

---

## Output Template

```markdown
## SQL Format: {dialect}

| Property | Value |
|----------|-------|
| Dialect | PostgreSQL |
| Statements | 1 |
| Syntax | ✓ valid |
| Lint warnings | 2 |

### Formatted SQL
```sql
{formatted_query}
```

### Lint Results
| Severity | Rule | Message |
|----------|------|---------|
| warning | no-select-star | SELECT * in line 3 |
| info | line-length | Line 12 exceeds 100 chars (wrapped) |

### Changes Applied
- Keywords uppercased
- 2-space indent applied
- JOIN conditions aligned
- Trailing commas added
```

---

## Anti-Patterns

- Formatting SQL without knowing the dialect
- Executing lint/fix against production database
- Quoting parameter placeholders during format
- `SELECT *` in production API queries without justification
- Uppercase table names inconsistently mixed with lowercase
- Removing comments during format (preserve all comments)
- Auto-fixing migrations without user review

---

## Cross-References

| Related need | Skill |
|--------------|-------|
| String escaping in SQL literals | `encode-decode` |
| JSON in SQL → format JSON separately | `format-convert` |
| Cron expressions in SQL scheduled jobs | `cron-builder` |
| Text diff of two query versions | `text-utils` |
| CSV import → SQL INSERT generation | `format-convert` |
| Hash comparison in SQL context | `hash-crypto` |
