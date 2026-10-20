---
name: dependabot-config
description: "Configure Dependabot update ecosystems, schedules, groups, and ignore rules in dependabot.yml."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["dependabot", "dependencies", "security", "github", "devops", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Dependabot Configuration AI Skill Guide

## Overview & Engine Architecture

Dependabot opens pull requests that bump dependency versions and alert on known vulnerabilities. Configuration lives in `.github/dependabot.yml` per ecosystem (npm, pip, docker, github-actions, terraform, etc.). Agents tune schedules, group related updates, ignore noisy packages deliberately, and require CI green before merge.

```
.github/dependabot.yml
   -> GitHub Dependabot service
       -> Version update PRs + security updates
           -> CI checks -> human/auto merge
```

## When to use this skill

- Enabling or retuning dependency update bots
- Reducing PR floods with groups and schedules
- Ignoring packages that must stay pinned
- Aligning security updates with SCA tools like `@snyk`

## Operational directives

1. Commit a valid `dependabot.yml` under `.github/`.
2. Prefer weekly schedules for apps; daily only if you can review volume.
3. Group minor/patch updates where supported to cut PR noise.
4. Never ignore all updates globally; ignore specific deps with reasons in comments/docs.
5. Auto-merge only patch/minor with required status checks - never blind major auto-merge.

## Config sketch

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
      day: monday
    open-pull-requests-limit: 10
    groups:
      production-patch:
        dependency-type: production
        update-types: ["minor", "patch"]
    ignore:
      - dependency-name: "legacy-sdk"
        versions: [">=3.0.0"]

  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly

  - package-ecosystem: docker
    directory: "/"
    schedule:
      interval: weekly
```

## Tuning matrix

| Problem | Adjustment |
| --- | --- |
| Too many PRs | Groups + lower limit + weekly interval |
| Majors break CI constantly | Manual majors; group only minor/patch |
| Private registry fails | Configure registry credentials in Dependabot secrets |
| Lockfile conflicts | Smaller groups; rebase settings; keep CI fast |

## Best practices

- Review security updates faster than routine version bumps.
- Keep Actions pinned to SHAs if that is org policy; Dependabot can still propose bumps.
- Document ignored dependencies in the repo security doc with owners.
- Pair with `@snyk` or GitHub Advisories - Dependabot is not the only signal.

## Limitations

- Ecosystem support and grouping features evolve - verify against current GitHub docs.
- Monorepos may need multiple `directory` entries.
- Some private/monolithic packages do not update cleanly without custom registries.

## Related skills

- `@snyk` - complementary SCA scanning and fix advice
- `@github-packages-npm` - private package consumption that Dependabot must authenticate to
- `@codeql` - code vulnerability scanning beside dependency bumps
