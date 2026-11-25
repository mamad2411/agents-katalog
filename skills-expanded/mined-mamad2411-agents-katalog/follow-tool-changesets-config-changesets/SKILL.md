---
name: follow-tool-changesets-config-changesets
description: Configure `.changeset/config.json` — access, baseBranch, linked/fixed packages
argument-hint: "[scope]"
related:
  - setup-cicd
  - run-release
  - follow-secret-manager
---

## Goal

Configure `.changeset/config.json` to match the project's versioning policy — `access`, `baseBranch`, `fixed`/`linked` packages, `updateInternalDependencies`, `ignore` — by merging, never clobbering

## Scope

Use when editing an existing Changesets config — install/init lives in `workflows/setup-changesets/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: read the original config before editing

1. Read `.changeset/config.json` — record the current keys
2. Read the root `package.json` workspaces — list every publishable package
3. If there is no `.changeset/` → run `workflows/setup-changesets/SKILL.md` first

### 2. Core Options

> Goal: set the core keys correctly

1. `"$schema"` — point at the `@changesets/config` schema matching the installed major version
2. `baseBranch` — default `"main"`, follow the repo's actual branch
3. `access` — `"restricted"` for scoped/private packages, `"public"` for public npm packages
4. `updateInternalDependencies` — `"patch"` to bump internal deps when a patch changes
5. `commit` — `false` to let git handle commits, or `true`/`@changesets/cli/commit` per the workflow
6. `ignore` — list packages that are not published (private apps, tooling packages)
7. `changelog` — default `"@changesets/cli/changelog"`, or a custom changelog generator if PR links are wanted

### 3. Linked And Fixed Packages

> Goal: define the version coupling of packages

1. `fixed` — array of package groups that always share one version (bump together and stay equal), e.g. `[["@scope/a", "@scope/b"]]`
2. `linked` — array of package groups that bump together but may hold different versions
3. Choose `fixed` when packages must release in lockstep; `linked` when they coordinate but versions may differ
4. Verify every package in the groups actually exists in the workspaces — a typo is a config error

### 4. Verify

> Goal: check the config is correct

1. Run `bunx changeset status` — the config must parse and show pending changesets
2. Create a test changeset and run `bunx changeset version` on a separate branch — confirm the fixed/linked bumps behave as intended (revert after checking)
3. If it breaks → revert the edited keys and report the diff with `/report-before-after`

## Rules

### 1. Merge Discipline

- Edit only the necessary keys — never overwrite the whole file
- Keep `$schema` matching the installed `@changesets/cli` major version

### 2. Version Coupling

- `fixed` = always the same version; `linked` = bump together but versions may differ — pick per the release policy
- private packages that are not published must be in `ignore`

### 3. Access

- `access: "restricted"` for scoped packages that are not public — getting this wrong fails the publish
- secrets (`NPM_TOKEN`) must never be in the config — keep them in env/secrets manager

- Use /run-release if needed

## Expected Outcome

- `.changeset/config.json` correct per the versioning policy
- `fixed`/`linked` groups behave as intended
- `changeset status` and `version` run cleanly
