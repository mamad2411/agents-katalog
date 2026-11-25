# Claude-et-Codex

Claude Code skill that sends your implementation plan to the OpenAI Codex CLI for a second-opinion review before you execute. Uses Codex “multi_agent” mode to spawn parallel sub-agents (an Explorer that reads/validates against real files and an Architecture reviewer that checks design/sequence/risk), then returns a structured verdict (APPROVE / APPROVE_WITH_CHANGES / BLOCK) with categorized findings and file:line evidence. It explicitly tries to counter Codex’s tendency to over-engineer via prompt filtering plus a second filtering pass by Claude.

## Triggers
- "claude et codex"
- "codex second opinion"
- "implementation plan review"
- "pre execution review"
- "codex validation"
- "dual ai review"

## Description
Claude-et-Codex is a skill that provides a second-opinion review of implementation plans by leveraging both Claude and Codex AI systems. Before executing a plan, it sends the implementation to OpenAI Codex CLI for analysis using multi-agent mode, then applies Claude-based filtering to counter Codex's tendency to over-engineer, resulting in a structured verdict with detailed feedback.

## Features
- Dual AI review system (Claude + Codex)
- Uses Codex multi_agent mode:
  - Explorer sub-agent: reads/validates against real files
  - Architecture reviewer: checks design/sequence/risk
- Structured verdict system:
  - APPROVE: ready to execute
  - APPROVE_WITH_CHANGES: needs modifications
  - BLOCK: should not execute
- Categorized findings with file:line evidence
- Prompt filtering to counter Codex over-engineering
- Second filtering pass by Claude for quality control
- Pre-execution validation workflow

## Usage
Use when you want to validate implementation plans with a second AI opinion before execution, particularly for complex or risky changes where you want to catch potential issues early.

## Example
```
/claude-et-codex review plan for database migration
/claude-et-codex validate implementation of new api endpoint
/claude-et-codex get second opinion on refactor proposal
/claude-et-codex approve-with-changes plan and show feedback
```
