---
name: vault-share
description: >-
  Audits, sanitizes (rewriting private entity links into enterprise archetype prose and scrubbing local file paths), and shares reusable architecture concepts and engineering invariants from the local knowledge vault to a shared Git pattern repository. Use when the user invokes /vault-share or /share-pattern, asks to share or publish a pattern to a team repository, or audits vault notes for sharing. Don't use for pulling upstream patterns into the local vault (use vault-pull).
---

# 🚀 Vault Pattern Sharing & Sanitization Skill (`/vault-share`)

This skill enables engineers and architects to safely contribute architectural patterns and invariants from their personal **Knowledge Compiler** Obsidian Vault (`$OBSIDIAN_VAULT_PATH`, defaults to `~/ObsidianVault`) into a shared team repository (`~/shared-okf-patterns` or `$OKF_PATTERNS_PATH`), with air-gapped protection of private organization data and personal notes.

---

## 🔒 Privacy & Air-Gap Guarantees

The sharing engine (`sync-patterns`) strictly enforces:
1. **Hard Path Blocklist**:
   - Files in `raw/` or `raw/assets/` are NEVER shareable.
   - Files in `wiki/entities/` (organization dossiers, account strategies) are NEVER shareable.
   - Files with `perf`, `salary`, `1:1`, or `resume` in the title or content are NEVER shareable.
   - *Terminology Note*: Avoid HR/salary terms (`base salary`, `total compensation`, `peer bonus`) in architectural concept notes; use domain-precise terms like *statutory indemnification* or *compensating saga rollback*.
2. **Automated Private `wiki/entities/` Detection & Enterprise Archetype Prose Rewriting**:
   - Both `sync_patterns.py` (`build_entity_archetype_map()` + `sanitize_markdown()`) and `sanitize_check.py` (`detect_private_entity_wikilinks()` + `rewrite_private_entity_wikilinks()`) inspect `tables/customers.md` (Customer Account + Industry columns) and `wiki/entities/*.md` YAML frontmatter (`#customer`, `#entity/customer`, `#private-equity`, `#industry/<slug>`).
   - Path-prefixed private entity links (`[[wiki/entities/AcmeCorp]]`, `[[wiki/entities/Northwind|Northwind]]`, `[[entities/CapitalPartners]]`) and bare customer entity links (`[[AcmeCorp]]`, `[[Contoso Rail|Contoso]]`) are **automatically converted into clean enterprise archetype prose** (e.g., `Multi-Tenant SaaS ISV`, `Global Food & Beverage Manufacturer`, `Class 1 Freight Railroad`, `Private Equity Sponsor`) while preserving fenced code blocks and inline code spans.
   - Public technology entity links in `wiki/entities/` that lack a shared repository note (e.g., `[[wiki/entities/Cloud Run|Google Cloud Run]]`) are unwrapped into clean prose (`Google Cloud Run`), and private `wiki/sources/` or `wiki/synthesis/` references are pruned from YAML frontmatter `sources:` and 5-way epistemic lists so **zero broken or private links ever reach the shared repository**.
   - Any unmapped `[[wiki/entities/<Unknown>]]` link fails closed to `'Enterprise Commercial Account'`, guaranteeing zero identifier leakage.
3. **Local Path Scrubbing**:
   - Absolute filesystem paths (`/usr/local/google/home/...`, `/home/...`, `/Users/...`) in body text or frontmatter `sources:` are scrubbed to `/workspace/...` to preserve environment anonymity.

---

## ⚡ Execution Workflow

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FEDERATED PATTERN SHARING PIPELINE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Step 1: Privacy & Isolation Audit]                                        │
│  Run `sync-patterns audit` to identify clean vs scrub-needed concepts       │
│                                │                                            │
│                                ▼                                            │
│  [Step 2: Automated Archetype Sanitization]                                 │
│  Convert private `wiki/entities/` & `[[Entity]]` links to archetype prose   │
│  Scrub local `/home` paths, prune private frontmatter edges                 │
│                                │                                            │
│                                ▼                                            │
│  [Step 3: Target Repository Sync & Strict Sanitize Gate]                    │
│  Write to `shared-okf-patterns/wiki/concepts/` or `wiki/patterns/`          │
│  Run `sanitize_check.py --fix --strict` (0 DLP leaks, 0 broken wikilinks)   │
│  Update `index.md` catalog and append entry to `log.md`                     │
│                                │                                            │
│                                ▼                                            │
│  [Step 4: PR or Direct Commit]                                              │
│  Commit changes, push to GitHub branch, and create PR via `gh pr create`    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Command Reference

### 1. Audit Patterns Before Sharing
```bash
python3 <plugin_dir>/scripts/sync_patterns.py audit --vault ~/ObsidianVault
```

### 2. Preview Sanitization (Dry-Run)
```bash
python3 <plugin_dir>/scripts/sync_patterns.py share "wiki/concepts/Dual Run.md" --dry-run
```

### 3. Share a Pattern to the Shared Repository
```bash
python3 <plugin_dir>/scripts/sync_patterns.py share "wiki/concepts/<Pattern>.md" --repo-dir "${OKF_PATTERNS_PATH:-$HOME/shared-okf-patterns}"
```

### 4. Run Strict DLP & Automated Private Entity Link Rewriter (`sanitize_check.py`)
Before committing or opening a PR on the shared repository, run `sanitize_check.py --fix --strict` to automatically rewrite any lingering `wiki/entities/` links into clean archetype prose and verify 100% link-graph resolution:
```bash
python3 <plugin_dir>/scripts/sanitize_check.py "${OKF_PATTERNS_PATH:-$HOME/shared-okf-patterns}" --vault ~/ObsidianVault --fix --strict
```

### 5. One-Command Isolated Worktree PR
Use `--open-pr` to stage the sanitized pattern on an isolated temporary `git worktree` branch (leaving your primary checkout untouched), commit, push, and open a Pull Request via `gh`:
```bash
python3 <plugin_dir>/scripts/sync_patterns.py share \
  "wiki/concepts/<Pattern>.md" --repo-dir "${OKF_PATTERNS_PATH:-$HOME/shared-okf-patterns}" --open-pr --base main
```
