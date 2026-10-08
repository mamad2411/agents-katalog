---
name: sh-kb-sqli
description: "Knowledge base for finding SQL injection (and query-language injection). Use when hunting SQLi, or when a hunter/reviewer needs sources, sinks, detection queries, payloads, false-positive filters, and remediation for injection into SQL/ORM raw queries. CWE-89, OWASP A03:2021-Injection."
---

# SQL Injection - Hunter Knowledge Base

SQLi happens when attacker-controlled input is placed into a SQL statement as **code** rather than
**data** - typically string concatenation/interpolation into a query instead of a bound parameter.

## When to hunt this
- Any code that builds SQL from variables: string concatenation, f-strings/template literals, `%`/`+`/`.format`.
- ORM "raw" escape hatches even when the ORM normally parameterizes.
- Dynamic query pieces attackers rarely expect to be bound: table/column names, `ORDER BY`, `LIMIT`,
  `IN (...)` lists, `LIKE` patterns.
- Reachability first: prioritize sinks reachable from an entry point in `codebase-map.json`.

## Sources (untrusted input)
Request params/body/query/headers/cookies, path segments, uploaded content, values from other services,
and anything from the entry-point inventory. Also "stored" sources: DB/file values that were themselves
attacker-influenced (second-order SQLi).

## Sinks by ecosystem (grep targets)
- **Python**: `cursor.execute(`, `cursor.executemany(`, `.execute(` on a DB conn; SQLAlchemy `text(`,
  `.from_statement(`, `session.execute(`, `engine.execute(`; Django `.raw(`, `.extra(`, `RawSQL(`,
  `connection.cursor()`. Danger sign: a `%`, `+`, `f"..."`, or `.format(` inside the SQL string.
- **JS/TS**: `db.query(`, `connection.query(`, `pool.query(`, `sequelize.query(`, `knex.raw(`,
  `.$queryRawUnsafe(` (Prisma), `client.query(`. Template literals with `${...}` inside SQL.
- **Java**: `Statement.execute*(`, `createStatement()` then `executeQuery(concat)`, JPA
  `createQuery`/`createNativeQuery` with string concat, MyBatis `${}` (vs safe `#{}`).
- **PHP**: `mysqli_query(`, `$pdo->query(`, `->exec(` with concatenation; `mysql_query(`.
- **Go**: `db.Query(`/`db.Exec(`/`QueryRow(` where the query string is built with `fmt.Sprintf`/`+`.
- **Ruby**: `where("... #{}")`, `find_by_sql(`, `exec_query(`, `.where(user_str)`.
- **.NET**: `SqlCommand(concat)`, `ExecuteReader` with interpolated string; EF `FromSqlRaw(`.

## Detection recipe (see references/graft-guide.md)
1. `graft grep "execute\(|\.query\(|raw\(|createNativeQuery|FromSqlRaw" --json` (or Grep).
2. For each hit, inspect the query argument: is it a bound-parameter call (safe) or string building (suspect)?
   Grep the same lines for `%|\+|\$\{|f\"|\.format\(|#\{|Sprintf|concat`.
3. `graft callers <enclosing-fn>` to reach an entry point; record the `data_flow[]` source->sink.
4. Confirm no whitelist/cast/parameterization intervenes.

## Payloads / PoC templates (curated)
- Detection: `'` , `''` , `1' OR '1'='1` , `1) OR (1=1` , `admin'--` , `" OR ""="`.
- Boolean-blind: `1 AND 1=1` vs `1 AND 1=2` (differing responses).
- Time-blind: `1; WAITFOR DELAY '0:0:5'--` (MSSQL), `1 AND SLEEP(5)` (MySQL), `1; SELECT pg_sleep(5)--` (PG).
- UNION: `1 UNION SELECT NULL,version(),NULL--` (adjust column count/types).
- Error-based: `1 AND extractvalue(1,concat(0x7e,version()))` (MySQL).
- Second-order: store `x'--` via one endpoint, trigger the vulnerable query via another.
See `references/cheatsheet.md` for per-DB detail and `ORDER BY`/`LIKE`/`IN` injection variants.

## False-positive filters (do NOT flag)
- Fully **parameterized** queries: `execute("... WHERE id = %s", [id])`, `?`/`:name` placeholders,
  Prisma `$queryRaw` tagged template (safe) vs `$queryRawUnsafe` (unsafe), MyBatis `#{}` (safe).
- The interpolated value is a **constant/enum/int-cast** the attacker cannot control, or is validated
  against an allowlist (e.g. sort column checked against a fixed set).
- ORM query builders (`.filter(User.id==id)`, `.where({id})`) that bind under the hood.
- Identifiers quoted via a proper quoting API (e.g. `psycopg2.sql.Identifier`).

## CWE / OWASP / severity
- CWE-89 (SQLi), CWE-943 (NoSQL/query injection). OWASP **A03:2021-Injection**.
- Severity: usually **critical** if unauthenticated and dumps/modifies data; **high** if authenticated
  or limited. Blind-only with narrow impact may be high/medium.

## Chaining hints
- SQLi -> read credential/secret tables -> auth bypass / account takeover.
- SQLi write -> stored XSS or config poisoning.
- SQLi -> read files (`LOAD_FILE`, `COPY ... FROM PROGRAM`) -> RCE on some DBs; -> SSRF via DB features.
- Feeds chains with `secrets`, `auth`, `access-control`.

## Mitigation (put a specific one on each finding)
Use parameterized queries / prepared statements for values; for identifiers use an allowlist or the
driver's identifier-quoting API; least-privilege DB accounts; ORM safe APIs. Never concatenate input into SQL.
