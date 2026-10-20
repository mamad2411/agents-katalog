---
name: github-packages-npm
description: "Publish or consume scoped npm packages through GitHub Packages, configure registry authentication, and troubleshoot package access."
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["github-packages", "npm", "registry", "publishing", "devops", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# GitHub Packages (npm) AI Skill Guide

## Overview & Engine Architecture

GitHub Packages hosts npm packages under `https://npm.pkg.github.com` tied to a GitHub user or organization. Publish with `publishConfig` and a scoped name (`@org/pkg`); authenticate with `GITHUB_TOKEN` in Actions or a PAT with `read:packages`/`write:packages` locally. Agents configure `.npmrc` correctly, avoid leaking tokens, and align package permissions with repo visibility.

```
package.json (name @org/pkg)
   -> npm publish
       -> npm.pkg.github.com
Consumers -> .npmrc (@org:registry=...) + token
```

## When to use this skill

- Publishing private or internal npm libraries to GitHub Packages
- Consuming `@org/*` packages in apps and Actions
- Migrating from npmjs private registries
- Debugging 401/403 publish or install failures

## Operational directives

1. Scope packages to the org (`@myorg/utils`); set `"registry": "https://npm.pkg.github.com"` in `publishConfig`.
2. Never commit tokens; use `NODE_AUTH_TOKEN` / `GITHUB_TOKEN` env substitution in `.npmrc`.
3. Grant least package permissions; `GITHUB_TOKEN` write is limited to the current repo unless workflows are configured otherwise.
4. Version with semver; prefer CI publish on tagged releases.
5. Document install steps for external contributors who need PATs.

## publishConfig sketch

```json
{
  "name": "@acme/sdk",
  "version": "1.4.0",
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}
```

## .npmrc sketches

```ini
# project or user level - token via env
@acme:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
```

```yaml
# GitHub Actions
- uses: actions/setup-node@v4
  with:
    registry-url: https://npm.pkg.github.com
    scope: "@acme"
- run: npm publish
  env:
    NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Common failures

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| 401 on install | Missing/invalid token | PAT with `read:packages` or SSO authorize |
| 403 on publish | Token lacks write / wrong repo | `write:packages` + package repo permissions |
| Package not found | Wrong scope registry mapping | `@org:registry=https://npm.pkg.github.com` |
| Duplicate version | Republish same semver | Bump version; do not force overwrite |

## Best practices

- Publish from CI on `v*` tags; keep local publish rare.
- Pair with provenance/signing policies your org requires.
- For public OSS, prefer npmjs.com; use GitHub Packages for private/internal.
- Delete/deprecate old packages carefully - consumers may pin exact versions.

## Limitations

- Cross-repo `GITHUB_TOKEN` publish permissions depend on Actions settings and org policy.
- Fine-grained PATs and classic PATs differ in package scopes - verify current GitHub docs.
- Yarn/pnpm registry config keys differ slightly from npm.

## Related skills

- `@dependabot-config` - update consumers of private packages carefully
- `@gpg-signing` - signed release tags before publish
- `@github-actions` - release workflow wiring
