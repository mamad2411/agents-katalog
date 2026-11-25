---
name: tokenscope
description: Judgment-layer review of Claude Code token usage. Use when the user asks to audit token costs, review Claude Code spending, check context waste, or interpret a tokenscope report. Runs the tokenscope profiler, then interprets its findings with knowledge of the project's actual workflow — separating mechanical waste from deliberate cost.
---

# TokenScope review

You are the judgment layer on top of the tokenscope profiler. The CLI is a
deterministic lookup table: it measures precisely but has **no model of the
user's workflow** — it cannot distinguish "expensive because wasteful" from
"expensive because verification is the product". Your job is to add that
judgment.

## Step 1 — Run the profiler

The tokenscope repo lives at `C:\Users\Asmit\OneDrive\bohra-labs\token-cost-mcp`
(if moved, find it with Glob for `**/src/cli.ts` containing "tokenscope").

```
node <repo>/src/cli.ts              # overview: all projects, scores, top findings
node <repo>/src/cli.ts <name>       # one project: score breakdown + recommendations
```

If the user names a project, run the detail view for it. Otherwise run the
overview and drill into the costliest or lowest-scoring project.

## Step 2 — Gather workflow context (this is what the CLI cannot see)

For the project under review:
- Read its `CLAUDE.md` and `.tokenscope.json` if they exist.
- Skim the opening user prompts of 2-3 recent sessions in
  `~/.claude/projects/<encoded-project-dir>/*.jsonl` (the first `"type":"user"`
  lines) to understand what kind of work happens there: coding tasks,
  planning/research, verification/adjudication, mixed.
- Note any protocol the project follows (e.g. "verify against the repo, never
  trust memory") — such protocols make some re-reading deliberate.

## Step 3 — Interpret, don't parrot

Classify each CLI recommendation:

- **Mechanical (apply-worthy):** environment notes from classified errors,
  unused MCP servers, head/archive splits of append-only logs, codemap for
  code files. These are safe regardless of workflow.
- **Intent-dependent (judge before recommending):**
  - *Re-read waste* — re-reads of actively-edited files, or reads mandated by
    a verification protocol, are the protocol working, not waste. The fix for
    those is cheaper structure (head/archive split), never "skip the read".
  - *Output filtering* — NEVER recommend truncating output the project
    measures or verifies against; a filtered count that returns 85 instead of
    87 manufactures false confidence. Scope filtering to test runs/build logs.
  - *Session splitting* — long planning sessions may be paying for continuity
    on purpose. Recommend splitting for task-shaped coding work only.
- **Look for what the CLI missed.** Its detectors are thresholds. Check: are
  hot files growing? Is one document serving as both current-state and
  history? Are many small reads actually one missing map (suggest
  `node <repo>/src/cli.ts codemap <dir>`)?

## Step 4 — Deliver the review

Short, numbers-first:
1. Cost + score, and whether the score is fair for this workflow.
2. Apply today (mechanical items, with the ready-to-paste blocks).
3. Ignore, and why (intent-dependent items that score deliberate cost as waste).
4. What the profiler missed, if anything.
5. A `.tokenscope.json` proposal if recommendations misfire for this workflow
   (`{"verification": true, "mute": ["<rec-id>"]}`).

## Rules

- Every claim cites a measured number from the report or the transcripts.
  Label anything else as judgment.
- Never apply fixes without explicit approval. When approved: CLAUDE.md
  blocks verbatim, real one-line summaries for key files (read just enough to
  write them), head/archive splits only with the user watching.
- Never modify the tokenscope source as part of a review.
