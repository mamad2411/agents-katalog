---
name: loom-pre-push
description: Runs local format, lint, type checks and focused tests for a Loom diff, fixing failures at their source. The full unit suite and other heavy checks run in CI. Use before a commit or push, after a rebase, or when asked "is this ready". Not for opening the PR (loom-ship-pr).
metadata:
  internal: true
---

# Loom local checks

Run format, lint, type checks and tests focused on the changed behavior locally. The full unit suite, coverage and other heavy checks run in CI; do not hold a push for a complete local run. An explicit request can still authorize a full local reproduction.

## 1. What changed

```bash
git fetch origin main
git diff --name-only origin/main...HEAD
git status --short          # untracked files are part of the change too
```

## 2. Always

```bash
make format                 # rewrites; commit the result
make lint                   # ruff, function-length + secret gates, every generator --check, Biome a11y on frontend/src
make typecheck              # mypy --strict on the SDK + the server ratchet
```

Run them in the worktree's `.venv`, on CI's Python (3.12), with `LOOM_ENV_FILE=` so a local `.env` does not change what a snapshot or generator renders. Run the tests that reproduce the bug and cover the changed behavior. CI runs the full unit and benchmark suites with `pytest -n auto -p randomly`; reproduce a failure as [`tests/README.md`](../../../tests/README.md) describes.

## 3. By path

Use this map to select local checks and inspect the matching CI jobs. Full integration suites, coverage, image builds and end-to-end checks run in CI by default; they do not block publishing a reviewable PR. Run a focused local integration check when needed to verify the change.

| Paths touched | Also run |
| --- | --- |
| `schemas/migrations/` | `make schema-dump` against a private, freshly migrated ClickHouse (`loom-dev-setup`), then `make schema-check`; `git diff schemas/schema.sql` shows only your change |
| a migration, a row builder, an enum value, a wire format, worker leasing | `make test-mixed-version` — builds N-1 and N on one throwaway ClickHouse (needs docker; skips without it, CI fails) |
| `server/**/api/`, op registry | `.venv/bin/python -m scripts.codegen.<gen>` for `sdk_py_gen`, `sdk_py_client_gen`, `sdk_ts_gen`, `docs_reference`, `op_reach_census` (without `--check` each regenerates) |
| `server/settings/` | `.venv/bin/python -m scripts.codegen.settings_reference` |
| `server/cli/` | `LOOM_UPDATE_CLI_SNAPSHOT=1 .venv/bin/python -m pytest tests/unit/test_cli_surface_snapshot.py` in a 3.12 virtualenv (a newer Python renders the help differently) — then read the snapshot diff |
| a ClickHouse statement builder | `pytest tests/analyzer -q` against a private, migrated ClickHouse; regenerate with `LOOM_ENV_FILE= .venv/bin/python -m tests.analyzer.corpus --write` on fake providers ([analyzer corpus](../../../docs/development/testing.md#the-analyzer-statement-corpus)) |
| `server/workers/` | `LOOM_UPDATE_WORKER_SNAPSHOT=1 .venv/bin/python -m pytest tests/unit/test_worker_registry_snapshot.py` for an intended change |
| server behaviour | the integration suite against a private server (`loom-dev-setup` §7) |
| auth, write paths, erasure, migrations, the worker supervisor | the per-module branch-coverage floors CI enforces: `make test-unit-cov` (about 30 minutes on two cores, less with more) |
| `integrations/`, `.claude-plugin/` | `.venv/bin/python -m scripts.codegen.agent_plugin_sync`; `claude plugin validate integrations/claude-code-plugin --profile directory --strict` and `claude plugin validate .` (the plugin and the marketplace listing); `node --test integrations/claude-code-plugin/tests/*.test.mjs`, `node --test integrations/grep-shim/tests/*.test.mjs`, `node --test integrations/cline/tests/*.test.mjs`, `bash integrations/cursor/test.sh`, `PYTHON=.venv/bin/python bash integrations/generic/test.sh`, and CI's loops: `node --check` over every hook, helper, shim and adapter `.mjs`, `sh -n` over `integrations/{claude-code-plugin,codex-plugin}/bin/loom-node` and `integrations/cline/hooks/*`, and `test -x` over `integrations/grep-shim/bin/*` and `integrations/cline/hooks/*` (job `agent-plugins` in `.github/workflows/ci.yml`); with `claude` or `codex` installed, `node integrations/claude-code-plugin/tests/e2e/agent-session.mjs claude --bin <path> --port <free port>` (`codex` needs port 7777 free, the URL its plugin ships; the other platforms run in `.github/workflows/plugin-platforms.yml`); for a behaviour change, both manifests bumped to a version no open PR uses |
| `.cursor-plugin/` | `.venv/bin/python -m pytest tests/unit/test_cursor_plugin.py tests/unit/test_release_prepare.py tests/unit/test_published_links.py`; its version follows the server's and is never bumped on its own |
| `plugin.json`, `mcp.json` (the Agent Plugins package) | `.venv/bin/python -m pytest tests/unit/test_agent_plugin.py tests/unit/test_release_prepare.py tests/unit/test_published_links.py`; its version follows the server's and is never bumped on its own |
| `frontend/` | `npm --prefix frontend run test && npm --prefix frontend run build && npm --prefix frontend run budget`; the Playwright run CI adds (`npx --prefix frontend playwright install chromium` once (its system libraries, `playwright install-deps`, only on a machine you own), then `E2E_PORT=<free port> npm --prefix frontend run e2e`); `make lint` covers the accessibility rules |
| `deploy/helm/` | the commands of CI's "lint and validate every overlay" step (`.github/workflows/ci.yml`, job `helm`): a `secrets.jwtSecret` of at least 32 characters (CI uses `openssl rand -hex 32`; `helm lint` passes a shorter one, the kind overlay's `helm template` refuses it), `helm lint --strict` and `helm template … \| kubeconform -strict -kubernetes-version 1.30.0` for each overlay, once more with every optional object on; then the job's `scripts/gates/helm_extractor_isolation.py`, `scripts/gates/helm_metadata_egress.py` and `scripts/gates/helm_assistant_isolation.py` |
| `extractor/`, `compose.yaml` | the extractor tests (`.venv/bin/python -m pytest tests/unit/test_extractor_service.py tests/unit/test_compose_extractor_service.py`), then push and read `docker-smoke.yml`'s Quickstart jobs, which build both images and run the installed stack's extractor probes; `dev/docker-compose.dev.yml` is checked by that compose test and `make dev`, no CI job runs it |
| `sdk/typescript/` | `npm --prefix sdk/typescript run check && npm --prefix sdk/typescript run check:dist` (the ESM/CJS build, dist tests, publint and attw) |
| `sdk/python/` | CI's "python sdk wheel" steps (job `sdk-python-package` in `.github/workflows/ci.yml`): `uv build sdk/python --out-dir dist`, a fresh Python 3.11 virtualenv with the wheel and its `Requires-Dist` installed at `--resolution lowest-direct`, then `scripts/gates/sdk_wheel_smoke.py dist/*.whl` in it; the server's 3.12 venv hides an undeclared dependency or a 3.12-only API |
| the files the hostile sandbox suite runs: `server/code/app/index/` `sandbox.py`, `egress.py`, `egress_relay.py`, `compiler_tier.py`, `gitrepo.py`, `server/core/hosts.py`, and `tests/unit/test_repo_job_sandbox*.py` | `LOOM_TEST_REQUIRE_SANDBOX=1 .venv/bin/python -m pytest tests/unit/test_repo_job_sandbox.py tests/unit/test_repo_job_sandbox_hostile.py -q` on a host where bubblewrap can create namespaces; without it the test fails here, as in CI. On a host where it cannot, push and read CI's `repository-job sandbox (real bubblewrap)` job; never install bubblewrap or change the user-namespace sysctl on a shared host |
| `deploy/apparmor/`, `dev/seccomp/`, `dev/docker-compose.colour.yml` | push and read `docker-smoke.yml`'s "Repository-job sandbox under the shipped profiles" job, which builds the image, loads the profile and runs the two sandbox suites in the container; the host test above never applies a profile. Reproduce that job only on a disposable VM: `apparmor_parser -r` replaces the profile host-wide, under any deployment's running repository jobs, and its sysctl changes every session's sandbox on that host |
| `docs/`, any `.md` | `.venv/bin/python -m pytest tests/unit/test_doc_links.py tests/unit/test_public_copy.py` |

## 4. Read the regenerated diff

A generator's output is part of the review. `git diff --stat` after regenerating: a file you did not expect to change means the source change reached further than intended.

## 5. Fix at the source

- A ratchet (`function_length_gate.py`, `mypy_gate.py`) failing on your file: split the function, fix the types. `--update` only ever lowers a baseline.
- A public-copy failure: rewrite the text as the technique, without the name, date or history. The digest list is not edited to let a name through.
- A doc-link failure: fix the link or the anchor; anchors are the heading lowercased with spaces as `-`.
- Never skip, `xfail` or loosen a test to get green. A test that is wrong is fixed in the same change, with the reason in the PR body.

## Done when

The local format, lint, type and focused test checks pass, `git status` shows only the files you mean to commit, and the PR states which heavy checks remain for CI. Do not describe a pending or interrupted run as passed.
