---
name: vault-correct
description: >-
  Sweeps a corrected fact through the OKF v0.2 knowledge vault by updating the single authoritative note, refactoring stale restatements into wikilinks, and preserving historical records byte-for-byte. Use when the user invokes /vault-correct, asks to correct a vault fact or update an obsolete claim, or when superseded claims are detected during /distill-session or /ingest. Don't use for creating new notes from raw files (use ingest) or read-only vault searches (use vault-query).
---

# ⚖️ Vault Correct & Write-Correctness Sweep (`/vault-correct`)

This skill sweeps a corrected fact through the central **Knowledge Compiler** Obsidian Vault (`$OBSIDIAN_VAULT_PATH` or `~/ObsidianVault`). It implements the **Write-Correctness Laws** to eradicate knowledge staleness and contradiction drift while strictly guarding historical decision ledgers, frontmatter, code blocks, links, and instruction files.

---

## 🚀 Triggers & Invocations

### 1. Explicit User Command
```bash
/vault-correct "<the corrected fact, stated as it is now true>" --stale "<old claim>" [--target "<authoritative note>"] [--replacement "<exact body substitution>"] [--apply]
```
*Examples:*
- Preview Plan/Diff (safe default, writes 0 files):
  `/vault-correct "Cloud Run supports 32GiB RAM" --stale "16GiB RAM" --target "Cloud Run Limits"`
- Apply changes atomically after reviewing the diff:
  `/vault-correct 'AcmeCorp MySQL spend is $25,000/mo across 20 Aurora clusters' --stale '$30k+/mo' --target "AcmeCorp" --apply`

### 2. Autonomous Trigger (Zero-Toil Mode)
Triggered during:
- **`/ingest`**: When a newly ingested document or proposal carries a newer timestamp and directly contradicts an older claim in an entity or concept note.
- **`/distill-session`**: When an active session empirically disproves a previous assumption (always run Plan preview first, verify `--stale "<old>"`, then pass `--apply`).

---

## 📐 Execution Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VAULT CORRECT EXECUTION PIPELINE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Step 1: Exact Sweep (--stale required)]                                   │
│  Scan living vault notes while excluding reserved/instruction/symlink paths │
│                                │                                            │
│                                ▼                                            │
│  [Step 2: Tri-State Classification]                                         │
│  Classify every matching note into:                                         │
│    1. AUTHORITATIVE: Single source of truth (wiki/entities/ or wiki/concepts)│
│    2. RESTATEMENT:   Living notes asserting the stale claim                 │
│    3. HISTORICAL:    Past records (raw/, wiki/sources/, dated, log.md)      │
│                                │                                            │
│                                ▼                                            │
│  [Step 3: Plan / Diff Preview (Default)]                                    │
│  • Inspect unified diff across body prose only                              │
│  • Frontmatter, fenced code, inline code, and [[wikilinks]] are masked      │
│  • Reserved paths (GEMINI.md, AGENTS.md, index.md, skills/, rules/) excluded│
│                                │                                            │
│                                ▼                                            │
│  [Step 4: Atomic Apply with SHA-256 CAS (--apply)]                          │
│  • Verify pre-write SHA-256 hashes (exit code 2 on concurrent modification) │
│  • Write temp + fsync + os.replace atomically; append audit entry to log.md │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ The Hard Rails (Safety Invariants)

1. **Plan-by-Default & Explicit `--stale`**:
   - Running `vault_correct.py` without `--apply` runs a read-only **Plan/Diff preview** (`0` files modified; `--dry-run` is also accepted as an explicit preview flag).
   - `--stale "<old>"` is **required** whenever refactoring restatements or doing in-place phrase replacement. No heuristic keyword guessing is performed.

2. **Historical & Reserved Files are Untouchable**:
   - Notes under `raw/`, `archive/`, `meetings/`, `1-1/`, `journal/`, `incidents/`, and `wiki/sources/` are **never edited**.
   - Reserved instruction, index, and config paths (`GEMINI.md`, `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.gemini/`, `rules/`, `skills/`, `hooks.json`, `plugin.json`, `index.md`, `wiki/skill-impact.md`) and **symlinks** are hard-excluded from mutation.
   - Any note whose filename carries explicit date provenance (`YYYY-MM-DD` or `(YYYY-MM)`) or whose frontmatter `status` is `superseded`, `archived`, `completed`, `deprecated`, or `done` is **never edited**.
   - `log.md` past entries are never edited (only a new audit entry is appended upon `--apply`).

3. **Frontmatter, Code & Link Masking**:
   - YAML frontmatter (`title`, `tags`, `aliases`, `sources`, `generated`, `verified`) is separated before any body replacement and never altered (only `updated:` is bumped when body bytes change).
   - Fenced code blocks, inline backtick code spans, and existing `[[wikilinks]]` are masked so they are never corrupted or double-wrapped.

4. **SHA-256 CAS & Atomic Writes**:
   - Writes verify pre-write SHA-256 digests (`exit 2` on CAS conflict) and persist via temporary file + `fsync` + `os.replace`.

5. **Table Pipe Invariant**:
   - In Markdown tables, never escape the pipe character within a wikilink alias (always `[[Target|Alias]]`, never `[[Target\|Alias]]`).

---

## ⚡ Step-by-Step Procedure

### Step 1: Preview the Plan & Unified Diff (Default)
Run the vault correction utility without `--apply` first to inspect classifications and diffs:
```bash
python3 <plugin_dir>/scripts/vault_correct.py "<corrected fact>" --stale "<old>" --target "<authoritative note>"
```
(`--dry-run` is accepted as an explicit synonym for Plan preview.)

### Step 2: Apply Atomically (`--apply`)
Once the Plan/Diff looks clean, re-run with `--apply` (and optional `--replacement` if the authoritative note needs a custom inline phrase):
```bash
python3 <plugin_dir>/scripts/vault_correct.py "<corrected fact>" --stale "<old>" --target "<authoritative note>" --apply
```
Exit codes: `0` on success, `1` on validation/missing-vault error, `2` on SHA-256 CAS conflict.

### Step 3: Programmatic Python Usage
When invoking from Python or tests:
```python
from scripts.vault_correct import execute_vault_correction

results = execute_vault_correction(
    vault_root=vault_path,
    fact="Cloud Run A2A agents natively persist session memory via Vertex AI Memory Bank",
    stale_claim="in-memory Cloud Run storage",
    target_authoritative="Agent Memory & Vertex AI Memory Bank",
    apply=True,
    auto=True,
)
```

### Step 4: Verify & Audit
1. Inspect the terminal output for:
   - `AUTHORITATIVE`: Target note confirmed and updated.
   - `RESTATEMENTS`: Redundant claims replaced with wikilinks.
   - `HISTORICAL RECORDS`: Preserved notes clearly listed with reason.
2. Run `python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}"` to confirm that all newly inserted wikilinks resolve cleanly with zero pipe violations.
