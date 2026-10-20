# AGENTS.md

Project conventions for cycle. Read before touching code or running the workflow.

## Workflow style

- **Trunk-based development.** All work goes directly on `master`. Commits land via fast-forward merge from local branches that are immediately deleted.
- **Do NOT use git worktrees in this repo.** No `EnterWorktree`, no `git worktree add`. Edit master directly.
- Pushes to `master` are authorized — no PR review required. See `.Codex/settings.local.json` for the `autoMode.allow` rule.
- **Trunk-based operation is enforced via `CYCLE_TRUNK_BASED=1` in `.cycle/.env`**, not via `workflows.yml`. The defaults ship `engine.commit.mode: worktree-pr`; the env var overrides it to `trunk` at engine bootstrap. Any repo needing trunk mode: create `.cycle/.env` with `CYCLE_TRUNK_BASED=1`, or pass `--trunk` to `cycle run`.

## Runtime

- Node ≥ 22.6 (`--experimental-strip-types`; no transpile step in tests).
- TypeScript floor is **ES2023** (`target`/`lib` in `tsconfig.json`). See [docs/RFC-002-typescript-es2023-floor.md](docs/RFC-002-typescript-es2023-floor.md).
- If `node --version` < 22: `nvm use 22.22.2`.

## Commands

| Command | Purpose |
|---|---|
| `npm test` | Full test suite. Auto-builds first. Must pass before commit. |
| `npm run test:coverage` | Tests with LCOV coverage. **Required in `build`/`fix` steps.** |
| `npm run check:coverage` | Enforce per-file floors against `.cycle/coverage.lcov`. Runs automatically after `test:coverage`. |
| `npm run check:invariants` | Enforce build-time structural invariants. Runs automatically after `test:coverage`. |
| `npm run typecheck` | `tsc --noEmit` — no warnings allowed. |
| `npm run build` | esbuild bundle `src/cli.ts` → `dist/cycle.js`. Runs via `pretest`. |
| `npm run sync-defaults` | Copy `src/defaults/` → `.cycle/`. Run after editing defaults. See [docs/sync-defaults.md](docs/sync-defaults.md). |
| `cycle status` | Print queue counts and in-flight cycle. Read-only. |
| `cycle triage --dry-run` | Re-run triage against `inbox/` without mutating state. Diagnostic for `engine.paused {reason: "all_triage_failed"}`. |
| `cycle cleanup [--dry-run|--yes] [--force]` | List (or delete with `--yes`) local `cycle/*` branches with no matching `in_progress` queue row. Safe by default: `--dry-run` is implicit; `--force` bypasses the dirty-tree guard. |
| `cycle help` | Print usage and exit 0. Also triggered by `--help` or `cycle run --help`. |

## Coverage policy

- **Coverage must not decrease** vs master baseline (as of 2026-05-13): Line ≥ 95%, Branch ≥ 75%, Function ≥ 90%.
- Report numbers in `BUILD.md` / `FIX.md`. Add tests in the same cycle, not as follow-up.
- **Per-file floors**: `src/engine/triage.ts` (95%), `src/engine/issue-lifecycle.ts` (95%), `src/engine/commit-cycle.ts` (95%), `src/engine/branch.ts` (90%), `src/engine/stale-dist.ts` (95%), `src/cli/run-one.ts` (70%), `scripts/sync-defaults.mjs` (90%), `src/cli/cleanup.ts` (70%), `src/engine/path-utils.ts` (100%), `src/engine/engine-lock.ts` (100%), `src/engine/child-env.ts` (100%), `src/engine/log-fmt.ts` (100%), `src/engine/dot-env.ts` (100%), `src/engine/queue.ts` (90%), `src/engine/run-cycle.ts` (90%). Enforced by `scripts/coverage-gate.mjs` (LCOV-driven). `scripts/**` no longer excluded from `test:coverage`. Extend the `FLOORS` table inside that script to add more floors.

## Test conventions

- **Exactly-once engine events must be cardinality-pinned.** Use
  `filter(predicate).length === 1` (not `find(predicate) !== undefined`) when
  asserting that an engine event fires exactly once. A bare `find` only confirms
  existence — it lets double-emission bugs slip through undetected.
- Use the `expectExactlyOne(events, eventName)` helper from `tests/helpers.ts`
  for events where you also need the payload. It asserts `length === 1` and
  returns the matched event.
- Background: cycles 0022 and 0051 established this rule. `engine.halted` and
  `reflection.summary` are the canonical exactly-once events.
- **`node:fs/promises` cannot be stubbed via `mock.method`.** ESM module properties are non-configurable, so `mock.method(nodeFsPromises, "rename", …)` throws at setup time. Use `node:fs` (a CJS module with configurable exports) for `mock.method` interception — confirmed working in `tests/engine/dot-env.test.ts`. For `node:fs/promises` targets, use real filesystem manipulation (`chmod`, temp directories) or refactor the target code to accept an injectable function.

## Structural-invariants policy

The `INVARIANTS` table in `scripts/structural-invariants.mjs` is the single source of truth for build-time structural rules. Extend it to register new invariants; enforced via `npm run check:invariants` (runs automatically after `test:coverage`).

> **Note:** Agent fleet consistency (REGISTRY in `exec.ts`, `Step.agent` union in `workflow.ts`, and `exec-*.ts` files) is not yet covered by a structural invariant — all three must be updated manually when adding a new agent.

## Architecture

Key modules: `src/engine/` (run-cycle, queue, triage, reflection, blocked, log, branch, exec-*, commit-cycle, issue-lifecycle), `src/cli.ts`, `src/defaults/`.

Registered step agents (via resolveAgent): `Codex`, `codex` (first-class; optional `model` and `thinking` step fields map to `--model`/`--thinking` argv flags), `gemini`, `auggie` (first-class; `model` maps to `--model`; `thinking` is silently ignored — auggie has no `--thinking` flag; uses `--print --instruction-file <path>` delivery; `CYCLE_AUGGIE_BIN` overrides binary for tests), `opencode` (first-class; optional `model` and `thinking` step fields map to `--model`/`--thinking` argv flags), `pi` (first-class; optional `model` and `thinking` step fields map to `--model`/`--thinking` argv flags). `bash` steps are dispatched directly via `execBashStep`, not through the agent registry.

`src/engine/log-fmt.ts` — shared `truncateHeadCapped(s, max)` and `stripFences(s)` helpers used by run-cycle and triage.

`src/engine/rate-limit.ts` — `isRateLimitError(result)` pure helper; returns `true` on exit 429 or exit 1 with rate-limit signal in stderr/stdout. The bare `"429"` substring pattern (`RATE_LIMIT_PATTERNS`) risks false positives on exit 1 when unrelated output contains that digit sequence; tightening to a word-boundary or context-anchored pattern is tracked in `inbox/`.

`src/engine/run-cycle.ts` — rate-limit retry loop: when a step result has `rateLimited: true`, the engine emits `engine.paused { reason: "rate_limit", retry_at }`, sleeps `engine.rate_limit_backoff_ms` ms (default 3,600,000), and retries the same step index. On first clean success after a rate-limited attempt, emits `engine.resumed { reason: "rate_limit_cleared" }`. The retry loop is unbounded — exits only on clean success or non-rate-limit failure. Backoff is injectable via `RunCycleOpts.sleepFn` for tests. Rate-limit retries are invisible to `run-one.ts` (complete inside `runCycle`), so they do not increment `consecutive_failures`.

`src/engine/path-utils.ts` — shared `isDenied(p)` denylist helper used by commit-cycle and run-cycle.

`src/engine/engine-lock.ts` — shared `acquireLock(lockPath)` / `releaseLock(lockPath)` PID-lockfile helpers used by the supervisor to enforce single-engine exclusion.

`src/engine/child-env.ts` — `buildChildEnv(extra)` builds the subprocess env: strips all `CYCLE_*` vars by prefix, prepends the parent Node's bin dir to PATH, then overlays `extra`. Callers must re-inject any `CYCLE_*` vars subprocesses legitimately need (e.g. `CYCLE_BASE`, `CYCLE_ID`, `CYCLE_TITLE`) via `extra`.

After editing `src/defaults/`, run `npm run sync-defaults`.

Issue lifecycle: `docs/cycle/issues/{raw,todo,done,blocked,failed}/` — see [docs/RFC-001-issue-lifecycle.md](docs/RFC-001-issue-lifecycle.md).

**Detailed engine implementation notes:** [docs/ENGINE.md](docs/ENGINE.md) — covers triage, queue drain, blocked propagation, halt policy, resume, restart policy, retry skip, reflection, documentation step, artifact sanitization, spec post-condition, review Pass 3, SPEC→PLAN traceability, engine-managed commit lifecycle, and touched.json footprint.

## Subprocess discipline

- Always `spawn` / `spawnSync` with array args. Never `exec` / `execSync`. Never `shell: true`.
- Subprocesses inherit a curated PATH via `src/engine/child-env.ts`.
- **Re-injection contract**: `buildChildEnv` strips all `CYCLE_*` vars. Any new `exec-*.ts` or subprocess wrapper that needs `CYCLE_ID`, `CYCLE_BASE`, etc. must pass them explicitly in the `extra` argument (typically via `cycleEnv`). Omitting them produces silent `undefined` in the subprocess — no runtime error.

## Workflow defaults

- Force `--workflow feature` until triage + multi-cycle decomposition land.
- Queue halts after `engine.max_consecutive_failures` consecutive terminal failures (default 2).
- `engine.rate_limit_backoff_ms` — milliseconds to sleep between rate-limit retries (default 3,600,000 = 1 hour).
- See `BRIEF.md` and `docs/ARCHITECTURE.md` for the full system design.

## Publishing

See [docs/publishing.md](docs/publishing.md).


<claude-mem-context>
# Memory Context

# [cycle] recent context, 2026-06-08 3:18pm EDT

Legend: 🎯session 🔴bugfix 🟣feature 🔄refactor ✅change 🔵discovery ⚖️decision 🚨security_alert 🔐security_note
Format: ID TIME TYPE TITLE
Fetch details: get_observations([IDs]) | Search: mem-search skill

Stats: 50 obs (12,110t read) | 112,898t work | 89% savings

### Jun 8, 2026
600 12:41p 🔵 Cycle doctor verification passed for realtimechat with codex agent
601 " ✅ Customized realtimechat verify.sh to support build-only verification
602 " 🔵 Verified realtimechat Git state and verify.sh customization
603 12:42p ✅ Installed npm dependencies in realtimechat project
604 " 🔵 Verified realtimechat Astro build succeeds with 0 errors
605 " ✅ Updated realtimechat .gitignore to exclude .vercel/ build output
606 12:43p ✅ Staged realtimechat project files for initial commit
607 " 🔵 Initial realtimechat commit staged: 144 files, 60,118 insertions
608 " ✅ Created initial commit for realtimechat project
609 " ✅ Created GitHub repository timothyjoh/realtimechat and pushed initial commit
610 12:44p 🔵 Realtimechat cycle queue initialized and empty, ready to accept issues
631 2:27p 🔵 Cycle issue workflow structure in realtimechat
S172 Create two markdown issue files with acceptance criteria in realtimechat project's Cycle inbox; approved for execution (Jun 8 at 2:28 PM)
632 2:28p 🔵 Cycle queue state clean before issue creation
S173 Add two markdown issues to realtimechat Cycle tracker and verify Cycle system recognizes them in queue (Jun 8 at 2:28 PM)
633 " 🟣 Created two expanded Cycle issues for real-time chat features
S174 Verify realtimechat Cycle issue folder structure and confirm two markdown issues are present in correct locations (Jun 8 at 2:29 PM)
634 2:29p 🔵 Cycle inbox files created but not auto-indexed into queue
S175 Review staged diff of two markdown issue files before committing to realtimechat repository (Jun 8 at 2:29 PM)
635 " 🔵 Cycle uses triage engine to load inbox issues from markdown files
S176 Launch local Cycle engine to process queued issues in realtimechat project (Jun 8 at 2:29 PM)
636 " ✅ Committed expanded realtime feature issues to realtimechat
S177 Check status of running Cycle engine processing the two queued issues (Jun 8 at 2:30 PM)
637 2:30p ✅ Pushed realtime feature issues to GitHub and started Cycle engine
S178 Diagnose Cycle engine process by inspecting logs and directory state to verify execution (Jun 8 at 2:30 PM)
638 " 🔵 Cycle background process exited; log empty
S179 Re-run Cycle engine with diagnostics to troubleshoot and resolve startup failure (Jun 8 at 2:30 PM)
639 " 🔵 Cycle log.jsonl not created; run.console.log empty
S190 Add two expanded Cycle issues for real-time chat features to realtimechat; commit, push, and start Cycle engine to process them. (Jun 8 at 2:30 PM)
640 2:31p 🔵 Cycle run succeeds in foreground; triage processing 2 inbox issues
641 " 🔵 Cycle triage completed; realtime-chat-page cycle started with codex agent
642 2:32p 🔵 Cycle spec step completed; SPEC.md generated; research step started
643 2:33p 🔵 Cycle research step completed; RESEARCH.md generated; plan step started
644 2:35p 🔵 Cycle plan step completed; PLAN.md generated; build step started
645 2:37p 🔵 Build step failed; no code changes detected; cycle restarting on attempt 1
652 2:38p 🔵 Retry cycle 0001 spec step completed; research step restarted
653 2:39p 🔵 Retry cycle research step completed; plan step started
654 2:41p 🔵 Retry cycle plan step completed; build step restarted (attempt to fix)
655 2:43p 🔵 Build step failed again on retry attempt; cycle restarting on attempt 2 of 3
656 2:45p 🔵 Third attempt cycle started; spec step completed
666 2:46p 🔵 Third attempt research step completed; plan step started
667 2:48p 🔵 Third attempt plan step completed; final build attempt starting
668 2:50p 🔵 Build step failed all 3 attempts; realtime-chat-page marked permanently failed; cycle 0002 started on second issue
669 2:52p 🔵 Cycle 0002 started for realtime-presence-homepage; spec step completed
670 " 🔵 Cycle 0002 research step completed; plan step started
671 2:55p 🔵 Cycle 0002 plan step completed; build step started for second feature
672 2:57p 🔵 Cycle 0002 build failed identically; systemic codex agent issue confirmed
673 " 🔵 Cycle 0002 retry started; spec step completed
674 2:58p 🔵 Cycle 0002 retry research step completed; plan step started
675 3:01p 🔵 Cycle 0002 retry plan step completed; second build attempt starting
676 3:02p 🔵 Cycle 0002 second attempt build failed identically; third attempt starting
677 3:03p 🔵 Cycle 0002 final attempt (3rd overall) started; spec step completed
678 3:04p 🔵 Cycle 0002 final attempt research step completed; plan step started
679 3:06p 🔵 Cycle 0002 final attempt plan step completed; third and final build attempt starting
680 3:08p 🔵 Both cycles failed; Cycle engine halted after max consecutive failures threshold
683 " 🔵 Codex agent in Cycle completes build step without generating source code
684 " ✅ Cycle engine with Codex agent deployed to realtimechat test project
681 " 🔵 Cycle engine final state: both issues in failed queue
682 " 🔵 Final state confirmed: both issues in failed queue, cycle directories archived
S191 Memory agent observing Codex session: integrated Codex with Cycle workflow engine in realtimechat test project, ran two feature issues through automated workflow, both failed at build step (Jun 8 at 3:10 PM)
**Investigated**: Cycle + Codex integration architecture; feature workflow execution (spec → research → plan → build); post-condition validation mechanism; build step code generation; engine retry and halting policy; queue state after engine halt

**Learned**: Codex agent completes workflow steps with passing validation but generates zero source code changes in build step; Cycle's git post-condition check (git status --porcelain) detects mismatch between reported success and actual file modifications; max_consecutive_failures=2 threshold triggers engine halt and blocks remaining queue; both cycles failed identically, suggesting systemic issue with codex build-step output generation rather than random failure

**Completed**: Cycle + Codex integration deployed to ~/wrk/realtimechat; two feature issues (realtime-presence-homepage, chat-window) ingested and queued; full workflow execution captured across two cycles with detailed step logs; discovered gap between codex step-completion signals and actual code generation; engine halted cleanly after threshold reached

**Next Steps**: User will likely investigate BUILD.md artifacts to understand what codex attempted; examine why codex doesn't actually modify source files despite reporting build success; may need to adjust codex prompts, build step context, or post-condition validation; second issue blocked until build-step gap resolved; approval request queued is read-only status check to confirm final queue state


Access 113k tokens of past work via get_observations([IDs]) or mem-search skill.
</claude-mem-context>