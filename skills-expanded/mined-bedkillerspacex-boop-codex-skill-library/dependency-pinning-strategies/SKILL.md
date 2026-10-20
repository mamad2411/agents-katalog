---
name: dependency-pinning-strategies
description: >
  Choose and enforce dependency pins: committed lockfiles, exact vs range versions, CI frozen
  installs, hash pinning, and Dependabot/Renovate update policy with supply-chain tradeoffs.
  Use when lockfiles, package-lock, yarn.lock, pnpm-lock, poetry.lock, uv.lock, go.sum,
  Cargo.lock, Pipfile.lock, version ranges, caret/tilde, pin vs float, reproducible builds,
  or npm ci / pip install --require-hashes — hand SBOM/CVE inventory to SBOM skills, confusion
  defenses to dependency-confusion, and Dependabot yml layout to dependabot-config-hardening.
---

# Dependency Pinning Strategies

## Scope And Authorization

- **In scope:** Application and library repos you own; CI install policies; private registry auth via secrets.
- **Out of scope:** Forcing pins on third-party projects; stripping integrity checks to unblock malware.
- Prefer changing pin policy in a feature branch with full CI before default-branch enforcement.
- Redact registry tokens; do not commit `.npmrc` auth tokens.
- Pair with `dependabot-group-updates`, `dependency-confusion`, and `code-quality-standards`.

## When To Use

- Builds are non-reproducible (“works on my machine” / different transitive tree each CI run).
- Choosing between `^1.2.3`, `~1.2.3`, exact `1.2.3`, and lockfile-only discipline.
- Enforcing `npm ci`, `pnpm install --frozen-lockfile`, `pip install --require-hashes`.
- Aligning app pins vs library range policies for public packages.
- Balancing freshness (automated updates) vs stability (frozen prod images).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dependabot full config hardening | `dependabot-config-hardening` |
| Grouping noisy update PRs | `dependabot-group-updates` |
| Private vs public name confusion | `dependency-confusion` |
| SBOM generation / CVE inventory | SBOM / supply-chain skills |
| License compliance | license skills in catalog |
| Outage when registry down | `dependency-outage-degrade` |
| Code quality baseline | `code-quality-standards` |

## Pinning model

| Layer | Role |
| --- | --- |
| Manifest ranges | Declare intent (`package.json`, `pyproject`, `go.mod`) |
| Lockfile | Pin full resolved tree + integrity where supported |
| CI install mode | Fail if lock and manifest disagree |
| Image/release | Bake resolved versions; rebuild to move |
| Update bot | Intentional, reviewed movement of pins |

**Apps/services:** commit lockfiles; CI frozen install.  
**Libraries you publish:** often wider ranges in manifest, but **your** CI still locks for tests.  
**Containers:** rebuild from lock; avoid `apk add foo` without version in prod Dockerfiles (see dockerfile skills).

## Ecosystem quick reference

| Ecosystem | Lock / integrity | Frozen CI command |
| --- | --- | --- |
| npm | `package-lock.json` | `npm ci` |
| yarn | `yarn.lock` | `yarn install --immutable` (Berry) / `--frozen-lockfile` |
| pnpm | `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| pip | hashes in requirements / `poetry.lock` / `uv.lock` | `pip install --require-hashes -r ...` or poetry/uv sync --frozen |
| Go | `go.sum` | `go mod download` with committed `go.sum`; `-mod=readonly` |
| Rust | `Cargo.lock` (apps) | `cargo build --locked` |
| .NET | lock files optional | enable `RestorePackagesWithLockFile` / locked mode |
| Maven | not full lock by default | use versions plugin / flatten / dependencyManagement discipline |

## Workflow

### 1. Confirm scope and success criteria

1. Classify each repo: application, library, infrastructure module, monorepo package.
2. Success: same commit → same dependency graph in CI; no registry float on release builds; update path via PR exists.
3. Note constraints: regulated pin freezes, air-gapped mirrors.

### 2. Inventory current state

```bash
# Owned repo probes
ls package-lock.json yarn.lock pnpm-lock.yaml poetry.lock uv.lock go.sum Cargo.lock 2>/dev/null
rg -n "\"\\^|\"~|>=|latest" package.json pyproject.toml 2>/dev/null | head
# CI: does it use npm install (float) or npm ci?
rg -n "npm ci|npm install|pip install|poetry install|go mod" .github/workflows Makefile 2>/dev/null
```

1. Flag missing lockfiles, lockfiles gitignored, or `npm install` in release pipelines.
2. Flag `latest` tags and unpinned GitHub Actions (`uses: foo@main`).

### 3. Choose policy by package class

| Class | Manifest | Lock | Updates |
| --- | --- | --- | --- |
| Production app | Prefer exact or caret + lock | Required committed | Dependabot/Renovate PR |
| Internal lib | Semver ranges OK | Lock for CI only | Consumers pin via their lock |
| Crypto/auth critical | Exact + frequent review | Required | Solo PRs, no mega-groups |
| Dev/lint tooling | Ranges OK | Lock recommended | Grouped patches |

1. Document: “ranges express compatibility; lockfiles express builds.”
2. Do not delete lockfiles to “pick up security fixes automatically”—use bots instead.

### 4. Enforce frozen installs in CI

```yaml
# GitHub Actions sketch
- run: npm ci
- run: pnpm install --frozen-lockfile
- run: cargo test --locked
- run: go test ./...   # with go.sum committed; consider -mod=readonly
```

```bash
# pip hashes (after pip-compile --generate-hashes)
pip install --require-hashes -r requirements.txt
```

1. Fail the job if lock outdated rather than silently rewriting on CI.
2. Cache keyed by lockfile hash.

### 5. Hash and integrity

1. Prefer package managers that store integrity (npm, poetry, cargo, go.sum).
2. For pip-tools: `--generate-hashes`; refuse raw unhashed `pip install pkg` in prod Dockerfiles.
3. Verify mirror integrity matches upstream when using internal caches.

### 6. Update strategy (move pins safely)

1. Enable Dependabot/Renovate (`dependabot-config-hardening` / `dependabot-group-updates`).
2. Patch cadence: weekly groups; majors isolated; security SLA separate.
3. After merge: release rebuild; avoid mutating pins directly on prod servers.
4. Periodic `npm outdated` / `cargo outdated` reports for visibility—not for unattended float.

### 7. Verify and hand off

```bash
# Reproducibility smoke (two clean installs)
rm -rf node_modules && npm ci && find node_modules -type f | sort | sha256sum | head
# Or compare lock resolution
npm ls --all > /tmp/tree1.txt
```

1. Prove release artifact dependency list matches lock (SBOM neighbor skill).
2. Document developer workflow: change manifest → refresh lock locally → PR both.
3. Apply `code-quality-standards` to any pinning automation scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| App build | `npm ci` + committed lock | `npm install` on release runner |
| Security fix | Bot PR updates lock | Delete lock “to get latest” |
| Library publish | Clear semver ranges | Pin all transitive deps in published wheel unnecessarily without docs |
| Actions | `actions/checkout@SHA` or immutable tag policy | `@master` |
| Docker | Install from lock | `pip install flask` unpinned |
| Ranges | Caret + lock for apps | Only ranges, no lock |

## Output Checklist

- [ ] Repo class and pin policy documented
- [ ] Lockfiles present and not gitignored for apps
- [ ] CI uses frozen/locked install commands
- [ ] Critical packages exact + review path defined
- [ ] Hash/integrity enabled where toolchain allows
- [ ] Update bot or manual cadence established
- [ ] Unpinned Actions/base images ticketed
- [ ] Reproducibility check evidence retained
- [ ] Developer “update lock” docs published
- [ ] Neighbors used for confusion/SBOM/Dependabot as needed

## Rules

- Reproducible builds beat floating “always latest” for production.
- Pins without an update path become unpatched risk—pair with bots/process.
- Never disable integrity checks to work around supply-chain issues.
- Library vs application policies differ; do not force one blindly.
- Authorized/owned repos only; keep tokens out of git.
