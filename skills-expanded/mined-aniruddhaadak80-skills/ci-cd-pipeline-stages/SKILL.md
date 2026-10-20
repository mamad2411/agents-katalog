---
name: ci-cd-pipeline-stages
description: "Stage ordering that fails cheap and fast: lint → unit → build → integration → deploy gates."
---
# Structure a fast, honest CI pipeline

> Stage ordering that fails cheap and fast: lint → unit → build → integration → deploy gates.

**Track:** ☁️ DevOps & Cloud · **Domain:** CI/CD · **Level:** intermediate · **~35 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Stage ordering that fails cheap and fast: lint → unit → build → integration → deploy gates.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Fail cheapest first: format+lint under 2 minutes before anything heavy
2. Parallelize independent suites; cache dependencies by lockfile hash
3. Run builds with strict env mirroring production
4. Gate deploys on required checks only; no manual memory of 'it passed locally'
5. Upload artifacts (coverage, bundles) visible in PR checks
6. Keep total pipeline under 10 min p95; split flaky suites out for quarantine

## Common Pitfalls

- Everything sequential behind one slow integration suite
- Cache keys ignoring lockfiles causing phantom dependency bugs

## Success Signals

- p95 pipeline under 10 minutes
- Flake rate below 1%

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill ci-cd-pipeline-stages
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill ci-cd-pipeline-stages -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills