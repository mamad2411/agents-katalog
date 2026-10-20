---
name: dagger-pipelines
description: >
  Build portable CI pipelines with Dagger (SDK + engine) for owned repos: define
  containers as code, cache mounts, secrets handling, local+CI parity, and
  module reuse. Use when migrating brittle YAML CI to Dagger functions or
  debugging Dagger engine/graph execution — not for attacking CI of others.
---

# Dagger Pipelines

## Scope And Authorization

- **In scope:** Your organization's repositories, container registries, and CI runners.
- **Out of scope:** Using Dagger to exfiltrate secrets from shared runners you do not own; building pipelines that target unauthorized systems.
- Prefer secret mounts over baking credentials into images/layers.
- Pair with `cosign-sign-verify-ci` when publishing images and `code-quality-standards` for pipeline code.

## When To Use

- Same pipeline runs locally (`dagger call`) and in GitHub Actions/GitLab.
- Replacing long Docker-in-Docker scripts with typed SDK (Go/TS/Python).
- Sharing reusable Dagger modules across repos.
- Speeding builds with explicit cache volumes.
- Complex monorepo graphs.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Image signing | `cosign-sign-verify-ci` |
| GitHub OIDC to cloud | `github-actions-oidc-aws` |
| General Dockerfile hardening alone | container security skills |
| K8s deploy policy | deploy/GitOps skills |
| Implementation quality baseline | `code-quality-standards` |

## Architecture sketch

```text
CLI/CI -> Dagger Engine -> DAG of container execs / files / secrets -> artifacts
```

| Piece | Role |
| --- | --- |
| Dagger Functions / modules | Pipeline API you write |
| Engine | Executes graph, manages cache |
| Clients | Go, TypeScript, Python, etc. |
| CI glue | Thin workflow invokes `dagger call` |

## Workflow

### 1. Confirm scope and success criteria

1. Pipeline steps today (lint, test, build, push).
2. Success: local `dagger call test` matches CI; caches warm; secrets not in logs; artifacts published.

### 2. Bootstrap

```bash
# Install dagger CLI per official docs for your OS
dagger version
# In repo
dagger init
```

Choose SDK language matching team skills.

### 3. Define core functions

```go
// Illustrative Go SDK shape - check current Dagger API for your version
func (m *MyModule) Test(ctx context.Context) (string, error) {
    return dag.Container().
        From("golang:1.22").
        WithDirectory("/src", dag.Host().Directory(".", dagger.HostDirectoryOpts{
            Exclude: []string{"**/node_modules", ".git"},
        })).
        WithWorkdir("/src").
        WithExec([]string{"go", "test", "./..."}).
        Stdout(ctx)
}
```

Patterns:

1. Pin base images by digest.
2. `WithMountedCache` for module downloads (`GOPATH/pkg/mod`, yarn cache).
3. Separate functions: `Lint`, `Test`, `Build`, `Publish`.

### 4. Secrets

```bash
# Pass secrets at call time; don't echo
dagger call publish --registry-token=env:REGISTRY_TOKEN
```

1. Use Dagger secret types / scrubbing; never `WithEnvVariable("TOKEN", raw)` if avoidable.
2. CI: map from GitHub Actions secrets / OIDC short-lived tokens.
3. Ensure engine logs redaction.

### 5. CI wiring (GitHub Actions sketch)

```yaml
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dagger/dagger-for-github@v6  # pin by digest in high-assurance orgs
        with:
          version: "0.x.y"
      - run: dagger call test
      - run: dagger call build
        env:
          REGISTRY_TOKEN: ${{ secrets.REGISTRY_TOKEN }}
```

Keep CI YAML thin; logic lives in Dagger module (reviewable, testable).

### 6. Caching and performance

1. Explicit cache mounts per package manager.
2. Avoid copying entire monorepo when a subdir suffices.
3. Parallelize independent functions when graph allows.
4. Measure cold vs warm runs; document for developers.

### 7. Verify

```bash
dagger call test
dagger call build
# CI green on PR
# Confirm no secrets in dagger logs / GH logs
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Logic location | Dagger module | 500-line YAML script |
| Images | Digest pins | `:latest` floating |
| Secrets | Secret API / env scrub | Echo token in exec |
| Local parity | Same `dagger call` | Works only in CI |
| Modules | Versioned reuse | Copy-paste functions |

## Output Checklist

- [ ] Dagger CLI/engine version pinned
- [ ] Module functions cover lint/test/build
- [ ] Base images pinned by digest
- [ ] Cache mounts configured
- [ ] Secrets path verified non-leaking
- [ ] CI thin wrapper works
- [ ] Local and CI parity confirmed
- [ ] Publish/sign handoff if images shipped
- [ ] Developer README for `dagger call`
- [ ] Residual runner privileges noted

## Rules

- Treat pipeline code as production code (review, pin, test).
- Never log secrets; prefer OIDC short-lived creds.
- Focus on **Dagger pipeline authoring and operation**.
