---
name: secrets-scanner
description: Detect and remediate leaked credentials in code and git-history — entropy/regex scanning with gitleaks/trufflehog/detect-secrets, rotate-first incident response, and pre-commit/CI gating to prevent reoccurrence.
---

# Secrets Scanner

## When to use

This skill covers three scenarios: an active leak (incident), preventive scanning, and setting up prevention. The action order differs sharply per scenario, so phase 1 explicitly asks which one you're doing.

Triggers:

- "I think I accidentally committed a key", "this token looks like it's leaking", "check whether there are secrets in the repo".
- A PR touches files like `.env`, `.env.*`, `config/*.yaml`, `docker-compose*.yml`, `helm/values*.yaml`, `*.pem`, `*.key`, `credentials.json`, or new files under `secrets/`, `vault/`.
- Setup of a new repo: install pre-commit plus CI secret-gate.
- Periodic audit of git history on an existing repo.
- A finding from `security-review` phase 3 (automated scan) that needs further triage.
- Anthropic/OpenAI-style token patterns in logs, screenshots, or shared notebooks.

### When NOT to use (handoff)

- Runtime secret injection (Kubernetes Secrets, External Secrets Operator, sidecar pattern) → `k8s-security` and `container-hardening`.
- Cloud IAM policy review (who can use which key) → `iac-security`.
- Secret-handling patterns in code (where a credential lives in memory, how it's passed) → `secure-coding` phase 4.
- Vulnerability triage on dependencies that leak credentials → `cve-triage`.
- Post-incident forensics where misuse is proven → `ir-runbook` and `forensics-assist`.

For an active leak this skill doesn't stop — rotation is its job. But escalate to `ir-runbook` as soon as there's evidence of misuse (CloudTrail hits, abnormal API traffic, data egress).

## Approach

Seven phases. **Phase 1 sets the order for the rest**: an active leak goes straight to phase 4 (rotation), 2/3/5/6 follow. For scan/prevention: normal order.

### 1. Determine urgency

One question: is there a credential that may right now be in the wrong hands? The clock starts the moment the secret is out of control.

Classification:

- **Active leak, credential still working**: phase 4 immediately. Hours matter. All other phases later.
- **Confirmed leak, credential status unknown or possibly dead**: phase 4 as soon as possible, with phases 2/3 in parallel for the full picture.
- **Suspected leak**: phase 2 (detection) first to confirm, then triage.
- **No leak, preventive scan or setup**: phase 2 → 3 → 6. Phases 4 and 5 don't apply.

Note the classification explicitly. It determines whether phase order can wait for deliberate analysis or whether speed beats thoroughness.

### 2. Detect

Tools in order of preference:

- **gitleaks** (MIT, Go). Scans working tree and full history. TOML rule sets; the community set covers 140+ providers out of the box. Default choice for both incident and scan.
- **trufflehog** (AGPL / commercial). Unique feature: `--only-verified` actively tests detected keys against the provider API (AWS STS, Stripe, GitHub, etc.) and separates dead keys from live ones. Required during incident triage where "does this still work?" is the critical question.
- **detect-secrets** (Yelp, Apache-2). Strength: baseline/allowlist workflow. A scan generates a `.secrets.baseline` that's git-diffable. New findings stand out; old known-safe ones don't get re-reported every run.
- **GitHub/GitLab native secret scanning + push protection**: always on. Complement, not replacement, for CI/local. The providers only catch known formats and only at push time.

Detection methods in combination:

- **Provider-specific regex** (examples of public format prefixes: `AKIA` for AWS access keys, `ghp_` / `gho_` / `ghs_` for GitHub, `xox[abpr]-` for Slack, `sk_live_` for Stripe, `AIza` for Google API keys, `sk-ant-api03-` for Anthropic, `npm_` for npm). High precision. Reference list: GitHub Secret Scanning patterns documentation.
- **Shannon entropy on base64/hex-style strings**. Use the tool defaults; don't tune yourself. Trufflehog and gitleaks have empirically calibrated values per context. High recall, low precision; triage always required.
- **Keyword + context** (`password\s*=`, `api_key:`, `BEGIN PRIVATE KEY`). Catches hardcoded-in-source and README accidents.

Command reference:

```bash
# gitleaks — full repo, working tree + history
gitleaks detect --source . --verbose --report-path gitleaks-report.json

# gitleaks — staged only (pre-commit usage)
gitleaks protect --staged --verbose

# trufflehog — git history, only verified live credentials
trufflehog git file://. --only-verified

# trufflehog — GitHub org scan (incident context)
trufflehog github --org=<org> --only-verified

# detect-secrets — baseline + audit
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

For non-git sources (logs, tarballs, backup dumps): gitleaks has `detect --no-git`, trufflehog has `filesystem` and `s3` subcommands. Same rule sets, different source.

### 3. Classify

Each hit becomes a finding only after you've determined:

- **Type of credential.** Cloud (AWS/GCP/Azure), SaaS (Stripe, SendGrid, Slack, Twilio), VCS (GitHub PAT, GitLab token, BitBucket app password), in-house (DB password, internal API key), crypto (private key, signing key), identity (JWT, session cookie).
- **Exposure surface.** Private repo, public repo, public Docker image, public website asset, leaked log file, backup tarball on S3 with public ACL, screenshot in a support ticket, gist. **Public = assume harvested.** Search engines, GitHub event archives, GH-Archive.org and third-party scrapers index within minutes.
- **Still active?** trufflehog `--only-verified` or a manual call against a read-only provider endpoint (e.g. `aws sts get-caller-identity` with the key configured).
- **Blast radius.** Read-only API key, write access, billing, admin, root account? On unknown scope: assume the maximum scope until proven otherwise.
- **Exposure window.** First commit: `git log -p --all -S '<unique-part-of-secret>'`. Or `git blame` on the file if it's still present. End time: now, or the moment of revocation.

Severity (parallel to `security-review` phase 6):

- **Blocker.** Production cloud-admin key, root DB credential, payment/signing key, code-signing key. Rotate immediately, everything else stops.
- **High.** Scoped prod API keys, SaaS with data/money impact, PATs with repo-write on org repos.
- **Medium.** Dev/staging keys, read-only tokens with limited scope, expired-but-still-valid session tokens.
- **Low.** Test fixtures with obvious fake values, expired tokens, public demo keys. Document, remove from history at the next cleanup, no rotation urgency.

### 4. Rotate-first remediation

**Order is law.** Rotate first, then communicate, then clean up. Anti-pattern: cleaning up git history and forgetting to rotate. That's cosmetics for a credential that's already been harvested.

1. **Rotate or revoke at the provider.** AWS: `aws iam delete-access-key` + create new, or roll via `aws iam update-access-key`. GitHub: Settings → Developer settings → PAT → Revoke. Stripe: Dashboard → Developers → API keys → Roll. Anthropic/OpenAI: console → revoke + generate new. DB: `ALTER USER … WITH PASSWORD …` or drop and recreate user. For signing/KMS keys: schedule deletion with a window, not instant-delete.
2. **Check provider logs for misuse** with the exposure window as the time range. AWS CloudTrail filtered on `userIdentity.accessKeyId`, GitHub Audit Log on PAT-owner, Stripe events, SaaS audit exports. On confirmed misuse: escalate to `ir-runbook` (the secret is no longer the story; the breach is).
3. **Replace in every place the old credential was used.** CI secrets, production hosts, team-member configs. Ideally lift them into a vault during this step — a rotation incident is a good catalyst to get secrets out of source.
4. **Incident log.** What, where, when leaked, when detected, when rotated, who acted, which systems affected. For compliance purposes minimum this set; more detail under `ir-runbook` when there's evidence of misuse.

### 5. Git-history cleanup (optional, destructive)

Only run when all three are true: the credential is verifiably revoked, the repo is private or the exposure window was short enough for removal to be meaningful, and the team accepts a force-push plus coordination moment.

Tools:

- **git-filter-repo** (modern, fast, actively maintained). Python, but ships as a standalone executable. Replaces `git filter-branch`, which is deprecated.
- **BFG Repo-Cleaner** (Java, fastest on large histories with many commits).

Commands:

```bash
# git-filter-repo — remove a file completely from history
git filter-repo --invert-paths --path path/to/secret-file

# git-filter-repo — replace text (patterns.txt: one regex per line)
git filter-repo --replace-text patterns.txt

# BFG — same idea
bfg --replace-text patterns.txt
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# Then synchronize
git push --force --all
git push --force --tags
```

Coordination: every collaborator must re-clone or do a careful reset. Old clones still hold the history. Public forks on GitHub keep the history. You can ask GitHub Support to invalidate caches, but there's no guarantee.

**Reality check.** For public repos or images: GitHub events, the Wayback Machine, GH-Archive.org, scraped copies on third-party sites. History cleanup only reduces casual-discovery surface; it doesn't undo the leak. Compliance or policy may still require cleanup despite this reality.

### 6. Set up prevention

Layered. One barrier always fails; the combination catches most mistakes.

**Pre-commit hook** (developer machine, first line). Uses the `pre-commit` framework (Python) or husky (Node):

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.x.y   # pin to latest stable at install
    hooks:
      - id: gitleaks
```

Developers can always run `git commit --no-verify`. Pre-commit is helpful, not a gate. CI is the backstop.

**CI gate** (GitHub Actions example):

```yaml
- name: secret scan
  uses: gitleaks/gitleaks-action@v2
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Make the step fail on findings. Whitelist only via `.gitleaksignore` with commit hash plus reason per entry. No wildcards or path globs that skip whole directories.

**Repo settings**:

- GitHub: Settings → Code security → Secret scanning on, **Push protection on**. Push protection blocks known patterns before they hit the server.
- GitLab: Secret Detection template in `.gitlab-ci.yml`.
- `.gitignore` explicitly for `.env`, `.env.*` (except `.env.example`), `*.pem`, `*.key`, `*.p12`, `id_rsa*`, `credentials.json`, `config/local.*`, `**/secrets/**`.
- `.env.example` committed with empty/placeholder values so developers know which env vars exist without seeing the real ones.

**Runtime secret store** (does not belong in source, also not in CI config as plain text):

- Cloud-native: AWS Secrets Manager, GCP Secret Manager, Azure Key Vault. IAM-gated, rotation schedule possible.
- Platform: HashiCorp Vault, Doppler, Infisical.
- Kubernetes: External Secrets Operator with one of the above as backend. Native K8s Secrets as the only layer is insufficient — they're base64-encoded, not encrypted, and RBAC determines who can read them. See `k8s-security`.

**Onboarding checklist**:

- New devs: where to get secrets, which classes of credentials exist, what happens if you commit something (incident procedure).
- Code-review standard: every config change is scanned for secrets before merge.

### 7. Verification-loop

**Incident mode**: Layer 1 scope check (all systems rotated? all team members notified? all CI pipelines updated?), assumptions (credential genuinely revoked or just "I clicked revoke"?), gaps (backups, read replicas, cached configs included?). Layer 2 red flags especially on claims: "key is dead" only when verified via trufflehog or a provider test; no assumed rotation.

**Prevention mode**: Layer 1 gaps (do the gates cover both staging and prod? do they work on new branches?), Layer 2 source quality (regex from GitHub Secret Scanning docs, not from a random blog).

## Output

**Incident mode**:

```
Secret leak incident — <short ID>
Detected: YYYY-MM-DD HH:MM | Status: <active | contained | closed>

Credential:
  Type: <AWS access key | GitHub PAT | Stripe live key | ...>
  Scope/blast radius: <known detail | assumed maximum>
  Exposure window: <first commit SHA/date> → <detected or removed>
  Exposure surface: <private repo | public repo | image | log | ...>
  Verified active: <yes | no | unknown — method>

Action path:
  [x] Rotate/revoke at provider — YYYY-MM-DD HH:MM by <actor>
  [x] Provider logs checked — <clean | attachment with hits>
  [x] Replaced in <CI, hosts, team-member configs>
  [x|-] Git-history cleanup — <done | skip with reason | in progress>
  [ ] Incident retrospective

Verification-loop:
  Verdict: <pass | revise | rewrite>
  Security verdict: <no red flags | red flag — ...>
```

**Prevention mode**: concrete deliverables, not a narrative report. Artifacts produced:

- `.pre-commit-config.yaml` (or husky equivalent).
- CI workflow file (`.github/workflows/secret-scan.yml` or `.gitlab-ci.yml` fragment).
- `.gitignore` additions.
- `.gitleaks.toml` if org-specific patterns (internal prefixes, domain names) are needed.
- `.secrets.baseline` for the detect-secrets path.
- Repo-settings checklist (push protection, secret scanning, required status checks).
- Test instruction: commit a canary string like `AKIAIOSFODNN7EXAMPLE` (AWS's own documentation placeholder) and verify that pre-commit and CI both block the push.

Don't deliver a report on incidents without the rotation status. Without rotation it's not remediation, and that needs to be in the report explicitly.

## References

- OWASP Secrets Management Cheat Sheet — [https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html). Canonical storage/lifecycle guidance.
- NIST SP 800-57 Part 1 Rev 5 — [https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final). Key management recommendations for rotation cadence and lifecycle.
- GitHub Secret Scanning patterns — [https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns). Primary source for vendor token formats.
- gitleaks — [https://github.com/gitleaks/gitleaks](https://github.com/gitleaks/gitleaks). TOML rules, local + CI + pre-commit.
- trufflehog — [https://github.com/trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog). `--only-verified` for active validation during incidents.
- detect-secrets — [https://github.com/Yelp/detect-secrets](https://github.com/Yelp/detect-secrets). Baseline workflow for repos with historical findings.
- git-filter-repo — [https://github.com/newren/git-filter-repo](https://github.com/newren/git-filter-repo). Modern history rewrite, replaces filter-branch.
- BFG Repo-Cleaner — [https://rtyley.github.io/bfg-repo-cleaner/](https://rtyley.github.io/bfg-repo-cleaner/). Faster option for large histories.
- pre-commit framework — [https://pre-commit.com/](https://pre-commit.com/). Host for the gitleaks/detect-secrets hooks.

## Categories

- core
- appsec
