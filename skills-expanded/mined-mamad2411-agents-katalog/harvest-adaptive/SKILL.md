---
name: harvest-adaptive
description: Adaptive content summarization - auto-detect content type and produce relevant summary
allowed-tools: [Bash, Read, Write, WebFetch, WebSearch]
keywords: [digest, summary, evaluate, library, tool, article, adaptive, overview]
---

# Harvest Adaptive (Digest)

Automatically detect content type and produce the most useful summary. A blog post gets key takeaways. A library gets feature evaluation. Documentation gets structure overview. API reference gets endpoint catalog.

## Usage

```
/digest <url>
```

## Examples

```bash
# Evaluate a library
/digest https://github.com/owner/cool-library

# Summarize an article
/digest https://blog.example.com/microservices-patterns

# Overview documentation
/digest https://docs.example.com
```

## Content Type Detection

| Type | Signals | Output Style |
|------|---------|-------------|
| Library/Tool | GitHub repo, npm page, PyPI | Feature matrix, ecosystem health, recommendation |
| Blog/Article | Single long-form content | Key takeaways, relevance assessment |
| Documentation | Multi-page, navigation structure | Structure map, coverage assessment, quality |
| API Reference | Endpoints, methods, params | Endpoint catalog, auth info, SDK availability |
| Comparison | Tables, vs, alternatives | Feature matrix, winner per category |
| Tutorial | Step-by-step, code blocks | Prerequisites, steps summary, outcome |

## Output Templates

### Library Evaluation
```markdown
# Library: [name]
> Source: [URL] | Stars: [X] | Last commit: [date]

## What It Does
[1-2 sentence description]

## Key Features
- Feature 1
- Feature 2

## Ecosystem Health
| Metric | Value |
|--------|-------|
| GitHub Stars | X |
| Weekly Downloads | X |
| Last Release | date |
| Open Issues | X |
| Contributors | X |

## API Surface
[Key classes/functions/exports]

## Verdict
[Use when... Don't use when... Alternatives: ...]
```

### Article Summary
```markdown
# Summary: [title]
> Source: [URL] | Author: [name] | Date: [date]

## Key Takeaways
1. [Point 1]
2. [Point 2]
3. [Point 3]

## Relevance
[How this applies to current project/context]

## Action Items
- [What to do based on this]
```

## Rules

- Auto-detect, don't ask user for content type
- Keep summaries under 500 words
- Always include source URL and date
- For libraries: check last commit date, flag if > 6 months
- For articles: check publication date, flag if > 1 year
- Confidence rating on every assessment
