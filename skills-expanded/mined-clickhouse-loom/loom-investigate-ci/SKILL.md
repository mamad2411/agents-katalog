---
name: loom-investigate-ci
description: Takes a failing Loom CI check to its cause and fix — the failed log, whether main fails too, a local reproduction. Use when a PR check is red, a PR shows no checks, a job looks flaky, or when asked why CI fails. Not for bugs found outside CI (loom-debug).
argument-hint: "[pr-number | run-url]"
metadata:
  internal: true
---

# Investigating Loom CI

## 1. Which job, which line

```bash
gh pr view <n> --json statusCheckRollup --jq '.statusCheckRollup[] | select((.conclusion // .state) | IN("SUCCESS", "SKIPPED", "NEUTRAL") | not) | "\((.conclusion // "") as $c | if $c == "" then (.state // .status) else $c end)\t\(.name // .context)\t\(.detailsUrl // .targetUrl)"'
gh run view <run-id> --log-failed | tail -200
```

No checks at all: the PR is stacked on a branch other than `main` or a `release/X.Y` line (retarget it), has a merge conflict, or the push was a no-op.

## 2. Is it yours?

```bash
gh run list --workflow ci.yml --branch main -L 5 --json conclusion,headSha,createdAt
```

- `main` red on the same job: the cause is on `main`. Run the failing test on a clean `origin/main` worktree before touching your branch. A test with a literal date in its fixture and a wall-clock staleness check fails the first day the date ages out; the fix is the clock seam, not a new date.
- `main` green, your branch red: your change, or your change combined with something that merged since your base — rebase on `origin/main` and re-run locally.

## 3. By job

| Job | Usual cause | Reproduce / fix |
| --- | --- | --- |
| `the ClickHouse release this run tests` (`ci.yml`, `docker-smoke.yml`) | the release lookup in `dev/clickhouse_release.sh` or the registry it reads | rerun once; if it fails again, run the script locally and read its error |
| `Quickstart (<arch>)` (`docker-smoke.yml`, on PRs and pushes to `main` or a `release/X.Y` line touching its `paths:`, weekly and on dispatch) | the image or its bundle, the quickstart stack, then the one-line installer in clean containers (`scripts/gates/installer_rehearsal.py`; its FAIL lines name the distribution they ran on); on a weekly or dispatched run, a scan step: a critical CVE with a fixed release in the image | the dashboard test dependencies CI installs first (`npm --prefix frontend ci && npx --prefix frontend playwright install chromium`, after `loom-dev-setup` §6's link check), `docker build -t "loom:smoke-$(basename "$PWD")" .`, then `python3 scripts/gates/docker_quickstart_smoke.py --image "loom:smoke-$(basename "$PWD")" --clickhouse-image <image>` (a tag per worktree: two sessions share the image store; `docker rmi` it afterwards), with the image from `bash dev/clickhouse_release.sh`. The rehearsal, with the tags fetched and Docker on `/var/run/docker.sock`: `python3 scripts/release/build_stack_bundle.py build --version <server __version__> --clickhouse-image <image> --output-dir <dir>`, then `python3 scripts/gates/installer_rehearsal.py --release-dir <dir> --upgrade --image <server image> --extractor-image <extractor image>`. A scan: build with `docker build --no-cache` (a cached apt layer keeps a fixed package), then `trivy image --severity CRITICAL --ignore-unfixed` on it names the package; move the pin that brings it in (a `Dockerfile` `ARG`, the base-image digest for a package the base image carries, or a lock file) |
| `Repository-job sandbox under the shipped profiles` (`docker-smoke.yml`) | the AppArmor or seccomp profile, or a sandbox change the profile blocks | the profiles row of `loom-pre-push` §3 |
| `ruff + mypy-gate` (lint) | a generator `--check` is stale (the plugin sync also compares executable bits); ruff; function-length or mypy ratchet | `make lint`, `make typecheck`; run the named generator without `--check` and commit its output; split the long function |
| `pytest unit part k` | order dependence; two tests sharing a file or port while they run side by side; a fake that drifted; a snapshot; a migration number `main` took since your base (renumber per the `migrations` rule) | the reproduction in [`tests/README.md`](../../../tests/README.md), with the part's `LOOM_TEST_SHARD=k/6` on the commands that name `tests/unit`; update a snapshot only for an intended change |
| `pytest unit coverage, floors and bench` | the combined coverage under 40% or a per-module coverage floor; a bench harness; `integrations/generic/test.sh` | the coverage-floor command in `loom-pre-push` §3; `pytest bench -q`; `PYTHON=.venv/bin/python bash integrations/generic/test.sh` |
| `repository-job sandbox (real bubblewrap)` | a change to the repository-job sandbox or the files it runs | the sandbox-suite row of `loom-pre-push` §3 |
| `schema.sql in sync with migrations` | `schemas/schema.sql` dumped from another ClickHouse release, or not regenerated | start a private ClickHouse on the release the run names (job "the ClickHouse release this run tests"): `LOOM_CLICKHOUSE_IMAGE=clickhouse/clickhouse-server:<ver>` plus the name and ports of `loom-dev-setup` §3, `bash dev/ci_start_clickhouse.sh`; migrate; `make schema-dump` |
| `builds N-1 and N on one ClickHouse` (mixed-version) | N writes something N-1 cannot read, or a lease or bundle rule broken | `make test-mixed-version REQUIRE=1` (docker); [rolling upgrades](../../../docs/architecture/rolling-upgrades.md) names the rule |
| `format` | an unformatted file; a dashboard accessibility rule (step "biome lint (dashboard accessibility)") | `make format` from the repository root (the pinned Biome reads `biome.json` there); `make lint` for the accessibility rules, fixed in the TSX ([dashboard design](../../../docs/development/dashboard-design.md#checks)) |
| `helm chart (lint, kubeconform)` | a template or value that does not render, or a manifest that fails the schema | the `deploy/helm/` row of `loom-pre-push` §3 |
| `coding-agent plugins` | a hook, grep-shim or Cursor test; a syntax error in a shipped `.mjs`; a non-executable `integrations/grep-shim/bin/` entry point | the commands of the `integrations/` row in `loom-pre-push` §3, which mirror the job's steps |
| `tsc (frontend)` | types, bundle budget | `npm --prefix frontend run build && npm --prefix frontend run budget` |
| `frontend vitest part k` | a vitest or axe failure | `npm --prefix frontend run test -- --shard=k/n`, n being the parts in the job's matrix in `ci.yml`, or `npm --prefix frontend run test` for all of it |
| `frontend playwright part k` | an e2e spec failure | `npx --prefix frontend playwright install chromium` once (its system libraries, `playwright install-deps`, only on a machine you own), then `E2E_PORT=<free port> npm --prefix frontend run e2e -- --shard=k/n`, n as above; the part's traces are the `frontend-e2e-k` artifact |
| `typescript sdk (...)` | generated types stale, lint, a vitest failure, the ESM/CJS dist build, publint or attw | `.venv/bin/python -m scripts.codegen.sdk_ts_gen`, then `npm --prefix sdk/typescript run check && npm --prefix sdk/typescript run check:dist` |
| `python sdk wheel (...)` | an undeclared dependency or a 3.12-only API (3.11 legs), a pin floor lower than the code needs (lowest-deps legs), a new release of a dependency (the other legs) | the `sdk/python/` row of `loom-pre-push` §3, on the leg's Python and with `--resolution highest` unless the job name says lowest deps |
| `pytest integration part k of 4`, `pytest integration isolation gates` | behaviour change; a test that needs an env CI lacks (self-signup) | the failing file, or the part (`LOOM_TEST_SHARD=k/4`), against a private server (`loom-dev-setup`); the isolation gates part runs the provider staging tests (`LOOM_PROVIDER_STAGING_LIVE_TEST=1`, on a freshly migrated database), the auth-on gates (reproduce against a server with `LOOM_AUTH_REQUIRED=true`) and the analyzer corpus; the failure report lists the last requests with `X-Request-Id` to find the server log line |
| `pytest integration (Postgres n memory authority)` | a read or write path that skips the Postgres authority; a head and its ClickHouse copy out of step | `LOOM_PG_IMAGE=postgres:n bash dev/ci_start_postgres.sh`, then the failing file against a private server with `LOOM_STORAGE_AUTHORITY=postgres` and `LOOM_PG_DSN` set as the job sets them |

## 4. Flaky or real

A failure is flaky only when the same commit passes on re-run *and* you can name the race (timing, order, a shared resource). Re-run once with `gh run rerun <run-id> --failed`; a second failure is real. Name the cause in the PR even when it is flaky, and fix the test rather than adding retries.

## 5. Report

The failing job and line, the root cause, whether `main` is affected, the fix (or the commit that fixes it), and the local command that now passes.
