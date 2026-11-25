---
name: distill-session
description: >-
  Scans the active conversation history or session transcript to extract and compile new architectural concepts, entity dossiers, decisions, and patterns into the local OKF v0.2 knowledge vault. Use when the user invokes /distill-session or /sync-vault, asks to distill or save the current session into the vault, or after completing a complex design or debugging workflow. Don't use for ingesting external files or slide decks (use ingest) or for read-only vault searches (use vault-query).
---

# 🧠 Distill Session (Cognitive Knowledge Compilation)

This skill enables Antigravity agents to retrospectively analyze the current conversation history, extract newly established architectural patterns, system discoveries, tool implementations, bug fixes, or benchmark metrics, and compile them into the persistent **Knowledge Compiler Obsidian Vault** (`$OBSIDIAN_VAULT_PATH` or `~/ObsidianVault`) following the **Open Knowledge Format (OKF v0.2)**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DISTILL-SESSION PIPELINE                        │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Scan Transcript & Working Context                                   │
│    ├── Trace conversation turns for key decisions, tools & concepts    │
│    └── Detect `/learn` rule updates (`rules/`, `GEMINI.md`)            │
│                                                                        │
│ 2. Distill Extraction Blueprint & Contradiction Sweep                  │
│    ├── Entities: Platforms, tools, organizations (wiki/entities/)      │
│    ├── Concepts: Architectural patterns, API invariants (wiki/concepts/)│
│    └── Run `/vault-correct` if new findings supersede older claims     │
│                                                                        │
│ 3. Author & Enrich OKF v0.2 Notes                                      │
│    ├── Write frontmatter (type, tags, sources, 5-way epistemic edges)  │
│    └── Inject reciprocal [[wikilinks]] (No escaped pipes in tables!)   │
│                                                                        │
│ 4. `/learn` Sync & Companion Shareability Check                        │
│    ├── Sync `/learn` rules into vault customization notes              │
│    └── Audit generalizable cloud/FinOps/A2UI invariants for `/vault-share`│
│                                                                        │
│ 5. Master Index, Graph Lint & Git Sync                                 │
│    ├── Update `index.md`, append `log.md`, and run `vault_lint.py`     │
│    └── Commit & sync updates to the local vault repository             │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Step-by-Step Execution Protocol

### Step 1: Discover Vault Root & Inspect Working Context
1. Locate the active vault path via environment variable `$OBSIDIAN_VAULT_PATH` or default to `~/ObsidianVault`.
2. Inspect the conversation turns or read the compact transcript at:
   `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`
3. Identify durable intellectual property generated during the session:
   - **Architectural Patterns**: Frameworks, lifecycle designs, protocols, schemas, API invariants.
   - **Entities**: New or modified software tools, libraries, Google Cloud services, customer accounts.
   - **Empirical Benchmarks & Metrics**: Sizing calculations, cost figures, performance gains, error fixes.

### Step 2: Formulate Extraction Blueprint
Before modifying notes, categorize items into the 3-layer wiki hierarchy:
- **`wiki/entities/<Name>.md`**: Product, tool, customer account, or library dossiers.
- **`wiki/concepts/<Topic>.md`**: Deep-dives into architectural principles, protocols, design patterns, or standards.
- **`wiki/synthesis/<Topic>.md`**: Cross-cutting analyses, trade-off comparisons, or customer strategy playbooks.

### Step 3: Contradiction Check & Write-Correctness Sweep
Before or during note authoring:
1. Determine if any newly established finding directly contradicts or supersedes a claim in existing notes (e.g., updated pricing metrics, corrected software versions, or revised customer architectures).
2. If a superseded claim is detected, execute an automated correction sweep via:
   ```bash
   python3 <plugin_dir>/scripts/vault_correct.py "<new fact>" --stale "<old claim>" --target "<authoritative note>" --apply
   ```
3. This strictly enforces the **Write-Correctness Laws**:
   - The single **AUTHORITATIVE** note is updated with the new fact and `updated:` timestamp.
   - All living **RESTATEMENTS** are refactored into `[[Authoritative Note]]` wikilinks to prevent duplication and future drift.
   - Historical records (`raw/`, `wiki/sources/`, dated files, `log.md`) are strictly **PRESERVED**.

### Step 4: Author / Enrich OKF v0.2 Markdown Notes
For each identified node:
1. Check if the file already exists in the vault.
2. If existing, enrich the content with new findings, version updates, or bug-fix discoveries while preserving prior knowledge.
3. If new, author the note with compliant OKF v0.2 YAML frontmatter:
   ```yaml
   ---
   title: "Canonical Title"
   type: concept | entity | synthesis
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   tags:
     - domain/topic
   status: stable
   sources:
     - id: source-slug
       resource: "https://..."
   generated: { by: knowledge-compiler/gemini-pro, at: YYYY-MM-DDTHH:MM:SSZ }
   aliases:
     - "Alternative Name"
   ---
   ```
   Omit `verified:` on agent-authored notes until explicit human review (`vault-lint --approve-human <note>`).
4. **Linking Invariants**:
   - Connect all related concepts and entities using reciprocal `[[wikilinks]]`.
   - **Never escape the pipe character inside Markdown tables** (always `[[Target|Alias]]`, never `[[Target\|Alias]]`).
   - In terminal output, provide clean ASCII diagrams alongside Mermaid code blocks.

### Step 5: `/learn` Rule Synchronization & Companion Shareability Check
Whenever a `/learn` rule (`rules/*.md`, project `GEMINI.md`, or `SKILL.md`) was created or updated during the session—or when a reusable technical invariant is crystallized:
1. **Local Vault Sync (`ObsidianVault`)**:
   - Synchronize the updated rule into `wiki/entities/Gemini CLI Environment & Customizations.md` and enrich the corresponding `wiki/concepts/` or `wiki/patterns/` dossier.
   - Append a structured `## [YYYY-MM-DD] learn | <Summary>` entry to `log.md`.
2. **Companion Plane 2 Shareability Check (`shared-okf-patterns`)**:
   - Evaluate whether the learned invariant is **Generalizable Enterprise Engineering IP** vs. **Personal / Organization-Specific Preference**:
     - **Promote to `shared-okf-patterns` (`/vault-share`)**: GCP service constraints, FinOps/CUR SQL & C2C pricing invariants (`EBSOptimized` `OS='NA'` filtering, bottom-up `vCPU+RAM` calculator rates, `$0.046/vCPU-hr` Windows PAYG separation, Two-Step Zero-Discount TCO Bridge), A2A v1.0 / A2UI v0.8 webhook contracts (`X-A2A-Extensions`, `task.artifacts` packaging), Google Slides/Sheets API schema rules, and MCP `stdio` lifecycle guards.
     - **Keep Local Only (Air-Gapped)**: Personal communication/verbosity preferences, personal booking URLs, organization-specific names/deal structures, or internal HR/performance notes.
   - For **Generalizable** invariants, automatically preview/stage promotion via:
     ```bash
     python3 <plugin_dir>/scripts/sync_patterns.py share "wiki/concepts/<Concept>.md" --repo-dir ~/shared-okf-patterns --dry-run
     python3 <plugin_dir>/scripts/sanitize_check.py ~/shared-okf-patterns --vault ~/ObsidianVault --fix --strict
     ```
     and either execute `/vault-share` (when authorized) or present a ready-to-promote summary to the user.

### Step 6: Update Master Index & Audit Log
1. Add new entries into `index.md` under the appropriate header (`## 🔬 Core Concepts & Frameworks`, `## 🏢 Entity Dossiers`, `## 🛠️ Tooling, Frameworks & Infrastructure`, or `## 📑 Synthesis & Research Analyses`).
2. Prepend a structured audit entry to `log.md`:
   ```markdown
   ## [YYYY-MM-DD] sync | Session Distillation: <Topic / Milestone>
   - **Action**: Retrospectively compiled session decisions, entities, and architectures into the vault.
   - **Key Artifacts Created / Updated**:
     - Concept Note: `[[wiki/concepts/<Concept>]]`
     - Entity Note: `[[wiki/entities/<Entity>]]`
     - Master Index: `[[index.md]]`
   ```

### Step 7: Verify Graph Integrity
Run the vault linter to guarantee 100% graph health:
```bash
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}"
```

### Step 8: Passive Git Push
Explain to the user the notes that were authored and updated (plus any companion shared pattern candidates). When enabled, Antigravity's **`Stop` lifecycle hook** (`auto_sync_vault.py`) stages, commits with session provenance, and pushes the newly compiled knowledge to `origin main`.
