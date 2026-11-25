---
name: knowledge-compiler
description: >-
  Compiles raw sources (PDFs, PPTX slide decks, Word docs, spreadsheets, transcripts, codebases, and URLs) into an Open Knowledge Format (OKF v0.2) Markdown wiki with a master index, audit log, and link linter. Use when initializing a knowledge vault, compiling documents or transcripts into wiki pages, or maintaining a persistent LLM-maintained knowledge base. Don't use for one-off web searches or temporary scratch notes unrelated to a knowledge vault.
---

# Skill: Knowledge Compiler & OKF v0.2 Vault Maintainer

This skill enables developers, architects, and AI agents to maintain a persistent, compounding **Knowledge Compiler Obsidian Vault** following the **Open Knowledge Format (OKF v0.2)** and Andrej Karpathy's compiled LLM-Wiki paradigm (*Obsidian is the IDE, the LLM is the maintenance programmer, and the markdown wiki is the persistent codebase*).

---

## 🏛 The 3-Tier Layering Model

1. **`raw/` (Immutable Ground Truth)**: Unmodified source documents, slide transcripts, PDFs, meeting transcripts, and `raw/assets/<Title>/` media images.
2. **`wiki/` (Compiled Knowledge Graph)**:
   - `wiki/sources/`: Distilled summaries of ingested sources.
   - `wiki/entities/`: Living dossiers for customers, platforms, tools, and partners.
   - `wiki/concepts/`: Architectural blueprints, design patterns, and engineering principles.
   - `wiki/synthesis/`: Cross-cutting comparisons and compound intelligence.
3. **Navigation & Auditing**:
   - `index.md`: Progressive disclosure master catalog.
   - `log.md`: Chronological operation history.

---

## ⚡ Core CLI Workflows

### 1. Initialize a New Vault
Scaffold directory hierarchy and starter files in any folder:
```bash
python3 scripts/init_vault.py --target /path/to/my-vault
```

### 2. Extract & Ingest Raw Sources
Extract text, speaker notes, tables, and unpacked diagrams from slide decks (`.pptx`), PDFs, documents, or URLs:
```bash
# Ingest single PPTX deck (extracts notes & saves images to raw/assets/<Title>/)
python3 scripts/extract_source.py ~/Downloads/customer_presentation.pptx

# Ingest all files in raw/
python3 scripts/extract_source.py raw/

# Ingest a web architecture guide
python3 scripts/extract_source.py https://cloud.google.com/architecture/waf
```

### 3. Multimodal Diagram Inspection & Transcribing
For extracted diagrams in `raw/assets/<Title>/`, use multimodal vision (`view_file`) to inspect the raster diagrams and transcribe key architecture topologies into live **Mermaid** blocks inside `wiki/concepts/` or `wiki/sources/`.

### 4. Audit & Lint Vault Graph Integrity
Validate 100% link resolution, orphan note detection, frontmatter schemas, and table formatting invariants:
```bash
python3 scripts/vault_lint.py /path/to/my-vault

# Automatically fix escaped pipe characters in tables:
python3 scripts/vault_lint.py /path/to/my-vault --fix
```

---

## 🚨 Critical Engineering Gotchas & Invariants

1. **Table Wikilink Invariant**:
   - Inside Markdown tables, **NEVER escape pipe characters** inside wikilink aliases.
   - ✅ Correct: `| [[Vertex AI Agent Engine|Agent Engine]] | Managed Runtime |`
   - ❌ Incorrect: `| [[Vertex AI Agent Engine\|Agent Engine]] | Managed Runtime |`
   - *Escaped pipes break Obsidian graph resolution and OKF linters.*

2. **Source Immutability**:
   - Never edit files in `raw/` directly after ingestion. If corrections are needed, document them in `wiki/sources/` or create a new versioned source.

3. **Reciprocal Wikilinks**:
   - When linking Note A $\rightarrow$ Note B, always check if Note B should reference Note A back. Bi-directional connections maximize graph density in Obsidian.

4. **OKF v0.2 YAML Frontmatter**:
   - Every note in `wiki/` must have OKF v0.2 frontmatter with `type` (plus recommended `title`, `tags`, `status`, `sources`, `generated`, and optional `aliases`). Omit `verified:` on agent-authored notes until explicit human review (`vault-lint --approve-human <note>`).

---

## 🔗 Inter-Skill Programmatic Integration

Other agent skills can integrate directly with the vault compiler utilities:

```python
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "scripts"))

from init_vault import init_vault
from extract_source import process_target
from vault_lint import run_vault_lint

# Initialize a project-specific vault
init_vault(Path("./project_vault"))

# Extract raw meeting transcript
process_target("./raw/meeting_transcript.txt", Path("./project_vault"))

# Audit graph integrity
report = run_vault_lint(Path("./project_vault"))
print(f"Vault Healthy: {report['is_healthy']}")
```
