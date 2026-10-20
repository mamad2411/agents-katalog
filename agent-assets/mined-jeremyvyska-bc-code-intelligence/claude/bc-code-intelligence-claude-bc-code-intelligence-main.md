# BC Code Intelligence Knowledge Repository

This repository contains structured knowledge for Business Central AL development, organized by specialist domains.

## Repository Structure

```
domains/           # Knowledge topics organized by specialist
  {specialist}/    # e.g., dean-debug/, roger-reviewer/
    *.md           # Topic files (conceptual, no code)
    samples/       # AL code examples for each topic
workflows/         # Workflow v2 definitions (YAML)
scripts/           # Validation scripts
templates/         # Templates for new content
indexes/           # Auto-generated indexes
```

## Writing Knowledge Topics

**Key principle**: Keep topic files atomic and conceptual, preferably under 100 lines after the frontmatter. All AL code samples go in a separate `samples/` file within the same domain folder, the file name matching the topic name.

### File Structure

For a new topic, create two files:
1. `domains/{specialist}/topic-name.md` - Conceptual guidance (no code)
2. `domains/{specialist}/samples/topic-name.md` - All AL code examples

See templates:
- `templates/knowledge.md` - Topic file template
- `templates/samples.md` - Samples file template

### Why Separate Samples?

- **Atomic topics**: Agents can load just the concept without code overhead
- **On-demand code**: Samples loaded only when implementation needed
- **Smaller context**: Keeps knowledge retrieval efficient
- **Easier maintenance**: Update code without touching concepts

### Required Frontmatter

```yaml
title: "Descriptive Title"
domain: "specialist-name"        # Must match folder name
difficulty: "beginner|intermediate|advanced"
tags: ["tag1", "tag2"]
samples: "samples/topic-name.md" # Points to code file
```

### V2 Relevance Signals

```yaml
relevance_signals:
  constructs: []                 # AL constructs: FindSet, SetLoadFields, etc.
  keywords: []                   # Technical terms for matching
  anti_pattern_indicators: []    # Phrases indicating bad patterns
  positive_pattern_indicators: [] # Phrases indicating good patterns

applicable_object_types: []      # codeunit, page, table, report, etc.
relevance_threshold: 0.5         # 0.0-1.0 (higher = stricter)
```

### Threshold Guidelines

| Threshold | Use Case |
|-----------|----------|
| 0.3-0.4 | Informational, good patterns |
| 0.5-0.6 | Standard patterns, common issues |
| 0.7-0.8 | Critical issues, security concerns |

### Topic Content (No Code)

1. **Overview** - What and why (2-3 sentences)
2. **How It Works** - Conceptual explanation
3. **When to Apply** - Bullet list of scenarios
4. **Best Practices** - Grouped guidance
5. **Common Mistakes** - What to avoid
6. **Summary** - Key takeaways
7. Footer linking to samples and related topics

### Samples Content (All Code)

- Good pattern examples with comments
- Bad pattern examples marked with ❌
- Corrected versions marked with ✅
- Multiple scenarios showing usage

## Validation

Run before committing:

```powershell
./scripts/frontmatter_validator.ps1 -Path "domains" -ExcludeSamples
```

## Specialists

| Domain | Focus Area |
|--------|------------|
| alex-architect | API design, architecture patterns |
| dean-debug | Performance, telemetry, SIFT |
| eva-errors | Error handling, validation |
| jordan-bridge | Integration, events |
| maya-mentor | Learning, syntax guidance |
| quinn-tester | Testing patterns |
| roger-reviewer | Code review, formatting |
| sam-coder | Coding patterns, AL idioms |
| seth-security | Security, permissions |
| taylor-docs | Documentation |
| uma-ux | User experience |
| victor-versioning | BC version migration, breaking changes |
