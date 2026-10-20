---
name: secret-lifecycle-auditor
description: "Secret lifecycle auditor: inventories every secret-shaped key/value across .env, k8s manifests, Vault configs, IAM refs, terraform. Per secret: age from git log -S, masked value (first-8/last-4), reachability-check against installed dependencies, type guess from key prefix. LLM judges rotation cadence and emits prioritized rotate-now / rotate-soon / remove-dead list. Read-only. Audience: Senior. Trigger: /secret-lifecycle"
trigger: /secret-lifecycle
---

## What this is for

Trufflehog/Gitleaks (and our `security-scan`) find the EXISTENCE of
hardcoded secrets. They do not answer: is the secret still active, who
owns it, is there a rotation policy, is the documented rotation overdue,
has the secret been expired-but-not-revoked. This skill inventories every
secret reference, reconciles them via git age and dependency reachability,
and the LLM judges each one's lifecycle health.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## ## What You Must Do When Invoked

### Step 1

1. If `-help` is passed, print the `## Usage` block below and stop.

### Step 2

2. Confirm `-ProjectDir` is provided and the path exists.

### Step 3

3. Run: `scripts/secret-census.ps1 -ProjectDir "<path>"`

### Step 4

4. LLM reads the JSON output. For each secret:

### Step 5

- Identify likely owner (last author of relevant file, via git).

### Step 6

- Classify by type (api-key, db-password, jwt, admin, hmac-secret).

### Step 7

- Recommend rotation cadence (API 90d, DB 60d, admin 30d, JWT 30d, HMAC per usage).

### Step 8

- Flag dead: no dependency reaches this secret (check

### Step 9

`referencedByDeps` plus manual grep).

### Step 10

- Flag stale: `ageDays > 180` AND in active use.

### Step 11

5. Write `secret-lifecycle-report.md` to the working directory.

## Usage

```
/secret-lifecycle                          # interactive
/secret-lifecycle <dir>                    # scan project
/secret-lifecycle <dir> -SecretFilePatterns ".env,*.tf"
/secret-lifecycle -help                    # show usage
```

Returns JSON with `secrets[]`:
`{key, file, line, maskedValue, length, firstCommit, firstSubject,
ageDays, serviceGuess, referencedByDeps}` plus summary counts.
