---
name: git-diff-summary
description: Get git diff and summarize changes using LLM
---

# Git Diff Summary

Get git diff and summarize changes using LLM

## When to Use

- User wants to git diff
- User wants to diff summary
- Keywords: git, diff, summary, changes

## Required Parameters

- **repo_path** (string): Path to git repository

## Output

- **files_changed** (number): Number of files changed
- **diff** (string): Raw diff output
- **summary** (string): LLM-generated summary

## Security

- Sandbox level: standard
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `get_diff` -> 6 steps -> Exit: `ret_ok`, `ret_fail`
