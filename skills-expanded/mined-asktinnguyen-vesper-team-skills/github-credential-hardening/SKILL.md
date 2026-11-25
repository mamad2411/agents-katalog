---
name: github-credential-hardening
description: This skill should be used when auditing or fixing potential GitHub credential leakage in codebases, especially around repo URLs, OAuth tokens, subprocess environment handling, IPC boundaries, and logs.
version: 1.0.0
---

# Github Credential Hardening

## Overview

Detect and remediate GitHub credential leakage paths in application code and configuration.
Use this skill when reviewing security around GitHub integration, MCP subprocesses, OAuth flows, and logging.

## When To Trigger

Use this skill when users ask to:
- "check for credential leakage"
- "audit GitHub token handling"
- "secure OAuth token flow"
- "sanitize repo URL handling"

Also trigger after code changes that touch:
- GitHub repo URL input or persistence
- subprocess `spawn`/`exec` environment maps
- IPC payloads crossing trust boundaries
- error logs containing request/response text

## Workflow

### Step 1: Build Threat Surface Map

1. Locate GitHub entry points: settings forms, OAuth handlers, token storage, API clients.
2. Locate trust boundaries: main-to-renderer IPC, parent-to-child process env, persisted config and logs.
3. Note every code path where user-controlled text or secrets can cross these boundaries.

### Step 2: Run Focused Static Scan

Run the bundled scan helper:

```bash
bash .claude/skills/github-credential-hardening/scripts/scan_github_credential_risks.sh .
```

Treat results as candidates. Confirm each hit manually before patching.

### Step 3: Confirm Real Leaks

For each candidate:
1. Confirm source: user-controlled input or secret-bearing field.
2. Confirm sink: persisted config, logs, IPC payload, or child process environment.
3. Assign severity:
- `high`: direct token exposure or broad secret propagation
- `medium`: possible leak with constrained preconditions
- `low`: noisy pattern without practical exfiltration

### Step 4: Apply Remediation Patterns

1. Sanitize GitHub URLs before save/log:

```ts
const sanitizedRepoUrl = stripCredentialsFromGitHubUrl(repoUrl)
save({ teamSkillsRepoUrl: sanitizedRepoUrl })
logger.info("Team skills config saved", { repo: redactRepoUrl(sanitizedRepoUrl) })
```

2. Filter env before subprocess spawn:

```ts
const safeEnv = { ...filterSensitiveEnv(process.env), ...explicitEnv }
spawn(command, args, { env: safeEnv })
```

3. Keep tokens in privileged process only:

```ts
// Return status metadata only. Do not return accessToken to renderer.
return { ok: true, account: user.login }
```

4. Redact token-like strings before logging:

```ts
logger.error("GitHub request failed", { error: redactSecrets(errText) })
```

### Step 5: Add Regression Coverage

Add tests for:
- credential stripping from GitHub URLs
- subprocess env filtering parity across runtime and validation paths
- IPC responses that must not include token fields
- log redaction for token formats like `ghp_`, `github_pat_`, and bearer/token headers

### Step 6: Record Outcome

Document non-trivial findings under `docs/solutions/security-issues/`.
Add or update references in `references/case-studies.md` to keep this skill's knowledge current.

## Resources

- Scan helper: `scripts/scan_github_credential_risks.sh`
- Seed case study: `references/case-studies.md`
