---
name: total-review
description: 'Run four independent Max-effort reviews (Fable 5.1, Opus 5.5, GPT-6 Astra, GPT-6.1 Sol), merge their findings, and fix only what the user approves. Manual only: run when a human types /total-review; agents must never invoke it on their own.'
disable-model-invocation: true
---

# Total Review

Four reviewers, the two best models from Anthropic and from OpenAI, all at `max` effort and in **full permission mode** (the harness maximum). Never swap or downgrade a model, effort, or permission mode. If one is unavailable, stop and tell the user.

## Permissions

Always spawn with `--permission-mode full`. That is Claude Code's bypass permissions (`--dangerously-skip-permissions`) and Codex's YOLO mode (no approvals, `danger-full-access` sandbox). A child cannot exceed its parent, so if this thread is not in full mode, stop and tell the user.

## Reviewers

- **Fable 5.1**: `--provider claude-code --model claude-fable-5-1`
- **Opus 5.5 (1M)**: `--provider claude-code --model 'claude-opus-5-5[1m]'`
- **GPT-6 Astra**: `--provider codex --model gpt-6-astra`
- **GPT-6.1 Sol**: `--provider codex --model gpt-6.1-sol`

## 1. Launch

1. Confirm each model is listed with `max` in `supportedReasoningEfforts`: <provider model-list command for Claude Code> and <provider model-list command for Codex>.
2. Spawn all four in parallel, one thread each, with the reviewer flags plus `--reasoning-level max --permission-mode full --title "Total review: <model>"`:
   - **Local thread:** <local thread-spawn command, with the appropriate project and environment selected>
   - **Cloud thread:** <cloud thread-spawn command>
   - **Fallback only:** <fallback thread-spawn command> (see <fallback CLI documentation>).
3. Confirm with <thread status command> that each thread runs the right model at `max` in `full` permission mode.

## 2. Brief

Send all four the same neutral brief: scope, paths, intended behavior, and diff/base revision.

Ask for a thorough senior-developer review, including related code and tests. Review only; change no files. Report serious or critical issues with file and line, a fix, and merge readiness. Separate verified findings from guesses. Use plain English.

Never hint at suspected bugs, mention the other reviewers, or share one reviewer's output with another.

## 3. Collect

Run <thread wait command>, then <thread output command>, on each. Idle status, timeouts, and queued retries are not completion. Report a failed reviewer; never pass off partial output as a review.

## 4. Merge and report

Read all four reports in full. Deduplicate. Keep only real bugs and risks; drop style preferences, theoretical edge cases, and non-issues. Agreement alone does not prove an issue is real.

Show the user:

- A numbered list, one line per issue: what + where.
- Tags for who found it: `[fable]`, `[opus]`, `[astra]`, `[sol]`. Most-reported first.
- One line: how many findings were dropped.
- Ask: approve these fixes, or adjust the list?

Share full reports only if the user asks.

## 5. Fix and ship

Only after the user approves: fix the approved issues, then commit and push using the applicable workflow.
