---
name: broco
description: On-demand crew skill for any coding agent host (Claude Code, Codex, Cursor, Antigravity, OpenCode, Pi). Summon other logged-in AI CLIs via broco when your own quota is tight, you want an independent cross-vendor worktree review, you need a modality you lack (image/audio/video/PDF), or you need sharded map batch jobs. Works zero-init (L0) in any directory once global workers are allowed.
---

Use the installed launcher {{launcher}} for every command (on Windows PowerShell, prefix a quoted path with `& `, e.g. `& {{launcher}} roster --json`). This skill works across any Agent Skills host (Claude Code, Codex, Cursor, Antigravity, OpenCode, Pi).

## When to summon broco (On-Demand Crew)

Default to doing quick work yourself or using your host's built-in subagents:
- **Do it yourself / host subagent**: 5-minute fixes, small single-file edits, straightforward debugging, or same-vendor quick questions.
- **Summon `broco` on demand** when one of these applies:
  1. **Tight quota / rate limits**: Your primary model's budget is running low — check `{{launcher}} roster --json` and hand off heavy work to a CLI with plenty of quota left.
  2. **Cross-vendor blind review & isolated edits**: Run `{{launcher}} say NAME ... --worktree` and `{{launcher}} review NAME` (omit `--by` to auto-pick a different vendor) so another model reviews the diff with fresh eyes.
  3. **Missing input modalities**: Need to inspect images, audio, video, or PDFs that your current host cannot read — check `capabilities.input` for `true` and pass `--attach PATH`.
  4. **Sharded batch work (`map`)**: Fan out one brief across N files or items with FIFO concurrency, per-shard retry, and batch acceptance.

## L0 Zero-Init vs L1 Project Isolation

- **L0 zero-init (default)**: Once global workers are allowed (`{{launcher}} setup` or `{{launcher}} allow <ids> --global`), `roster`, `say`, `review`, `map`, `ls`, `show`, `wait`, `diff`, `done`, `clean`, `stats`, `status`, `retry`, and `stop` work directly in any directory. `broco` resolves `canonical(gitRoot || cwd)` internally in `~/.broco/` and inherits global allowlist, default worker, and concurrency **without** creating `.broco/` or editing `AGENTS.md` / `CLAUDE.md`.
- **L1 project isolation (`init`)**: Run `{{launcher}} init [--allow ...] [--default-worker ...] [--concurrency N] [--host auto|agents|claude|codex|cursor|agy|opencode|pi] [--manager-mode] [--no-agents-md]` when a repository (such as a private workspace) needs strict project-level allowlist, concurrency, or rules that override global settings. By default `init` writes lightweight on-demand crew guidance to `AGENTS.md` (or updates an existing `CLAUDE.md` when `AGENTS.md` does not exist, or when `--host claude` is passed); pass `--manager-mode` for heavy manager-only guidance. `{{launcher}} uninit` removes `.broco` and strips the marked block.

## Recursion Guard (No Nested Worker Fan-Out)

Worker sessions run with `BROCO_IN_WORKER=1`. Inside a worker session, `say`, `review`, `map`, and `retry` are **rejected by default** to prevent recursive dispatch loops. Complete your assigned task and report back to your caller instead; only pass `--allow-nested` when explicitly authorized to orchestrate sub-workers.

## Antigravity (`agy`) Terms-of-Service Warning

Google's consumer plans (Free, AI Plus, Pro, Ultra) do not allow third-party agents to drive the Antigravity CLI; using `agy` as a `broco` worker may get the account suspended. It should only be used with a Gemini API key or a Gemini Enterprise / Google Cloud project (details: `https://broco.yanauto.me/docs/workers/#agy`).

- **Always relay this warning to the user** before allowing `agy` (`setup`, `allow`, `init`) or dispatching work to `agy` (`say`, `map`, `review`).
- **Prefer other allowed workers** (`pi:<provider>`, `codex`, `claude`, `cursor-agent`) by default unless the user explicitly picks `agy`.

## Workflow

Quote names, short prompts, and option values as separate arguments. For multi-line, backtick-heavy, or `$VAR`-containing prompts, pass `--file /path/to/prompt.md` or read stdin via `-` (`{{launcher}} say NAME - --bg --json <<'EOF' ... EOF`). To work in another directory while keeping the current project's policy, pass `say --cwd DIR` on a new name (`~/` expands automatically; conflicts with `--worktree`). From outside a directory, pass `--project PATH`.

1. **Inspect health, roster & live quota**:
   - `{{launcher}} status [--all] --json` checks runner health, uptime, web URL, active proxies, active/queued tickets, batches, and cleanable worktrees without auto-starting an offline runner.
   - `{{launcher}} roster --json` (pass `--global` to inspect global defaults, `--refresh` only when CLI logins/models just changed; otherwise allowed CLIs share a 45s cache). Disallowed workers return only `id`/`allowed: false`; top-level `warnings` explains sign-in/install commands for allowed workers that are missing or signed out.
   - Check `capabilities.input` (`image`, `audio`, `video`, `pdf`) and require `true` before `--attach`. Read `quota` (`avoid`, `plentiful`, `tightGroups`) and `recentProblem`: switch worker when `avoid` is true or `recentProblem` is present; raise concurrency via `{{launcher}} set concurrency N` when `plentiful` is true and you have parallel work. A model's own `record` (3+ non-blocked tasks) outranks catalog grades.
2. **Dispatch single tasks**:
   - `{{launcher}} say research "the task" --worker WORKER --model MODEL --effort LEVEL --bg --json` (or `--file PATH` / stdin `-`). Prompts never appear in worker `ps` arguments.
   - Add `--worktree` on the first `say` for isolated parallel code edits from committed `HEAD`. Attach verified media with repeated `--attach PATH`. Reuse a name to continue its native session, or pick a new name for parallel work.
3. **Fan out bulk / sharded work (`map`)**:
   - `{{launcher}} map PREFIX --brief-file brief.md --inputs shard-*.jsonl --worker WORKER --model MODEL --effort LEVEL --bg --json` (supports `--brief`, `--brief-file -`, `--input`, `--inputs`, `--inputs-file PATH|-`, and `{input}`, `{index}`, `{count}`, `{name}` placeholders).
   - Wait for all shards with `{{launcher}} wait PREFIX --json`, inspect with `{{launcher}} show PREFIX [--status error|review] [--full] --json`, retry failed/stopped shards via `{{launcher}} retry PREFIX [--worker ID] [--model ID] --bg --json`, and close ready shards with `{{launcher}} done PREFIX --result pass --why "one line"`.
4. **Wait, inspect, review & clean**:
   - Wait asynchronously using your host's background shell execution (e.g. `run_in_background: true`) with `{{launcher}} wait NAME [TURN] --json`. Event-driven `/wait` wakes immediately on completion and returns `reply`, `task`, `cwd`, `worktree`, `branch`, `changedFiles`, `contextWarning`, `quota`, and `problem`.
   - Read receipts (`queue`, `note`, `rules`, `reminders`, `contextWarning`, `sessionWarning`). If an initial turn failed before binding a native session, use `{{launcher}} retry NAME [--model ID] [--effort LEVEL] [--worker ID] --bg --json` to replay the stored prompt and snapshotted attachments cleanly.
   - Keep context lean: `{{launcher}} ls --active --json`, `{{launcher}} show NAME --compact --json` (or `--turn N`), `{{launcher}} diff NAME [--stat] [--json]`.
   - Cross-vendor review: `{{launcher}} review NAME [--by OTHER_WORKER] [--model MODEL] [--bg] [--json]` — omitting `--by` automatically selects an allowed worker from a different vendor. Accept writer and reviewer separately with `done`, then remove retained worktrees with `{{launcher}} clean [NAME|PREFIX] [--delete-branch] [--dry-run] --json`.
   - Handle `problem.class`: `quota` or `region` -> switch worker and close with `--result blocked`; `policy` -> rephrase; `network` -> `{{launcher}} retry NAME`; `auth` -> ask user to sign in; `context` -> hand off with `{{launcher}} say NEW_NAME "next task..." --from OLD_NAME --worker WORKER --bg --json`. Never record infrastructure blocks as `fail`.
5. **Direct configuration & audit**:
   - Settings apply immediately, log an audit entry, and print a one-command undo (all accept `--global` or `--project PATH`, plus `--json`):
     - `{{launcher}} set concurrency <1..64|inherit>` / `{{launcher}} set default-worker <worker>`
     - `{{launcher}} defaults <worker> [--model ID] [--effort LEVEL] [--clear]`
     - `{{launcher}} note <worker> "concise operational note"` (or `--clear`)
     - `{{launcher}} allow <w1,w2> [--default-worker w]` / `{{launcher}} deny <w1,w2>` (only change allowlists when aligned with the user's instructions)
     - `{{launcher}} rules [--add "rule"] [--rm "rule"] [--clear] [--worker ID] [--override]`
     - `{{launcher}} hide <worker> <m1,m2>` / `{{launcher}} unhide <worker> <m1,m2>`
     - `{{launcher}} audit [--global|--all] [--limit N]` / `{{launcher}} undo [ID]`

## Task Boundaries and Results

A name is a persistent worker session, not the unit of the performance record. Its first `say` starts task 1; each task spans consecutive turns (`tasks` in `show`). Use ordinary `say NAME` or `retry NAME` for clarifications and revisions toward the same acceptance criteria. After recording an outcome for the current task, pass `--new-task --title "short title"` when starting independent work on the same session. Record outcomes with `{{launcher}} done NAME --result pass|rework|fail|blocked --why "reason"` (`--task N` amends an earlier task; explicit `--result` also closes interrupted `error`/`stopped` tickets after inspection, while bare `done` requires `review` status). Check cross-project or per-project records anytime with `{{launcher}} stats [--project PATH] --json`.
