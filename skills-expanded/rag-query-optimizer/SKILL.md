---
name: rag-query-optimizer
description: Automatically analyzes RAG pipeline retrieval results and generates optimized query refinement suggestions to improve answer relevance.
---

# rag-query-optimizer

## 1. Name & Description

**rag-query-optimizer** — Automatically analyzes RAG pipeline retrieval results and generates optimized query refinement suggestions to improve answer relevance.

## 2. Core Capabilities

- Analyze RAG pipeline retrieval results for relevance patterns and gaps
- Detect low-relevance retrievals through statistical score analysis
- Identify query-document semantic mismatches
- Generate intelligent query refinement suggestions based on retrieval analysis
- Suggest synonym expansions and contextual rewrites
- Recommend query decomposition strategies for complex queries
- Support multiple RAG pipeline configurations and retrieval strategies
- Provide CLI interface for direct query optimization tasks
- Integrate seamlessly with OpenClaw agent workflows
- Handle errors gracefully with non-zero exit codes on failure

## 3. Triggers

- "I need to optimize my RAG queries"
- "Analyze my retrieval results and suggest query improvements"
- "Help me refine my RAG pipeline queries for better relevance"
- "Generate query optimization suggestions for my RAG system"
- "My RAG retrieval needs improvement, what query refinements do you suggest?"
- "Review my RAG pipeline and provide query refinement recommendations"
- "Automate query refinement analysis for our RAG system"
- "How can I improve my retrieval relevance scores?"
- "Suggest better queries for my RAG pipeline"
- "Optimize search queries for my document retrieval system"

## 4. Out of Scope

- Does not execute actual RAG pipelines or perform retrievals
- Does not implement query refinement (only generates suggestions)
- Does not provide vector database management or indexing
- Does not handle document preprocessing or chunking
- Does not offer real-time query monitoring or dashboarding
- Does not support proprietary RAG framework integrations
- Does not provide performance benchmarking tools
- Does not manage embedding model selection or training

## 5. References

- `references/rag-patterns.md` — Common RAG optimization patterns for analysis matching
- `references/query-techniques.md` — Query refinement methodologies used by the suggestion engine
- `references/config-examples/` — Sample configurations for different RAG systems

## 6. Key Files

- `SKILL.md` — Skill documentation and metadata
- `README.md` — User guide and usage documentation
- `scripts/main.js` — CLI entry point and orchestration logic
- `scripts/analyzer.js` — RAG retrieval analysis engine
- `scripts/suggester.js` — Query refinement suggestion generator
- `scripts/config.js` — Configuration management and validation
- `scripts/error-handler.js` — Error handling and exit management
- `scripts/utils.js` — Shared utility functions
- `references/rag-patterns.md` — Optimization patterns reference
- `references/query-techniques.md` — Refinement methodologies reference
- `assets/examples/` — Sample input/output datasets
- `assets/templates/` — Configuration templates

## 7. API Usage

```bash
# Analyze a retrieval results file
node scripts/main.js analyze <results-file>

# Analyze with custom configuration
node scripts/main.js analyze <results-file> --config <config-file>

# Output as JSON
node scripts/main.js analyze <results-file> --format json

# Show help
node scripts/main.js --help
```

## 8. Integration

Agent workflow integration:

1. Agent sends retrieval results via `sessions_send`
2. Skill deployed via `sessions_spawn` with task "optimize-query"
3. Results returned through `message` tool to user's session

```bash
# Example agent invocation
node scripts/main.js analyze results.json --format json
```

## 9. Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success — suggestions generated |
| 1 | General error — unexpected failure |
| 2 | Invalid input — malformed results file |
| 3 | Configuration error — invalid config |
| 4 | No results — empty retrieval data |
