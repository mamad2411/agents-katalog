---
name: repo-sensitive-data-handling
description: Handles secrets, credentials, tokens, private keys, PII, logs, telemetry, test fixtures, and suspected leaks safely. Use when writing files, reviewing diffs, redacting values, or responding to exposed sensitive data.
---

# Repo Sensitive Data Handling

Use this skill whenever work touches secrets or sensitive data.

## When to Use This Skill

Use this skill when:

- writing `.env`, config, credential, certificate, key, token, or secret-like files
- reviewing logs, telemetry, traces, screenshots, fixtures, or docs
- handling API keys, database URLs, OAuth tokens, cookies, session identifiers, or private keys
- encountering suspected leaked secrets
- creating examples that need placeholders
- writing tests that involve user data or realistic credentials

## Required Behavior

- Use placeholders for secrets.
- Redact sensitive values.
- Do not copy secrets into new files.
- Do not print secrets in responses.
- Do not store production data in tests or fixtures.
- If a real secret appears to be present, stop using it and recommend rotation.

## Workflow

Use `workflows/repo-secret-leak-response-workflow.md` for suspected leaks.

## Resources

Use `resources/sensitive-data-classification.md` to classify data.

## Scripts

This skill owns:

```text
scripts/guard-secret-write.py
```

The root-level `hooks.json` file calls this script before file-write tools. Run it with `--help` before manual use.
