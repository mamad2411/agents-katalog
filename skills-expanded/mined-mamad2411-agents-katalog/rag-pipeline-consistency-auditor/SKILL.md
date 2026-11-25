---
name: rag-pipeline-consistency-auditor
description: "Audit RAG pipeline configuration for consistency issues that produce bad answers. Trigger: /rag-consistency"
trigger: /rag-consistency
---
# /rag-consistency

RAG applications are fragile: retrieval finds wrong content, context windows truncate, chunking splits mid-concept. This skill audits RAG configuration holistically.

## What this is for

- Chunk size vs context window mismatch (retrieved > context window → silent truncation)
- Embedding dimension vs vector index dimension mismatch
- Retriever config inconsistent with model capabilities
- **Read-only skill.** No code changes.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/rag-consistency -help` or `/rag-consistency -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir`. Get confirmation.

### Step 3 - Scan

```powershell
& "<SKILL_DIR>/scripts/rag-scan.ps1" -ProjectDir "<path>"
```

### Step 4 - Classification

For each RAG config:

- **Consistent**: all settings compatible
- **Overflow-risk**: retrieved tokens > context window
- **Mismatch**: embedding or model incompatibility

### Step 5 - Write report

File `rag-consistency-report.md` in current working directory:

1. **Summary** - configs by classification.
2. **Config table** - broken first. Per config: file, line, embedding model, LLM model, chunk size, top K, retrieved tokens, context window, overflow risk, recommendation.
3. **Open questions**.

### Step 6 - Summarize

State report path, highlight configurations that will produce bad retrieval results.

## Usage

```
/rag-consistency               # interactive
/rag-consistency <dir>         # scan project
/rag-consistency -help
```


