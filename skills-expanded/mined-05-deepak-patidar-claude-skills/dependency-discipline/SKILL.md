---
name: dependency-discipline
description: Choosing, pinning, upgrading, and auditing third-party dependencies — and supply-chain safety. Use when adding a library or framework, running npm/pip/cargo installs, responding to a CVE or security advisory, upgrading major versions, or when the user says "which library", "add a package", "dependency", "vulnerability alert", "outdated packages", or "supply chain".
---

# Dependency Discipline

Every dependency is code you now ship, maintained by strangers, on their schedule, with your name on the incident. `npm install` is the easiest way to adopt a liability while feeling productive. The discipline: **adopt deliberately, pin exactly, upgrade continuously, and keep the exits marked.**

## Gate 1: Before adding — the adoption review

First question: **can 30 lines of your own code do this?** For anything smaller than a real domain (left-pad-class utilities, one date format, a simple retry), writing it beats importing it — your 30 lines have no transitive tree, no CVE feed, no maintainer burnout. Import for genuine domains: crypto (NEVER hand-roll — threat-model-security), parsers for messy formats, timezone data, database drivers, frameworks.

If importing, spend five deliberate minutes:
- **Aliveness**: commits/releases in the last year, issues getting answers, more than one maintainer (bus factor). A dead dependency is a fork you haven't admitted to yet.
- **Weight**: what does it drag in transitively? (`npm ls`, dependency graph). A 3-line convenience with 40 transitive deps is a bad trade; prefer libraries with shallow trees.
- **Blast radius when it breaks**: dev-only tool (low bar) vs runtime-critical path vs touches-money-or-auth (high bar: popularity, audit history, and your own reading of its core code).
- **License** compatible with your use (GPL in a proprietary SaaS backend is usually fine; in distributed code it's a legal meeting).
- **Exit cost**: how hard to replace later? High-exit-cost deps (frameworks, ORMs) deserve real evaluation; for the rest, keep them behind your own adapter so the exit stays cheap (architecture-design).

## Gate 2: Pinning — builds must not drift

- Lockfiles committed, always, and honored in CI/production installs (`npm ci`, `pip install -r requirements.txt` with pins, `poetry.lock`, `cargo.lock`). An unlocked build means yesterday's green and today's deploy are different software (deployment-safety Gate 1).
- Docker base images by specific tag (ideally digest), never `latest`. Same for GitHub Actions (`@v4` minimum; SHA-pin for anything with secrets access).
- The rule: **a rebuild with no code change produces the same artifact.** Any violation of that is a drift channel; close it.

## Gate 3: Upgrading — small, often, boring

The counterintuitive truth: teams that upgrade *more often* have *fewer* upgrade disasters. Staying two majors behind doesn't avoid the migration; it batches it into a death march with security pressure attached.

- Cadence: patch/minor updates in a regular small batch (monthly, or automated via Renovate/Dependabot with CI gating); major versions individually, deliberately, reading the changelog/migration guide first.
- One dependency (or one coherent batch) per PR, tests green, deployed normally — so when something breaks, `git bisect` has one suspect (root-cause-debugging: "find what changed").
- Read the changelog *before* upgrading, not after the incident. Breaking changes announce themselves; nobody listens.
- Framework/language runtime upgrades are projects, not chores: branch, upgrade, run the full suite + golden-path verification, then merge — not "bump it and see".

## Gate 4: Vulnerability response — triage, don't panic

Scanner alerts (Dependabot/`npm audit`/`pip-audit`) are inputs, not verdicts. Triage each:
1. **Is the vulnerable path reachable in your usage?** A ReDoS in a dev-only build tool ≠ an RCE in your request parser. Severity × reachability = your actual priority.
2. Reachable + serious → patch now via the smallest jump that fixes it, deploy through the normal (fast) pipeline.
3. Not reachable → note the reasoning, schedule with the regular batch. Suppressing alerts silently trains everyone to ignore the channel (observability-readiness's alert-fatigue rule applies).
4. No fix released? Mitigate (disable the feature, input-validate ahead of it, vendor-patch as last resort) and track the upstream issue.

## Supply-chain paranoia (the part everyone skips until it's news)

- New-package hygiene: check the exact name (typosquats live on one-letter differences), the publish date vs popularity (a "popular" package published last week is a flag), and whether install scripts run (`--ignore-scripts` where feasible).
- CI is the crown jewel: it holds your secrets and builds your artifacts. Third-party CI actions/plugins get the same adoption review as runtime deps, pinned by SHA.
- Your registry account (npm/PyPI) with publish rights gets 2FA — you're someone else's supply chain too.
- Periodic pruning: every dependency audit removes something. Unused deps are pure attack surface; `depcheck`/`pip-extra-reqs`-class tools find them.

## The ledger

Keep the *why* of non-obvious dependencies findable (ADR line, lockfile comment, or docs): "we use X over the popular Y because Z". Six months later, someone (or some AI) will "simplify" by swapping it back, rediscovering Z in production (docs-and-runbooks).
