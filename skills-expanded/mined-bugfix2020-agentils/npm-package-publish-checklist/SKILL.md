---
name: npm-package-publish-checklist
description: 'Use when: preparing, reviewing, publishing, or fixing an npm package, scoped package, CLI package, .npmrc, .npmignore, publishConfig, package.json files, README, npm pack, npm publish, pnpm publish, or release metadata.'
---

# npm Package Publish Checklist

Use this skill before publishing or reviewing any npm package in this workspace.

## Sources To Trust

- npm package README docs: package pages render the package-root `README.md`; include installation, configuration, usage, and other helpful user information.
- npm scoped public package docs: scoped public packages should publish with `npm publish --access public` or equivalent package metadata.
- npm packlist behavior: package contents are controlled by `package.json.files`, `.npmignore` / `.gitignore`, and npm always-included files such as `package.json` and README files. Prefer a small `files` whitelist and verify with `npm pack --dry-run`.

## Required Package Checks

For the target package root, inspect and configure:

- `package.json` has the intended `name`, `version`, `description`, `type`, `main`, `module`, `types`, `bin`, `exports`, `files`, `engines`, `dependencies`, and scripts.
- `package.json` includes `repository` and `license` fields (required for npm OIDC provenance):
    ```json
    "repository": {
        "type": "git",
        "url": "https://github.com/bugfix2020/AgentILS",
        "directory": "packages/<package-name>"
    },
    "license": "MIT"
    ```
    Without `repository.url`, OIDC publish fails with `E422 repository.url is empty`.
- Scoped public packages include `publishConfig.access = "public"`.
- Packages intended for npm include `publishConfig.registry = "https://registry.npmjs.org/"`.
- Package-level `.npmrc` sets:

```ini
registry=https://registry.npmjs.org/
access=public
```

- Package-level `.npmignore` excludes source and build-only files that should not be packed, even when `files` is present:

```gitignore
src/
tsconfig.json
tsup.config.ts
*.tsbuildinfo
node_modules/
dist/**/*.map
```

Adjust the ignore list for packages that intentionally publish source, templates, or source maps.

**Source maps pitfall**: when `files` includes `"dist"`, the `.npmignore` `dist/**/*.map` rule is ignored because `files` takes precedence as a whitelist. To actually exclude source maps, use a specific glob with negation in `files`:

```json
"files": [
    "dist/**/*.js",
    "dist/**/*.d.ts",
    "!dist/**/*.map"
]
```

Always verify with `npm pack --dry-run` that no `.map` files appear in the tarball.

## README Checks

The package-root README should let a user understand the package without reading source code:

- What the package is.
- What problem it solves.
- How to install or run it with common package managers.
- Copy-paste usage examples.
- CLI/API options if applicable.
- Agent/LLM behavior notes if the package is meant for agents.
- What the package does not do, if scope boundaries matter.

Use the existing package README style in this repo when possible. For Chinese package docs, compare against `packages/quality-gate/README.zh-CN.md`.

### Standard README Structure

Every publishable package in this repo must follow this structure (established by `@agent-ils/quality-gate` and `@agent-ils/logger`):

```markdown
# <Package Title>

<p align="center">
  <!-- npm version badge (required) -->
  <a href="https://www.npmjs.com/package/<scope>/<name>">
    <img alt="npm" src="https://img.shields.io/npm/v/<scope>/<name>?label=npm&color=CB3837">
  </a>
  <!-- tech stack badges -->
  <img alt="TypeScript" src="..."> ...
</p>

<p align="center">
  English | <a href="<GITHUB_ABSOLUTE_URL>/README.zh-CN.md">简体中文</a>
</p>

One-line description.
What it does NOT do.

## Install / Usage

pnpm / npm / yarn / bun examples

## ... feature sections

## API

export table

## What It Does Not Do

explicit boundaries
```

### Link Rules for npm Compatibility

npm renders the package-root `README.md` on the package page. Files not included in the npm tarball (via `files` or `.npmignore`) cannot be linked with relative paths.

**Always use GitHub absolute URLs for:**

| Target         | Relative (broken on npm) | Absolute (works everywhere)                                                       |
| -------------- | ------------------------ | --------------------------------------------------------------------------------- |
| Chinese README | `./README.zh-CN.md`      | `https://github.com/bugfix2020/AgentILS/blob/main/packages/<pkg>/README.zh-CN.md` |
| English README | `./README.md`            | `https://github.com/bugfix2020/AgentILS/blob/main/packages/<pkg>/README.md`       |
| Examples dir   | `./examples/...`         | `https://github.com/bugfix2020/AgentILS/tree/main/packages/<pkg>/examples/...`    |
| LLM_USAGE.md   | `./LLM_USAGE.md`         | `https://github.com/bugfix2020/AgentILS/blob/main/packages/<pkg>/LLM_USAGE.md`    |

Reference implementations: `packages/quality-gate/README.md`, `packages/logger/README.md`.

## Verification Commands

Run from the repository root unless the package requires otherwise:

```sh
pnpm --filter <package-name> typecheck
pnpm --filter <package-name> build
```

Run from the package root:

```sh
npm pack --dry-run
```

Check the tarball output for:

- Correct package name and version.
- `README.md` included.
- `package.json` included.
- Expected `dist` files included.
- Source files, tsconfig, tsup config, tsbuildinfo, node_modules, and unwanted maps excluded.

For CLI packages, also run the built CLI:

```sh
node <package-root>/dist/<entry>.js --version
node <package-root>/dist/<entry>.js --help
```

The CLI version should come from `package.json`, not a duplicated hard-coded constant.

## Changeset Gate (CI)

CI enforces a changeset check on every PR that modifies publishable package release scope. This includes `packages/quality-gate/**`, `packages/logger/**`, `packages/workflow-sdk/**`, and `packages/logger-collector/**` because the collector binary is released from `@agent-ils/logger@*` tags. If release-scoped files are changed but no new `.changeset/*.md` file is added, CI fails.

Before pushing a PR that touches release-scoped files:

```sh
pnpm changeset
# Select the affected package(s), choose bump type (patch/minor/major), write a summary.
```

For `packages/logger-collector/**`, select `@agent-ils/logger`.

The generated `.changeset/*.md` must be committed alongside the code changes. This applies to feature branches too — do not wait until the release branch.

## First-Time Publish

New packages must be published manually from local before CI (Trusted Publisher / OIDC) can take over.

Use the automated script:

```sh
node scripts/dev/npm-first-publish.mjs <package-name>
```

This script handles: login check → package existence check → build → verify (`npm pack --dry-run`) → publish (with OTP/2FA support) → git tag.

After the first publish, configure Trusted Publisher on the npm package page:

```
https://www.npmjs.com/package/<name>/access
```

Add `bugfix2020/AgentILS` as a trusted publisher with the `release.yml` workflow. After this, all subsequent publishes are handled automatically by CI.

## Automatic CI Publish (changeset flow)

After the first manual publish and Trusted Publisher setup, all publishes are automatic:

1. Developer adds `.changeset/*.md` alongside code changes in a feature PR.
2. PR merges to `main` → release workflow runs `pnpm changeset version` → creates/updates "Version Packages" PR.
3. "Version Packages" PR merges → release workflow runs `pnpm changeset publish` → publishes to npm via OIDC.

**No manual `npm publish` needed after first-time setup.**

## Release Branch & Tag Workflow (Manual Override)

Every publish must be reproducible from `main`. Do not publish from an integration branch or a local-only commit.

1. Sync `main`:

    ```sh
    git checkout main
    git pull origin main
    ```

2. Cut a dedicated release branch named `chore/release-<package>-<version>` (matches `branch-name-standard` skill):

    ```sh
    git checkout -b chore/release-quality-gate-0.0.2 main
    ```

3. Bump only the target package's `package.json` `version` field. Do not bundle unrelated changes into a release commit.
4. If the publish ships behavior changes, ensure the matching feature/fix commits are already on `main` before opening the release PR.
5. Commit with a `chore(<package>): release v<version>` message and push the branch:

    ```sh
    git add packages/<package>/package.json
    git commit -m "chore(<package>): release v<version>"
    git push -u origin chore/release-<package>-<version>
    ```

6. Open a PR against `main`, get it merged (squash or merge commit, repo default).
7. After merge, sync `main` locally, then publish from `main`:

    ```sh
    git checkout main && git pull origin main
    pnpm --filter <package-name> build
    cd packages/<package>
    npm pack --dry-run    # final sanity check
    npm publish
    ```

8. Tag the published commit and push the tag. The tag name is always the full
   npm package name plus the version:

    ```sh
    git tag <package>@<version>
    git push origin <package>@<version>
    ```

    Examples:

    ```sh
    git tag @agent-ils/logger@0.1.2
    git tag @agent-ils/quality-gate@0.0.3
    ```

    Do not use repository-level semver tags such as `v0.1.2`, and do not use
    shortened package names such as `logger@0.1.2`.

This keeps `npm view <pkg>` `dist.tarball` ↔ git tag ↔ `main` commit in 1:1 correspondence so any future bisect or PR review can trace a published artifact back to the exact tree.

### Pre-existing Version Conflicts

`npm` rejects republishing the same `version` even with different content (`E403 cannot publish over previously published versions`). If `npm view <pkg> versions` shows the version already exists (possibly from a prior squatter or earlier release), bump to the next available patch version on the release branch instead of trying to overwrite.

## Common Mistakes

- Missing `repository` field in `package.json` — npm OIDC provenance requires `repository.url` to match the GitHub repo. Without it, publish fails with `E422 repository.url is empty`.
- Missing `license` field in `package.json`.
- New packages starting at `version > 0.0.0` — must start at `0.0.0` and let changesets bump to `0.0.1` on first release.
- Using `minor` instead of `patch` in changeset for a new package's first release — first release should be `patch` (0.0.0 → 0.0.1), not `minor` (0.0.0 → 0.1.0).
- Publishing from `dev` or a feature branch — the npm tarball commit will not exist on `main` and `repository.directory` traceability breaks.
- Forgetting to configure Trusted Publisher (OIDC) after first manual publish — CI auto-publish will fail with `E404` or `E422` until configured at `https://www.npmjs.com/package/<name>/access`.
- Relative links in README (`./examples/...`, `./README.zh-CN.md`) — these break on npmjs.com because the files aren't in the tarball. Always use GitHub absolute URLs.
- Updating README after publishing; npm package README updates only when publishing a new package version — if you fix README links, you need a new changeset to trigger a version bump + republish.
- Removing `private: true` but forgetting `publishConfig.access = "public"` for a scoped public package.
- Adding `.npmrc` but forgetting `.npmignore` or `files`.
- Trusting `.gitignore` without checking `npm pack --dry-run`.
- Publishing source maps unintentionally.
- Hard-coding a CLI version instead of reading package metadata.
- Forgetting to push the git tag after `npm publish` — the tag is the only durable bridge between npm and git history.
- Tagging a package release with `v<version>` or `<short-name>@<version>`
  instead of `<full-npm-package-name>@<version>`.
- Forgetting to add a `.changeset/*.md` file when modifying `packages/*` — CI will block the PR with "Verify changeset present" failure.
- Using `"files": ["dist"]` and expecting `.npmignore` to exclude `.map` files — `files` whitelist takes precedence, use explicit `!dist/**/*.map` negation instead.
