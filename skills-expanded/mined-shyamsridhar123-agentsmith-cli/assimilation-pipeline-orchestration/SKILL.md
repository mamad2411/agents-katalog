---
name: assimilation-pipeline-orchestration
description: "Use to run the end-to-end assimilation phases - scan, analyze via Copilot SDK, license check, generate assets, build registry, and execute hooks."
---

# Assimilation Pipeline Orchestration

Use to run the end-to-end assimilation phases: scan, analyze via Copilot SDK, license check, generate assets, build registry, and execute hooks.

## When to Use

Use this skill when:

- Working with code in `src/commands/assimilate.ts/`
- User mentions "assimilate"
- User mentions "generate"
- User mentions "pipeline"
- User mentions "copilot"
- User mentions "post-generate"

## Patterns

- phase-based workflow with ordered execution
- dry-run and verbose options gating side effects
- remote cloning and temporary cleanup
- license policy gate before generation
- post-generate hook execution with failure handling

## Examples

```
new Scanner(resolved.path, options.verbose).scan(); new Analyzer(options.verbose).analyze(scanResult); const generator = new Generator(outputPath, options.dryRun, options.verbose);
```

## Category

**architecture** - Structural patterns and system design
