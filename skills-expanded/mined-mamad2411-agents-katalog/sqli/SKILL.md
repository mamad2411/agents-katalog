---
name: sqli
description: "Detect SQL injection where user input reaches SQL query construction through string concatenation, template literals, or ORM raw query methods."
metadata:
  filePattern:
    - "**/*.js"
    - "**/*.ts"
    - "**/*.py"
    - "**/*.go"
    - "**/*.rb"
    - "**/*.php"
  bashPattern:
    - "semgrep.*sqli"
    - "grep.*(query|execute|raw|cursor)"
  priority: 85
---

# SQL Injection Detection

## When to Use

Audit database-backed applications, ORM wrappers, query builders, and any code that constructs SQL queries from user input.

## Process

### Step 1: Find SQL Query Construction

```
# JavaScript
grep -rn "query(\|execute(\|\.raw(\|\.rawQuery(" .
grep -rn "knex\.raw\|sequelize\.query\|prisma\.\$queryRaw" .

# Python
grep -rn "cursor\.execute\|execute(\|executemany(" .
grep -rn "\.raw(\|RawSQL\|text(" .
grep -rn "f\".*SELECT\|f\".*INSERT\|f\".*UPDATE\|f\".*DELETE" .

# Go
grep -rn "db\.Query\|db\.Exec\|db\.QueryRow\|tx\.Query" .
grep -rn "fmt\.Sprintf.*SELECT\|fmt\.Sprintf.*INSERT" .

# Ruby
grep -rn "find_by_sql\|execute\|select_all\|where.*#\{" .

# PHP
grep -rn "query(\|prepare(\|exec(\|mysql_query\|mysqli_query" .
```

### Step 2: Check for String Concatenation/Interpolation

```
# Template literals in SQL
grep -rn "query.*\`.*\$\{" . --include="*.js" --include="*.ts"

# String concatenation in SQL
grep -rn "SELECT.*\+\|INSERT.*\+\|UPDATE.*\+\|DELETE.*\+" .

# Python f-strings in SQL
grep -rn 'f".*SELECT\|f".*INSERT\|f".*UPDATE\|f".*DELETE' .

# Format strings in SQL
grep -rn "\.format(.*SELECT\|\.format(.*INSERT" .
```

### Step 3: Check for Parameterized Queries

Parameterized queries are SAFE:
```js
// SAFE: parameterized
db.query('SELECT * FROM users WHERE id = ?', [userId]);

// UNSAFE: string concatenation
db.query('SELECT * FROM users WHERE id = ' + userId);
```

### Step 4: Check ORM Raw Methods

ORMs are generally safe, but `.raw()` / `.query()` methods often bypass protections:
```js
// SAFE: ORM query builder
User.findOne({ where: { id: userId } });

// UNSAFE: raw query with interpolation
sequelize.query(`SELECT * FROM users WHERE id = ${userId}`);
```

### Step 5: Check Non-Parameterizable Locations

Some SQL elements CANNOT be parameterized:
- ORDER BY column names
- Table names
- Column names in SELECT
- LIMIT/OFFSET (in some databases)

If user input reaches these, it is SQLi even with prepared statements.

## CVSS Guidance

- Data exfiltration (UNION/blind): HIGH 8.1-8.8
- Data modification: HIGH 8.1
- Unauthenticated with admin data access: CRITICAL 9.8
- Authenticated: HIGH 8.8
- ORDER BY injection (limited): MEDIUM 5.3

## References

- [Sinks](references/sinks.md) -- SQL query sinks by language
- [False Positive Indicators](references/false-positive-indicators.md)
- [PoC Skeleton](references/poc-skeleton.md)
