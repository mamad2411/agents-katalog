---
name: vault-pull
description: >-
  Pulls and synchronizes curated OKF v0.2 architectural patterns and engineering invariants from a shared Git pattern repository into the local knowledge vault ($OBSIDIAN_VAULT_PATH or ~/ObsidianVault). Use when the user invokes /vault-pull or /pull-patterns, asks to pull shared patterns, sync team patterns, or import patterns from a shared repository. Don't use for sharing local vault notes outbound to a shared repository (use vault-share) or for read-only vault queries (use vault-query).
---

# 📥 Vault Pattern Pull & Ingestion Skill (`/vault-pull`)

This skill allows engineers and architects to pull verified architectural patterns, framework concepts, and engineering invariants contributed by teammates from a shared OKF pattern repository (`~/shared-okf-patterns` or `$OKF_PATTERNS_PATH`) into their personal **Knowledge Compiler** Obsidian Vault (`$OBSIDIAN_VAULT_PATH`, defaults to `~/ObsidianVault`).

---

## 🛡 Isolation & Local Vault Protection

The pull engine guarantees:
1. **Target Directory Allowlist**:
   - Pulled files are strictly written into `wiki/concepts/` and `wiki/patterns/`.
   - Never touches or modifies local private entity dossiers in `wiki/entities/`, raw sources in `raw/`, synthesis notes in `wiki/synthesis/`, or tables in `tables/`.
2. **Local Overwrite Safeguards**:
   - If a local file has identical contents, it is skipped without modification.
3. **Automatic Index & Log Maintenance**:
   - Newly pulled patterns are indexed in local `index.md` and an entry is logged in `log.md`.
   - Automatically runs `vault_lint --fix` to verify graph connectivity.

---

## ⚡ Execution Workflow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FEDERATED PATTERN PULL PIPELINE                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Step 1: Upstream Sync]                                                    │
│  Fetch latest changes from shared OKF patterns repository                   │
│                                │                                            │
│                                ▼                                            │
│  [Step 2: Scoped Ingestion]                                                 │
│  Copy `wiki/concepts/` and `wiki/patterns/` into local vault                │
│                                │                                            │
│                                ▼                                            │
│  [Step 3: Graph Lint & Auto-Repair]                                         │
│  Run `vault-lint --fix` to update wikilinks and check graph invariants      │
│                                │                                            │
│                                ▼                                            │
│  [Step 4: Audit Trail]                                                      │
│  Update local `index.md` catalog and append sync entry to `log.md`          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Command Reference

### 1. Preview Incoming Patterns (Dry-Run)
```bash
python3 <plugin_dir>/scripts/sync_patterns.py pull --dry-run
```

### 2. Auto-Clone & Pull Patterns into Personal Vault
If the shared patterns repository is not cloned locally yet, `sync_patterns.py pull` can clone it automatically via `--repo-url` (or `$OKF_PATTERNS_REPO_URL`, or the default configured team repository) and fast-forward it on subsequent runs:

```bash
python3 <plugin_dir>/scripts/sync_patterns.py pull --vault "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}"
```

To point at an explicit shared Git repository URL or local directory:

```bash
python3 <plugin_dir>/scripts/sync_patterns.py pull --repo-url https://github.com/your-org/shared-okf-patterns.git --vault "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}"
```

