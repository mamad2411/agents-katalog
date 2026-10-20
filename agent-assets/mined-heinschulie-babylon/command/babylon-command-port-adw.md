---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebFetch
description: Port a Python ADW workflow to TypeScript using Bun and the Claude Agent SDK
argument-hint: [path/to/python/adw.py]
model: opus
---

# Purpose

Port a Python ADW (AI Developer Workflow) script to TypeScript, targeting the Bun runtime and `@anthropic-ai/claude-agent-sdk`. Follow the `Instructions` for critical SDK gotchas learned from prior ports, then execute the `Workflow` step by step.

## Variables

SOURCE_PATH: $0
TARGET_DIR: adws/workflows

## Instructions

- The source Python ADW at `SOURCE_PATH` must be ported to TypeScript in `TARGET_DIR/`
- Use Bun APIs (`Bun.spawn`, `Bun.write`, `import.meta.main`) — no Node-only patterns
- **Use `createSDK()` and `runStep()` — NEVER instantiate the SDK directly or write per-step boilerplate:**
  - `createSDK({ model?, cwd? })` encapsulates all SDK options (permissionMode, settingSources, etc.) — returns `{ query }`. All SDK config lives in one place.
  - `runStep(opts)` encapsulates per-step boilerplate: banner, tagged logger, usage tracking, finalize, comment posting, and status updates. Each step is a single `runStep()` call.
  - `runStep()` returns `RunStepResult` with `{ ok, result, usage }`. Use `onFail: "halt"` (default) for critical steps, `onFail: "continue"` for non-fatal steps like test/document.
- **Use `getAdwEnv()` for workflow config** — returns `{ prompt, workingDir, models }` from env vars. Replaces manual env reads.
- Reuse existing shared modules from `adws/src/` — read them before writing new utilities:
  - `agent-sdk.ts` — `createSDK()`, `runStep()`, `RunStepOpts`, `RunStepResult`, `runPlanStep()`, `runBuildStep()`, `runReviewStep()`, `runTestStep()`, `runDocumentStep()`, `quickPrompt()`, `formatUsage()`, `sumUsage()`, `StepUsage`, `QueryResult`
  - `utils.ts` — `getAdwEnv()`, `ADWEnv`, `makeAdwId()`, `extractPlanPath()`, `createCommentStep()`, `createFinalStatusComment()`, `fmtDuration()`, `parseJson()`, `checkEnvVars()`, `exec()`, `getProjectRoot()`
  - `logger.ts` — `createLogger(adwId, triggerType)` dual console+file logger (returns logger with `.logDir`), `taggedLogger(parent, tag, { logDir, step })` per-agent colored logger with file isolation, `TaggedLogger` interface with `.finalize(ok)` for status tracking
  - `git-ops.ts`, `worktree-ops.ts`, `github.ts` — git/GitHub helpers
- For logging assistant messages, use `summarizeContent()` from `agent-sdk.ts` to extract readable text from content block arrays (avoids `[object Object]` in logs)
- Use `parseArgs` from `"util"` for CLI arg parsing (Bun-compatible, no deps)
- `--issue` is a standard parseArgs option for all workflows (optional, type: `"string"`). GitHub issues are the primary entry point for most ADW work, but some workflows (e.g. cron-triggered maintenance) run without an issue. The issue number is used for posting progress comments — all GitHub commenting is gated on `--issue` being provided.
- Env vars for config: `ADW_PROMPT`, `ADW_WORKING_DIR`, `ADW_MODEL`, `ADW_REVIEW_MODEL`
- **Per-phase model selection:** When a workflow has steps with different cost/capability needs, use `getAdwEnv().models` which provides:
  - `models.research` — `ADW_RESEARCH_MODEL` (default: `claude-haiku-4-5-20251001`)
  - `models.default` — `ADW_MODEL` (default: `claude-sonnet-4-20250514`)
  - `models.review` — `ADW_REVIEW_MODEL` (default: `claude-sonnet-4-20250514`)
  - Use the cheapest model that can handle each phase — haiku for research/read-heavy, sonnet for generation, opus only when explicitly requested via env var
- Log files go to `agents/{adw-id}/{trigger_type}/execution.log` via `createLogger`
- **Per-agent logging is MANDATORY.** Every step that runs an agent must:
  - Create a `taggedLogger(logger, tag, { logDir: logger.logDir, step: "step-name" })` — this gives the agent a colored console prefix AND writes to its own file at `agents/{adw-id}/{trigger_type}/{step}/{tag}.log`
  - Pass the tagged logger (not the base logger) to the SDK step function
  - Call `tlog.finalize(ok, result.usage)` when the agent completes — this writes `status.json` (with usage stats) in the step folder and renames the log to `.error.log` on failure
  - For parallel agents this is critical for debugging; for sequential steps it provides per-step file isolation
  - See `adw_research-codebase_produce-readme_update-prime.ts` for parallel usage and `adw_plan_build.ts` for sequential usage
- Keep the workflow file focused — delegate SDK interaction to `agent-sdk.ts`, add new step functions there if needed
- When a workflow step invokes a `/skill`, verify the skill exists in `.claude/commands/` before wiring it up
- Use visually distinct step banners: `"═".repeat(60)` surrounding the step name
- **GitHub issue progress comments (when `--issue` is provided).** Use `createCommentStep(issueNumber)` and `createFinalStatusComment(issueNumber)` from `utils.ts` — these return functions that handle posting and no-op gracefully when no issue number is provided. `runStep()` handles per-step comments automatically when given a `commentStep` function.
- **Usage tracking is MANDATORY for all workflows.** Every workflow must:
  - Import `formatUsage`, `sumUsage`, and `StepUsage` from `agent-sdk.ts`
  - Import `writeWorkflowStatus` from `logger.ts`
  - Declare `const allStepUsages: { step: string; ok: boolean; usage: StepUsage }[] = []` before the try block
  - `runStep()` returns usage in `RunStepResult` — push each result to `allStepUsages`
  - In the final summary, log per-step usage and a `TOTAL:` line using `sumUsage()`
  - At the end of the workflow, call `writeWorkflowStatus(logger.logDir, { workflow, adwId, ok, startTime, totals })` and `commentFinalStatus()`
  - See `adw_plan_build.ts` or `adw_plan_build_review.ts` for the exact pattern
- **`ADWState` for cross-step persistence.** When a workflow needs to carry structured data between steps or across retries, use `ADWState` from `state.ts`:
  - `new ADWState(adwId)` or `ADWState.load(adwId, logger)` to create/restore
  - `state.update({ plan_file, branch_name, worktree_path, ... })` to persist fields
  - `state.get("plan_file")` for typed reads; `state.save()` writes to `agents/{adwId}/adw_state.json`
  - Use ADWState when: multiple steps share mutable context (plan paths, branch names, ports), or workflow supports resume/retry
  - Don't use ADWState for: simple linear pipelines where return values flow step-to-step — use `runStep()` result passing instead
  - See `adw_plan.ts` and `adw_patch.ts` for real usage

## Workflow

1. Read the source Python ADW at `SOURCE_PATH` thoroughly — understand every step, subprocess call, and data flow
2. Read existing shared modules in `adws/src/` to understand what's already available (agent-sdk.ts, logger.ts, utils.ts, git-ops.ts)
3. Identify which Python subprocess calls map to SDK `query()` calls vs direct `exec()` calls
4. Identify any `/skill` invocations in the Python code and verify those skills exist in `.claude/commands/`
5. If new SDK step functions are needed (beyond plan/build), add them to `adws/src/agent-sdk.ts` following the existing pattern: create query, consume with `consumeQuery()`, return `QueryResult`
6. Write the TypeScript workflow file to `TARGET_DIR/adw_{workflow_name}.ts` following the `adw_plan_build.ts` pattern: parseArgs entrypoint with --adw-id and --issue flags, `getAdwEnv()` for config, `runStep()` for each step
7. Run `bun run adws/workflows/{new_file}.ts --adw-id test-port` with a simple test prompt to verify it works end-to-end
8. Fix any issues found during the test run

## Report

Return a summary of:
- Source file ported and target file created
- Which shared modules were reused vs new code written
- Any new step functions added to `agent-sdk.ts`
- Skills referenced and whether they exist
- Test run result (pass/fail) and any issues encountered
