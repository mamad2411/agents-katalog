---
name: knowledge-base-integration
description: Use when configuring or running product-level Knowledge Ingest, target-ref Feature catalogs, Evidence Policy decisions, Revision Sets, idempotent smoke, or local/remote knowledge runners across repositories.
---

# Knowledge Base Integration

Use this Skill for the P1 read-only integration runtime. Repository-owned `.feature` files at configured target refs remain the behavior SOT. The runtime produces rebuildable catalogs and evidence bundles; it does not change source repositories.

## Steps

1. Read the product registry and server workspace mapping. Validate both with `scripts/knowledge_base_p1.py validate-config`. Completion: every required repository has an explicit remote, role, target ref, feature root, and contained local mapping.
2. Resolve Evidence intent before a formal run with `decision`. Completion: the immutable decision records `required` / `not-required` / `blocked`, targets, source rule, reason, policy version, and digest.
3. For `read / 读取`, run `ingest`. Completion: every available ref is fixed to a full commit SHA; complete no-ID Gherkin structures, locators, bindings, conflict candidates, `metrics.json`, and `ingest-summary.json` exist; `mutation` is `none`.
4. For CI or knowledge-server smoke, run `smoke` only after runner, environment, account, data, service, device, and app-artifact prerequisites are known. Completion: staged native commands ran through the local or configured command Runner Adapter; current-run reports, Chinese summaries, artifact manifest, checksums, metrics and evidence bundle exist, or the run is explicitly `blocked`.
5. Report exact status and paths. P1 publication is always `not-configured`; PR checks, remote publication, invalidation, retention, quarantine and gates belong to P2.

## Commands

```bash
python scripts/knowledge_base_p1.py validate-config \
  --product /path/to/product.yaml \
  --workspace /path/to/workspace.local.yaml

python scripts/knowledge_base_p1.py decision \
  --product /path/to/product.yaml \
  --repository smart-fuzi-web \
  --trigger pull-request \
  --execution-profile developer-local

# CI-generated PR evidence resolves the same policy with an explicit CI source.
python scripts/knowledge_base_p1.py decision \
  --product /path/to/product.yaml \
  --repository smart-fuzi-web \
  --trigger pull-request \
  --execution-profile ci

python scripts/knowledge_base_p1.py ingest \
  --product /path/to/product.yaml \
  --workspace /path/to/workspace.local.yaml \
  --output /path/to/generated/products/smart

python scripts/knowledge_base_p1.py smoke \
  --product /path/to/product.yaml \
  --workspace /path/to/workspace.local.yaml \
  --output /path/to/runtime/runs/smart-smoke \
  --trigger schedule \
  --execution-profile knowledge-server \
  --suite-key smoke \
  --attempt 1
```

Read [runtime-contract.md](references/runtime-contract.md) before configuring retry/attempt identity, staged smoke, report integrity, trusted deployment metadata, or a non-local Runner Adapter. Start deployment metadata from [deployment-manifest.example.yaml](references/deployment-manifest.example.yaml).

Pass trusted deployment metadata with `--deployment-manifest`. `verified` requires its path, issuer and digest to be trusted, its repository SHAs to equal the Revision Set, and its expected runner/tool/image attestation to match the Adapter result. For local execution, `workspace.local_runner` plus repeatable `--runner-label` describes current capabilities. For Mobile or another device pool, declare `runner` and `required_runner_labels` on the command and configure that runner key in the server Workspace.

`smoke --execution-profile` accepts `ci` or `knowledge-server`; developer-local reports remain owned by project-native validation. A CI smoke envelope uses clean detached worktrees, exact revisions, and `Evidence Publication: not-configured` until a P2 publisher accepts it.

Use `--no-fetch` only when the configured refs are already present locally and the caller explicitly wants an offline run. A missing ref is `blocked`; the runtime never falls back to the current or default branch.

## Configuration and Schemas

- Start from [product.example.yaml](references/product.example.yaml) and [workspace.local.example.yaml](references/workspace.local.example.yaml).
- Validate persisted artifacts against the JSON Schemas in `references/`, including product/workspace, decision, Revision Set, deployment metadata, Runner job/result, artifact manifest and metrics contracts.
- YAML input requires PyYAML; JSON configuration remains available without it. Install the pinned minimums in [requirements.txt](requirements.txt) in the knowledge-server runtime environment.

## Hard Boundaries

- `sync / 同步` remains the writable BDD Sync Mode in `gherkin-bdd`. Invoke this Skill's `read / 读取` branch only for explicit read-only intent with no add/change/update/delete intent; mixed read-and-mutate requests remain in the normal BDD workflow.
- Existing Feature and Scenario text is parsed without adding IDs, owner tags, scope tags, or a Gherkin runner.
- Long-lived clones are fetch caches. Smoke commands run in detached isolated worktrees.
- Smoke command strings are shell-free argv strings. Use `stage` for preflight, preparation, tests and cleanup; cleanup remains runnable after an earlier stage blocks.
- Formal report declarations provide an exact relative path or glob for a runner report and its same-stem Chinese Markdown summary. Only pairs created or refreshed by the current command are collected; stale, non-Chinese, missing, unsafe or sensitive artifacts make Evidence `blocked`.
- Current report-only smoke continues to emit `schemaVersion: 1` with `featureSources: []`. That envelope remains valid generic evidence and must not be treated as BDD scenario coverage. Scenario-backed knowledge evidence requires a separate v2 envelope; do not rewrite v1 smoke into v2 links.
- Duplicate logical runs reuse their idempotency record. Use a new `--attempt` for an intentional rerun; infrastructure retries stay inside that attempt and assertion failures do not retry automatically.
- `smoke-only`, contract, mock, app-mocked, and backend-only modes retain their actual meaning.
- Configuration and artifacts contain no credentials, tokens, PII, production data, or sensitive request content.

## Output

Report:

- `Knowledge Ingest`: `run` / `partial` / `blocked` / `not-needed`
- `Evidence Contract`: `not-required` / `required` / `blocked`
- `Evidence Intent` and `Evidence Targets`
- `Revision Set`: id, status, and each repository ref/SHA
- `Knowledge Server Smoke`: `passed` / `failed` / `blocked` / `not-needed`
- `Evidence Source`: `ci` / `knowledge-server` / `not-needed` for smoke runs
- `Environment Alignment`: `verified` / `unverified` / `mismatch` / `not-needed`
- `Evidence Publication`: `not-configured` for P1
- generated catalog, summary, report, and envelope paths
- idempotency key, parser version, suite key and attempt
- artifact manifest, checksums, runner attestation and metrics paths
