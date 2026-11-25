---
name: oss-forensics-orchestration
description: Orchestrates multi-agent forensic investigations on public GitHub repositories, coordinating parallel evidence collection, hypothesis formation, verification, and report generation.
metadata:
  version: 0.2.0
  category: oss-forensics
---
# OSS Forensics Orchestration

## Quick Start
```bash
# Initialize investigation directory and environment
source .venv/bin/activate && python .claude/skills/oss-forensics/github-evidence-kit/scripts/init_investigation.py
```

## Workflow
1. **Initialize**: Run the init script and extract the working directory.
2. **Parse Prompt**: Identify repositories, actors, dates, and vendor reports.
3. **Evidence Collection**: Spawn specialist investigators in parallel (GH Archive, GitHub API, Wayback Machine, IOC Extractor).
4. **Hypothesis Formation**: Iterate through findings to form and refine an investigation hypothesis.
5. **Verification**: Confirm evidence against original sources.
6. **Validation**: Validate the final hypothesis against verified evidence.
7. **Report**: Generate a forensic report summarizing timeline, attribution, and impact.

## Rules & Constraints
- **Sole Orchestrator**: You are the ONLY agent that spawns other specialist agents.
- **Parallelism**: ALWAYS spawn Phase 2 investigators in a single message with multiple Task calls.
- **Wait for Completion**: Do not proceed to the next phase until all active agents complete.
- **State Management**: Every agent MUST receive the absolute `workdir` path.
- **Iteration Limits**: Strictly respect `max_followups` and `max_retries` flags.

## When to Use
- Investigating suspected supply chain attacks on GitHub repositories.
- Reconstructing developer activity or malicious actor intent.
- Gathering evidence from multiple forensic sources (Wayback, GH Archive).

## When NOT to Use
- Single-agent tasks that don't require orchestration.
- Investigations on private repositories or non-GitHub sources.

## References
- [Skill Manual](references/oss-forensics-orchestration-manual.md)
- [Evidence Kit Scripts](../github-evidence-kit/scripts/)
