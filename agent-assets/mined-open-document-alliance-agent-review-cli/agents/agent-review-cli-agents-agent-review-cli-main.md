# agent-review-cli

## Vision

**agent-review** is a parallel, multi-agent code review and fix CLI. It orchestrates multiple AI coding agents to systematically discover real bugs in a codebase, fix them in parallel, verify the fixes, and open a pull request — all with a single command.

The goal is to be the **best automated review loop** available: fast parallel discovery, immediate parallel fixing, robust verification, and a polished terminal UI that gives the user full visibility into what every agent is doing at every moment.

### Core Principles

1. **Fully parallel.** Discovery agents run concurrently (read-only). Fix agents also run concurrently, each in its own git worktree. Their branches are merged into the integration branch after all fixes complete. Verification runs as a single agent on the merged result.

2. **Backend-agnostic.** Supports Codex (OpenAI), Claude Code (Anthropic), and OpenCode as interchangeable backends. Mixed mode distributes agents across all available backends. Adding a new backend means implementing the `BackendDriver` interface.

3. **Smart file partitioning.** The codebase is split by directory structure, not round-robin, so each agent reviews a coherent slice of the codebase. Large directories are recursively subdivided to ensure even distribution.

4. **Resilient execution.** Agents may time out, crash, or produce malformed output. The orchestrator handles all of these gracefully — synthesizing results from git commits when output files are missing, surfacing errors clearly in the dashboard, and never blocking the pipeline on a single agent failure.

5. **Informative TUI.** The Ink-based dashboard is the primary user interface. It must always give an accurate, real-time picture: which phase is active, what each agent is doing, how many issues are found/fixed, token usage, and a scrolling activity log. The user should never have to guess what's happening.

6. **Clean git workflow.** Discovery uses a shared worktree (read-only). Fix agents each get their own worktree branched from the integration branch. After fixing, branches are merged back. After verification, the branch is rebased onto the default branch, pushed, and a PR is created. All worktrees and local branches are cleaned up automatically.

---

## Architecture

### Pipeline Phases

```
INIT → PLAN → DISCOVER → FIX → INTEGRATE → VERIFY → PUBLISH → DONE
```

| Phase | What happens |
|-------|-------------|
| **Init** | Resolve git root, branch, create shared worktree, detect available backends |
| **Plan** | Identify target directories from the user's natural language prompt (agent-assisted or heuristic) |
| **Discover** | N agents run in parallel (read-only on shared worktree), each reviewing a directory-grouped segment of files |
| **Fix** | N fix agents run in parallel, each in its own worktree branched from the integration branch |
| **Integrate** | Merge each fix agent's branch into the integration branch (auto-resolve conflicts favoring fixes) |
| **Verify** | A final agent runs type-checks, builds, and tests on the merged result; applies minimal corrective fixes |
| **Publish** | Rebase onto default branch, push, create PR via `gh` |
| **Cleanup** | Remove all worktrees, prune git bookkeeping, delete local branches |

### File Structure

```
agent-review-cli/
  bin/agent-review.js    # Thin entry point that imports dist/index.js
  docs/                  # Product intent and feature behavior docs
  src/
    index.tsx            # CLI argument parsing (Commander), Ink app mount
    orchestrator.ts      # Core orchestration — phases, agents, git, prompts, schemas
    dashboard.tsx        # Ink TUI components — header, phase bar, stats, agent table, log
    types.ts             # All shared TypeScript types
  dist/                  # tsup build output (single ESM bundle)
  package.json
  tsconfig.json
```

### Key Abstractions

- **`BackendDriver`** — Interface for backend CLIs. Each driver implements `checkVersion()`, `buildArgs()`, and `parseStdoutLine()`.
- **`AgentReviewOrchestrator`** — Main class. Manages the full pipeline, agent lifecycle, issue store, git worktrees, and snapshot emission.
- **`RunSnapshot`** — Immutable state object emitted to the dashboard on every change. Contains all data the TUI needs.
- **`IssueStore`** — JSON file persisted in the run directory tracking all discovered issues and their status transitions.

### Backend Drivers

Each backend CLI is spawned as a child process. The orchestrator reads JSONL from stdout and parses it via the driver's `parseStdoutLine`.

| Backend | Command | Output format | Schema support |
|---------|---------|--------------|---------------|
| Codex | `codex exec --json` | JSONL events | `--output-schema` + `-o` |
| Claude Code | `claude -p --output-format stream-json --verbose` | JSONL events | Schema embedded in prompt + Write tool |
| OpenCode | `opencode run --json` | JSONL events | `-o` |

**Important driver quirks:**
- Claude Code requires `--verbose` when using `--output-format stream-json`
- Claude Code doesn't support `--output-schema`; the schema is embedded in the prompt and the agent is instructed to write the output file using the Write tool
- Codex removed the `-a never` flag in 0.98.0; use `-s read-only` instead
- Codex requires `additionalProperties: false` on all schema objects and does not accept `$schema` fields

### Mixed Mode

When `-b mixed` is specified, the orchestrator:
1. Detects which backends are installed (`detectAvailableBackends`)
2. Assigns backends round-robin to agents (`assignBackend`)
3. Each agent uses its own driver for spawning and output parsing
4. The planner and verification agents default to the first available backend

### File Partitioning

`splitFilesIntoDirectorySegments` groups files by directory at depth 2, then recursively subdivides oversized groups at depths 3-5. Final chunks are bin-packed (largest-first, greedy) across N agents. This ensures:
- Each agent gets a coherent directory slice, not scattered files
- No agent gets dramatically more files than others
- Related files stay together for better contextual review

### Fix Agent Parallelism & Integration

Fix agents run fully in parallel. Each fix agent:
1. Gets its own worktree branched from the integration branch (`agent-review/{runId}-fix-{i}`)
2. Runs independently — no shared file state, no git races
3. Commits fixes to its own branch

After all fix agents complete, the **integration phase** merges each fix branch into the integration branch:
- Clean merge attempted first
- On conflict: abort and retry with `-X theirs` (favor the fix agent's changes)
- If still failing: skip that agent's fixes and log the conflict

---

## Build & Development

### Commands

```bash
# From the agent-review-cli directory:
pnpm build              # Bundle with tsup (fast, no type-checking)
pnpm type-check         # Run tsc --noEmit (MUST do this — tsup skips type-checking)
npm link                # Symlink globally so `agent-review` command is available
```

### Critical: tsup does NOT type-check

The build uses **tsup** (esbuild under the hood) which transpiles but **never reports TypeScript errors**. A build succeeding does NOT mean the code is correct. Always run `pnpm type-check` before considering changes done.

### Testing a build

```bash
pnpm type-check && pnpm build && npm link
agent-review 3 -b claude-code -t "papertrail web app"
agent-review 5 -b mixed -t "the chrome extension"
```

---

## TUI Design

The dashboard is built with **Ink** (React for terminals). It renders a full-screen layout that updates in real time via snapshot subscriptions.

### Layout (top to bottom)

1. **Header** — Run ID, backend, elapsed time, branch, target paths (rounded border, cyan)
2. **Phase Bar** — Horizontal pipeline: INIT ━━ PLAN ━━ DISCOVER ━━ FIX ━━ INTEGRATE ━━ VERIFY ━━ PUBLISH ━━ DONE. Filled circles for completed, target circle for active, empty for pending.
3. **Stats Row** — Three stat cards side-by-side: Issues (found/fixed/open/failed), Agents (running/done/failed/pending), Tokens (input/cached/output)
4. **Agent Table** — Grouped by phase (Planning, Discovery, Fix, Verification). Each row: name, status, assigned count, found count, fixed count, tokens, info/error message. Running agents show a braille spinner.
5. **Activity Log** — Scrolling log (last 40 entries) with timestamps. Errors highlighted red, completions green.
6. **Completion Panel** — Shown when done. Double-bordered box with final stats, PR URL, branch, report path.

### Design Goals for the TUI

- **Information density.** Show as much useful data as fits without clutter. Use color to draw attention to important state changes (errors red, success green, active yellow).
- **Responsive width.** All panels adapt to terminal width. The INFO column in the agent table uses remaining space.
- **Real-time feedback.** The user should see agent progress, token accumulation, and log entries as they happen, not just at the end.
- **Clear error attribution.** When an agent fails, the error message should appear on that agent's row AND in the activity log with enough detail to diagnose the issue.

---

## Conventions & Gotchas

### Code Style
- TypeScript strict mode, ESM modules, Node 20+ target
- React JSX for Ink components (`.tsx` files)
- No external state management — snapshot pattern with `subscribe()` callback
- Async/await throughout, no callbacks
- `allowFailure: true` for git/CLI commands that may legitimately fail

### React / Ink Rules
- **Hooks must be called unconditionally.** No hooks after early returns. This is a common bug source in the dashboard components.
- Ink re-renders on state changes, same as React. Use `useTimer` for periodic updates (spinners, elapsed time).

### Data & Paths
- Run data directory: `.agent-review/runs/{runId}/`
- Worktrees directory: `.agent-review/worktrees/{runId}/`
- Integration branch: `agent-review/{runId}`
- Fix agent branches: `agent-review/{runId}-fix-{i}`
- All file paths in the issue store are relative to repo root, forward-slash normalized
- The `.agent-review/` directory is gitignored at the monorepo root

### Token Tracking
- Tokens are tracked **incrementally** in `runBackendExec`'s stdout handler via `addAgentUsage`
- Do NOT add tokens again after exec returns — this causes double-counting
- The `CodexExecResult.usage` field is for diagnostics, not for updating the snapshot

### Timeouts
- Overall timeout: 600s (10 min) per agent
- Inactivity timeout: 180s (3 min) — resets on any stdout/stderr output
- Configurable via `--timeout` and `--inactivity-timeout`

### Output File Reliability
- Codex writes output files natively via `--output-schema` + `-o`
- Claude Code is instructed to write output files via prompt; if it doesn't, the orchestrator:
  1. Tries to extract JSON from the captured result text in stdout
  2. For fix agents: if a commit was created but no output file exists, synthesizes a success result
- Always check for output file existence before reading; handle ENOENT gracefully

### Cleanup
- Worktrees are cleaned up by default after the run (use `--no-cleanup` to keep them)
- Cleanup: `git worktree remove --force` → fallback `fs.rm` → `git worktree prune` → `git branch -D`

---

## Agent Self-Improvement Protocol

When working on this project, you are not just implementing features — you are maintaining a living system with accumulated knowledge. Follow these rules:

### Timing gate (default: no update during planning)

Do not persist self-improvement updates during planning-only work:

- User is brainstorming, requesting a plan, or evaluating approaches
- The session is in analysis/Plan Mode with no completed implementation

Only evaluate/persist learnings after an actual code session is complete (implementation done).
If no code changes were completed, skip self-improvement updates.

### Materiality gate (default: no doc update)

Do **not** update memory/docs on every correction. A persistence update is required only when the lesson is likely to help future sessions, not just the current diff.

Persist only when **at least one** is true:

- The same mistake happened more than once (or is likely to recur)
- Behavior/architecture expectations changed in a durable way
- A backend/CLI quirk changed and would break future runs
- Product intent or UX expectations changed for users (not just implementation details)

Skip persistence updates for one-off wording preferences, temporary debugging notes, or edits that are obvious from the code diff.

### Generality gate (default: express as general principles)

Learnings must be expressed as **general principles**, not project-specific implementation notes.

- Bad: "Remember to update the dashboard TUI when adding a new pipeline phase"
- Good: "When adding enum values, update all exhaustive type usages (Record types, switch statements)"
- Bad: "Make sure the agent table supports the new verification column"
- Good: "When data models change, check and update all dependent UI components"

Ask: "Would this rule make sense to someone working on a completely different feature?"

### Where to persist

1. **Update AGENTS.md** for durable conventions, architecture/behavior corrections, or driver/CLI compatibility notes
2. **Create or update a skill** for repeatable command workflows that should be automated
3. **Update the memory file** (`~/.claude/projects/.../memory/MEMORY.md`) for cross-project conventions outside `agent-review-cli`
4. **Maintain markdown docs in `agent-review-cli/docs/`** for user-facing behavior:
   - What features do
   - What the product is expected to do
   - Important operational constraints

### Documentation maintenance rule

When behavior or product expectations materially change, update the relevant `docs/*.md` files in the same task. If no docs exist yet, create a minimal baseline before adding details.

### What to capture

- **Bug patterns** — recurring mistakes and their prevention (expressed as general principles)
- **CLI breaking changes** — backend flags/behavior changes
- **Architecture decisions** — chosen approach and rationale
- **General engineering principles** — patterns that prevent classes of bugs, not just one specific bug

### How to decide

Ask: "Would this still matter to a fresh agent next week working on a different feature, with no chat context?"  
If yes, persist it as a general principle. If not, leave docs unchanged.
