---
name: follow-tool-bruno
description: Use the Bruno API client and bru CLI for collections, spec imports, and running tests in CI
argument-hint: "[scope]"
related:
  - deep-test
  - follow-tool-hurl
  - follow-tool-github-actions
  - follow-test

---

## Goal

Use Bruno to manage API collections in a Git-native way (`.bru` / OpenCollection files) and run tests via the `bru` CLI both locally and in CI/CD

## Scope

For projects that want an offline API client, collections as text files in the repo, and collection tests in the pipeline

- Latest: `@usebruno/cli@4.2.0` (verified 2026-09-24); GitHub Action `usebruno/bruno-cli-action@v1`
- If a lighter plain-text test format is needed (not the collection model) → `/follow-tool-hurl`; docs/mock from a spec → `/follow-tool-scalar`

## Execute

### 1. Installation

> Goal: install the Bruno CLI

1. Project dev-dep: `bun add -D @usebruno/cli` (binary named `bru`)
2. Global: `mise use -g npm:@usebruno/cli` or `npm i -g @usebruno/cli`
3. An official Docker image also exists for CI without Node
4. Verify with `bru --version`

### 2. Collection Structure

> Goal: understand the collection layout

1. Classic format: folders of `.bru` files + `bruno.json` + `environments/*.bru`
2. OpenCollection format (new default): `opencollection.yml` + `.yml` requests — human-readable YAML
3. No collection yet → create one from a spec with `bru import openapi` (next step) or run `/gen-postman-collection`

### 3. Import Specs

> Goal: convert OpenAPI/WSDL into a Bruno collection via the CLI

1. `bru import openapi --source <spec.yaml|url> --output <dir> --collection-name "API"` — default format `opencollection`, use `--collection-format=bru` for classic
2. Single file: `--output-file collection.json` instead of `--output`
3. WSDL (SOAP): `bru import wsdl --source <file.wsdl> --output <dir>`
4. Shorthand: `-s` (source), `-o` (output), `-n` (collection-name)
5. Details in 

### 4. Run Collections

> Goal: run a collection with env and reporters

1. `bru run <collection>` — add `-r` for recursive
2. Environment: `--env <name>`, `--global-env <name>`, `--env-var k=v`, `--env-file <file>`
3. Control: `--bail` (stop on failure), `--tags`/`--exclude-tags`, `--tests-only`, `--parallel`, `--iteration-count`, `--delay`, `--csv-file-path`/`--json-file-path` (data-driven)
4. Sandbox: `--sandbox safe` (default since v3) or `developer` when full Node APIs are needed
5. Reporters: `--reporter-json`, `--reporter-junit`, `--reporter-html` + `--reporter-skip-*` to hide secrets/bodies in artifacts

### 5. Secrets And Security

> Goal: handle secrets and TLS in CI

1. `--secrets-env-file` + `externalSecrets` block → fetch from HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Cloud Secret Manager (never written to disk/log)
2. mTLS: `--client-cert-config <config.json>`; CA: `--cacert`; proxy bypass: `--noproxy`
3. Never commit credentials — always use env vars/secret managers

### 6. GitHub Actions

> Goal: run Bruno in CI with the official action

1. Use `usebruno/bruno-cli-action@v1` — a composite action that prepends `bru` for you (write `run --env prod`, not `bru run --env prod`)
2. Auto-injects `--reporter-junit` when unspecified; exposes outputs: `exit-code`, `passed`, `failed`, `total`, `duration-ms`
3. Inputs: `command` (required), `bru-version`, `working-directory`
4. See workflow examples and downstream actions in 

## Rules

### 1. Collection Hygiene

- Keep the collection in the same repo as the API code — diffable in PRs
- Separate secrets from `.bru`/`.yml` files — use env vars or secret managers
- Pick one format per collection: `opencollection` (new) or `bru` (classic)

### 2. CI Discipline

- Use `--bail` for fail-fast, `--tests-only` when the collection mixes in exploratory requests
- Give `--reporter-junit` an explicit path when feeding downstream actions
- Pin `@v1` for compatible updates, or `@v1.x.y` when immutability is required

### 3. Safety

- `--sandbox safe` is the default — switch to `developer` only when collection scripts need Node APIs
- Do not run collections against production envs without user confirmation

- Use /deep-test api if needed
- Use /follow-tool-github-actions if needed (tool bruno)

## References




- Use /follow-test if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Bruno collections under version control with environments
- `bru import openapi` builds a collection from a spec inside the pipeline
- `bru run` executes via CLI with full reporters
- The GitHub Actions workflow runs collections with the official action and gates on the exit code
