---
name: content-ingestion-check
description: >-
  Base skill that checks whether a content object (identified by its git
  blob SHA-1) is present/known in a content-addressable archive, using the
  archive's lookup API. Domain-agnostic — works with any archive that exposes
  an HTTP endpoint to verify object existence by hash (Software Heritage,
  IPFS, etc.).
category: General-File
---

# Content Ingestion Check Skill (v1)

This is a **base** skill. It checks whether one or more content objects (by
git blob SHA-1) are already present in a content-addressable archive, using the
archive's hash-lookup API. Domain-agnostic: the target archive and endpoint
template are configurable via arguments, defaulting to Software Heritage.

***

## 1. Scope & Intent

- **In scope**:
    - Check a single hash: `--hash <sha1_git>` → HTTP lookup, print `KNOWN` or `UNKNOWN`
    - Check many hashes in one batch (via `known` endpoint): `--hashes <file>` (one sha per line)
    - Configurable archive base URL (`--api-base`) and lookup path template
    - JSON output (`--json`) for programmatic use
    - Exit code contract: 0 = all known, 1 = at least one unknown, 2 = transport/auth error
- **Out of scope**:
    - Fetching raw content (use `GET /content/.../raw/` in the target archive)
    - Blob hash computation (delegated to `git-blob-hash`)
    - Archive-specific swhid assembly or qualifier handling

***

## 2. Environment & Dependencies

### 2.1 Runtime
- **Python 3.12+**
- No third-party dependencies (stdlib `urllib.request`, `json`, `argparse`).

### 2.2 Required Setup
None.

### 2.3 Required Skill Loading
Load `SKILL.md` before invoking.

***

## 3. Protocol

### 3.1 Step 1 — Run Ingestion Check

```bash
python3 .agents/skills/general/file/content-ingestion-check/scripts/check-ingestion.py \
  --hash 53b4386b87deffff71a256acb04f33ea4c6807fe
python3 .agents/skills/general/file/content-ingestion-check/scripts/check-ingestion.py \
  --hashes hashes.txt --api-base https://archive.softwareheritage.org/api/1
```

### 3.2 Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--hash` | One of `--hash` or `--hashes` | — | Single SHA-1 git blob hash to check |
| `--hashes` | No | — | File path with one hash per line (batch) |
| `--api-base` | No | SWH | Archive API root URL (e.g. `https://archive.softwareheritage.org/api/1`) |
| `--single-path` | No | `/content/sha1_git:{hash}/` | URL template for single lookups (use `{hash}` placeholder) |
| `--batch-path` | No | `/content/known/{hashes}/` | URL template; `{hashes}` is comma-joined list (batch known check) |
| `--timeout` | No | `30` | Per-request timeout in seconds |
| `--json` | No | false | JSON output |

### 3.3 Output Contract

- **stdout** (text): `KNOWN <hash>` or `UNKNOWN <hash>` per line
- **stdout** (JSON): `{"checks": [{"hash": "...", "known": true}], "all_known": true}`
- **Exit 0**: All hashes are KNOWN
- **Exit 1**: At least one hash is UNKNOWN
- **Exit 2**: Transport error (network, HTTP 4xx/5xx, Anubis 403)

### 3.4 Script

| Script | Language | Purpose |
|--------|----------|---------|
| [`scripts/check-ingestion.py`](scripts/check-ingestion.py) | Python | HTTP client for content lookup; single + batch modes |

***

## 4. Edge Cases

- **HTTP 403**: Treated as transport error (exit 2) with Anubis hint — not "unknown". Anubis blocks automated clients; instruct the user to solve the PoW manually first.
- **Batch with mixed results**: All hashes checked; exit 1 if ANY are unknown.
- **Malformed hash**: Exit 2 (usage error, not ingestion status).

***

## 5. Composition Rationale

This skill is **base** because "is this content hash archived yet?" is a generic
question needed by SWH link minting, IPFS pinning workflows, package registry
verification, etc. The archive is parameterized, not hardcoded.

***

## 6. Composition by Higher-Level Skills

| Composer Skill | Composition Mechanism |
|----------------|----------------------|
| [`swh-content-link-mint`](../../software-heritage/content-link-mint/SKILL.md) | Delegates ingestion check to this base skill to enforce the "`;lines=` only after ingest confirms" gate. |

***

## 7. Verification

```bash
python3 scripts/check-ingestion.py --hash e69de29bb2d1d6434b8a4f3e0e7ad23c0d2c5d4c
# Empty git blob — virtually always KNOWN in SWH.
```
