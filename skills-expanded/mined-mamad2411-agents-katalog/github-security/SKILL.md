---
name: github-security
description: GitHub Advanced Security standards — Dependabot, CodeQL, secret scanning, branch protection, and GHAS setup. Load when configuring GitHub security features.
user-invocable: false
stack: code-quality/github-security
paths:
  - ".github/dependabot.yml"
  - ".github/workflows/codeql*"
  - ".github/workflows/security*"
  - ".github/workflows/**"
---

Full standards in [github-security.md](github-security.md). Always-on summary:

**Dependabot:**
- Enable for both `npm` and GitHub Actions (`github-actions`) in `.github/dependabot.yml`
- Set a weekly or daily schedule — not monthly; stale deps accumulate vulnerabilities
- Group minor/patch updates into a single PR; leave major updates separate for review
- Set `open-pull-requests-limit: 10` to avoid PR spam

**CodeQL:**
- Run CodeQL on `push` to main and `pull_request` — never just on schedule
- Use the `security-extended` query suite, not just `security-and-quality`
- Pin CodeQL Action to a specific SHA (`uses: github/codeql-action@v3`) — not `@latest`

**Secret scanning:**
- Enable at the repository and organisation level (Settings → Security)
- Add custom patterns for internal tokens (internal API keys, service account formats)
- Set up push protection to block secrets before they land on the remote

**Branch protection:**
- Require status checks (CI, CodeQL) to pass before merge
- Enable "Require signed commits" for main and release branches
- Set "Restrict who can push to matching branches" — no direct commits to main

**Never:**
- Disable secret scanning push protection to unblock a developer — rotate the secret instead
- Merge Dependabot PRs without reading the changelog — major bumps may break the API
- Run CodeQL only on a cron schedule — PRs can slip through with vulnerabilities

**Related skills:** `core/secret-scanning`, `ci/github-actions`, `core/security-review`
