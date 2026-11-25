---
name: copilot-sdk-analysis-session
description: Run semantic analysis with the Copilot SDK to extract skills, agents, and hooks.
---

# Copilot Sdk Analysis Session

Run semantic analysis with the Copilot SDK to extract skills, agents, and hooks.

## When to Use

Use this skill when:

- Working with code in `src/analyzer/`
- User mentions "analyze"
- User mentions "copilot"
- User mentions "skills"
- User mentions "agents"
- User mentions "hooks"

## Patterns

- invoke Analyzer.analyze on scan results
- derive skill definitions with category/triggers
- agent hierarchy construction
- hook definitions for lifecycle events

## Examples

```
const analyzer = new Analyzer(verbose); const analysis = await analyzer.analyze(scanResult);
```

## Category

**architecture** - Structural patterns and system design
