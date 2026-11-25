---
name: redact-sensitive-content
description: Review and sanitize Markdown content before it is published, shared externally, committed to a public repo, pasted into social posts, or included in blog articles and incident writeups. Use when the user asks to 脱敏, 内容审查, 检查敏感信息, 清理隐私数据, sanitize Markdown, or verify that text files do not expose personal information, internal infrastructure, secrets, or business-sensitive details.
---

# Redact Sensitive Content

## Overview

Inspect Markdown files for sensitive content, replace unnecessary identifiers with safe stand-ins, and verify that obvious leaks are gone before the content leaves a private workspace.

Use the scanner as a fast guardrail, then patch the file manually for context-aware redaction. Do not trust regex-only checks as a complete safety guarantee.

## Quick Start

1. Read `references/content-review-checklist.md`.
2. Run `scripts/scan_sensitive_content.py` on the target file or directory.
3. Patch each finding to remove or generalize private details.
4. Re-run the scanner until the remaining hits are intentional and safe.
5. If the content is going public, do one final human read focused on screenshots, examples, code blocks, stack traces, and links.

## Workflow

### 1. Decide what needs protection

- Always review:
  - personal email addresses, phone numbers, IDs, real names, usernames
  - internal IPs, internal domains, hostnames, cluster names, namespace names
  - filesystem paths with real usernames or machine structure
  - access tokens, API keys, JWTs, cookies, passwords, signed URLs
  - customer names, contract numbers, ticket links, screenshots with dashboards or internal links
- Preserve only the technical lesson. Remove everything that is not required for public understanding.

### 2. Run the scanner

From the repo root or any workspace:

```bash
python ~/.codex/skills/redact-sensitive-content/scripts/scan_sensitive_content.py path/to/file.md
python ~/.codex/skills/redact-sensitive-content/scripts/scan_sensitive_content.py docs
```

The script exits with:

- `0` when it finds nothing obvious
- `2` when it finds potential leaks

Use the findings as review targets, not as an excuse to redact blindly.

### 3. Redact with context

- Preferred replacements:
  - `someone@example.com`
  - `138****5678`
  - `10.x.x.x`
  - `internal.example.com`
  - `/path/to/project`
  - `某客户`
  - `工程师 A`
  - `***REDACTED***`
- For screenshots, crop or recreate them instead of publishing raw internal captures.
- For incident writeups, keep chronology and root cause, but remove customer identifiers and operational handles.

### 4. Re-scan and finish

- Run the scanner again after editing.
- If findings remain, decide one by one whether they are safe examples or still require redaction.
- Call out any residual risk explicitly if a realistic example must stay for technical accuracy.

## Resources

- `references/content-review-checklist.md`
  - Review rules and replacement patterns for public-safe content.
- `scripts/scan_sensitive_content.py`
  - Detect common sensitive strings in Markdown files.
