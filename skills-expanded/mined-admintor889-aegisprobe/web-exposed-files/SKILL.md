---
name: web-exposed-files
category: security
risk_level: high
default_permission: approval
requires_approval: true
tools:
  - security_probe
  - curl.exe
  - Select-String
outputs:
  - exposed file evidence
  - sensitive path candidates
  - reproducible request
---

# Web Exposed Files Skill

Use this skill when current evidence mentions `robots.txt`, directory listing, `/ftp`, backup files, public documents, indexes, or download endpoints.

- Treat `robots.txt` and directory indexes as routing evidence, not as permission to crawl everything.
- Confirm one candidate path at a time with `curl.exe -s -i --max-time 10 URL`.
- After confirming a directory listing, extract `href` values narrowly before guessing filenames.
- Use PowerShell filters such as `Select-String -Pattern 'href=["''][^"'']+["'']' -AllMatches | ForEach-Object { $_.Matches.Value } | Select-Object -Unique -First 40`.
- When a listing contains multiple readable document types, prioritize filenames that imply non-public business, operational, or diagnostic content such as acquisitions, incident/support, suspicious/errors, package manifests, configs, backups, exports, credentials, keys, tokens, logs, or reports. Avoid low-signal legal/readme/license files unless no better candidate exists.
- When a listing contains both readable document types and blocked/archive/binary-looking files, first confirm one high-signal readable `.md`, `.txt`, `.log`, `.json`, or `.yml` candidate to establish exposure.
- After one readable exposure is confirmed, test blocked or high-value extensions such as `.bak`, `.old`, `.zip`, `.db`, `.sqlite`, `.kdbx`, `.pem`, or `.key` one at a time.
- For binary-looking files, prefer a header or range probe before downloading a full body.
- If a server blocks a file extension, test one well-known encoding or suffix-bypass idea only when the error message suggests it.
- Record status code, content type, filename, and a short non-secret excerpt as the fact.
- Stop this branch after one confirmed sensitive file, or when only low-value public assets remain.
