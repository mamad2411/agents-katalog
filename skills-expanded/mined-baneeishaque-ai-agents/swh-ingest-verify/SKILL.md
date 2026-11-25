---
name: swh-ingest-verify
description: >-
  Composer skill that verifies the Software Heritage archive has ingested the
  expected git revisions for a set of origins. Runs as a GitHub Actions
  workflow on every push, querying the SWH REST API to confirm origin known,
  revision archived, and HEAD present as a branch target in the latest
  snapshot. Optionally triggers a save-code-now POST if the origin is unknown.
category: Software-Heritage
---

# SWH Ingest Verify Skill (v1)

This is a **composer** skill. It verifies that the Software Heritage archive has
ingested the expected git revisions for specified origins, typically the
superproject HEAD and submodule gitlink SHAs. Runs as a GitHub Actions workflow
on every push.

***

## 1. Scope & Intent

- **In scope**:
    - Resolve expected SHAs (superproject HEAD + submodule gitlink) from the checkout
    - For each origin: query `GET /api/1/origin/<url>/get/`, then `GET /api/1/revision/<sha>/`,
      then `GET /api/1/origin/<url>/visit/latest/` + `GET /api/1/snapshot/<id>/` branch scan
    - Report VERIFIED / PENDING / FAILED verdicts
    - Optionally POST a Save-code-now request if the origin is unknown
- **Out of scope**:
    - The Save-code-now submission UI automation (delegated to `swh-save-code-now`)
    - Content hash computation (delegated to `git-blob-hash`)
    - Ingest-status checking for individual blobs (delegated to `content-ingestion-check`)

***

## 2. Environment & Dependencies

### 2.1 Runtime
- **Python 3.12+** (runs in GitHub Actions `ubuntu-24.04`)
- **Bash 4+** (workflow script wrappers)
- No third-party dependencies (stdlib `urllib`, `json`, `hashlib`).

### 2.2 Required Setup
None — runs in GitHub Actions with no secrets required (SWH API is public).

### 2.3 Required Skill Loading
- This skill's `SKILL.md`
- [`swh-save-code-now`](../../software-heritage/save-code-now/SKILL.md) (if using `--trigger-save`)

***

## 3. Protocol

### 3.1 Step 1 — Run the Verification Engine

```bash
python3 .agents/skills/software-heritage/ingest-verify/scripts/verify-ingest.py \
  --check https://github.com/baneeishaque/ai-suite,6f94215412b809faf3a85f66c10fcfb9b7df2d42 \
  --check https://github.com/baneeishaque/ai-agent-rules,e81343ca0b8a2a64d7a95549aec945944e6d3e47
```

### 3.2 Step 2 — Trigger Save (Optional)

```bash
python3 scripts/verify-ingest.py --check <origin>,<sha> --trigger-save
```

### 3.3 Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--check <url>,<sha>` | One+ | — | Origin URL + expected git SHA-1 |
| `--trigger-save` | No | false | Fire best-effort Save-code-now POST before verifying |
| `--timeout` | No | 30 | Per-request timeout |
| `--json` | No | false | Machine-readable JSON report |

### 3.4 Output Contract

- **stdout** (text): `[VERIFIED|PENDING|FAILED] <origin> rev <sha>`
- **Exit 0**: VERIFIED — all origins' HEADs in latest snapshots
- **Exit 1**: PENDING — origin known but HEAD not yet snapshotted
- **Exit 2**: FAILED — origin unknown / API error

### 3.5 CI Integration

| File | Role |
|--------|------|
| [`scripts/verify-ingest.py`](scripts/verify-ingest.py) | Verification engine |
| [`scripts/resolve-heads.bash`](scripts/resolve-heads.bash) | Resolve superproject + submodule SHAs (writes `$GITHUB_OUTPUT`) |
| [`scripts/run-swh-verify.bash`](scripts/run-swh-verify.bash) | Map exit codes to CI annotations (`::error::` vs `::warning::`) |
| [`scripts/verify-ingest.py.md`](scripts/verify-ingest.py.md) | Industrial Explainer for the engine |
| `.github/workflows/swh-verify.yml` | GitHub Actions workflow (repo root; references the scripts above via relative paths) |

***

## 4. Verification Logic

For each origin, three-stage check (mirrors manual procedure):

1. **Origin known**: `GET /api/1/origin/<url>/get/` → 200 (404 = not archived; 403 = Anubis)
2. **Revision archived**: `GET /api/1/revision/<sha>/` → 200
3. **HEAD in latest snapshot**: `GET /api/1/origin/<url>/visit/latest/?require_snapshot=true` → `GET /api/1/snapshot/<id>/` → scan all branch targets for the expected SHA

***

## 5. Composition Rationale

Composes:
- **`content-ingestion-check`** (base) — for `--trigger-save` blob-level confirmation
- **`swh-save-code-now`** — referenced for manual save on FAILED/PENDING

The CI wrapper scripts (`resolve-heads.bash`, `run-swh-verify.bash`) live in this
skill's `scripts/` dir (not `.github/workflows/scripts/`) so the full verification
pipeline is portable and testable outside CI; the workflow at repo-root
`.github/workflows/swh-verify.yml` references them via relative paths.

***

## 6. Related Skills

- [`swh-save-code-now`](../../software-heritage/save-code-now/SKILL.md) — manual save automation
- [`swh-content-link-mint`](../../software-heritage/content-link-mint/SKILL.md) — content-link minting
- [`content-ingestion-check`](../../general/file/content-ingestion-check/SKILL.md) — base: blob ingestion check
- [`git-blob-hash`](../../general/file/git-blob-hash/SKILL.md) — base: blob SHA computation
