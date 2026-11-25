---
name: preflight
description: Environment health check before starting session work. Tests Keychain secrets, env files, MCP servers, GCP auth, and GitHub identity. Outputs a green/red status table.
user_invocable: true
---

# Preflight Check

Run a full environment health check before starting session work. Reads a declared-state file and verifies each entry.

## Arguments

- No arguments: full check of everything in declared-state
- `--fix`: enable auto-fix mode (confirms before each fix)
- `--quiet`: only show failures, skip green rows

## Setup

Create `~/.claude/preflight-state.json` to declare what to check. Example:

```json
{
  "keychain_keys": [
    { "service": "GEMINI_API_KEY", "label": "Gemini API Key" },
    { "service": "FIGMA_ACCESS_TOKEN", "label": "Figma Token", "expires": "2026-06-24", "warn_days_before": 30 }
  ],
  "env_files": [
    {
      "path": "~/.claude/my-project.env.local",
      "required_vars": ["API_TOKEN", "PROJECT_ID"],
      "expected_perms": "600"
    }
  ],
  "mcp_servers": [
    { "name": "slack", "type": "http", "url": "http://localhost:PORT/health" },
    { "name": "google-calendar", "type": "stdio", "command": "npx" }
  ],
  "gcp": {
    "expected_account": "you@yourdomain.com",
    "expected_project": "your-gcp-project-id"
  },
  "github": {
    "expected_user": "your-github-username",
    "expected_email": "you@yourdomain.com"
  }
}
```

If the file is missing, Claude will tell you and offer to generate a default.

## Execution Steps

### Step 0: Load Declared State

Read `~/.claude/preflight-state.json`. Parse it and extract all check categories. Initialize a results array to collect status for the final table.

### Step 1: Keychain Keys

For each entry in `keychain_keys`, run:

```bash
security find-generic-password -a "$USER" -s "SERVICE_NAME" -w >/dev/null 2>&1 && echo "OK" || echo "MISSING"
```

**Do NOT capture or display the key value.** Only check existence.

For keys with an `expires` field, calculate days until expiry from today. If within `warn_days_before`, mark as WARN with the expiry date.

Record result:
- OK: key exists in Keychain
- WARN: key exists but approaching expiry
- FAIL: key missing from Keychain

### Step 2: Env Files

For each entry in `env_files`:

1. Check file exists and has correct permissions:
```bash
[ -f FILE_PATH ] && stat -f "%Lp" FILE_PATH
```

2. Check required vars are present (existence only, never display values):
```bash
grep -q '^VAR_NAME=.\+' FILE_PATH && echo "SET" || echo "EMPTY"
```

**Never `cat`, `head`, or display env file contents.**

Auto-fix wrong permissions (if `--fix`):
```bash
chmod 600 FILE_PATH
```

### Step 3: MCP Server Connectivity

**HTTP servers**: Test with a HEAD request:
```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 5 URL
```
- 200-399: OK
- 401/403: WARN (reachable, auth issue)
- 0 or 5xx: FAIL

**stdio servers**: Check command availability:
```bash
command -v COMMAND >/dev/null 2>&1 && echo "OK" || echo "MISSING"
```

### Step 4: GCP Auth

```bash
gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null
gcloud config get-value project 2>/dev/null
```

Compare against `gcp.expected_account` and `gcp.expected_project`.

### Step 5: GitHub Identity

```bash
gh auth status 2>&1
git config --global user.email
```

Compare against `github.expected_user` and `github.expected_email`.

### Step 6: Output Status Table

```
## Preflight Results - [DATE]

| #  | Check                     | Status | Detail                          |
|----|---------------------------|--------|---------------------------------|
| 1  | Keychain: GEMINI_API_KEY  | OK     | Present                         |
| 2  | Keychain: FIGMA_TOKEN     | WARN   | Expires 2026-06-24 (84 days)   |
| 3  | Env: my-project.env.local | OK     | Exists, perms 600, vars set     |
| 4  | MCP: slack                | OK     | HTTP 200                        |
| 5  | GCP: auth                 | OK     | you@domain.com / project-id     |
| 6  | GitHub: identity          | OK     | username / you@domain.com       |
```

Status: **OK** = passed, **WARN** = caveats, **FAIL** = blocked.

Summary line:
- All OK: "Preflight complete. All N checks passed."
- Warnings: "Preflight complete. N passed, W warnings."
- Failures: "Preflight BLOCKED. F failures must be resolved before starting work."

## Rules

- Never display, echo, or log any secret values. Check existence via exit codes only.
- Never use `cat`, `head`, or `Read` on env files. Use `grep -q` only.
- Auto-fixes require user confirmation before executing.
- If a check category is missing from `preflight-state.json`, skip it silently.
