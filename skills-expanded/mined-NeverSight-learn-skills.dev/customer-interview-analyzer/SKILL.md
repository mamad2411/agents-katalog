---
name: customer-interview-analyzer
description: Use when a PM or UX researcher has interview transcripts (text/Notion/Drive) and needs themes, pain points, JTBD, and verbatim quotes synthesized into a research report.
---

# Customer Interview Analyzer

## When to invoke
- "Synthesize these 12 user interviews."
- "What are the top pain points across last quarter's research?"
- "Pull JTBD statements from these transcripts."

## Inputs needed
1. **Transcripts** — folder of `.txt`/`.md`/`.vtt` files, or Notion/Drive docs.
2. **Research question** (optional) — focuses the analysis.
3. **Persona / segment tags** (optional).

## Workflow
1. **Ingest** — load all transcripts; clean speaker labels.
2. **Code** — extract candidate themes by frequency + co-occurrence.
3. **Cluster** — group similar codes into themes; tag each with a verbatim quote.
4. **Report** — produce: research question, methodology, themes (with frequency), JTBD statements, surprises, recommendations.

## Output format
```
## Research question
## Methodology (n, recruit, dates)
## Themes (ranked)
  Theme — # mentions — verbatim — implication
## JTBD statements
## Surprises / disconfirmations
## Recommendations
```

## Guardrails
- Always cite a verbatim quote with source file + line for every theme.
- Distinguish observations (what users said/did) from interpretations.
- Surface contradictions across interviews.

## Reference code
`analyze.py` does keyword + n-gram extraction with simple clustering. Optional `--llm` flag uses any chat-completions API for richer themes (provide endpoint + key via env vars).
