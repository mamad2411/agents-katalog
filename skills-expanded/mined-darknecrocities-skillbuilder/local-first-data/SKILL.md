---
name: local-first-data
description: Architect local-first browser/desktop storage (IndexedDB, OPFS, SQLite WAL), public-vs-private vendored data boundaries, zero-fabrication completeness markers (PARTIAL/NEEDS_RESEARCH), and offline privacy invariants.
---

# Local-First Storage & Public-Private Data Boundaries (`/local-first-data`)

> **Role**: Principal Local-First & Data Integrity Architect  
> **Philosophy**: *Choose the right device store for the payload. Never mix private source research into public vendored artifacts. Never fabricate missing records—mark gaps explicitly as `PARTIAL` or `NEEDS_RESEARCH`.*

Distilled from `domodomo` (offline browser/SQLite persistence) and `bettersanfernando` (strict civic public-data boundaries and anti-fabrication guarantees).

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/storage-and-public-private-boundaries.md](references/storage-and-public-private-boundaries.md) | IndexedDB vs OPFS vs SQLite WAL matrix, schema migration rules, vendored public-data boundary, anti-fabrication markers. |
| [scripts/verify_local_first_hygiene.py](scripts/verify_local_first_hygiene.py) | CLI auditor checking for unversioned storage writes, raw generated JSON imports bypassing typed layers, and silent telemetry. |

---

## 2. Device Storage Selection Matrix

| Storage Engine | Ideal Payload | Max Scale | Avoid Using For |
| :--- | :--- | :--- | :--- |
| **`localStorage`** | Tiny UI prefs (`theme`, `sidebarCollapsed`) | `< 100 KB` | Structured entities, binary blobs, search indexes (blocks main thread synchronously). |
| **`IndexedDB`** | Structured user records, offline queues, chat history | `50 MB – GBs` | High-frequency byte-range writes (use OPFS instead). |
| **`OPFS` (Origin Private FS)** | Large media blobs, SQLite-Wasm WAL files, model weights | `GBs` (quota-bound) | Simple key-value flags. |
| **`SQLite` (WAL mode)** | Desktop/local-backend relational queries, FTS5, `sqlite-vec` | `GBs` | Unbounded unindexed full-table scans. |

---

## 3. Public vs. Private Data Boundary & Zero-Fabrication (`bettersanfernando` Standard)

1. **Two-Layer Vendoring**:
   - Raw research files, PDFs, spreadsheets, and unverified records stay in private/raw storage — **never** committed into the public application repo.
   - Public-safe exports live in a dedicated read-only generated directory (`src/data/generated/`) and **must never be edited by hand** or imported directly by UI routes.
   - All UI/API consumers read strictly through a **typed access layer** (`src/data/domain/`).
2. **Explicit Uncertainty Over Mock Fabrication**:
   - When real records are missing or incomplete, tag status explicitly as `PARTIAL` or `NEEDS_RESEARCH` in typed metadata. Never invent placeholder statistics, fake hotlines, or synthetic rows.
3. **Offline Privacy Invariant**:
   - Local-first features must work offline with zero silent telemetry or unrequested cloud uploads.

---

## 4. Automated Local-First & Boundary Auditor

```bash
python3 skills/local-first-data/scripts/verify_local_first_hygiene.py --path . --strict
```
