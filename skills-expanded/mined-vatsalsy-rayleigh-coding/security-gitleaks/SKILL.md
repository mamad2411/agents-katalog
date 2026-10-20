---
name: security-gitleaks
description: >-
  Use when the user says "scan for leaks", "check for secrets", "gitleaks scan", "did I commit a key", or asks for Gitleaks-Action CI on a repo. NOT for general security audits (security-best-practices).
---

# Gitleaks — Secret Scanner

Scan repos for accidentally committed secrets (API keys, tokens, passwords) in current files and full git history. Optionally install Gitleaks-Action for automatic CI scanning on every PR/commit.

---

## Install

```bash
brew install gitleaks    # macOS
# or: go install github.com/gitleaks/gitleaks/v8@latest
gitleaks version         # verify
```

---

## One-off Scan

### Scan current HEAD (fast)
```bash
cd <repo-root>
gitleaks detect --source . --verbose
```

### Scan full git history (thorough — always do this for high-risk repos)
```bash
gitleaks detect --source . --log-opts="--all" --verbose
```
`--log-opts="--all"` passes `--all` to `git log`, scanning every branch and every commit ever made.

### Scan a specific branch or commit range
```bash
gitleaks detect --source . --log-opts="origin/main..HEAD"
```

### Save report to JSON (for archiving or CI)
```bash
gitleaks detect --source . --log-opts="--all" --report-format json --report-path gitleaks-report.json
```

---

## CI Setup — Gitleaks-Action (GitHub)

Adds automatic scanning on every PR and push. Blocks merges if secrets are found.

### Step 1 — Create workflow file

Create `.github/workflows/gitleaks.yml` in the repo:

```yaml
name: gitleaks

on:
  push:
    branches: ["main", "develop"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

jobs:
  scan:
    name: Secret Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # full history — required for complete scan

      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          # GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}  # needed for org repos only
```

> ⚠️ `fetch-depth: 0` is critical — without it, only the latest commit is checked.

### Step 2 — License key (org repos only)

For repos under a GitHub organisation (e.g. `EXAMPLE_ORG`), a free license key is required.
- Get it: https://forms.gle/8e8xPF72nS3TiY7G9
- Add as a GitHub secret: repo/org Settings → Secrets → `GITLEAKS_LICENSE`
- Uncomment the `GITLEAKS_LICENSE` line in the workflow above.

Personal account repos (`OWNER/*`): no license needed.

### Step 3 — Push the workflow

```bash
# Commit goes as Your Name (plain git):
git add .github/workflows/gitleaks.yml
git commit -m "ci: add gitleaks secret scanning on PRs and pushes"
git push
```

---

## Custom Rules (`.gitleaks.toml`)

Override or extend the default ruleset. Place at repo root:

```toml
[extend]
# Extend the default ruleset
useDefault = true

[[rules]]
id = "comphy-openai-key"
description = "OpenAI API key"
regex = '''sk-[a-zA-Z0-9]{48}'''
tags = ["key", "openai"]

[allowlist]
# Ignore false positives
regexes = [
  '''EXAMPLE_KEY''',
  '''test-token-placeholder''',
]
paths = [
  '''.gitleaks.toml''',
  '''tests/fixtures/''',
]
```

Useful for false positive suppression (e.g. test fixtures, example configs).

---

## Handling a Real Finding

If Gitleaks finds a committed secret:

1. **Rotate the key immediately** — assume it's compromised, regardless of whether the repo is public.
2. **Remove from history** using BFG Repo Cleaner or `git filter-repo`:
   ```bash
   pip install git-filter-repo
   git filter-repo --replace-text <(echo "OLD_SECRET_VALUE==>REDACTED")
   git push --force --all
   ```
3. **Audit usage** — check API provider logs for unexpected calls during the exposure window.
4. **Add to `.gitleaks.toml` allowlist** (the redacted placeholder) to prevent future false positives.

> ⚠️ Force-pushing rewrites history. Coordinate with any collaborators on the repo first.

---

## High-priority scan targets

Prioritise:

- Public repos with CI that inject secrets
- Any repo with `.env` in history (`git log --all --full-history -- .env`)
- Deploy-connected apps (Vercel, Netlify, Render, Cloudflare Workers)

Do not keep a personal repository inventory inside this skill.

---

## Quick Audit Workflow

When the user asks to scan a repo:

1. Verify `gitleaks` is installed: `gitleaks version`
2. `cd` to the repo root
3. Run full history scan: `gitleaks detect --source . --log-opts="--all" --verbose`
4. If findings: report each finding (file, line, rule triggered, commit hash)
5. If clean: confirm clean with commit count scanned
6. Ask: "Want me to also add Gitleaks-Action CI to this repo?"

---

## Gotchas

1. **`fetch-depth: 0` in CI is non-negotiable.** Shallow clones (default in most CI) only have the tip commit. Gitleaks won't scan history without the full clone.

2. **Org repos need a free license key.** `EXAMPLE_ORG/*` repos require `GITLEAKS_LICENSE` secret. Personal `OWNER/*` repos do not. Getting the key is a one-time form fill.

3. **`.env` files deleted from current HEAD are still in history.** `git rm .env` doesn't remove it from git history — it's still accessible via `git show <commit>:.env`. Always scan with `--log-opts="--all"`.

4. **Don't paste real secrets in the Gitleaks Playground** (playground.gitleaks.io). It's browser-local but still bad practice.

5. **`git filter-repo` requires a fresh clone.** It refuses to run on repos with uncommitted changes or existing remotes without `--force`. Clone to a temp dir, run there, then replace.

6. **False positives are common with entropy-based rules.** Long random-looking strings in test fixtures, UUIDs, base64 data will trigger rules. Suppress via `.gitleaks.toml` allowlist, not by disabling the rule.
