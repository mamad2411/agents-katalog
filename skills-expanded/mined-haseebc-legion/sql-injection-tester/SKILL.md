name: sql_injection_testing
description: Detect and probe for SQL injection in a URL parameter or POST body for bug bounty, pentest engagements, or CTFs. Use when the user asks to test for SQLi, check a parameter for SQL injection, find injectable fields, or discover UNION column counts. Not for unauthorized targets.

# SQL Injection Testing

> All payloads here are detection-only — no destructive (DROP/DELETE/UPDATE/INSERT) statements.

## Inputs
- A target URL containing the literal placeholder `FUZZ` where the injectable parameter value goes, e.g. `https://target.tld/product?id=FUZZ`.
- Or a POST body via `-d` with `FUZZ` in it.
- No live target required to read this skill — but the probe script does make real HTTP requests when run.

## Workflow

### Phase 1: Recon
Identify user-controllable parameters (URL query params, form fields, JSON body keys, headers like `X-Forwarded-For`). Note which look like they touch a database (`id`, `category`, `search`, `sort`, `filter`, `user`).

### Phase 2: Detection — run the probe script
```bash
scripts/sqli_probe.sh -u "https://target.tld/filter?category=FUZZ"
```
This sends a baseline request, then a battery of error-based, boolean-based, and time-based payloads, and a report of status/size/timing per payload, flagging:
- `[status-diff]` — HTTP status changed vs. baseline
- `[size-diff:Nb]` — response body length changed >15%
- `[ERROR-SIGNATURE:...]` — a DB error string appeared (MySQL/Postgres/SQLite/Oracle/MSSQL)
- `[POSSIBLE TIME-BASED SQLI]` — response took ≥80% of the injected `SLEEP()`/`WAITFOR DELAY` duration

For POST bodies: `scripts/sqli_probe.sh -u "https://target.tld/login" -d "user=admin&pass=FUZZ"`

Add auth/session context as needed: `-H "Authorization: Bearer ..."`, `-b "session=..."`.

### Phase 3: Column-count discovery (once injection is confirmed)
```bash
scripts/sqli_probe.sh -u "https://target.tld/filter?category=FUZZ" --union 15
```
Sends `' UNION SELECT NULL --`, `' UNION SELECT NULL,NULL --`, etc., incrementing until no error signature appears — that column count matches the original query's `SELECT`.

### Phase 4: Manual exploitation (not automated by this skill)
Once the column count is known, hand-craft UNION payloads to pull data, replacing a `NULL` at a time with a real expression, e.g.:
```
' UNION SELECT NULL,version(),NULL,NULL --
' UNION SELECT NULL,table_name,NULL,NULL FROM information_schema.tables --
' UNION SELECT NULL,column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users' --
```
This step is deliberately manual/interactive — see `references/payloads.md` for the reference payload set and DB-specific syntax. Stop at proof-of-concept (e.g. dumping `version()` or one row of a non-sensitive table) rather than bulk-exfiltrating data unless the engagement scope explicitly calls for it.

## Reference
`references/payloads.md` has the full payload catalogue: comment-syntax by DB engine, boolean/error/time/union payloads, and common WAF-bypass encodings.

## Notes / tips
- **NULL is safe** as a UNION placeholder — no type mismatch, doesn't reference real data.
- **Comment syntax varies by engine:** `--` (needs a trailing space in MySQL, or use `-- -`), `#` (MySQL only), `/* */` (MySQL/Postgres/Oracle).
- **Error-driven testing:** error messages reveal DB engine and sometimes schema — that's real signal even without confirmed exploitation.
- **Suppressed errors ≠ not injectable:** if error-based detection is silent, still run the boolean-based (`AND 1=1` vs `AND 1=2`) and time-based checks — many production apps hide DB errors but are still vulnerable.
- **False positives are common** with automated heuristics (WAFs, rate limiting, CDN caching can all produce size/timing diffs). Manually verify any flagged payload before reporting it as a finding.
- **Prevention** (for writeups/reports): parameterized queries / prepared statements, input validation/allowlisting, least-privilege DB accounts, ORM usage, WAF as defense-in-depth, and suppressing detailed DB errors in production.

Source: "SQL injection" methodology writeup (nexusphere, Medium).
