---
name: repo-sanitization-audit
description: Strip personal credentials, paths, and identifiers from a code repo before sharing or open-sourcing. Regex scans, credential patterns, and YAML-safe replacement.
category: security
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [sanitization, open-source, security, credentials, audit, git]
    triggers:
      - clean repo for sharing
      - remove personal info from repo
      - prepare for open source
      - strip credentials from code
      - sanitize config files
    related_skills: [hermes-system-backup, skill-library-maintenance]
---

# Repo Sanitization Audit

Systematic process for removing personal/sensitive information from a code repository before sharing, open-sourcing, or publishing. Designed for private repos being made public.

## Threat Model

| Severity | What to find | Example |
|----------|-------------|---------|
| 🔴 Critical | Live credentials | API keys, tokens, passwords, private keys |
| 🟡 High | Personal identifiers | Email addresses, phone numbers, real names |
| 🟡 Medium | Infrastructure fingerprints | Discord IDs, internal URLs, absolute paths |
| 🟢 Low | Organization context | Project names, internal tooling names |

## Step 1: Scan Everything

Use Python `re` with targeted patterns across ALL repo files (exclude `.git/`):

```python
import re, os

patterns = [
    # API keys / tokens
    (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI-style API key'),
    (r'[xX][oO][xX][psb][a-zA-Z0-9]{20,}', 'Slack/Discord token'),
    (r'gh[pors]_[a-zA-Z0-9]{36}', 'GitHub token'),
    (r'hf_[a-zA-Z0-9]{20,}', 'HuggingFace token'),
    (r'glpat-[a-zA-Z0-9\-]{20,}', 'GitLab PAT'),
    # Gmail app passwords (16 lowercase letters, often with spaces)
    (r'[a-z]{16}', 'potential app password'),
    (r'[a-z]{4} [a-z]{4} [a-z]{4} [a-z]{4}', 'spaced app password'),
    # Email addresses
    (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'email address'),
    # Discord IDs (17-19 digit snowflakes)
    (r'[0-9]{17,19}', 'Discord/channel ID'),
    # Absolute Windows paths
    (r'[A-Z]:\\\\(Users|Documents|Backup).*', 'Windows path'),
    (r'C:/Users/\w+', 'Windows path (forward slash)'),
    # Private keys (64-char hex)
    (r'[a-f0-9]{64}', 'potential private key'),
]
```

## Step 2: Replace with Placeholders

Replace ALL matches with generic placeholders:

```python
replacements = {
    # Email addresses
    "<your-email>@gmail.com": "REPLACE_WITH_YOUR_EMAIL@gmail.com",
    "<your-email>@gmail.com": "REPLACE_WITH_YOUR_SECONDARY_EMAIL@gmail.com",
    # Gmail passwords
    "${GMAIL_APP_PASSWORD}": "REPLACE_WITH_YOUR_APP_PASSWORD",
    "${GMAIL_APP_PASSWORD}": "REPLACE_WITH_YOUR_APP_PASSWORD",
    # Windows paths
    r"C:\\Users\\<you>": r"$HOME",
    r"${USER_HOME}": r"$HOME",
    r"${USER_HOME}": r"$HOME",
    "yourdata": "Documents",
    # Discord IDs (17-19 digit)
    r"'[0-9]{17,19}'": "'<discord-channel-id>'",
    # Personal names
    "the operator": "User",
}
```

Replace **in file**, not in-memory, so YAML/JSON files are correctly updated:

```python
content = open(fp).read()
content = re.sub(r"'?[0-9]{17,19}'?", "'<discord-channel-id>'", content)
content = content.replace("the operator", "User")
content = re.sub(r'C:\\\\Users\\\\<you>', r'$HOME', content)
open(fp, 'w').write(content)
```

## Step 3: Verify YAML/JSON Validity

After replacements, validate all structured files:

```python
import yaml, json

for f in glob.glob("**/*.yaml", recursive=True):
    yaml.safe_load(open(f))  # raises on invalid YAML
for f in glob.glob("**/*.json", recursive=True):
    json.loads(open(f).read())  # raises on invalid JSON
```

Broken YAML after replacement means a regex was too aggressive or didn't account for YAML syntax. Common breakages:

- Replacing inside a YAML key (not value) breaks the key name
- Replacing inside a comment is fine but misleading
- Multi-line string values may have embedded patterns that get corrupted

## Step 4: Verify Python Syntax

For `.py` files that were modified:

```python
import py_compile
py_compile.compile(fpath, doraise=True)
```

## Step 5: The .gitignore Check

Ensure these patterns are in `.gitignore`:

```
.env
.env.*
!.env.example
*.db
*.sqlite
__pycache__/
*.py[cod]
.hermes/
```

If `.hermes/` or `.env` files are already tracked, remove them first:

```bash
git rm -r --cached .hermes/
git rm --cached profiles/*/.env 2>/dev/null || true
```

## Step 6: Resync Template Files

If you maintain `.example.yaml` or `.example.env` templates alongside live configs, regenerate them from the **already-sanitized** originals after Step 2-4:

```python
shutil.copy("config/config.yaml", "config/config.example.yaml")
shutil.copy("config/gateway.yaml", "config/gateway.example.yaml")
```

## Step 7: Final Verification

Run a comprehensive scan that matches on **original values** to ensure zero remain:

```python
remaining = []
for root, dirs, files in os.walk(repo):
    if '.git' in root: continue
    for fname in files:
        content = open(os.path.join(root, fname), encoding='utf-8', errors='ignore').read()
        for original_val in ["the operator", "youraccount", "yourapppassword", "C:\\Users\\<you>"]:
            if original_val in content.lower():
                remaining.append((fname, original_val))
```

Zero remaining = clean. Any remaining = repeat Steps 2-4 for those patterns.

## Summary Checklist

- [ ] Scan all files with regex patterns
- [ ] Replace real emails with placeholders
- [ ] Replace passwords/tokens with placeholders
- [ ] Replace absolute paths with `$HOME`
- [ ] Replace Discord IDs with `<placeholder>`
- [ ] Replace personal names with "User"
- [ ] Validate all YAML/JSON files
- [ ] Validate Python syntax for modified .py files
- [ ] Update .gitignore with secret patterns
- [ ] Remove any tracked .env / .hermes directories
- [ ] Regenerate `.example.*` templates from sanitized originals
- [ ] Final verification scan — zero remaining
- [ ] Commit with descriptive security message

## Pitfalls

### 🚨 Blind string replace can break YAML keys
If a personal value appears in a YAML key position (e.g. `the operator's config:`), replacing it to `User's config:` changes the key. Use targeted key-aware replacements or manually review YAML changes.

### 🚨 Gmail app passwords have two formats
Gmail app passwords come in both `${GMAIL_APP_PASSWORD}` (contiguous) and `${GMAIL_APP_PASSWORD}` (spaced). Scan for both. The hash changes between them (dots vs spaces), so a single regex won't catch both.

### 🚨 .example files lag behind
If you sanitize config files but forget to regenerate `.example.*` files, the examples still contain the old real values. Always copy sanitized originals over the examples as the final step.

### 🚨 .hermes/ directories get accidentally tracked
`hermes init` creates `.hermes/` in the repo root with a config.yaml that may contain personal info. Add `.hermes/` to `.gitignore` early, or `git rm --cached` it if already tracked.

### 🚨 Nostr private keys in JSON files
When including Nostr key data in a repo, always truncate: `secret_key[:8] + "..." + secret_key[-8:]`. Full 64-char hex keys are as good as the password itself.

### 🚨 Discord IDs look like numbers but are secrets
17-19 digit Discord snowflakes encode the exact creation time of a channel/server/user. An attacker can derive your infrastructure timeline. Always replace with `<discord-channel-id>`.
