---
name: direnv-dotenv-security
description: >
  Secure use of direnv and .env files: .envrc trust model, direnv allow, secret layout,
  blocking .env commits, dotenv vs secret managers, shell export hygiene, and team DevEx
  without leaking tokens. Use when direnv, .envrc, dotenv security, direnv allow, stdlib
  dotenv, or local secret loading for owned repos — hand production secrets platforms to
  secrets-management-hygiene.
---

# Direnv Dotenv Security

## Scope And Authorization

- **In scope:** Developer workstations and repos you control; local env loading patterns.
- **Out of scope:** Committing production credentials; bypassing corporate secret brokers; using direnv to inject secrets into untrusted project clones without review.
- Prefer secret managers / OIDC for CI and prod; direnv is for **local** DX.
- Redact env dumps in screenshots and support tickets.
- Pair with `secrets-management-hygiene`, `devbox-nix-dev-env`, and `code-quality-standards`.

## When To Use

- Standardizing local secrets via `direnv` + `.envrc` / `.env`.
- Preventing accidental `git add .env` of AWS keys.
- Reviewing whether `direnv allow` trust model is understood by the team.
- Migrating from hand-exported shell secrets to project-scoped loads.
- Auditing `.env.example` vs real secret files.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org secret storage/rotation (Vault, ASM) | `secrets-management-hygiene` |
| CI secret injection | CI skills (`drone-ci-secrets`, GitHub OIDC patterns) |
| Reproducible toolchains | `devbox-nix-dev-env` |
| Production 12-factor config | platform config skills |
| Code quality baseline | `code-quality-standards` |

## Threat model

| Risk | Mitigation |
| --- | --- |
| `.env` committed | gitignore + pre-commit + secret scan |
| Malicious `.envrc` in cloned repo | direnv block until `allow`; code review |
| Secrets in process list / logs | avoid `set -x` dumping; careful scripts |
| Shared `.env` on chat | personal secrets via manager; never Slack keys |
| Prod keys on laptops | scoped dev credentials; short-lived tokens |
| World-readable `.env` | file mode 600 |

## Workflow

### 1. Confirm scope and success criteria

1. Which repos use direnv; which secrets are local-dev vs prod.
2. Success: no secret files tracked by git; new clones cannot execute `.envrc` until allow; CI never depends on developer `.env`.
3. Document break-glass for revoked laptop credentials.

### 2. Inventory

```bash
ls -la .env .env.* .envrc 2>/dev/null
git check-ignore -v .env .envrc 2>/dev/null
rg -n "direnv|dotenv|load_dotenv" README* .github 2>/dev/null
# History bleed (owned repo)
git log --all --full-history -- .env 2>/dev/null | head
```

1. If `.env` ever committed, rotate all secrets and purge history per org process.
2. List tools that auto-load dotenv (Docker Compose, frameworks).

### 3. Hardened layout

```gitignore
# .gitignore
.env
.env.*
!.env.example
!.envrc.sample
```

```bash
# .envrc — preferred pattern: load dotenv without printing
dotenv_if_exists .env
# or: source_env_if_exists .env.local

# Optional: watch files for reload
watch_file .env

# Never:
# export AWS_SECRET_ACCESS_KEY=AKIA...   # hardcoding in .envrc that gets committed
```

```bash
# .env.example — placeholders only
DATABASE_URL=postgres://user:pass@localhost:5432/app
API_BASE=http://localhost:8080
```

1. Commit `.envrc` only if it contains **no secrets** (loads local `.env` or vault CLI).
2. Real `.env` is gitignored; mode `chmod 600 .env`.

### 4. direnv trust workflow

```bash
# After clone / .envrc change
direnv allow   # only after reviewing .envrc content
direnv deny    # revoke trust
direnv reload
```

1. Train team: **read `.envrc` before allow**—it can run arbitrary shell.
2. Prefer `dotenv` / `dotenv_if_exists` stdlib helpers over raw `source` of unknown scripts.
3. Corporate: consider `direnv` whitelist policies or strict shell.

### 5. Better secret sources

| Source | Use |
| --- | --- |
| 1Password / Vault CLI / `op run` | Inject without long-lived flat files |
| Cloud OIDC + short-lived keys | Prefer over static IAM users on laptops |
| `.env` from `make secrets` | Generate from manager, still gitignored |
| Kubernetes/devbox | Not a place for prod master keys |

```bash
# Example: envrc calls vault-ish CLI (illustrative)
# export DATABASE_URL="$(op read 'op://Dev/app/DATABASE_URL')"
```

### 6. Runtime hygiene

1. Disable debug that prints env in shared logs.
2. Frameworks: ensure production does not load `.env` from CWD unexpectedly.
3. Docker: pass env via compose `env_file` that is gitignored; never bake into images.
4. Pre-commit: `gitleaks` / `detect-secrets` on the repo.

```yaml
# .pre-commit-config.yaml sketch
# - repo: gitleaks
#   hooks: [{ id: gitleaks }]
```

### 7. Verify and hand off

```bash
git status --ignored | head
git check-ignore -v .env
# Ensure allow required
# (new clone simulation) remove direnv allow and confirm blocked
```

1. README: copy `.env.example` → `.env`, `direnv allow` after review.
2. Rotate any secrets found in history.
3. Apply `code-quality-standards` to scripts that touch env loading.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| `.env` | gitignored, 600 | committed with prod keys |
| `.envrc` | loads dotenv / vault | committed plaintext secrets |
| Trust | review then `allow` | `direnv allow` blind in script |
| CI | OIDC/secrets store | CI copies developer `.env` |
| Example | `.env.example` placeholders | Real tokens in example |
| Shell | no `set -x` on secret export | Debug logs full env |

## Output Checklist

- [ ] `.env` / secret files gitignored and untracked
- [ ] `.env.example` documents keys without values
- [ ] `.envrc` reviewed, secret-free, uses safe loaders
- [ ] Team trained on `direnv allow` trust model
- [ ] File permissions tightened
- [ ] Secret scan / pre-commit enabled
- [ ] History checked; rotations done if leaked
- [ ] CI/prod path independent of local dotenv
- [ ] Prefer manager/short-lived creds documented
- [ ] README onboarding steps verified

## Rules

- direnv executes project code—treat `.envrc` like code review.
- Local dotenv is not a production secrets architecture.
- Rotate on any commit or chat leak of credentials.
- Never disable secret scanning to “move faster.”
- Owned DevEx only; keep focus on direnv/dotenv hygiene.
