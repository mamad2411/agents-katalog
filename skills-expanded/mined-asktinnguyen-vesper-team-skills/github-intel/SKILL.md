---
name: github-intel
description: This skill should be used when the user asks to "discover trending repos", "find GitHub repositories", "research AI coding tools", "crawl GitHub for best practices", "extract code patterns from repos", "build knowledge from GitHub", "find Claude Code extensions", "discover MCP servers", or mentions finding valuable open source code, extracting architecture patterns, or building compound documentation from repositories.
version: 1.0.0
---

# GitHub Intelligence Skill

Automated discovery and analysis of GitHub repositories to extract valuable code, architecture patterns, best practices, and compound documentation. Uses subagents for parallel research and knowledge extraction.

## Overview

This skill provides a complete pipeline for:
1. **Discovery** - Find trending repos matching keywords (Claude Code, Codex, MCP, agents, etc.)
2. **TODO Generation** - Create structured exploration tasks for each repo
3. **Exploration** - Clone and analyze repos with specialized subagents
4. **Extraction** - Capture valuable patterns to knowledge store
5. **Indexing** - Semantic vector search via QMD integration

## Quick Start

```bash
# Discover trending repos
./crawler/run.sh discover

# Check discovery status
./crawler/run.sh status

# Explore a specific repo
./crawler/run.sh explore <repo-name>

# Extract knowledge
./crawler/extract.sh add <category> <name>

# Search indexed repos (requires QMD)
qmd vsearch "multi-agent orchestration" -c ai-coding-repos
```

## Discovery Pipeline

### Step 1: Configure Search

Edit `crawler/config.sh` to customize:

```bash
# Minimum stars threshold
MIN_STARS=50

# Days since last update
DAYS_AGO=90

# Keywords to search
KEYWORDS=(
    "claude-code"
    "codex cli"
    "mcp server"
    "ai coding assistant"
    "llm code generation"
)
```

### Step 2: Run Discovery

```bash
./crawler/run.sh discover
```

Outputs:
- Individual TODO files in `todos/repos/`
- Index file at `todos/repos/INDEX.md`
- Sorted by stars, deduplicated

### Step 3: Index for Semantic Search

```bash
# Create QMD collection
qmd collection add todos/repos --name ai-coding-repos --mask "*.md"

# Generate vector embeddings
qmd embed
```

## Subagent Orchestration

### Exploration Subagent

Triggered via `./crawler/run.sh explore <repo-name>`:

1. Clones repository to `.clones/`
2. Analyzes codebase structure
3. Identifies key files and patterns
4. Updates TODO with findings

Use the exploration prompt template:
```bash
cat crawler/prompts/explore.md
```

### Review Subagent

For deep code analysis, spawn a review subagent:

```
Launch Explore agent to analyze the codebase at .clones/<repo-name>

Focus on:
1. Architecture patterns worth extracting
2. Reusable utilities and helpers
3. Novel approaches to common problems
4. Code quality and best practices
```

### Compound-Docs Subagent

For knowledge extraction:

```
Launch agent to create compound documentation for <pattern-name>

Extract from .clones/<repo-name>:
1. Core concept explanation
2. Implementation details
3. Code examples
4. Usage patterns
```

## Knowledge Store Structure

```
knowledge/
├── architecture/     # System design patterns
├── patterns/         # Code patterns and idioms
├── utilities/        # Reusable helper code
├── frameworks/       # Framework-specific knowledge
└── INDEX.md          # Master index
```

### Adding Knowledge

```bash
# Interactive extraction
./crawler/extract.sh add architecture "plugin-system"
./crawler/extract.sh add patterns "hook-interceptor"
./crawler/extract.sh add utilities "regex-cache"
```

### Knowledge Entry Format

Each entry in `knowledge/<category>/<name>.md`:

```markdown
# Pattern Name

**Source:** repo-name
**Category:** architecture|patterns|utilities|frameworks

## Overview
Brief description of the pattern.

## Implementation
Code examples and details.

## Usage
When and how to apply this pattern.

## References
Links to source files.
```

## Workflow Examples

### Example 1: Discover Claude Code Extensions

```bash
# Set focused keywords
export CRAWLER_KEYWORDS="claude-code skill hook mcp-server"

# Run discovery
./crawler/run.sh discover

# Check results
./crawler/run.sh status
```

### Example 2: Deep Dive into a Repo

```bash
# Explore the repo
./crawler/run.sh explore anthropics-claude-code

# Launch exploration agent
# (In Claude Code session)
> Explore the codebase at .clones/anthropics-claude-code
> Focus on plugin architecture and hook system
```

### Example 3: Extract and Document Pattern

```bash
# After exploring, extract pattern
./crawler/extract.sh add patterns "progressive-disclosure"

# Edit the generated file
# Add implementation details from exploration
```

### Example 4: Semantic Search

```bash
# Search for specific concepts
qmd vsearch "multi-agent workflow" -c ai-coding-repos -n 10

# Combined search with reranking
qmd query "how to implement hooks" -c ai-coding-repos
```

## Prompt Templates

### Exploration Prompt

Located at `crawler/prompts/explore.md`:
- Initial codebase analysis
- Structure discovery
- Key file identification
- Pattern recognition

### Review Prompt

Located at `crawler/prompts/review.md`:
- Deep code analysis
- Quality assessment
- Best practice identification
- Improvement suggestions

### Compound-Docs Prompt

Located at `crawler/prompts/compound.md`:
- Knowledge extraction format
- Documentation structure
- Example generation
- Cross-referencing

## Integration with Other Skills

### With /commit

After extracting knowledge:
```bash
git add knowledge/
/commit
```

### With Code Review

Spawn parallel review agents:
```
Launch 3 review agents in parallel to analyze:
1. .clones/repo-a - focus on architecture
2. .clones/repo-b - focus on patterns
3. .clones/repo-c - focus on utilities
```

### With QMD Search

```bash
# Find related patterns
qmd query "your search" -c ai-coding-repos --files

# Get full document
qmd get qmd://ai-coding-repos/repo-name.md
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `crawler/run.sh` | Main entry point |
| `crawler/discover.sh` | GitHub API crawler |
| `crawler/generate-todos.sh` | TODO file generator |
| `crawler/extract.sh` | Knowledge extraction |
| `crawler/config.sh` | Configuration |

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `MIN_STARS` | 50 | Minimum repo stars |
| `DAYS_AGO` | 90 | Max days since update |
| `RATE_LIMIT_SLEEP` | 2 | Seconds between API calls |
| `CRAWLER_KEYWORDS` | (see config) | Search keywords |

## Additional Resources

### Reference Files

- **`references/workflow.md`** - Detailed workflow guide
- **`references/subagents.md`** - Subagent patterns
- **`references/qmd-integration.md`** - QMD search setup

### Example Files

- **`examples/discovery-output.json`** - Sample discovery results
- **`examples/knowledge-entry.md`** - Template for knowledge entries

### Scripts

- **`scripts/batch-explore.sh`** - Batch exploration utility
- **`scripts/sync-qmd.sh`** - QMD index synchronization
