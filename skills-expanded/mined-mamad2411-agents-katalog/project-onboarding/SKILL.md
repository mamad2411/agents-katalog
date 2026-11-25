---
name: project-onboarding
description: Execute or resume deterministic ADS onboarding for any software project. Use for "Onboard <project>", onboarding hardening, repository contract creation, local verification, legacy/production/Git reconciliation, or deciding whether a repository may be declared ONBOARDED. Support both the stack-neutral generic profile and the stronger Mauro PHP profile; never infer PHP-only requirements for unrelated repositories.
---

# Project Onboarding

Use the canonical flow in `ai-development-system/04-project-onboarding`. Do not invent a parallel checklist.

## Authority

Use this order:

1. target repository/workspace evidence;
2. ADS onboarding contracts and executable gates;
3. repository `.ai/project.json`, `AGENTS.md`, `PROJECT.md`, and `REPO_MAP.md` when present;
4. relevant shared skills;
5. assumptions, always marked and never used to pass a gate.

Production/FTP/SFTP may provide evidence or deployment transport, but is never the agent workspace.

## Canonical entry point

```bash
python3 <ADS_ROOT>/04-project-onboarding/scripts/ads_onboard.py onboard /absolute/project/root
python3 <ADS_ROOT>/04-project-onboarding/scripts/ads_onboard.py status /absolute/project/root
python3 <ADS_ROOT>/04-project-onboarding/scripts/ads_onboard.py verify /absolute/project/root
```

Treat `Onboard <project>` as authorization to continue through every safely resolvable phase. Return only when onboarding is complete or a genuine ambiguous/destructive blocker requires a human decision.

## First decision: profile

Do not assume the project is PHP.

### Generic

Use `generic` for repositories that do not follow Mauro's PHP application conventions: Python, Node/TypeScript, Go, Rust, Java, WordPress/non-standard PHP, CLI tools, libraries, static sites, and other software stacks.

The generic repository contract is:

```text
.ai/project.json
AGENTS.md
PROJECT.md
REPO_MAP.md          optional when topology is non-obvious
dev/verify-local.sh  project-owned deterministic verification
```

`dev/verify-local.sh` must run the real checks appropriate to that repository. Examples include `pytest`, `npm test`, `npm run build`, `go test ./...`, `cargo test`, linting, integration tests, browser checks, or any coherent combination. Do not require PHP parity, MySQL, a `.test` web URL, DB UI, or a web functional matrix unless the project itself actually needs them.

### Mauro PHP

Current Mauro PHP repositories use this configuration boundary:

```text
.env                  runtime-only, ignored; LOCAL_* + PROD_* values
  -> require/ads.php  reusable ADS::load() loader
  -> configure.php    thin application adapter
  -> existing app bootstrap
```

Requirements:

- `require/ads.php` owns `.env` parsing, process-env precedence, environment detection, local/production safety, `get()`, `bool()`, and `requireValues()`;
- `configure.php` calls `ADS::load(__DIR__)` and maps `$ADS->get(...)` into the constants/variables already expected by the application;
- use one root `.env`; do not recreate the old `.env.local` split;
- track `.env.example` with placeholders/examples only;
- preserve project-specific constants, paths, flags and bootstrap behavior instead of copying another application's adapter;
- old inline ADS routers and split `configure.local.php` / `configure.production.php` files are migration evidence, not the current target;
- existing repositories with a legacy machine profile id remain readable, but new onboarding should resolve to `mauro-php`.

For Mauro PHP, the stronger web/runtime certification remains applicable: PHP parity, local DB isolation where applicable, production-write isolation, local URL/path safety, runtime smoke, and representative functional verification.

## Mandatory flow

```text
request
  -> canonical GitHub Issue when durable work occurs
  -> identify workspace and Git authority
  -> resolve profile
  -> classify source/config/secrets/runtime data
  -> normalize only the profile-specific boundaries
  -> create/update .ai/project.json + repository knowledge
  -> establish project verification entry point
  -> execute verification
  -> clean/publish Git baseline
  -> final preflight/audit
  -> ONBOARDED
```

No later phase can hide an earlier `FAIL`, `UNKNOWN`, `UNAVAILABLE`, or `NOT_RUN` state.

## Repository knowledge

At minimum create/update:

- `AGENTS.md`: durable operating/safety/verification rules for any agent or orchestrator;
- `PROJECT.md`: durable project-specific purpose, stack, architecture, data, integrations, configuration, constraints and verification facts;
- `REPO_MAP.md`: only when repository structure is not obvious;
- `.ai/project.json`: machine-readable profile and verification pointer.

Use `ai-development-system/examples/repository/` as the reference shape. Do not copy transient task notes into these files.

## Skill composition

Load only what the project/task requires:

- Mauro PHP conventions: `mauro-coding-style`;
- Mauro CRUD framework: `mauro-crud`;
- MySQL persistent/schema work: `mysql-change-safety`;
- unknown defect: `bug-investigation`;
- frontend/responsive behavior: `frontend-change`;
- AI/LLM integration in PHP: `php-ai-integration`;
- review: `code-review`;
- non-trivial implementation planning: `feature-planning`.

Generic onboarding must not load Mauro-specific skills merely because the onboarding system itself is maintained by Mauro.

## Verification truth

A verification result must be reported as exactly one of:

- `PASS`;
- `FAIL`;
- `UNAVAILABLE`;
- `NOT_RUN`;
- `NOT_APPLICABLE`.

Missing evidence is never PASS.

For `generic`, the primary executable proof is the repository's `dev/verify-local.sh` declared in `.ai/project.json`.

For Mauro PHP, use the richer ADS local certification evidence in addition to the project verifier.

## Final gate

```bash
python3 <ADS_ROOT>/04-project-onboarding/scripts/onboarding_final_gate.py <workspace>
```

Do not declare `ONBOARDED` from narrative judgment. The finalizer must recompute current repository state and pass its executable checks.

## Reporting

Always return:

```text
STATE
PROJECT
PROFILE
WORKSPACE
VERIFICATION
GIT_HEAD / ORIGIN / UPSTREAM
GATES
```

Add runtime-specific fields such as `APP_URL`, `DB_UI_URL`, or PHP versions only when they actually apply. Add `BLOCKER` and `RESUME_ACTION` when not onboarded.

## Detailed gates

Read `references/deterministic-gates.md` before executing or changing onboarding.
