---
name: openai-security-ownership-map
description: Analyzes git history to build a security ownership map, compute bus factors, and identify orphaned sensitive code. Useful for risk assessment and maintainer mapping.
allowed-tools:
- Bash
- Read
- Grep
- Glob
- Write
- Edit
metadata:
  version: 0.2.0
  category: security-analysis
---
# Security Ownership Map

## Quick Start
```bash
python scripts/run_ownership_map.py \
  --repo . \
  --out ownership-map-out \
  --since "12 months ago" \
  --emit-commits
```

## Workflow
1. **Scope Repo**: Define the target repository and time window (`--since`/`--until`).
2. **Define Rules**: Set sensitivity rules for tagging files (e.g., auth, crypto, secrets).
3. **Build Map**: Run `run_ownership_map.py` to generate the ownership and co-change graphs.
4. **Query Risk**: Use `query_ownership.py` to identify orphaned code, bus factor hotspots, and hidden owners.
5. **Cluster Files**: Analyze communities to understand how files are maintained together.
6. **Export/Visualize**: Export to GraphML or Neo4j for deep architectural insights.

## Rules & Constraints
- **RULE-1**: Exclude bots (e.g., dependabot) by default via `--ignore-author-regex`.
- **RULE-2**: Ignore large, noisy commits (e.g., lockfiles, `.github/*`) in co-change graphs.
- **RULE-3**: Merge commits are excluded by default to avoid attribution noise.
- **RULE-4**: Always use bounded JSON slices (`query_ownership.py`) instead of loading the full graph into context.

## When to Use
- Identifying owners for critical code paths during risk assessments.
- Mapping ownership drift or highlighting code with dangerously low bus factors.
- Discovering orphaned or stale sensitive code.

## When NOT to Use
- Analyzing code content or functionality (use standard security scanners).
- Assessing real-time contributor activity (this tool focuses on historical ownership).

## References
- [Skill Manual](references/openai-security-ownership-map-manual.md)
- [Neo4j Import Guide](references/neo4j-import.md)
