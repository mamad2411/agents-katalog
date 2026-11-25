---
name: agent-assimilation-pipeline
description: Orchestrate scan, analyze, generate, registry build, and hook execution with dry-run/verbose modes.
---

# Agent Assimilation Pipeline

Orchestrate scan, analyze, generate, registry build, and hook execution with dry-run/verbose modes.

## When to Use

Use this skill when:

- Working with code in `src\commands\assimilate.ts/`
- User mentions "assimilate"
- User mentions "analyze"
- User mentions "generate"
- User mentions "registry"
- User mentions "hooks"

## Patterns

- phased pipeline: Scan → Analyze → Generate → Registry → Hooks
- output path selection for remote vs local targets
- Copilot SDK analysis integration boundary
- summary and cleanup of temporary clones

## Examples

```
const analysisResult = await analyzer.analyze(scanResult);
```

## Category

**architecture** - Structural patterns and system design
