# Living Review

## Overview
Maintains a continuously updated, structured literature review for a research team. Ingests papers from multiple sources, synthesizes findings across the team's collective reading, and produces a living document that evolves as new work is published.

## When to Use
- User asks to "update our literature review" or "add this paper to the review"
- User wants a summary of what their team has read on a topic
- User asks "what do we know about X based on our papers?"
- Onboarding a new team member who needs a fast overview of prior work
- Preparing a manuscript introduction or related work section

## Key Capabilities
- Ingest PDFs, DOIs, arXiv IDs, or PubMed IDs into a shared knowledge base
- Extract key claims, methods, datasets, and limitations per paper
- Auto-group papers by theme, methodology, or recency
- Generate a structured Markdown or LaTeX review draft
- Track which team member added which paper and when
- Flag papers that conflict with or extend each other
- Diff the review against previous versions to show what changed

## Usage Examples

### Add a paper to the living review
```python
review.add_paper(
    doi="10.1038/s41586-024-00001-0",
    added_by="alice",
    tags=["transformer", "protein-folding", "benchmark"]
)
```

### Generate a living review draft on a topic
```python
review.generate_draft(
    topic="attention mechanisms in protein language models",
    format="latex",
    max_papers=40,
    include_team_notes=True
)
```

### Show what changed since last week
```python
review.diff(since="2024-01-01", show_new_papers=True, show_updated_claims=True)
```

## Output Format
Produces structured Markdown with sections: Background, Key Methods, Datasets Used, Open Questions, Recent Additions. Each claim is traceable to a source paper and team contributor.

## Notes
- Works best when combined with `arxiv-monitor` and `semantic-scholar` skills for automatic ingestion
- Team notes and annotations are preserved across updates — never overwritten
- Supports BibTeX export for manuscript preparation
