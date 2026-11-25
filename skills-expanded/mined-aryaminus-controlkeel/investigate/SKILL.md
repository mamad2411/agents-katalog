---
name: investigate
description: "Read-only codebase Q&A: trace code paths, answer how/why/where questions without changes. Trigger: 'how does X work', 'why was Y built this way', 'trace the data flow'."
when_to_use: "Activate for read-only exploration questions. Do NOT use when code changes are needed."
argument-hint: "[question about the codebase]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: exploration
  ck_mcp_tools: [ck_memory_search]
  related_skills: [architect-first]
---

# Investigate

Read-only codebase Q&A. Trace code, not guesses. No file changes.

## Do NOT use when
- Code changes are needed (use appropriate dev skill)
- The question is about planning (use `align`)
- The question is about security (use `security-review`)

## Workflow

1. Search `ck_memory_search` for prior analysis on this area.
2. Trace actual code paths for the question type:
   - **How**: entry point → call chain → data flow → side effects
   - **Why**: `git log --oneline -20 -- <file>`, linked issues, commit messages
   - **Where**: search for function/module references, trace callers
   - **What-if**: trace the code path for that scenario, identify edge cases
3. Check multiple sources: source control, tests, comments. Code shows what, not why.
4. Answer concisely: direct answer + evidence (file:line, commit SHA) + caveats.

## Rules

- Read-only — no file changes. If fix needed, record and recommend appropriate skill.
- Every claim backed by code evidence or git history.
- Answer what was asked — do not explore tangentially.
- Stop at external boundaries — say so instead of speculating.

## Output

- Concise answer with file:line evidence
- Optional `ck_memory_record` for durable findings
- No file changes
