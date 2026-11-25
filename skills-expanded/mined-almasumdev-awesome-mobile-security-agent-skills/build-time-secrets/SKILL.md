---
name: build-time-secrets
description: Keeping build-time secrets out of the repository — gitleaks, .gitignore discipline, and scoped CI credentials. Use when wiring up signing, store deploys, or CI secrets.
---

# Build-Time Secrets

## Instructions

Build-time secrets (signing keys, store API credentials, Fastlane `match` passphrases, Sentry auth tokens) are the ones that most often end up committed by accident. Harden the pipeline, not the developer.

### 1. What's a Build-Time Secret

- Android: upload keystore, key password, key alias password, Play Developer API JSON, Firebase service account.
- iOS: Apple Developer API key (`AuthKey_*.p8`), App Store Connect issuer ID, `fastlane match` passphrase, certificates.
- Cross-cutting: Sentry auth token, npm / Maven publish token, release webhook URLs with embedded tokens.

None of these belong in the repo — including in `/android`, `/ios`, `/fastlane`, or encrypted-but-plaintext-in-CI files.

### 2. `.gitignore` Discipline

Commit a strict `.gitignore` before the first push:

```gitignore
# Android signing
*.keystore
*.jks
keystore.properties
key.properties
google-services.json
play-api-key.json

# iOS signing
*.mobileprovision
*.p12
*.p8
AuthKey_*.p8
ios/fastlane/report.xml

# Generic
.env
.env.*
!.env.example
secrets/
*.pem
*.pfx
```

Provide `.env.example` / `keystore.properties.example` with placeholder values so onboarding is clear.

### 3. Pre-Commit and CI Scanning

Run `gitleaks` (or `trufflehog`) as:

- A pre-commit hook.
- A required CI check on every PR.
- A scheduled scan over the full history (for legacy repos).

```yaml
# .github/workflows/gitleaks.yml
name: gitleaks
on: [pull_request, push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          fail: true
```

Fail the build on findings. Add allow-listed false positives via `.gitleaksignore` with a comment explaining why.

### 4. If a Secret Was Ever Committed, Rotate It

History rewrites with `git filter-repo` / BFG **do not** undo a leak:

- Any CI caches / mirrors / forks still have it.
- It was likely indexed by a secret scanner within minutes.
- GitHub, GitLab, and others forward leaked credentials to AWS / Stripe / Google who may auto-revoke.

Policy: every commit that ever contained a secret → **rotate at the provider**, even if the commit was amended or force-pushed away.

### 5. CI Secret Scopes

GitHub Actions / GitLab CI / Bitrise all support scoped secrets. Apply least privilege:

- Protect environments (`production`) — require manual approval.
- Restrict secrets to specific workflows (`environment: production` gating).
- Never expose production signing to PR workflows from forks (`pull_request` from forks runs without secrets by default; do not bypass this).

```yaml
jobs:
  release:
    environment: production # gated
    runs-on: ubuntu-latest
    steps:
      - run: echo "Signing..."
        env:
          ANDROID_KEYSTORE_BASE64: ${{ secrets.ANDROID_KEYSTORE_BASE64 }}
          ANDROID_KEY_PASSWORD:    ${{ secrets.ANDROID_KEY_PASSWORD }}
```

### 6. Signing Keys

- Android: use **Play App Signing** so the upload key is not the production key. Losing the upload key is recoverable via Google; losing the production key used to be fatal.
- iOS: `fastlane match` with a private encrypted git repo **plus** MFA on the Apple Developer account.
- Back up keys in a dedicated password manager / HSM, not in Google Drive.

### 7. Handling Files in CI

For keystores / `.p8` / `.mobileprovision` files, store **base64** in CI secrets and materialize at runtime:

```bash
echo "$ANDROID_KEYSTORE_BASE64" | base64 -d > app/release.keystore
trap 'shred -u app/release.keystore' EXIT
```

Always delete after the build step. Never upload the key as a build artifact.

### 8. Audit Trail

- Every access to a production secret should be loggable (CI run URL + commit SHA + actor).
- Rotate on any suspicious access — especially for secrets a terminated employee had.
- Review secrets quarterly: is each one still used? Revoke the rest.

## Checklist

- [ ] `.gitignore` blocks keystores, provisioning profiles, `.p8`, `.env`, and service-account JSON.
- [ ] `gitleaks` (or equivalent) runs on pre-commit and on every PR, blocking on findings.
- [ ] Any secret ever committed is rotated, regardless of history rewrites.
- [ ] CI secrets are scoped by environment; fork PRs cannot access production secrets.
- [ ] Android uses Play App Signing; iOS uses `match` with MFA on Apple accounts.
- [ ] Signing files are injected at runtime from base64 secrets and shredded post-build.
- [ ] A quarterly review exists to revoke unused CI secrets.
