---
name: synthesize-research
description: >
  Transforms scattered research notes into a coherent, structured findings
  document. Consolidates dispersed research, identifies themes, surfaces
  contradictions, and highlights gaps. Use when you need to synthesize
  research, summarize findings across multiple files, or create a synthesis
  document from dispersed notes.
license: MIT
compatibility: Designed for Claude Code and similar AI coding assistants.
metadata:
  author: Octon Harness
  created: "2025-01-12"
  updated: "2026-02-10"
skill_sets: [executor]
capabilities: [domain-specialized]
allowed-tools: Read Glob Write(/.octon/inputs/exploratory/syntheses/*) Write(/.octon/state/evidence/runs/skills/*)
---

# Synthesize Research

Transform scattered research notes into coherent, structured findings documents.

## When to Use

Use this skill when:

- You have research notes scattered across multiple files
- You need to consolidate findings into a single document
- You want to identify themes and patterns across research
- You need to surface contradictions or gaps in research

## Quick Start

```markdown
/synthesize-research /.octon/instance/capabilities/runtime/skills/resources/synthesize-research/topic/
```

## Core Workflow

1. **Gather Materials** - Read all markdown files in the input folder
2. **Extract Findings** - Pull out explicit findings, insights, and conclusions
3. **Identify Themes** - Group related findings into 3-7 themes
4. **Synthesize** - Write executive summary and themed sections
5. **Output** - Save synthesis document and execution log

## Parameters

Parameters are defined in `.octon/framework/capabilities/runtime/skills/registry.yml` (single source of truth).

This skill accepts one required parameter: a folder path containing research notes (markdown files).

## Output Location

Output paths are defined in `.octon/framework/capabilities/runtime/skills/registry.yml` (single source of truth).

Outputs are written to `.octon/inputs/exploratory/syntheses/` (synthesis document) and `/.octon/state/evidence/runs/skills/synthesize-research/` (execution log).

## Output Format

```markdown
# Research Synthesis: {{topic}}

**Generated:** {{timestamp}}
**Source:** {{input folder path}}

## Executive Summary

{{3-5 sentence overview of key findings}}

## Key Themes

### Theme 1: {{Name}}

**Insight:** {{Clear statement}}

**Evidence:**
- {{Supporting point 1}}
- {{Supporting point 2}}

**Confidence:** {{High/Medium/Low}}

## Contradictions & Resolutions

| Finding A | Finding B | Resolution |
|-----------|-----------|------------|

## Open Questions

1. {{Question that remains unanswered}}

## Sources Reviewed

- {{File 1}}
- {{File 2}}
```

## Boundaries

- Never fabricate findings not present in source materials
- Always cite which source file supports each finding
- Do not make recommendations beyond what evidence supports
- Write only to designated output paths
- Preserve nuance—don't oversimplify complex findings

## When to Escalate

- If input folder is empty or contains no `.md` files, report error
- If research goal is unclear, ask one clarifying question
- If major contradictions cannot be resolved, flag for human review
- If findings span domains requiring specialized expertise, note limitations

## References

For detailed documentation:

- [I/O contract](references/io-contract.md) - Inputs, outputs, dependencies, command-line usage
- [Behavior phases](references/phases.md) - Full phase-by-phase instructions
- [Safety policies](references/safety.md) - Tool and file policies
- [Examples](references/examples.md) - Full synthesis examples
- [Validation](references/validation.md) - Acceptance criteria
- [Error handling](references/errors.md) - Error codes, recovery procedures, troubleshooting
