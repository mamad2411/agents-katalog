---
name: env-example-creation
description: 'Generate a sanitized .env.example file from an existing .env by replacing sensitive values (credentials, org-specific hosts, internal paths) with canonical placeholders. Use when onboarding a developer, publishing a repo, or documenting required env vars without leaking secrets.'
category: DevOps & Environment
---

# Env Example Creation Skill

Create a `.env.example` file from an existing `.env` file by replacing
sensitive values (passwords, API keys, internal hostnames, absolute paths)
with canonical placeholders per the
[redaction-portability](../redaction-portability/SKILL.md) skill.

The result is a safe-to-commit template that documents every required
environment variable without leaking credentials or internal topology.

## When to Use

- Onboarding a new developer who needs to know which env vars are required
- Preparing a project for open-source or cross-team publication
- A `.env.example` is missing or outdated after adding new env vars
- You just fetched a `.env` from staging and need to create a clean template

## Environment & Dependencies

- **No runtime dependencies**. This is a judgement-guided workflow, not a
  deterministic script. The agent classifies each value using contextual
  knowledge and the redaction-portability tier model.

## Procedure

### Step 1 — Locate the `.env` File

Find the project's `.env` file. Common locations:

```text
<repo-root>/.env
<repo-root>/<frontend-app>/.env
<repo-root>/<backend-app>/.env
```

If multiple `.env` files exist (frontend + backend), process each one
separately — create a `.env.example` for each.

### Step 2 — Read the Existing `.env`

Read the full `.env` file. Note:

- **Active vs commented-out lines**: A commented-out var (`# KEY=value`)
  means the value is optional or was an alternative. Preserve it as
  commented-out in the example.
- **Provided vs placeholder values**: Some `.env` files already use
  placeholders (`your-api-key-here`, `change-me`). Keep those as-is.
- **In-line comments**: Preserve any trailing comments (`# explanation`)
  — they document what the var is for.

### Step 3 — Classify Each Value Per Redaction Tiers

For every `KEY=VALUE` pair, classify the VALUE using the three-tier model
from the
[redaction-portability](../redaction-portability/SKILL.md) skill:

| Tier | Examples | Treatment |
| --- | --- | --- |
| **A** — Credentials | Passwords, API keys, secret keys, JWT secrets, database passwords, SSH keys, auth tokens | Replace with `<descriptive-placeholder>` (e.g., `<db-password>`, `<api-key>`, `<secret-key>`) |
| **B** — Org topology | Internal hostnames/FQDNs, staging domains, internal IPs, absolute paths, customer names, project codenames | Replace with `<descriptive-placeholder>` (e.g., `<staging-domain>`, `<backend-host>`, `<internal-path>`) |
| **C** — Universal | `localhost`, `127.0.0.1`, `True`/`False`, standard ports (`5432`, `6379`), example emails, debug settings | Keep verbatim |

**Placeholder convention** (per redaction-portability §2):
Use `<lower-case-hyphenated-description>`. Examples:

| Original value | Placeholder |
| --- | --- |
| `smtp.gmail.com` | `<smtp-host>` |
| `587` | `<smtp-port>` |
| `postgresql://user:pass@localhost:5432/mydb` | `postgresql://<db-user>:<db-password>@<db-host>:<db-port>/<db-name>` |
| `/home/user/project/media` | `<media-root-path>` |
| `https://api.staging.example.com` | `<api-base-url>` |

### Step 4 — Write `.env.example`

Write the sanitized output to `.env.example` in the same directory as the
source `.env`. Rules:

1. **One var per line**, preserving the original order.
2. **Preserve all comments** (full-line `# ...` and inline `# ...`).
3. **Preserve commented-out vars** — they signal optional/alternative values.
4. **Required vars** should be uncommented with a placeholder value.
5. **Optional vars** should remain commented-out (`# KEY=<placeholder>`).
6. **Group related vars** with section comments if the original has none
   (e.g., `# Database`, `# Auth`, `# Email`).

### Step 5 — Verify the Output

Check:

- No real credentials, API keys, or secrets remain
- No internal hostnames, absolute paths, or org-specific values remain
- Every placeholder is descriptive enough to fill in
- The file is valid `KEY=VALUE` syntax (no spaces around `=` unless quoted)
- Lint clean via `markdownlint-cli2` (if the file contains markdown)

## Related Skills

- [`redaction-portability`](../redaction-portability/SKILL.md) — The three-tier
  classification model and canonical placeholder vocabulary this skill depends on
- [`staging-env-fetch`](../database/staging-env-fetch/SKILL.md) — Fetch `.env` from a
  staging server via MCP; use this skill to sanitize the fetched file into a `.env.example`
