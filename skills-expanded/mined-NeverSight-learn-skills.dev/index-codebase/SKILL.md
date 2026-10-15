---
name: index-codebase
description: Index a codebase for agent code understanding using codemogger (semantic + keyword search) and cx (symbol navigation). Optionally add zoekt (trigram regex). Use when preparing for architecture analysis, exploring an unfamiliar codebase, onboarding to a project, or when grep/ripgrep returns too many irrelevant matches. Do NOT use if indexes already exist and are current, for non-code assets, or for single-file lookups where grep suffices.
---

# Index Codebase

Set up local indexes that give agents fast, token-efficient code understanding. Two complementary tools:

- **codemogger** — semantic + keyword search ("find code related to authentication")
- **cx** — symbol navigation: overview, definition, references ("show me function X")

Together they cover **discovery** (find relevant code) and **navigation** (inspect specific symbols). Neither requires Docker, API keys, or running servers.

## When to Use Which

```
What does the agent need?
├─ "Find code related to <concept>"     → codemogger (semantic search)
├─ "What symbols are in this file?"     → cx overview
├─ "Show me function X"                 → cx definition
├─ "Where is X used?"                   → cx references
├─ "Find all files matching <pattern>"  → ripgrep (not this skill)
└─ "Understand full file context"       → Read tool (not this skill)
```

**Use codemogger** when the agent doesn't know symbol names yet — exploring an unfamiliar codebase, searching by concept, or finding code by natural language description.

**Use cx** when the agent knows a target — getting a file overview before reading, extracting a function body before editing, or tracing references before refactoring.

**Use both** for architecture analysis: codemogger discovers relevant modules → cx navigates their internals.

## Instructions

### Step 1. Check what's already indexed

```bash
# codemogger — check for existing database
ls .codemogger/ 2>/dev/null && echo "codemogger: indexed" || echo "codemogger: not indexed"

# cx — check for existing index
ls .cx-index.db 2>/dev/null && echo "cx: indexed" || echo "cx: not indexed"
```

If both exist and files haven't changed significantly, skip to Step 4 (verify). If files changed since last codemogger index, run `npx codemogger reindex` instead of full index. cx updates automatically on invocation (mtime-based).

### Step 2. Install and index with cx

cx is a Rust binary. Install once:

```bash
# Check if installed
cx --version 2>/dev/null || cargo install cx-cli
```

Install language grammars for the project's languages. cx auto-detects what's needed:

```bash
cx overview src/main.rs 2>&1 || true
# If cx reports missing grammars, it prints the exact install command:
# cx lang add rust typescript python  (adjust to project languages)
```

First invocation builds `.cx-index.db` automatically. Add to `.gitignore`:

```bash
grep -q '.cx-index.db' .gitignore 2>/dev/null || echo '.cx-index.db' >> .gitignore
```

### Step 3. Install and index with codemogger

```bash
npx codemogger index .
```

This parses all source files with tree-sitter, chunks them into semantic units, embeds them with a local model (~22MB, no API key), and stores everything in `.codemogger/`. First run on a large codebase takes minutes; incremental updates are fast.

Add to `.gitignore`:

```bash
grep -q '.codemogger' .gitignore 2>/dev/null || echo '.codemogger/' >> .gitignore
```

### Step 4. Verify

Run test queries to confirm both indexes work:

```bash
# cx: file overview (should list symbols with signatures)
cx overview "$(find . -name '*.rs' -o -name '*.ts' -o -name '*.py' | head -1)"

# cx: project-wide symbol search
cx symbols --kind fn | head -10

# codemogger: semantic search
npx codemogger search "main entry point"
```

Each must return at least 1 result. If cx reports missing grammars, install them with `cx lang add <language>`.

### Step 5 (Optional). Zoekt for trigram regex search

For very large codebases (>10k files) where complex regex patterns are needed:

```bash
# Install if missing
which zoekt-index || go install github.com/sourcegraph/zoekt/cmd/...@latest

# Index
zoekt-git-index -index ~/.zoekt .
```

## Agent Workflow After Indexing

The indexed codebase enables this escalation hierarchy — start cheap, escalate only when needed:

| Step | Tool | Token cost | When |
|------|------|-----------|------|
| Discover | `npx codemogger search "concept"` | ~500 tokens | Don't know what to look for |
| Overview | `cx overview <file>` | ~200 tokens | Know the file, want structure |
| Navigate | `cx definition --name <symbol>` | ~200 tokens | Know the symbol, want body |
| Trace | `cx references --name <symbol>` | ~100–500 tokens | Need impact analysis |
| Deep read | Read tool | ~1,200 tokens | Need full file context |

Instruct agents via cx's built-in skill file:

```bash
# For Claude Code
cx skill > ~/.claude/CX.md
# Add @CX.md to ~/.claude/CLAUDE.md

# For AGENTS.md-compatible tools
cx skill >> AGENTS.md
```

## Non-Negotiables

- At minimum **one** index must exist after completion (cx or codemogger).
- Both `.cx-index.db` and `.codemogger/` must be in `.gitignore`.
- A test query on each installed tool must return at least 1 result.
- Do NOT modify any source files during indexing.

## Output

```
Index complete.
- cx: <N> files indexed in .cx-index.db (languages: rust, typescript, ...)
- codemogger: <N> files indexed in .codemogger/
- zoekt: indexed at ~/.zoekt/ (if applicable)
- .gitignore: updated
- Agent skill file: cx skill injected into AGENTS.md (if applicable)
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `cx: no language grammars installed` | Run `cx lang add <languages>` — cx tells you which |
| `cx: database locked` | Another cx process is writing. Wait 2s or `rm .cx-index.db` |
| codemogger returns 0 results | Run `npx codemogger reindex .` |
| cx not found | `cargo install cx-cli` (requires Rust toolchain) |
| codemogger slow on first run | Normal — embedding is ~97% of time. Subsequent runs are incremental |
| Monorepo indexes too much | Use `--root` with cx or scope codemogger to a subdirectory |

## In This Reference

| Tool | What it does | Query style |
|------|-------------|-------------|
| **cx** | Symbol index + byte-range extraction | Exact: name, kind, file filters |
| **codemogger** | AST-chunked embeddings + dual search | Fuzzy: natural language + keywords |
| **zoekt** | Trigram regex index | Regex patterns across all files |
| **ripgrep** | Line-level text search | Exact text/regex (no indexing) |
