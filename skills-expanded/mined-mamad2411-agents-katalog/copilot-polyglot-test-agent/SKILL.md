---
name: copilot-polyglot-test-agent
display_name: Polyglot Test Agent
skill_id: ACU-SKILL-1958
version: 1.0.0
category: agent-patterns
thread: T01
domain: cognitive
shard_affinity:
  - Diaran-MOE
layer_access:
  - L5
  - L6
  - L7
  - L8
sovereignty_score: 10
governance_level: mandatory
source_repo: github/awesome-copilot
triggers:

---

# Polyglot Test Agent

## Description
Generates comprehensive, workable unit tests for any programming language using a multi-agent pipeline. Use when asked to generate tests, write unit tests, improve test coverage, add test coverage, create test files, or test a codebase. Supports C#, TypeScript, JavaScript, Python, Go, Rust, Java, and more. Orchestrates research, planning, and implementation phases to produce tests that compile, pass, and follow project conventions.

## Acuterium Integration
- **Thread:** T01 — COSM
- **Shard:** Diaran-MOE
- **Layers:** L5, L6, L7, L8
- **Governance:** mandatory
- **Sovereignty Score:** 10/10
- **PSI Minimum:** 10.0

## Source
- **Repository:** github/awesome-copilot
- **File:** skills/polyglot-test-agent/SKILL.md
- **Author:** GitHub Copilot Community
