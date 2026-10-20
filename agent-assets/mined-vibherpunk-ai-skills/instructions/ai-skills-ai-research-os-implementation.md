# Copilot Instructions: Ai Research Os Implementation
Description: A comprehensive system for transforming personal research notes and external sources into a queryable, evolving knowledge base using AI agents and file-based indexing.

# AI Research Operating System Skill

## Overview

This skill transforms scattered research materials into an organized, queryable knowledge base using a file-based approach. Unlike traditional RAG systems, it emphasizes:

- **Personal Context**: Anchors research in your existing notes and values ([Core Concepts](references/core_concepts.md))
- **Progressive Disclosure**: Minimizes token usage through hierarchical data access
- **Living Documentation**: Evolves with each interaction through automatic wiki updates

## Workflow

1. **Initialize Project**
   - Create project directory with standard structure ([Workflow Guide](references/workflow_guide.md#1-initial-setup))
   - Connect relevant data sources (Obsidian, Readwise, GitHub)

2. **Ingest Sources**
   - Add materials via CLI or API:
     ```bash
     python ingest.py --type=youtube --url=https://youtu.be/agent_tutorial
     ```
   - System generates summaries and updates index.yaml

3. **Conduct Research**
   - Run targeted queries with depth control:
     ```python
     research("attention mechanisms", depth="light")
     ```
   - Agent follows [query protocol](references/core_concepts.md#progressive-disclosure)

4. **Review Outputs**
   - Check generated wiki pages in Obsidian
   - Verify automatic concept linking
   - Monitor open_questions/ directory

5. **Iterate**
   - Add follow-up questions to expand wiki
   - Re-index when adding significant new sources

## Best Practices

- **Start Small**: Begin with 2-3 key sources before scaling up
- **Depth Control**: Use 'light' research mode for 80% of cases
- **Source Diversity**: Combine codebases, articles, and videos
- **Regular Review**: Audit open questions weekly

## Common Pitfalls

1. **Over-Indexing**
   - Example: Running 'deep' research on broad topics
   - Fix: Scope topics narrowly ("Transformer memory" vs "AI")

2. **Stale Derivatives**
   - Example: Not updating comparisons when new research emerges
   - Fix: Set calendar reminders for key topics

3. **Source Overload**
   - Example: Adding 100+ papers without curation
   - Fix: Pre-filter with [ranking algorithm](references/code_examples.md#source-ranking-algorithm)

## Validation

1. **Completeness Check**
   - Verify all expected concepts appear in wiki/
   - Confirm bidirectional links between related topics

2. **Freshness Test**
   - Check ingested_date in index.yaml for key sources
   - Run timestamp comparison:
     ```python
     if (now - ingested_date) > timedelta(days=90):
         trigger_reindex()
     ```

3. **Query Accuracy**
   - Compare agent responses against source material
   - Track precision/recall for sample questions

## Maintenance

- Archive stale projects to `/research_archive/`
- Prune low-value derivatives quarterly
- Update connectors when APIs change

For complete implementation details, see:
- [Core Architecture](references/core_concepts.md)
- [Workflow Examples](references/workflow_guide.md)
- [Code Templates](references/code_examples.md)

## Reference Guides

### Code Examples

# Implementation Code Samples

## Index YAML Structure

```yaml
# index.yaml example
sources:
  - origin: "github"
    title: "OpenAI GPT-3 Repository"
    authors: "OpenAI"
    url: "https://github.com/openai/gpt-3"
    summary: "Main repository for GPT-3 containing model architecture and examples"
    ingested_date: "2023-11-15"
    wiki_derivatives:
      - "wiki/concepts/transformer_architecture.md"
      - "wiki/comparisons/gpt3_vs_palm.md"

wiki_pages:
  - "wiki/concepts/agent_loops.md"
  - "wiki/entities/openai.md"
```

## Research Agent Prompt Template

```python
def generate_research_questions(topic, existing_context):
   prompt = f"""You are an AI research assistant. Given the following topic and context:
   TOPIC: {topic}
   CONTEXT: {existing_context}
   
   Generate 3-5 specific research questions that would:
   1. Explore unknown aspects of the topic
   2. Connect to related concepts in our knowledge base
   3. Identify practical implementation concerns
   
   Format as a numbered list with brief rationale for each question."""
   return llm_query(prompt)
```

## Source Ranking Algorithm

```python
def rank_sources(sources, topic):
   """Score sources 0-1 based on relevance to topic"""
   scores = []
   for source in sources:
       prompt = f"""Rate relevance from 0-1:
       Topic: {topic}
       Source: {source['summary']}
       
       Consider:
       - Depth of coverage
       - Authority of author
       - Novelty of information
       - Practical applicability
       
       Return ONLY a decimal number."""
       score = float(llm_query(prompt))
       scores.append((source, score))
   
   return sorted(scores, key=lambda x: x[1], reverse=True)
```

### Core Concepts

# Core Concepts of AI Research OS

## Three-Layer Architecture

The system operates on three distinct layers:
1. **Raw Layer**: Immutable source files (articles, videos, code repos) stored in their original format
2. **Index Layer**: A YAML-based catalog containing metadata and summaries of all sources
3. **Wiki Layer**: AI-generated derivatives including:
   - Concept explanations
   - Entity definitions
   - Comparative analyses
   - Open research questions

## Key Principles

- **File-Based Organization**: Avoids complex databases in favor of simple file structures
- **Progressive Disclosure**: Agents first check summaries, then wiki pages, only accessing raw sources when necessary
- **Organic Growth**: Every interaction leaves traces in the wiki through new concepts or notes
- **Project-Centric**: Research is scoped to specific initiatives (articles, videos, codebases)

## Component Integration

The system connects with:
- Obsidian for note management
- Readwise for content highlights
- Notebook LM for research assistance
- GitHub for codebase analysis
- Web scrapers for external content

Each component remains independent while contributing to the unified index, allowing for flexible customization based on user needs.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Turn 10,994 Notes Into Memory - Paul Iusztin, Decoding AI & Louis-François Bouchard, Towards AI](https://www.youtube.com/watch?v=ZRM_TfEZcIo)** by AI Engineer

### Workflow Guide

# Step-by-Step Implementation Guide

## 1. Initial Setup

1. Create directory structure:
   ```
   research_os/
   ├── raw/
   ├── wiki/
   │   ├── concepts/
   │   ├── comparisons/
   │   └── entities/
   └── index.yaml
   ```

2. Configure integrations:
   - Set up Obsidian vault symlink
   - Install Readwise CLI
   - Configure API access for Notebook LM

## 2. Ingestion Process

For new content:
1. Run ingestion script with source type and location:
   ```python
   python ingest.py --type=github --url=https://github.com/openai/gpt-3
   ```

2. System will:
   - Download raw content
   - Generate executive summary
   - Extract key concepts
   - Update index.yaml

## 3. Research Workflow

1. Initiate research session:
   ```
   python research.py --topic="agent memory management" --depth=light
   ```

2. Agent will:
   - Formulate research questions
   - Query connected systems
   - Rank results by relevance
   - Generate wiki derivatives

## 4. Ongoing Maintenance

- Weekly review of `open_questions/` directory
- Monthly re-indexing of priority projects
- Quarterly archive of stale research

## 5. Query Interface

```python
from research_os import query_engine

response = query_engine(
   wiki_path="/path/to/project_wiki",
   question="How do major harnesses implement sandboxing?",
   context_level="summary"  # summary|wiki|raw
)
```