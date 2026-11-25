---
name: follow-create-github-action
description: Build GitHub Actions with TypeScript, composite, or Docker
argument-hint: "[scope]"
related:
  - follow-create-bun-cli
  - follow-create-sdk
  - follow-create-web
  - follow-dot-github
  - follow-release
  - follow-tool-github-actions
  - run-test
  - deep-review-codebase
  - report

---
## Goal

Build a GitHub Action that runs inside workflows, supporting TypeScript, composite, and Docker actions with `action.yml`, build, tests, and release

## Scope

Use when creating actions for GitHub Marketplace or private repos, covering inputs, outputs, runs, branding, and `dist/` for TS actions

- Packages: `@actions/core`, `@actions/github` + bundler (`esbuild`/`@vercel/ncc`) — always confirm the latest versions and `runs.using` runtime with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`); pin `actions/*` with the latest major version tag from the marketplace (verify before use)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest `@actions/*` packages and `runs.using` runtime, then run `/deep-review-codebase` to summarize the tech stack
2. Record the rationale for the chosen stack and libraries for future reference (create github action)
3. Record the rationale for the chosen stack and libraries for future reference (create github action)

### 2. Choose Action Type

> Goal: pick the action type

1. For complex logic: use `node24` + TypeScript (node20 deprecated — runners require node24 since 2026-06 and drop node20 on 2026-09-23)
2. To chain multiple commands: use `composite`
3. For a fully controlled environment: use `docker`
4. Define the required inputs and outputs

### 3. Setup Project

> Goal: scaffold the action structure

1. Create a repo or directory for the action
2. Create `action.yml` at the root
3. Create `README.md` documenting usage
4. Create `.github/workflows/ci.yml` to test the action

### 4. Write action.yml

> Goal: define the action manifest

1. Set `name`, `description`, `author`, `branding`
2. Define `inputs` with `required`, `default`, `description`
3. Define `outputs` for the results
4. Set `runs.using` to `node24`, `composite`, or `docker` (for `node24`, point `runs.main` at `dist/index.js`)

### 5. Implement Logic

> Goal: write the action logic

1. For TypeScript: create `src/index.ts` using `@actions/core`, `@actions/github`
2. For composite: define `steps` with `run` and `shell`
3. For Docker: create `Dockerfile` and `entrypoint.sh`
4. Pass secrets in via `core.getInput()` — never hardcode them

### 6. Build TypeScript Action

> Goal: build `dist/index.js` for TypeScript

1. Install `esbuild`, `@vercel/ncc`, or `rollup`
2. Run `bun run build` to bundle `src/index.ts` → `dist/index.js`
3. Include `licenses.txt` when using `ncc`
4. Commit `dist/` to the repo

### 7. Add Tests

> Goal: test the action

1. Create `__tests__/index.test.ts` for mocked inputs
2. Use `vitest` or `bun:test`
3. Create `.github/workflows/test.yml` to run the action on `workflow_call` or `push`
4. Verify outputs and side effects

### 8. Release

> Goal: create release tags

1. Create the git tag `v1.0.0`
2. Point the major tag `v1` at the latest commit
3. Create a GitHub release with release notes
4. Run `/ship`

## Rules

- Use `@actions/core` for inputs/outputs/exports
- Never log secrets or credentials
- TypeScript actions must commit `dist/index.js`
- Set `branding.icon` and `branding.color` in `action.yml`
- Use major version tags (`v1`) for consumers
- Test the action on a GitHub runner before releasing

- Use /follow-create-bun-cli if needed
- Use /follow-create-sdk if needed
- Use /follow-create-web if needed
- Use /follow-dot-github if needed
- Use /follow-release if needed
- Use /follow-tool-github-actions if needed (create github action)
- Use /run-test if needed
- Use /report if needed

## Expected Outcome

- `action.yml` is valid and `name` is unique
- The TypeScript action has an up-to-date `dist/index.js`
- Tests pass
- The action runs in a GitHub workflow
- Release tags `v1` and `v1.0.0` are correct

