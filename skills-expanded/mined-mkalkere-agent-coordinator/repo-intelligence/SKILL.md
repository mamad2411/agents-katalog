---
name: repo-intelligence
version: 1.0.0
description: Build and query repository understanding for context-aware work
uses:
  - core/repo-indexing
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - repo:read
  requires_approval: false
---

# Repository Intelligence

Build deep understanding of a repository through accumulated experience. This knowledge persists across sessions, enabling increasingly informed work — better reviews, better implementations, and faster onboarding.

## Execution Model

This is a **builtin skill** (`handler: type: builtin`). When `query_repo_context` is invoked, the executor reads from accumulated intelligence files in the agent's memory directory (patterns, conventions, known issues, file relationships, review trajectories). The tool schema in tool.yaml defines the external contract; the executor handles the retrieval directly.

## When to Use

- Before starting any work on a file — understand its context
- Before reviewing code — load known issues and patterns
- After reviewing code — update known issues and record trajectory
- When onboarding to a new repository — run initial analysis
- When diagnosing a problem — check known issue patterns

## Methodology

### 1. Initial Analysis (First Time or Stale)

On first encounter with a repository, analyze:
- **Language and frameworks**: Detect tech stack from config files and source code
- **Patterns and conventions**: Code style, naming conventions, architectural patterns
- **File relationships**: Which files depend on which, test-to-implementation mappings
- **Known issues**: Existing problems detected by analysis

### 2. Record Repository Context

Store structured intelligence in agent memory:

| File | Content |
|------|---------|
| `repo_context.yaml` | Language, frameworks, patterns, conventions |
| `file_relationships.yaml` | Dependency and test mappings |
| `known_issues.yaml` | Persistent list of known problems |
| `conventions.yaml` | Coding style and project conventions |
| `trajectories/` | Review history per PR/task |

### 3. Query Before Work

Before starting any work, load relevant context:
- What patterns does this codebase use?
- Are there known issues in the files I'm touching?
- What test files correspond to these implementation files?
- What have previous reviews found in this area?

### 4. Update After Work

After completing work, update intelligence:
- New patterns discovered → update `repo_context.yaml`
- New issues found → add to `known_issues.yaml`
- Review completed → create trajectory in `trajectories/`
- Conventions clarified → update `conventions.yaml`

### 5. Accumulate Over Time

Intelligence improves with each session:

| Sessions | Knowledge Level |
|----------|----------------|
| 1 | Basic tech stack detection |
| 2–3 | Pattern recognition, testing conventions |
| 5+ | Known issues library, common pitfalls |
| 10+ | Deep file relationship map |
| 20+ | Comprehensive codebase understanding |

## Output Format

```
## Repository Intelligence

### Repository Context
- Language: [language]
- Frameworks: [list]
- Test framework: [framework]
- Code style: [conventions]

### Known Issues (relevant to query)
| # | Severity | Issue | Location | Status |
|---|----------|-------|----------|--------|
| 1 | [level] | [description] | [file:line] | [open/resolved] |

### File Relationships
- [file] → test: [test file]
- [file] → depends on: [dependencies]
- [file] → depended on by: [dependents]

### Review History
- [PR/task]: [verdict] — [key findings]
```

## Quality Criteria

- Repository context is accurate and up-to-date
- Known issues are verified (not false positives)
- File relationships reflect actual dependencies
- Review trajectories capture key findings and lessons
- Intelligence is updated after each work session
- Stale intelligence is identified and refreshed

## Common Mistakes

- **Not loading context before work**: Starting a review or implementation without checking known issues and patterns. You'll miss things that previous sessions already identified.
- **Not updating after work**: Completing a review but not recording the trajectory or new findings. The next session loses that knowledge.
- **Trusting stale intelligence**: Using context from weeks ago without checking if the codebase has changed. Always compare to recent commits.
- **Over-relying on intelligence**: Intelligence is a guide, not a replacement for actual analysis. Always verify against current code.
- **Not recording negative findings**: Only recording issues, not patterns that are correct. Recording "this codebase handles async correctly" is also valuable.
- **Hardcoding provider-specific details**: Intelligence should describe the codebase, not reference specific AI tools or providers. Keep it provider-agnostic.

## Completion

Repository intelligence is complete when:
- Initial analysis has been run and context files created
- Known issues are catalogued with severity and location
- File relationships are mapped
- Intelligence is queryable for any file or pattern
- Context is updated after each work session
