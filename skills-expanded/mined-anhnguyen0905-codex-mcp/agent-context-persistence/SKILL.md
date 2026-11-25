---
name: agent-context-persistence
description: Design rules for agent state persistence and token-budgeted read-back — tiered slices, git-SHA anchoring, restorable pointers, deterministic snapshots, and drift detection for file-based agent memory on large projects. Use when building or reviewing code/instructions that write agent working state to disk and read it back across sessions.
---

# Agent Context Persistence (embed into Codex prompts)

How to persist agent working state (plans, decision logs, task files) so a fresh session on a LARGE
project resumes within a fixed token budget without trusting stale claims. Distilled from
`docs/context-persistence-research-2026-08-06.md` (Anthropic context-engineering, Manus, Cognition,
Letta/MemGPT, Aider repo-map, spec-kit, event-sourcing); items marked (derived) are our own
inference, verify in review.

## Standards block

```
Context-persistence rules (mandatory when writing or reading agent state files):
- Fixed read budget: every read-back artifact has a hard token ceiling enforced by code
  (rank items, cut to budget), never by prose convention. Budget overflow drops whole
  lowest-priority items, not truncated sentences.
- Restorable compression: when something is dropped from a slice, append a pointer line naming
  where the full content lives (file + section). Content is one read away; never silently omit.
- Pointers, not payloads: durable state references code as path:line + enclosing symbol,
  never pasted snippets — pasted code is stale the moment the file changes.
- Anchor every write: state blocks record the git HEAD SHA at append time. On read-back,
  git diff --stat <anchor>..HEAD plus a dirty-tree check classifies each block fresh vs verify;
  a block without an anchor is always verify.
- Trust but verify: written state is hypothesis; filesystem + git are ground truth. A resuming
  agent must re-check any [verify] claim against current code before acting on it.
- Deterministic over generated: derived views (slices, resume summaries) are produced by
  deterministic code from the source-of-truth file, regenerated on every read — never by an LLM
  summarization step (which silently loses constraints) and never hand-edited.
- Single source of truth: the append-only log/plan file remains authoritative on disk; derived
  slice files are disposable and regenerable at any time.
- Never persist a code inventory: persist "where to look" (contracts, entry points, pointers);
  regenerate any structural view of the code at read time. Persisted descriptions of code are
  drift source #1. (derived from Claude Code no-index finding + Aider rebuild-per-message)
- Budget is a test invariant: tests build a large fixture (long log, many tasks) and assert
  tokensOf(slice) <= budget, plus a legacy-format fixture that degrades without crashing.
```

## Reviewer checklist

- A slice over budget, a truncated mid-sentence render, or a missing omitted-pointer line is a
  correctness bug, not a style issue.
- Any pasted code block inside a durable state file is a finding (use path:line + symbol).
- Any LLM-generated "current state" file that replaces rather than derives from the log is a finding.
- Anchor-less new blocks (when the writer had a git repo) are a finding; anchor-less legacy blocks
  must parse as verify, not crash.
