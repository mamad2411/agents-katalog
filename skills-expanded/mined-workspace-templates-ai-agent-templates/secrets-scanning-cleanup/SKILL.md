---
name: secrets-scanning-cleanup
description: Finds API keys and passwords committed to a repository, plans their rotation, removes them from history and adds a check against repeats.
---

# Secrets scanning cleanup

Treat every secret you find as already compromised. Rotation comes before cleanup.

## Steps

1. Scan the working tree and history. Use gitleaks or trufflehog if installed (`gitleaks detect --redact`); otherwise search with patterns for `AKIA`, `ghp_`, `sk_live_`, private key headers, and assignments like `password=` in config files.
2. Triage each hit: real credential, test value, or example. Record file, commit, and the service it belongs to. Mask values to the first four characters in every message you write.
3. Produce a rotation list for the user: which provider console, which key, what depends on it. Do not rotate anything yourself. Wait for confirmation that each key is revoked.
4. Move the value out of code: read it from an environment variable or secret manager, add the file to `.gitignore`, and commit a `.env.example` with empty names.
5. Only after rotation, offer a history rewrite with `git filter-repo --replace-text`. Explain it changes commit hashes and forces every collaborator to re-clone. Ask before running it, and never force-push without a yes.
6. Prevent repeats: add a gitleaks pre-commit hook and a CI step that fails on new findings.

## Rules

- Never paste a full secret into chat, logs or a commit message.
- Deleting the file in a new commit is not a fix.
- Check for the same secret in CI variables, Docker images and build logs.

## Report

Findings table (masked), rotation checklist with status, what changed in the repo, and the guard added.
