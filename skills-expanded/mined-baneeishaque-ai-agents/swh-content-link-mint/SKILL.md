---
name: swh-content-link-mint
description: >-
  Composer skill that mints Software Heritage content (browse) links from
  local git blob hashes. Delegates blob-hash computation to the
  git-blob-hash base skill and ingest confirmation to the
  content-ingestion-check base skill, then assembles canonical
  swh:1:cnt:<sha>;origin=<url>;path=<rel>[;lines=N] browse URLs.
category: Software-Heritage
---

# SWH Content Link Mint Skill (v1)

This is a **composer** skill. It produces citable Software Heritage content
links of the form:

```
https://archive.softwareheritage.org/swh:1:cnt:<sha1_git>;origin=<url>;path=<rel>[;lines=N-M]
```

It composes two base skills (`git-blob-hash` for local hashing, `content-ingestion-check`
for the `;lines=` ingest gate) and adds the SWH-specific link assembly.

***

## 1. Scope & Intent

- **In scope**:
    - Compute git blob SHA-1 for each input file (delegates to `git-blob-hash`)
    - Optionally confirm each blob is archived (delegates to `content-ingestion-check`)
    - Assemble the canonical `swh:1:cnt:...;origin=...;path=...` browse URL
    - Append `;lines=N-M` ONLY after ingest confirmation (or `--force-lines`)
    - Output formats: `url` (one per line), `markdown` (bullet list), `json`
- **Out of scope**:
    - Save-code-now submission (delegated to `swh-save-code-now`)
    - Per-push ingest verification (delegated to `swh-ingest-verify`)
    - Git tree/directory hashing

***

## 2. Environment & Dependencies

### 2.1 Runtime
- **Python 3.12+** (Tier 1)
- No third-party dependencies.

### 2.2 Required Skills
- [`git-blob-hash`](../../general/file/git-blob-hash/SKILL.md) — computes `compute-blob-sha1.py`
- [`content-ingestion-check`](../../general/file/content-ingestion-check/SKILL.md) — computes `check-ingestion.py`

### 2.3 Script Resolution
Per the layered-composition mandate, the composer MUST resolve the base scripts
via a relative path anchored on the composer's OWN location, and exit non-zero
with a clear error if the base script is missing.

***

## 3. Protocol

### 3.1 Step 1 — Mint Links

```bash
python3 .agents/skills/software-heritage/content-link-mint/scripts/mint-content-links.py \
  --origin https://github.com/baneeishaque/ai-suite \
  --repo-root . \
  .agents/skills/general/planning/versioned-artifact-superset-build/SKILL.md
```

### 3.2 Step 2 — Verify + Add Line Ranges

```bash
python3 scripts/mint-content-links.py --origin <url> --verify --lines 9-15 <file>
```

### 3.3 Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `files` | One+ | — | Files to mint links for |
| `--origin <url>` | Yes | — | SWH origin URL qualifier (e.g. `https://github.com/baneeishaque/ai-suite`) |
| `--repo-root <dir>` | No | `.` | Root that `path=` is relative to |
| `--verify` | No | false | Confirm each blob is ingested before emitting |
| `--lines N[-M]` | No | — | Append `;lines=` (requires `--verify`) |
| `--force-lines` | No | false | Append `;lines=` without ingest confirmation |
| `--timeout` | No | 30 | Per-request timeout |
| `--format` | No | `url` | `url`, `markdown`, or `json` |

### 3.4 Output Contract

- **stdout** (`url`): one link per line
- **stdout** (`markdown`): `- [\`<file>\`](<link>)` bullet per line
- **stdout** (`json`): `[{"file":..., "sha1_git":..., "ingested":..., "link":...}]`
- **Exit 0**: All links minted (and all verified blobs ingested)
- **Exit 1**: At least one file skipped (not a file, unreadable, or un-ingested under `--verify`)
- **Exit 2**: Usage error (`--lines` without `--verify`/`--force-lines`), or SWH 403

### 3.5 Script

| Script | Language | Purpose |
|--------|----------|---------|
| [`scripts/mint-content-links.py`](scripts/mint-content-links.py) | Python | Composer engine: hashes files, optional ingest check, assembles links |

***

## 4. Canonical Link Order

The SWHID spec's recommended presentation order is:

```text
swh:1:cnt:<sha>;origin=<origin-url>;path=<relative-path>[;lines=N-M]
```

`visit` and `anchor` qualifiers are intentionally omitted: they pin a snapshot,
while content links address content observable at the origin across crawls.

***

## 5. The `;lines=` Gate

Per the crawl-submission procedure, `;lines=` qualifiers are appended ONLY after
ingest confirms the content revision exists in the archive. This is enforced by
requiring `--verify` (which calls `content-ingestion-check` and gets HTTP 200) or
an explicit `--force-lines` override.

```bash
# Enforced failure — no --verify/--force-lines:
#   error: --lines requires --verify ... or --force-lines
python3 scripts/mint-content-links.py --origin <url> --lines 9-15 <file>
# exit 2
```

***

## 6. Composition Rationale

This composer delegates:
- **Blob hashing** → `git-blob-hash`'s `compute-blob-sha1.py` (via relative
  `../../../general/file/git-blob-hash/scripts/compute-blob-sha1.py`)
- **Ingest confirmation** → `content-ingestion-check`'s `check-ingestion.py`
  (via relative `../../../general/file/content-ingestion-check/scripts/check-ingestion.py`)

Both base skills are domain-agnostic; this composer adds only the SWH-specific
link assembly, keeping the primitives reusable (e.g. IPFS, package registries).

***

## 7. Verification

```bash
# Known SWH blob (procedure example):
python3 scripts/mint-content-links.py \
  --origin https://github.com/baneeishaque/ai-suite \
  .agents/skills/general/planning/versioned-artifact-superset-build/SKILL.md
# Expect: https://archive.softwareheritage.org/swh:1:cnt:53b4386b87deffff71a256acb04f33ea4c6807fe;origin=...;path=...
```

***

## 8. Related Skills

- [`git-blob-hash`](../../general/file/git-blob-hash/SKILL.md) — base skill for computing git blob SHAs locally.
- [`content-ingestion-check`](../../general/file/content-ingestion-check/SKILL.md) — base skill for verifying a blob is archived.
- [`swh-save-code-now`](../../software-heritage/save-code-now/SKILL.md) — run first to ensure the origin+HEAD is archived, then mint links.
- [`swh-ingest-verify`](../../software-heritage/ingest-verify/SKILL.md) — per-push verification that the latest snapshot contains expected HEADs.