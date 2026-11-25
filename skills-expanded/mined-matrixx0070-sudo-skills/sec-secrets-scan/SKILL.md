---
name: sec-secrets-scan
version: 1.0.0
description: Scan a repository, its git history, and logs for leaked secrets and produce a credential rotation runbook.
author: matrixx0070
tags: [security, secrets, credentials, rotation, git-history, defensive]
capabilities: []
---

## When to use

Use this when onboarding a repo, after a suspected leak, before open-sourcing code, or on a recurring cadence. It detects exposed credentials so they can be revoked and rotated.

**Not for:** using found credentials to access systems; testing whether a leaked key still works against a live provider; or exfiltrating data. Detect and rotate — never authenticate with a discovered secret.

## Method

1. **Define targets.** Enumerate what to scan: working tree, full git history, CI logs, application logs, and config/env files.
2. **Pattern scan.** Search for high-entropy strings and known token shapes: AWS keys (`AKIA...`), private keys (`BEGIN ... PRIVATE KEY`), JWTs, `Bearer` tokens, DB connection strings, and `password=`/`api_key=` assignments.
3. **History sweep.** Scan committed history, not just HEAD — secrets often live in old commits. *Decision point:* deleting a file does NOT remove it from history; treat any secret ever committed as exposed and rotate it.
4. **Triage findings.** Classify each hit as true positive, test/placeholder, or false positive. Record where it is exposed and its blast radius.
5. **Rotation runbook.** For each confirmed secret: revoke the credential at the provider, issue a replacement, update the secret store, redeploy, then purge history if warranted.
6. **Prevent recurrence.** Recommend pre-commit secret scanning, `.gitignore` hardening, and a secrets manager.

## Example

You find `AWS_SECRET_ACCESS_KEY=wJalr...` in commit `a1b2c3d`, deleted three commits later but still in history. Classification: true positive, blast radius = full account. Runbook: (1) revoke the key in IAM, (2) issue a new key, (3) update it in the secrets manager, (4) redeploy consuming services, (5) verify no code references the old key, (6) purge history and force-push after team coordination.

## Pitfalls

- **Scanning HEAD only.** The most damaging leaks sit in old commits. Always sweep full history.
- **Rotating before revoking.** Issuing a new key while the old one still works leaves the leak live. Revoke first.
- **Committing test placeholders that look real.** Use obvious dummies (`AKIAEXAMPLE`) so scanners and humans can tell.
- **Purging history and calling it done.** History rewrite does not un-expose a secret others may have copied; the credential must still be rotated.

## Output format

```
## Scan scope
Targets covered: <working tree / history / logs / config>

## Findings
| Secret type | Location (file:line / commit / log) | Confidence | Blast radius |
|-------------|-------------------------------------|------------|--------------|

## Rotation runbook
Per secret: revoke → reissue → update store → redeploy → verify

## Prevention
- <tooling and policy recommendations>
```
