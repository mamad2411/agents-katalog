---
name: follow-release
description: Choose and set up a release strategy for npm, crates, Docker, VSCode and monorepo versioning
argument-hint: "[crates|docker|vscode-marketplace] [scope]"
related:
  - follow-tool-auto-it
  - follow-tool-semantic-release
  - follow-tool-release-it
  - follow-tool-pkg-new
  - follow-tool-changesets
  - run-release
  - run-check
  - run-build
  - run-test
  - run-verify
---

## Goal

Choose and set up the release strategy that fits the project — for npm, crates.io, Docker, VS Code Marketplace, preview, and monorepo versioning — with setup and deploy on the chosen platform

## Scope

Use when a project must release to external platforms or needs versioning, changelog, and preview releases for:
- npm: use `auto`, `semantic-release` or `release-it` for automated npm publish
- crates.io: use `release-plz` or `cargo-release` for Rust crates
- Docker: use Docker Hub or GHCR for container images
- VS Code Marketplace: use `vsce` for extension publish
- Preview: use `pkg.pr.new` or Changesets Snapshot
- Monorepo: use Changesets for versioning and changelogs

## Execute

### 1. Detect Release Targets

> Goal: identify the platforms the project will release to

1. Read `package.json` — check `private`, `publisher`, `workspaces`
2. Read `Cargo.toml` if a Rust crate exists
3. Read `Dockerfile` if a container image exists
4. Read `package.json` — check `publisher` and `engines.vscode` for a VS Code extension
5. Ask the user if it is unclear which release is wanted

### 2. Choose Release Strategy

> Goal: pick the appropriate strategy

For releasing to a real platform:
- npm/bun: run `/follow-tool-auto-it`, `/follow-tool-semantic-release` or `/follow-tool-release-it`
- Rust: do Step 3 (crates)
- Docker: do Step 4 (Docker)
- VS Code: do Step 5 (VS Code)

For previewing every PR/commit:
- run `/follow-tool-pkg-new` for continuous preview releases

For monorepo versioning/changelog:
- run `/follow-tool-changesets` to manage versioning and changelogs

### 3. Release To crates.io

> Goal: configure Cargo for automated releases to crates.io

1. check `Cargo.toml` has `name`, `version`, `authors`, `description`, `license`, `repository`, `homepage`, `keywords`, `categories`
2. install `cargo install release-plz` or `cargo install cargo-release` and set up the release-plz action
3. create config in `release-plz.toml` or `.release.toml` — set `changelog_config` to conventional and `release_branch: main`
4. add the API token from crates.io as `CARGO_REGISTRY_TOKEN` in GitHub secrets
5. create `.github/workflows/release.yml` — set `permissions: contents write, pull-requests: write`, `fetch-depth: 0`, `persist-credentials: false`, and jobs `release-plz-release` + `release-plz-pr`

### 4. Release To Docker

> Goal: configure Docker images for automated releases to Docker Hub or GHCR

1. check `Dockerfile` has a base image, labels, multi-stage build, and `.dockerignore`
2. choose between Docker Hub and GitHub Container Registry, then define the image name and tags
3. create an access token from Docker Hub or use `GITHUB_TOKEN` for GHCR
4. add `DOCKER_USERNAME`, `DOCKER_PASSWORD` as environment variables
5. create `.github/workflows/release.yml` — set `permissions: contents write, packages: write` and trigger from push to `main`

### 5. Release To VS Code Marketplace

> Goal: configure the VS Code extension for automated releases to the Marketplace

1. check `package.json` has `publisher`, `name`, `version`, `displayName`, `description`, `repository`, `bugs`, `homepage`, `engines.vscode`, `categories`, `keywords`
Latest: `@vscode/vsce@4.0.0` (verified 2026-09-16) — the original `vsce` package was renamed to `@vscode/vsce`

2. install `bun add -D @vscode/vsce` and use `bunx vsce` in scripts
3. create a publisher on `marketplace.visualstudio.com` and set it in `package.json`
4. create a PAT token from Azure DevOps as `VSCE_PAT` in environment variables, then run `vsce login publisher-name`
5. create `.github/workflows/release.yml` — set `permissions: contents: write`, the `VSCE_PAT` env, and trigger from push to `main`

### 6. Combine Changesets And pkg.pr.new

> Goal: use both together safely

- use `pkg.pr.new` for previews on every PR/Commit without touching npm
- use `Changesets` when merging into `main` for real releases to npm
- if you want a Changesets snapshot release, add a script:
  ```json
  {
    "scripts": {
      "release:snapshot": "changeset version --snapshot canary && changeset publish --tag canary"
    }
  }
  ```

### 7. Compare Preview Options

> Goal: choose the right preview release tool

| Capability | `Changesets Snapshot` | `pkg.pr.new` |
| --- | --- | --- |
| Package storage | Publishes to the real `npm Registry` | Hosted on StackBlitz's `CDN` |
| Install method | `bun add package-name@0.0.0-snapshot-...` | `bun add https://pkg.pr.new/owner/repo` |
| Cleanliness | Pollutes the `version history` on npm | Does not touch the `npm Registry` |
| Setup | Requires an `NPM_TOKEN` and a snapshot script | Zero config, no token needed |

### 8. Run Release

> Goal: complete the release successfully

1. verify tokens/permissions before releasing (`NPM_TOKEN`, `CARGO_REGISTRY_TOKEN`, `VSCE_PAT`, `DOCKER_PASSWORD`)
2. run `/run-release` for automated multi-platform release
3. verify tags, changelogs, and published artifacts

### Workflows

> Goal: dispatch to the workflow per release target

| Target/Argument | Workflow |
|-----------------|----------|
| `crates`, `cargo` | `workflows/deploy-crates/SKILL.md` — `cargo publish` to crates.io |
| `docker`, `image` | `workflows/deploy-docker/SKILL.md` — build/tag/push the Docker image |
| `vscode-marketplace`, `vsce`, `extension` | `workflows/deploy-vscode-marketplace/SKILL.md` — `vsce publish` to the Marketplace |

1. if the argument names a target → read `workflows/deploy-<target>/SKILL.md` and follow the flow there — do not execute directly from this table
2. if no target is given → follow steps 1-8 to choose the release strategy first

## Rules

### 1. Strategy Selection

- use `pkg.pr.new` for previews of every commit/PR
- use `Changesets` for real releases and changelogs
- use `semantic-release` or `auto` for conventional-commit-based releases

### 2. Package Configuration

- npm: check `name`, `description`, `version`, `author`, `private: false`, `publishConfig.access: public`
- crates: check `name`, `version`, `authors`, `description`, `license`, `repository`, `homepage`, `keywords`, `categories`
- Docker: check the `Dockerfile` is valid — base image, labels, multi-stage build, `.dockerignore`
- VS Code: check `publisher`, `name`, `version`, `displayName`, `description`, `engines.vscode`, `repository`, `categories`, `keywords`

### 3. Authentication

- npm: check `NPM_TOKEN` in GitHub secrets or `GITHUB_TOKEN`
- crates: check `CARGO_REGISTRY_TOKEN` in secrets or trusted publishing
- Docker: check `DOCKER_USERNAME`, `DOCKER_PASSWORD` or `GITHUB_TOKEN` for GHCR
- VS Code: check `VSCE_PAT` from Azure DevOps via `vsce login`

### 4. GitHub Workflow

- set `permissions` matching the platform
- use the trigger from push to the `main` branch
- crates: use `fetch-depth: 0`, `persist-credentials: false`, `concurrency` for the release-pr job

### 5. Safety

- keep preview workflows separate from real releases
- never accidentally publish a preview to the real npm
- verify tokens before running
- with `Changesets Snapshot`, beware of polluting the `version history`
- `pkg.pr.new` suits PR previews without touching the npm Registry
- Use /run-check if needed
- Use /run-build if needed
- Use /run-test all if needed
- Use /run-verify if needed

## Expected Outcome

- a release strategy that fits the project
- npm, crates.io, Docker, VS Code Marketplace set up correctly
- tools installed and fully configured
- authentication tokens ready to use
- GitHub workflows working on the chosen platform
- preview and real releases follow their flows
- no conflict between snapshot and official versions
