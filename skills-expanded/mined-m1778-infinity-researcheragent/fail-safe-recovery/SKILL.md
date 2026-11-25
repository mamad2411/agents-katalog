---
name: fail-safe-recovery
description: Deterministic fallback ladders and error recovery routines when APIs fail, tools return errors, or rate limits are encountered.
license: MIT
---

# Fail-Safe Recovery & Error Handling Protocol

When tools fail, network connections drop, or rate limits are reached, the agent must NOT panic, give up, or output generic apologies. Follow these explicit recovery ladders.

## 1. Search Engine Fallback Ladder

If an engine call returns an error or empty result:
```
Primary Call Failed
  ├── Step 1: Retry with simplified query (strip Boolean operators, quotes, or colons)
  ├── Step 2: Fall back to adjacent zero-cost engine:
  │     ├── arXiv failed          → Semantic Scholar or CrossRef
  │     ├── PubMed failed         → Europe PMC or CrossRef
  │     ├── Semantic Scholar 429  → arXiv API or CrossRef
  │     ├── DuckDuckGo blocked    → SearXNG or GitHub Code Search
  │     └── Exa budget exhausted  → Auto-divert to Semantic Scholar / arXiv
  └── Step 3: If all search APIs fail:
        └── Query local workspace artifacts, cached research files, or existing codebase
```

## 2. Command & Process Failure Recovery

When a command exits with code $\neq 0$:
1. **Analyze Stderr**: Read the exact error message and exit code.
2. **Diagnose Category**:
   - `ENOENT` / Missing file: Verify path existence with `ls` or `find` before retrying.
   - Syntax / Type error: Inspect target file lines around error report; fix source before re-running.
   - Timeout (code 124 / 30000ms): Break command into smaller atomic batches or add flags to bypass interactive pagers.
   - Permission denied: Verify execution permissions (`chmod +x`).

## 3. Rate Limit & Network Backoff Rules

- On HTTP 429 (Too Many Requests):
  - Do NOT hammer the endpoint in a tight loop.
  - Check headers for `Retry-After`.
  - Switch to an alternative unmetered zero-cost backend.

## 4. Graceful Degradation Principles
- Always return partial verified findings rather than failing completely.
- State clearly: "Source X was temporarily unreachable; retrieved supplementary evidence via Source Y."
