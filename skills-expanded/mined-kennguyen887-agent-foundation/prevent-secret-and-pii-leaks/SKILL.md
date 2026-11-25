---
name: prevent-secret-and-pii-leaks
description: Use BEFORE committing to a public/shared repo, pushing, publishing a package, or syncing/exporting code, config, docs, or skills to an open-source or external destination — to avoid leaking secrets, PII, or internal identifiers. Also the remediation playbook if something already leaked (untrack → rewrite history → force-push → forks/cache → support → rotate). Prevention >> remediation: you can't fully un-publish.
metadata:
  last-updated: 2026-06-22
  author: Ken Nguyễn <ntnpro@gmail.com>
---

## When to use

About to `git push` to a public or shared repo, open-source something, publish a package, or run an **export/sync/vendor** step that copies your local content into a public destination. Also: reviewing a diff before it goes out, or cleaning up after a leak.

## Reason about THREE classes, not just "secrets"

Be precise — they differ in severity and remediation:

1. **Credentials / secrets** — API keys, tokens, passwords, private keys, connection strings, `.env` values. **Highest.** If exposed → **rotate immediately** (assume compromised), then scrub.
2. **PII** — emails, real names, usernames, teammate handles, customer data. Can't be "rotated"; once public, treat as disclosed.
3. **Internal identifiers** — cloud account IDs, internal hostnames/URLs, IAM user names, resource/cluster/ARN/bucket names, private org or project codenames, ticket IDs. **Info-disclosure, not credentials** — don't call these "secrets," but keep them out of public/OSS too.

All three must stay out of a public/shared destination; only the severity and fix differ.

## Before you publish (prevention — this is where the win is)

1. **Confirm the destination's visibility first.** Public vs private — check, never assume (`gh repo view --json visibility`). "It's probably private" has caused real leaks.
2. **Scan the EXACT bytes being published, not just the obvious files.** Include config, fixtures, lockfiles, CI files, and the **tooling itself**. → *The sanitizer-isn't-sanitized trap:* an export/sync script that scrubs identifiers often **hard-codes those very identifiers in its own config** (the scrub list = a list of your real emails/orgs/usernames/handles). Keep such local-only tooling **gitignored**, never vendored.
3. **Publish OUTPUT, not source/tooling.** Vendor only sanitized, generic content; replace every real identifier with a placeholder (`<account-id>`, `my-service`, `example.com`, `your-org`). Docs/skills: principle-first, no org/customer names, no real infra identifiers.
4. **Make the pipeline fail-closed.** A publish/export step should run a secret+PII scan and **exit non-zero if anything survives** — don't rely on eyeballing the diff. Add a pre-commit/pre-push hook for the same.
5. **Default-deny for shared (public/partner) destinations.** When unsure whether something is safe to publish, leave it out and ask.

## If it already leaked (remediation)

Order matters; do not skip rotation for credentials.

1. **Credentials → ROTATE NOW**, before anything else. Scrubbing history does not un-leak a key that bots may have already scraped.
2. **Stop the bleeding:** `gitignore` + `git rm --cached <file>` (untrack). **This does NOT remove it from history** — past commits still contain it.
3. **Rewrite history:** back up first (`git bundle create backup.bundle --all`), then remove the file/secret from every commit — `git filter-repo --path <file> --invert-paths` (preferred), or `git filter-branch --index-filter 'git rm --cached --ignore-unmatch <file>' -- <branch>` if filter-repo isn't installed.
4. **Force-push** the rewritten history (destructive — rewrites SHAs, breaks clones; have the backup): `git push --force-with-lease`.
5. **Residuals you can't reach by force-push:**
   - **Forks** keep the old history independently (`gh repo view --json forkCount`; `gh api repos/<o>/<r>/forks`). You can't rewrite someone else's fork.
   - **Platform caches** keep old commits reachable by SHA for a while.
   - → For both, the lever is **GitHub Support** ("remove sensitive data"): they purge cached views and remove the data across the fork network.
6. **Triage by class:** credentials = rotated (step 1); PII / internal identifiers = can't rotate → scrubbed + treated as disclosed.

## Mindset

You can never fully un-publish — history, forks, caches, and scrapers persist. So the budget belongs in **prevention**: verify visibility, scan the exact published bytes (including the tooling that handles secrets), placeholder everything, and fail closed.
