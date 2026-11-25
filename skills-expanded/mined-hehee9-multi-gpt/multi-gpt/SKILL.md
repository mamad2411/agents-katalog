---
name: multi-gpt
description: Run local parallel-reasoning Multi GPT through the async `multi_gpt_start`, `multi_gpt_status`, and `multi_gpt_cancel` MCP tools. Use when the user asks for Multi GPT, Super GPT, GPT Pro-style multi-agent reasoning, multiple independent approaches with merge/judge/refine, complex design comparison, deep code or architecture review, long-form problem solving that benefits from Planner to parallel Solver to Refiner to Loop to Organizer orchestration, or canceling a mistakenly started Multi GPT job. Do not use for simple one-shot advice; use Codex sub-agents or normal reasoning instead.
---

# Multi GPT

## Overview

Use `multi_gpt_start`, `multi_gpt_status`, and `multi_gpt_cancel` for local parallel reasoning. Multi GPT is not a single Codex consultation call; it starts a background job that orchestrates multiple read-only `codex exec` stage calls as Planner -> parallel Solvers -> parallel Refiners -> Loop(Merger -> Refiner -> Judge) -> Organizer.

## Workflow

Call `multi_gpt_start` when the task needs several independent approaches, comparison, synthesis, or a judge/refine loop. The tool returns quickly with a `job_id`, avoiding the roughly 120-second MCP tool-call limit.

Multi GPT is slow by design. A typical run takes about 5 to 20 minutes, and most normal runs finish around 10 to 15 minutes. Do not poll `multi_gpt_status` every minute. After starting a job, wait several minutes before the first status check, then check only occasionally unless the user explicitly asks for tighter monitoring.

Poll `multi_gpt_status` with that `job_id` until it returns `status: completed`, `status: failed`, or `status: canceled`.

If a Multi GPT job was started by mistake, call `multi_gpt_cancel` with the `job_id`. Treat `status: canceled` as a terminal state and stop polling. Cancel only works for running jobs owned by the current MCP server process; after an MCP server restart, stale job files can still be inspected with `multi_gpt_status` but their former child processes cannot be targeted reliably.

Do not use Multi GPT for ordinary short answers, quick code questions, or one-off model consultation; the user expects those to use normal Codex reasoning or sub-agents.

Pass inputs to `multi_gpt_start` as follows:

- `prompt`: preserve the user's original request as the main prompt.
- `files`: pass absolute local file paths that should be read into context. The MCP server reads files read-only and rejects missing or overly large files.
- `model`: omit unless the user specifies a model. When omitted, Codex CLI uses its configured or recommended default model, so Multi GPT can follow Codex's latest recommended non-small model without hardcoding a model slug.
- `reasoning_effort`: omit for the default `medium`. Use `none` only when the user explicitly asks for non-reasoning mode. Valid values are `none`, `low`, `medium`, `high`, and `xhigh`.
- `max_iterations`: omit unless the user asks to change the loop budget. The default is `5`.

## Behavior to Preserve

Treat Multi GPT as a local parallel reasoning pipeline:

1. Planner analyzes the problem and creates several approaches.
2. Solvers independently solve each approach in parallel.
3. Initial Refiners improve each Solver result, falling back to the original solution on failure.
4. The loop runs Merger -> Refiner -> Judge up to the iteration limit.
5. Judge can stop early by selecting the best sufficient solution.
6. Organizer converts the selected solution into the final user-facing answer.

When `multi_gpt_status` returns `status: completed`, show `result.final_answer` to the user. Stage summaries and fallback metadata may be used to report reliability or diagnose failures, but do not expose hidden chain-of-thought or raw internal transcripts.

When `multi_gpt_status` returns `status: canceled`, briefly say the job was canceled. Do not present partial internal stage outputs as an answer.

## Runtime Constraints

The MCP server runs locally with Node.js and invokes local `codex exec` with read-only sandboxing and no approval prompts for each reasoning stage. Use absolute file paths when passing file context.
