---
name: distill-yourself
description: "本地 Claude Code/Codex/agent 对话历史的唯一检索入口。搜索、查看、恢复或分析过去的 agent 对话时使用，含项目级事实、压缩上下文及 ~/.claude/projects、~/.codex/sessions JSONL。Git/浏览器/文件历史及项目 data/sessions、runs、logs、results、MLflow 等运行记录不触发。也用于蒸馏偏好、Memory、画像和反复纠正；Memory/Profile 仅由 agent 暂存，用户在 UI 中同步。"
---

# Distill Yourself

你是本地 agent 对话历史的统一检索入口，也是用户认知的蒸馏器。你用本地 `distill` CLI 读取 Claude Code / Codex 历史，由当前对话里的 agent 自己分析、追证据并暂存结果。Memory/Profile 的配置同步默认交给用户在 UI 中操作。不要把蒸馏任务再外包给另一个模型，除非用户明确要求并且你给子任务提供完整 CLI 路径、scope 和约束。

## Core Rules

- 检索本地 Claude Code、Codex 或 agent 对话历史时，先用 `distill` 定位并核验证据，不扫描原始 transcript。
- 追查“哪个 Agent 用什么工具、命令或 patch 产生了某个文件”时，先用 `tool-search` 定位，再用 `read-tool-event` 定点核验；不要从消息搜索直接跳到原始 JSONL。
- 工具索引只保存每条调用参数最多 2 KB 的有界搜索投影（为 structured anchors、head 和 tail 设置 fixed quotas）、调用坐标和匹配结果的 result locator；精确 call ID 由 dedicated `call_id` column 匹配。不保存工具结果正文，result body is never stored in the SQLite search index。需要结果时给 `read-tool-event` 加 `--include-result`，由它根据 result locator 从原 JSONL 定点读取并截断。
- 当 `distill` 的有界消息或工具读取器无法提供所需细节时，report the bounded-reader limitation, improve the locator or anchor, or stop；never direct-read raw rollout or session JSONL，即使面对压缩边界、旧格式或缺失 locator 也没有 raw fallback。
- 不要扫描、打开或直接读取 session/rollout JSONL，也不要对它运行 `rg -n`、`rg -l`、`head`、`sed`、`jq`、Python 等 shell/content reader。JSONL 单行可能包含数万 token；`filePath` 和 byte locator 只供 `distill` 的有界读取器内部使用。
- 若任务还匹配其他工作流 skill，先完成历史取证，再把核验后的上下文交给后续流程。
- `distill` 只负责取数、检索和暂存；结论由你基于证据生成。
- 不创建 Episode 或 Resume Context 这类持久模式。把 `search` 找到的 `sessionId + idx` 与 `read-window` 的范围、角色投影和正文预算自由组合，由当前 Agent 根据任务语义选择需要的多轮片段。
- `profile-digest` / `aggregates` / `stats` 是地图，不是结论。写入 Memory/Profile/Twin 前必须用 `read-window`、`session-brief` 或其他有界 `distill` reader 核验；不能把“核验原 session”解释为直接读取 session JSONL。
- 不把 assistant echo、IDE/file context、task notification、agent/subagent prompt、工具输出噪声当作主证据。
- 蒸馏长期偏好、Memory、Rules 或 Patterns 时，检索命令加 `--evidence-only`；普通历史定位不要加，以免隐藏诊断线索。
- Memory/Profile 的标准流程止于 `distill evolve-write`。告诉用户结果已暂存，并由用户在 UI 中预览、确认和同步；不要代替用户运行 `distill evolve-sync --execute`。
- 只有用户明确要求使用 CLI 同步时，才把 `distill evolve-sync` 作为后备入口，并仍须先展示完整预览/diff、再次取得明确确认。不要手搓 Claude/Codex 配置格式。
- Twin 写回仍走 `distill twin-sync`；任何对 `~/.claude/`、`~/.codex/AGENTS.md` 或 `~/.agents/skills/` 的写入都必须先展示完整预览/diff，并得到用户明确确认。
- 经用户确认更新本 Skill 后，调用项目内置的 `distill install-skill --force`，不要手工复制；该命令将仓库内 `skills/distill-yourself` 同步到 `~/.claude/skills/distill-yourself` 和 `~/.agents/skills/distill-yourself`。
- Codex/Claude 子进程可能隔离用户配置、rules、plugins；面向子进程的 prompt 必须自包含，不依赖当前 session 的隐式记忆。

## CLI Entry

优先使用 PATH 上的 `distill`。如果没有，把命令替换成 `python3 <repo>/analyze.py`。

探索命令读取本地 `~/.claude/` 和 `~/.codex/` 历史；`distill refresh` 默认只增量更新新增或已变化的 session，`--force` 才全量重解析。`evolve-write` 只修改持久蒸馏数据，Memory/Profile 的配置同步默认由用户在 UI 中执行。`twin-batch` 和 `twin-sync --execute` 会修改持久认知模型数据或 Claude/Codex 配置。

## Standard Workflow

```text
0. INDEX    -> refresh local SQLite/cache
1. ORIENT   -> load digest/aggregates/stats
2. EXPLORE  -> search, select candidates, then read-window
3. DISTILL  -> produce evidence-backed insight
4. STAGE    -> persist approved Memory/Profile results with evolve-write
5. HANDOFF  -> user previews and confirms configuration sync in the UI
```

Choose the scope before retrieval. For an exact fact, phrase, session, or project discussion, use the fast path: refresh once, retrieve one page of at most 20 candidates, then verify only the best 2-4 windows. Do not load digest/aggregates/stats for a simple lookup.

Resolve the user's time wording before retrieval. For a reproducible calendar range, use `--start YYYY-MM-DD --end YYYY-MM-DD`; both boundaries are inclusive, either boundary may be omitted, and these options must not be combined with `--date`. Treat `--date 1d/7d/30d/90d/all` as a quick relative shortcut only. When the user says “过去一周” or another relative period, resolve it against the current date, state the interpreted dates, and carry the same exact range through every locating command. If the user requests commands only, state the interpretation in a short shell comment before the commands. By default, “过去 N 天” includes today and the preceding `N-1` calendar dates; surface a materially different interpretation instead of silently changing it.

```bash
distill refresh
distill search "<query>" --recall normal --role user --evidence-only --format jsonl --max-chars 500 --limit 20 --page 1 --date 90d
distill search "<query>" --recall normal --role user --format jsonl --max-chars 500 --limit 20 --page 1 --start 2026-07-01 --end 2026-07-07
distill read-window --batch '[{"sessionId":"session_id","idx":123,"before":8,"after":5,"include":"user:2000,assistant:600"}]'
```

For exact tool provenance, use a separate bounded ladder. If the user already gives a filename, path, command fragment, patch target, or call ID, start at step 2:

```text
1. CONTEXT  -> use message search only when you still need to identify the discussion
2. LOCATE   -> tool-search the narrowest stable anchor
3. SELECT   -> keep the best 1-3 sessionId + eventIdx locators
4. VERIFY   -> read-tool-event for the exact call input
5. RESULT   -> add --include-result only when the result is necessary
6. STOP     -> answer as soon as the provenance is established
```

```bash
distill refresh
distill tool-search "<filename-or-command>" --format jsonl --max-chars 500 --limit 20 --page 1 --date 90d
distill read-tool-event <session-id> --event-idx <N> --max-chars 2000
distill read-tool-event <session-id> --event-idx <N> --around "<known-anchor>" --max-chars 2000
distill read-tool-event <session-id> --event-idx <N> --include-result --max-chars 2000
```

`tool-search` searches only bounded call-input projections, never tool results. The 2 KB projection assigns fixed quotas to a prioritized subset of structured anchors (paths, basenames, commands, patch headers, and nested tool names), head, and tail, so one category cannot consume the others' entire budget. It does not promise to retain every arbitrarily numerous anchor; a filename actually within the fixed tail remains searchable without indexing or printing the full input. Exact call IDs are matched separately against the dedicated `call_id` column rather than being described as input-projection anchors. Its `filePath` is provenance, not permission to print that JSONL.

`read-tool-event` seeks to the indexed byte range, returns a default bounded head projection, and caps model-visible output. If that head omits a known fact, use `--around "<known-anchor>"` to center the same bounded budget on that anchor; do not increase the budget. If the result is requested, it follows the indexed result locator rather than scanning to EOF, applies the same cap, and does not persist the body.

Whenever you recommend `--include-result`, say explicitly that the result body is read on demand from the source JSONL through an indexed result locator and that the result body is never stored in the SQLite search index. This distinction explains why the command is safe and why `tool-search` cannot search result bodies.

`--max-chars 2000` is a hard ceiling for tool-event reads, not a first step in progressive expansion. If the needed fact is outside the returned projection, report the bounded-reader limitation, improve the locator or anchor, or stop; never propose 4000, 10000, a raw fallback, or any direct rollout/session JSONL read.

If `tool-search` misses, refresh once, retry with a shorter stable basename or command fragment, then use message search to identify a better anchor. Because the index reserves fixed quotas for structured anchors and head + tail, do not compensate by increasing `--limit`, walking later pages indefinitely, globally grepping transcripts, or reading the beginning of a rollout file.

Choose the scope before ORIENT, and use ORIENT only for broad profile, trend, correction-pattern, or cognitive-model analysis. If the user asks about a recent/project-specific topic, carry that `--date` / `--project` into the orienting commands; otherwise use `--date all --source all`.

For exact calendar requests, carry `--start` / `--end` instead of `--date` into `search`, `tool-search`, `sessions`, `queries`, `corrections`, `find-repeats`, and other history-locating commands. Once a precise `sessionId + idx` or `sessionId + eventIdx` is selected, the bounded reader uses that locator directly and does not need the time filter repeated.

For broad global analysis, start with:

```bash
distill refresh
distill profile-digest --date all --source all
distill aggregates --json
distill stats --date all
```

For a scoped run, use the same scope consistently:

```bash
distill profile-digest --date 90d --source all --project "<project>"
distill aggregates --json
distill stats --date 90d --project "<project>"
```

Expand to `all` only when evidence is thin.

## Retrieval Routing

| Need | First tool | Follow-up |
|---|---|---|
| Exact preference phrase or correction | `distill search "<phrase>" --recall normal --role user --evidence-only --format jsonl --limit 20 --page 1` | Select 2-4 direct user hits, then `read-window --batch` |
| Conceptual preference | Split into 2-4 concrete anchors, then run `search --recall normal` for each | If direct user evidence is thin, repeat with `--recall high`, then page |
| Topic, project, or historical discussion | `distill find-repeats "<question>" --limit 5 --json` | `session-brief` / `read-window --batch` for top candidates |
| Complete multi-turn discussion or compaction recovery | Locate 1-3 direct user anchors with `search` | Read a wider message window; separately verify relevant tool events, files, Git, or tests when needed |
| Possible orchestration noise | `distill evidence-audit --json` | Treat `artifactReason` rows as diagnostic only |
| Session-level context | `distill session-brief <id>` | `distill read-window <id> --idx N` |
| Tool call, command, patch, or file provenance | `distill tool-search "<exact-anchor>" --format jsonl --limit 20 --page 1` | `distill read-tool-event <session> --event-idx N`; add `--include-result` only if needed |

Important commands:

| Command | Purpose |
|---|---|
| `distill corrections --limit 100` | Correction anchors with a session-scoped `idx` and the nearest user/assistant pair in `conversation` |
| `distill queries --limit 50` | User requests, including possible acceptance signals |
| `distill highlights --limit 20` | High-signal sessions ranked by correction/decision density |
| `distill search "<query>" --recall normal --format lines --limit 20 --page 1` | Compact exact results with explicit `session`, `idx`, and `role` labels |
| `distill search "<query>" --recall high --format jsonl --limit 20 --page 1` | Hybrid high-recall results with match reasons, artifact downranking, and `idx` |
| `distill find-repeats "<question>" --limit 5 --json` | Evidence buckets: strong, related, weak, artifacts |
| `distill read-window <id> --idx N --before 8 --after 5 --include user:2000,assistant:600` | Compose a bounded multi-turn window around a hit |
| `distill read-window --batch '[...]'` | Verify several windows at once |
| `distill evidence-audit --json` | Estimate contamination from prompts/tasks/context noise |
| `distill tool-search "<query>" --format jsonl --limit 20 --page 1` | Bounded search over tool-call inputs with JSONL locators |
| `distill read-tool-event <id> --event-idx N --max-chars 2000` | Read one indexed call as a bounded head projection |
| `distill read-tool-event <id> --event-idx N --around "<known-anchor>" --max-chars 2000` | Center the bounded call projection on an already known anchor |
| `distill read-tool-event <id> --event-idx N --include-result --max-chars 2000` | Read the matching result through its indexed locator without indexing its body |

`corrections` and `search` JSON/JSONL expose `sessionId`, `idx`, and sometimes `messageIndex`; use `sessionId + idx` as the read coordinate. `idx` belongs to the current session index snapshot: it is neither a global ID nor a permanent cross-refresh identifier, and gaps are allowed. A missing or duplicate target is an error rather than a guessed match.

```bash
distill read-window <session_id> --idx 123
distill read-window --batch '[{"sessionId":"session_id","idx":123,"before":8,"after":5,"include":"user:2000,assistant:600"}]'
```

`read-window` defaults to two actual indexed messages before and after the target and `--include user:2000,assistant:600`. Set `--before` / `--after` independently up to 20; it selects actual neighboring messages first, then applies the role projection. `--include` accepts role budgets such as `user:2000,assistant:600`; omit a role to filter it out. Use `--around "<exact target text>"` only when that literal occurs exactly once in the target role's full indexed source; zero or multiple matches are errors, so lengthen the anchor instead of guessing.

Every `read-window` rendering uses the same bounded serializer: human, `--json`, and all output formats share `batch size <= 5` and `total serialized output <= 20 KB`. Structured `text` remains pure source projection; human output adds visible truncation markers, while JSON reports truncation, source completeness, coordinates, and freshness as metadata. Future parsed messages retain full user source before projection; legacy rows may report source completeness unknown and are not silently treated as complete. If freshness is stale or the source is missing, refresh before drawing a negative conclusion. Do not reconstruct one truncated transcript with multiple batches, later pages, another format, or raw JSONL; narrow the selected locators or exact anchor instead.

For manual triage, prefer `--format lines`; for scripts or incremental aggregation, prefer `--format jsonl`. `--limit N` is the page size and `--page 2`, `--page 3`, ... retrieves later pages. Keep the standard page size at 20 and page instead of requesting one oversized result. Mirrored copies of the same timestamped message are folded before paging, while `duplicateCount` / `duplicateSessionIds` preserve provenance in structured output.

`-C/-B/-A` are optional inline previews for a human terminal, not the Agent verification path. Search without inline context, select a few locators, then use `read-window`. Every `read-window` format is bounded and marks per-message and total-output truncation; structured output is not an escape hatch for retrieving complete indexed text.

Stop retrieval when you have enough direct user evidence. More searching after 2-4 strong, verified quotes usually adds noise.

For tool provenance, stop after 1-3 exact verified events. Tool outputs are routing or execution evidence, not durable evidence of a user preference.

## Required References

Before doing any task below, read the matching reference. Do not rely on memory for product-specific SOPs.

| User intent | Required reference |
|---|---|
| 蒸馏偏好 / 记住我的习惯 / 更新 memory | `references/memory-profile.md` |
| 我是什么样的开发者 / 生成画像 / profile / persona | `references/memory-profile.md` |
| 写回 ~/.claude / 同步到 Claude 配置 / 保存为长期偏好 | `references/memory-profile.md` |
| 我反复纠正了什么 / 纠正趋势 / 反复踩的坑 / rules / signals / patterns | `references/rules-signals-patterns.md` |
| 建认知模型 / 分析我怎么决策 / Twin / runtime pack / cognitive model | `references/twin-cognitive-model.md` |

If the user asks to "do all of it", ask them to choose Memory/Profile, Rules report, or Twin first. Twin is much heavier than Memory/Profile.

## Evidence Discipline

- Prefer user-role messages and direct user acceptance/correction signals.
- Use assistant text only as context for what the user reacted to, not as evidence of the user's preference.
- Treat IDE context, active file lists, task notifications, agent prompts, and tool outputs as routing clues only.
- Every durable insight must carry enough evidence to trace back to original `session_id` and quote/window.
- If evidence is ambiguous, report the ambiguity instead of writing a durable preference.

## Writeback Discipline

- Keep write scope consistent. If staging uses `--source all --date all`, tell the user to select the same scope in the UI before syncing.
- After `evolve-write`, summarize what was staged and hand off the final preview and sync action to the user in the UI.
- Do not run `evolve-sync --execute` as part of the standard Memory/Profile workflow. If the user explicitly requests CLI sync, `evolve-sync` without `--execute` is the preview step; show its complete output and require a separate confirmation before execution.
- `twin-sync` also defaults to preview. It writes the Runtime Pack to `judgment-decision-model` Skills for Claude/Codex and keeps only short entry pointers in `CLAUDE.md` / `AGENTS.md`.
- Twin preview commands must be shown to the user before execute commands.
- `install-skill` targets Claude Code at `~/.claude/skills/distill-yourself` and Codex at `~/.agents/skills/distill-yourself`.

## Install

```bash
pip install git+https://github.com/QuantaAlpha/Distill-Yourself.git
distill install-skill
```

For local development, run commands from this repository with `python3 analyze.py <command>` if `distill` is not installed.
