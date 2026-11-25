---
name: vuln-sqli
description: SQL injection validation — detect SQL injection with manual error, boolean, time-based, and union oracles; confirm DBMS and extract database version as harmless proof; automated tools require explicit destructive-risk approval and must be run with minimal flags first.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# SQL injection — structured query language injection validation

Use this skill to validate SQL injection on an authorized, in-scope target. Confirm that user-controlled input reaches a SQL query and can alter query logic using manual probing (error-based, boolean-based, time-based, UNION-based). Extract only proof-level data: database version identifier, current user, and database name. Never enumerate tables, dump rows, extract user credentials, or write files. Automated tools (sqlmap, ghauri) require explicit destructive-risk approval.

## Required inputs

- Written scope naming the target, authorized endpoints for SQL injection testing, allowed injection techniques (error, boolean, time, UNION, OOB), and explicit permission for SQL injection validation including the approved proof-extraction limit (version, user, database name only).
- Valid authorization cache. Caution risk class: SQL injection can read, modify, and delete database content. Strictly limit extraction to proof-level data only.
- Known or suspected DBMS from recon — MySQL (default `SLEEP()`, `@@version`), PostgreSQL (`pg_sleep()`, `version()`), MSSQL (`WAITFOR DELAY`, `@@version`), Oracle (`dbms_lock.sleep()`, `v$version`), SQLite (`randomblob()`, `sqlite_version()`). If unknown, test MySQL syntax first — it is the most common.
- List of candidate injection parameters from recon: `?id=`, `?product=`, `?user=`, `?search=`, `?category=`, `?page=`, `?sort=`, `?order=`, `?filter=`, JSON body fields, Cookie values, HTTP headers (`User-Agent`, `Referer`, `X-Forwarded-For`).

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when automated tools are needed.
5. `pentest_agent_execute_tool` for execution — never raw shell. Automated scanners require destructive-risk approval.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — manual probing (required first)

Before any automated tool, manually confirm at least two of three classic signals:

**Signal 1: syntax error probe**
```text
Inputs that typically break SQL syntax:
id=1'     (single quote — unbalances string literal)
id=1"     (double quote — unbalances quoted identifier)
id=1\     (backslash — escapes the next character in some DBMS)
id=1')    (close paren + quote — breaks nested function)
id=1'--   (quote + comment — may comment out remaining SQL)
```

Observe the response:
- If the response contains a SQL error message (`You have an error in your SQL syntax`, `Unclosed quotation mark`, `ODBC Driver`, `ORA-`, `PG:`) → error-based SQL injection confirmed.
- If the response is an HTTP 500 with no detail but differs from the normal response → possible blind injection.
- If the response is identical to a normal request → the input is likely sanitized or not injectable via this parameter.

**Signal 2: boolean tautology comparison**
```text
Test pairs (must return different results):
id=1 AND 1=1   (true — should return same as id=1)
id=1 AND 1=2   (false — should return different/empty)

Alternative pairs:
id=1' AND '1'='1   (true — string context)
id=1' AND '1'='2   (false — string context)
```

Procedure:
1. Request `id=1 AND 1=1` and save the response (body length, status code, content hash).
2. Request `id=1 AND 1=2` and compare.
3. If the responses differ in content length, status code, or visible output → boolean-based SQL injection confirmed.
4. If the responses are identical → the `AND 1=1`/`AND 1=2` is not being evaluated as SQL.

**Signal 3: time-based delay**
```text
MySQL:
id=1 AND SLEEP(5)-- 
id=1' AND SLEEP(5)-- 
id=1' AND IF(1=1,SLEEP(5),0)-- 

PostgreSQL:
id=1 AND pg_sleep(5)-- 
id=1' AND pg_sleep(5)-- 

MSSQL:
id=1; WAITFOR DELAY '0:0:5'-- 
id=1'; WAITFOR DELAY '0:0:5'-- 
```

Procedure:
1. Measure baseline response time (3 requests, record median).
2. Send the sleep payload and measure response time.
3. If response time increases by ≥4 seconds consistently → time-based SQL injection confirmed.
4. Vary the sleep duration (3s, 5s) to distinguish from network jitter.

### Phase 2 — DBMS identification

After confirming injection, identify the DBMS without extracting data:

- **MySQL/MariaDB**: `@@version` returns version string. `SLEEP()` is specific to MySQL.
- **PostgreSQL**: `version()` returns version string. `pg_sleep()` is specific to PostgreSQL. Stacked queries use `;`.
- **MSSQL**: `@@version` returns version string with `Microsoft SQL Server`. `WAITFOR DELAY` is specific to MSSQL.
- **Oracle**: `SELECT banner FROM v$version`. `dbms_lock.sleep()` is specific to Oracle.
- **SQLite**: `sqlite_version()` returns version. `randomblob(100000000)` can be used for time-based detection.
- **No injection**: if time delays work but no standard version function returns output → the injection may be in a NoSQL database. Switch to vuln-nosql.

Confirm the DBMS without extracting data beyond the version string. Record the DBMS type and version for the finding.

### Phase 3 — proof-level data extraction

With DBMS confirmed, extract exactly three proof data points:

1. **Database version**: `SELECT @@version` or `SELECT version()` — confirms DBMS and version.
2. **Current database user**: `SELECT user()` (MySQL), `SELECT current_user` (PostgreSQL), `SELECT SYSTEM_USER` (MSSQL) — confirms the privilege context.
3. **Current database name**: `SELECT database()` (MySQL), `SELECT current_database()` (PostgreSQL), `SELECT DB_NAME()` (MSSQL) — confirms database access.

These three data points constitute sufficient proof of a SQL injection vulnerability. Never extract:
- Table names, column names, or schema structure.
- Row data, user records, password hashes, or PII.
- File contents via `LOAD_FILE()` or `COPY ... TO PROGRAM`.

### Phase 4 — UNION-based injection (when applicable)

When the injection point is in a SELECT statement and output is reflected in the response:

1. Determine the number of columns using `ORDER BY N` (increment N until error) or `UNION SELECT NULL,NULL,...`.
2. Once column count is known, replace NULLs with version/user/database calls: `UNION SELECT 1,@@version,database(),4`.
3. If the version string appears in the response → UNION-based SQL injection confirmed.

UNION-based injection should be used only to retrieve the three proof data points. Do not enumerate the schema.

### Phase 5 — automated tool usage (requires approval)

Automated SQL injection tools (sqlmap, ghauri) must not be used without explicit destructive-risk approval because:

- They can generate hundreds to thousands of requests and may disrupt the target.
- Default flags attempt schema enumeration, data dumping, and file-system access.
- They may trigger WAF blocks, IDS alerts, or rate limiting that affects production users.

When approved, run with minimal flags:
```text
sqlmap -u "URL" --batch --level=1 --risk=1 --technique=B (boolean only)
sqlmap -u "URL" --batch --level=1 --risk=1 --banner (version only)
```

If sqlmap confirms injection with `--banner`, stop. Do not escalate to `--dbs`, `--tables`, `--dump`, `--os-shell`, or `--file-read` without separate explicit maintainer approval.

### Phase 6 — false-positive checks

SQL injection detection has nuanced false positives:

- **Application-level error handling**: some frameworks catch SQL errors and return a generic 500 page. The error-based signal may be missed even though injection is present.
- **WAF/IDS interference**: a WAF may block `' OR 1=1` but pass `' AND SLEEP(5)`. Test multiple techniques.
- **Query context mismatch**: integer context (`id=1`) vs string context (`name=admin`). Use the correct quote style for each parameter.
- **Cached responses**: CDN/proxy caching may return the same response regardless of payload. Add cache-busting parameters or use POST instead of GET.
- **Rate limiting**: if the endpoint rate-limits after 3-5 requests, time-based detection becomes unreliable. Use boolean differential instead.

## Decision points

- **Stop at two confirmed signals**: if error-based AND boolean differential both work → SQLi confirmed. Time-based is supplementary.
- **Stop after extracting version, user, database name**: this is sufficient proof. Do not enumerate further.
- **WAF bypass is not required for a finding**: if the injection works without a WAF, that is sufficient. Bypass techniques are only needed if the target blocks basic probes.
- **Stacked queries are higher severity**: if `; DROP TABLE` or `; INSERT` is possible, the impact includes data modification. Document but do not test destructive statements.

## Prohibited behavior

- Extracting table names, column names, row data, user records, password hashes, PII, or any production data.
- Using `INTO OUTFILE`, `INTO DUMPFILE`, `COPY ... TO`, or `xp_cmdshell` to write files, execute commands, or establish persistence.
- Modifying data via `INSERT`, `UPDATE`, `DELETE`, `DROP`, `TRUNCATE`, or `ALTER`.
- Running sqlmap or ghauri with `--dump`, `--dump-all`, `--tables`, `--columns`, `--os-shell`, `--os-cmd`, or `--file-read` without separate explicit approval.
- Using OOB (out-of-band) exfiltration to send data to attacker-controlled servers. OOB can be used for detection only (DNS/HTTP callback with no data).
- Attempting authentication bypass via SQL injection on production login forms during business hours without explicit coordination.

## Stop conditions

- Error-based signal confirmed (SQL error in response) → SQLi confirmed, proceed to identify DBMS.
- Boolean differential confirmed (different responses for true/false conditions) → SQLi confirmed, proceed to identify DBMS.
- Time delay ≥4 seconds consistently → SQLi confirmed, proceed to identify DBMS.
- DBMS identified and proof data (version, user, database) extracted → sufficient evidence, stop.
- All manual probes return identical results → negative for this parameter. Move to next.
- WAF consistently blocks probes with 403 → parameter is protected, document.

## Evidence — SQL injection matrix

For each tested parameter, record:

```text
Parameter: <name> | endpoint: <URL> | method: <GET | POST | Cookie | Header>
DBMS: <MySQL 8.0 | PostgreSQL 14 | MSSQL 2019 | Oracle 19c | SQLite | unknown>
Error-based: <SQL error in response | no error | blocked>
Boolean-based: <true/false differential | no differential>
Time-based: <delay: N seconds | no delay>
UNION-based: <columns: N | version reflected | not applicable>
Proof extracted: <@@version: X.Y.Z | user(): name@host | database(): name>
Automated tool used: <none | sqlmap --banner | ghauri --confirm>
Impact: <none | SQL injection confirmed | stacked-query possible>
Confidence: <confirmed | likely | needs-review>
```

Aggregate into a parameter × technique matrix. Never store: extracted data beyond version/user/database, sqlmap output with schema enumeration, database error messages with internal IPs or file paths, or the raw SQL payloads with version extraction.

## Report handoff

When a finding is confirmed:
1. `pentest_agent_record_finding` with affected parameter, injection type, DBMS, CVSS estimate (7.5–8.5 for read-only SQLi, 8.5–9.5 for read-write, 9.5–10.0 for command execution via SQLi), and remediation guidance.
2. Reference the SQL injection matrix.
3. Recommend: use parameterized queries (prepared statements) for all database access, never concatenate user input into SQL strings, use an ORM with safe defaults, apply least-privilege database user, validate and sanitize input types (integers, enumerated values), run SQL injection tests in CI with sqlmap or equivalent, and enable database activity monitoring to detect injection attempts.
