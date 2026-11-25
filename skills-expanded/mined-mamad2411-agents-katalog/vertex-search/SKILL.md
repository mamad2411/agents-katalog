---
name: vertex-search
description: Search knowledge from Vertex AI RAG (phsysics project). Use "/vertex-search <query>" or ask "Search in Vertex"
user-invocable: true
---

# Vertex AI RAG Search Skill

## Purpose
Search related knowledge from phsysics project's BigQuery (4,362 embeddings) + GCS (context/, decisions/, session_logs/)

## Search Method
1. Analyze query and extract keywords
2. BigQuery vector similarity search (COSINE_SIMILARITY)
3. GCS metadata search
4. Integrate and sort results by relevance

## Usage Examples
```bash
/vertex-search NoiseComputer multiplication rules
/vertex-search previous debate results
/vertex-search RTL optimization patterns
```

## Output Format
- Relevance score (0.0-1.0)
- Content snippet
- Source (BigQuery/GCS)
- GitHub link (if available)
- Timestamp

## Configuration
Edit `config/vertex_config.yaml` to adjust:
- `similarity_threshold`: Minimum relevance (default: 0.7)
- `max_results`: Maximum results to return (default: 10)

## Implementation
Python script: `.claude/skills/vertex-search/vertex_search.py`
- Uses BigQuery client for embedding similarity search
- Uses GCS client for metadata search
- Combines results with relevance ranking
