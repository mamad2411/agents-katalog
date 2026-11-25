---
name: ingest
description: >-
  Extracts, distills, and compiles raw sources (PPTX slide decks, PDFs, Word docs, Excel sheets, web URLs, transcripts, codebases, or raw/ directories) into persistent, structured Knowledge Compiler markdown wikis following the Open Knowledge Format (OKF v0.2) and Andrej Karpathy LLM-Wiki standard. Use when the user invokes /ingest, asks to ingest raw files or a target path, compile knowledge, update the wiki, or extract unstructured files into markdown knowledge bases. Don't use for retrospectively compiling the active chat conversation without external files (use distill-session) or for read-only vault lookups (use vault-query).
---

# 📥 Knowledge Compiler Ingestion & Compilation Skill (`/ingest`)

This skill automates the end-to-end ingestion, multimodal extraction, distillation, cross-pollination, indexing, and health-checking of unstructured and structured sources into a **Knowledge Compiler** vault following the **Open Knowledge Format (OKF v0.2)**.

---

## 🚀 Triggering `/ingest`

This skill handles any of the following invocations:
- `/ingest` or `/ingest raw`: Batch-scans and ingests all pending/unprocessed source files in the vault's `raw/` directory (leveraging SHA-256 caching to skip unchanged files).
- `/ingest <file_or_dir>`: Ingests a specific local file (e.g. `/ingest ~/Downloads/deck.pptx` or `/ingest ./docs/`).
- `/ingest <url>`: Ingests a web page, blog post, or public document.
- `/ingest <git_repo>`: Analyzes and compiles a local or remote code repository into architectural patterns, entity dossiers, and source summaries.

---

## ⚡ Two-Step Decomposition Workflow

To ensure maximum extraction fidelity, dense cross-referencing, and graph connectivity, the ingestion workflow is explicitly split into **two distinct passes**:

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TWO-STEP INGESTION & COMPILATION PIPELINE                       │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [Step 0: Extract & Cache Check]                                                       │
│  Run extract_source.py (computes SHA-256 hex digest, checks .ingest_cache.json)        │
│  Unpack text/tables to raw/<Title>.md and raster images to raw/assets/<Title>/         │
│                                │                                                       │
│                                ▼                                                       │
│  [PASS 1: Structured Analysis & Cross-Reference Mapping]                               │
│  - Read raw/<Title>.md + visual inspection of raster diagrams via view_file            │
│  - Consult purpose.md and index.md to align with active strategic priorities           │
│  - Produce structured blueprint: Entities, Concepts, New Claims, Contradictions, Links│
│                                │                                                       │
│                                ▼                                                       │
│  [PASS 2: Compilation & Cross-Pollination]                                             │
│  - Create wiki/sources/<Title>.md with OKF frontmatter & source_sha256                 │
│  - Create/Update wiki/entities/ dossiers & wiki/concepts/ architectural patterns       │
│  - Transcribe raster architectures to Mermaid in notes + clean ASCII diagrams in chat  │
│  - Update index.md catalog & prepend timestamped audit entry to log.md                 │
│                                │                                                       │
│                                ▼                                                       │
│  [Validation & Linter]                                                                 │
│  - Run vault_lint.py: 0 broken links, 0 orphans, 100% OKF compliance                   │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Step 0: Locate Vault Root, Extract & Check Cache
Locate the active Knowledge Compiler vault (checks current working directory, upward parent directories for `GEMINI.md`/`raw/`/`wiki/`, or defaults to `$OBSIDIAN_VAULT_PATH` or `~/ObsidianVault`).

Run the automated extraction script to unpack text, tables, speaker notes, and embedded media assets with SHA-256 caching:
```bash
uv run --with python-pptx --with openpyxl python <plugin_dir>/skills/ingest/scripts/extract_source.py [target]
```

### 2. Pass 1: Structured Analysis & Cross-Reference Mapping
Before writing or modifying any permanent wiki notes:
1. **Read & Inspect**: Read `raw/<Title>.md`. Use `view_file` to visually inspect any extracted raster images in `raw/assets/<Title>/` (identifying architectural diagrams, topology charts, and tables not captured in raw text).
2. **Context Alignment**: Read `purpose.md` and `index.md` to identify active customer engagements, architectural themes, and existing related notes.
3. **Draft Structured Extraction Blueprint**:
   - **Core Thesis & Claims**: Primary takeaways, architectural models, benchmark statistics, and quotes.
   - **Entities Identified**: Products, organizations, platforms, people, or datasets (`wiki/entities/`).
   - **Concepts & Architecture**: Design patterns, security models, protocols, formulas (`wiki/concepts/`).
   - **Contradictions & Shift in Consensus**: Highlight differences with prior ingested materials.
   - **Target Wikilinks**: Exact list of reciprocal `[[wikilinks]]` to inject across the vault.

### 3. Pass 2: Compilation, Cross-Pollination & OKF Generation
Consume the structured blueprint from Pass 1 to execute the changes:
1. **Source Summary Note (`wiki/sources/<Title>.md`)**:
   - Author complete OKF v0.2 YAML frontmatter (`type: source-summary`, `source_sha256`, `sources: [{ id: "<slug>", resource: "<path_or_url>" }]`, `tags: [...]`, `status: stable`, `generated: { by: knowledge-compiler/gemini-pro, at: YYYY-MM-DDTHH:MM:SSZ }`). Omit `verified:` on agent-authored notes until human review (`vault-lint --approve-human <note>`).
   - Include executive summary, detailed topic breakdowns, comparison tables, and Mermaid architecture diagrams.
2. **Entity & Concept Synthesis (`wiki/entities/` & `wiki/concepts/`)**:
   - Create or enrich corresponding entity and concept notes.
   - Ensure reciprocal links (`A -> B` and `B -> A`).
   - **Table Formatting Invariant**: Inside markdown tables, **never escape the pipe character** (always use `[[Target|Alias]]`, never `[[Target\|Alias]]`).
   - **CLI Terminal Visual Invariant**: In Antigravity CLI terminal output, always provide a clean ASCII/Unicode text box diagram for immediate terminal readability alongside references to the Mermaid diagrams.
3. **Master Index & Audit Log**:
   - Add new notes with concise one-line summaries into `index.md`.
   - Prepend a chronological audit log entry to `log.md` in the format:
     `## [YYYY-MM-DD] ingest | <Source Title>`

### 4. Integrity Validation
Run the vault linter to guarantee 100% OKF compliance and zero broken links:
```bash
python3 <plugin_dir>/scripts/vault_lint.py "${OBSIDIAN_VAULT_PATH:-$HOME/ObsidianVault}"
```

---

## 📚 Reference Documentation
- **OKF v0.2 Specification**: [references/okf_spec.md](references/okf_spec.md)
- **Compiler Ingestion Protocol**: [references/compiler_protocol.md](references/compiler_protocol.md)
- **Extraction Helper**: [scripts/extract_source.py](scripts/extract_source.py)
