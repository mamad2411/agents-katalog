---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebFetch
description: Create a new TypeScript ADW workflow from a list of slash commands
argument-hint: [comma-separated slash commands e.g. /plan, /build, /review]
model: opus
---

# Purpose

Create a new TypeScript ADW (AI Developer Workflow) that chains the specified slash commands into a sequential workflow. Each command becomes a step executed via the Claude Agent SDK. Follow the `Instructions` for SDK patterns and conventions, then execute the `Workflow` step by step.

## Variables

COMMANDS: $0
PROMPT: $1
TARGET_DIR: adws/workflows
SHARED_SRC: adws/src

## Instructions

- Parse `COMMANDS` as a comma-separated list of slash commands (e.g. `/plan,/build,/review`)
- Each command becomes a numbered step in the workflow, executed sequentially
- The `PROMPT` variable, if it is provided, will give further instructions about how the adw should behave.
- The workflow file name is prefixed with `adw_` and derived from the command names joined by underscores, preserving hyphens within command names (e.g. `/research-codebase,/produce-readme` → `adw_research-codebase_produce-readme.ts`). Only use underscores as the separator BETWEEN commands, never replace hyphens within a command name.
- Use Bun APIs (`Bun.spawn`, `Bun.write`, `import.meta.main`) — no Node-only patterns
- **Use `createSDK()` and `runStep()` — NEVER instantiate the SDK directly or write per-step boilerplate:**
  - `createSDK({ model?, cwd? })` encapsulates all SDK options (permissionMode, settingSources, etc.) — returns `{ query }`. All SDK config lives in one place.
  - `runStep(opts)` encapsulates per-step boilerplate: banner, tagged logger, usage tracking, finalize, comment posting, and status updates. Each step is a single `runStep()` call.
  - `runStep()` returns `RunStepResult` with `{ ok, result, usage }`. Use `onFail: "halt"` (default) for critical steps, `onFail: "continue"` for non-fatal steps like test/document.
- **Use `getAdwEnv()` for workflow config** — returns `{ prompt, workingDir, models }` from env vars. Replaces manual env reads.
- Reuse existing shared modules from `SHARED_SRC` — read them before writing new utilities:
  - `agent-sdk.ts` — `createSDK()`, `runStep()`, `RunStepOpts`, `RunStepResult`, `runPlanStep()`, `runBuildStep()`, `runReviewStep()`, `runTestStep()`, `runDocumentStep()`, `quickPrompt()`, `formatUsage()`, `sumUsage()`, `StepUsage`, `QueryResult`
  - `utils.ts` — `getAdwEnv()`, `ADWEnv`, `makeAdwId()`, `extractPlanPath()`, `createCommentStep()`, `createFinalStatusComment()`, `fmtDuration()`, `parseJson()`, `checkEnvVars()`, `exec()`, `getProjectRoot()`
  - `logger.ts` — `createLogger(adwId, triggerType)` dual console+file logger (returns logger with `.logDir`), `taggedLogger(parent, tag, { logDir, step })` per-agent colored logger with file isolation, `TaggedLogger` interface with `.finalize(ok)` for status tracking
  - `git-ops.ts`, `worktree-ops.ts`, `github.ts` — git/GitHub helpers
- For logging assistant messages, use `summarizeContent()` from `agent-sdk.ts` to extract readable text from content block arrays
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
- Data passing between steps:
  - `/plan` produces a plan file path — extract with `extractPlanPath(result, workingDir, adwId)`
  - `/build` consumes a plan file path
  - `/review` consumes the original prompt and plan file path
  - `/test` runs after build with no special input
  - For custom commands, assume they take the original prompt unless the command name suggests otherwise
- Verify every `/command` in `COMMANDS` exists in `.claude/commands/` before wiring it up
- Follow the pattern established in `adws/workflows/classic/adw_plan_build.ts` and `adws/workflows/classic/adw_plan_build_review.ts`

## Workflow

1. Parse `COMMANDS` into an ordered list of command names (strip `/` prefix)
2. Read existing shared modules in `SHARED_SRC` to understand available step functions: `agent-sdk.ts`, `logger.ts`, `utils.ts`
3. Read existing workflow files in `TARGET_DIR` to understand the established patterns (`adw_plan_build.ts`, `adw_plan_build_review.ts`)
4. For each command in the list, verify the corresponding skill exists in `.claude/commands/{command}.md` — log a warning if missing
5. Identify which commands already have step functions in `agent-sdk.ts` (e.g. `runPlanStep`, `runBuildStep`, `runReviewStep`) vs which need new ones
6. If new step functions are needed, add them to `SHARED_SRC/agent-sdk.ts` following the existing pattern: create query with `/skill` prompt, consume with `consumeQuery()`, return `QueryResult`
7. Write the workflow file to `TARGET_DIR/adw_{command_names_joined}.ts` with:
   - JSDoc header with usage example
   - `parseArgs` entrypoint with `--adw-id` and `--issue` flags
   - `getAdwEnv()` for config (prompt, workingDir, models)
   - `runWorkflow()` function using `runStep()` for each step
   - Data passing between steps (plan path extraction, prompt forwarding, etc.)
   - Duration tracking and final summary log
8. Run `bun run TARGET_DIR/adw_{new_file}.ts --adw-id test-create` with `ADW_PROMPT="test" ADW_WORKING_DIR=$(pwd)` to verify it parses and starts correctly
9. Fix any issues found during the test run

## Report

Return a summary of:

- Commands parsed and workflow file created
- Which commands had existing step functions vs new ones added
- Any commands that were missing from `.claude/commands/` (warnings)
- Data flow between steps (what each step produces/consumes)
- Test run result and any issues encountered
