---
name: research-reproducibility-audit
description: Audit a paper, codebase, benchmark, or artifact for reproducibility gaps in ML, systems, and hardware research. Use when checking whether claims can be reproduced, comparing paper-versus-code behavior, validating release readiness, or preparing an artifact evaluation package.
---
# Research Reproducibility Audit

Use this skill when a result looks plausible but the path to reproducing it is weak.

## Core Workflow

1. Enumerate the paper or artifact claims.
2. Map each claim to code, config, data, hardware, and evaluation evidence.
3. Separate what is released from what is merely described.
4. Identify blockers:
   - missing checkpoints,
   - hidden preprocessing,
   - absent seeds,
   - undocumented hardware,
   - unstable dependencies,
   - benchmark ambiguity.
5. Rank reproduction risk by impact and fix cost.

## Execution Rules

1. Distinguish claim failure from release incompleteness.
2. Prefer exact paths, commands, and config names over summaries.
3. Treat hardware and software environment drift as first-class risks.
4. End with the minimum changes required for a third party to reproduce the result.

## Output Contract

Return:

1. Claim-evidence map.
2. Blocking gaps.
3. Nice-to-have gaps.
4. Reproduction verdict.
5. Release hardening checklist.
