---
name: agent-collab
description: >
  Cross-repo work tickets (platform skill). Use when the user wants to file a
  ticket from one project to another (提单 / 跨仓委托 / 开给别的仓库的单), or in
  the receiving project to list inbox, claim, challenge assumptions, reply, or
  close (有没有我的单 / 认领 / 关单). Agent loads this skill and runs the
  co-located runner; humans only state intent. Target repos come from the local
  allowlist config, not from this description.
---

# Cross-repo ticket (work tickets)

**Who runs:** the coding agent (Host TUI / OpenClaw), **not** the human.  
**Never** tell the user to copy-paste `run.sh` as the primary path.

Single source: this directory (`SKILL.md` + `run.sh` + `test.sh`). Other paths
are symlinks from `scripts/dev/link-platform-skills.sh`.

Skill id: **`agent-collab`**. Short CLI on PATH (optional): **`ticket`**.

## Three modes (hard rule)

| Mode | User intent | You do | Must NOT |
| --- | --- | --- | --- |
| **1. 主会话创建工单** | 提单 / 跨仓委托 / 只交票 | `create`（**无** `--run`） | 自动 `run` / worktree / worker |
| **2. 主会话认领并开发** | 有没有我的单；认领；认领后改 | `inbox` → `claim` → `show` → **在当前 TUI/cwd 开发** | `run` / `create --run` / 建 `ticket-*` worktree |
| **3. 主会话建单并委托开发** | 明确说后台跑 / 派工人 / 委托开发 | `create … --run` 或已有单上 `run --phase auto` | 把 Mode 2 的认领误当成 Mode 3 |

`claim` 默认 **session**（`owner=human`）。Headless worker 才用 `claim --as-worker`（由 `run` 内部调用）。  
**认领 ≠ 派工人。** 用户在 TUI 认领后，由**当前主会话**读票、调研、改代码、`challenge` / `close`。

Concrete repo names live only in `~/.agent/tickets/config.yml` (and the user’s words), not in this skill’s trigger text.

## Routing: ticket vs multi-dir mount

**Default for 跨仓委托 / 认领 / 挑战 / 关单:** this skill (Modes 1–3).  
Product multi-dir mounts (Claude `--add-dir`, Codex multi-folder, Cursor multi-root, parent-folder workspaces) are a **tactical** way to keep one semantic edit coherent across checkouts. They do **not** replace the ticket protocol (ownership, `observed`/`assumed`, challenge/reply, allowlist, audit).

| User signal | You do |
| --- | --- |
| 提单 / 跨仓委托 / 有没有我的单 / 认领 / 挑战假设 / 关单 / 派工人 | Modes 1–3 below |
| Same intent must land in 2+ repos in one sitting (shared type rename, co-edited contract) | Allow a **short** product multi-dir session; do not invent a second ticket store; prefer tickets when ownership or challenge is needed |
| Source-repo agent wants to “keep context” by writing the allowlisted target as standing practice | **Refuse that framing** — file/claim on the target (Mode 1/2) or Mode 3 worker on a target worktree |

More visible files are not better cross-repo context for delegation: the target session must load **that** repo’s `AGENTS.md` / `CLAUDE.md`, keep the single-writer lease, and leave a reviewable contract. Policy detail: [`docs/agent-scheduling.md#ticket-vs-multi-dir-mount`](../../docs/agent-scheduling.md#ticket-vs-multi-dir-mount) (from repo root: `docs/agent-scheduling.md#ticket-vs-multi-dir-mount`).

**Skip / redirect:** long exploratory design → interactive TUI / OpenClaw C2 handoff, not a ticket loop.
## Mode 3 only — explicit headless dispatch

```bash
"$D" create … --run [--backend claude|codex|grok]
# = research; if verdict=accept → implement immediately
# if challenge/need_input → stops for initiator

"$D" run --id <id> --phase auto|research|implement
"$D" reply --id <id> --decision "…" --continue   # after challenge (worker-owned only)
"$D" watch --id <id> [--once] [--interval 20]    # blocked initiator loop (worker-owned)
"$D" progress --id <id> [--after N]              # one-shot: progress.json + events
```

**Step feedback (avoid hard-wait silence):** Mode 3 writes `_data/<id>/progress.json` and
`progress` rows into `events.jsonl` at milestones (`research_start` → `research_done` →
`implement_start` → `implement_done`, plus `worktree_ready` / watch kicks). Long invokes also
heartbeat into `progress.json` (default every 15s; `TICKET_PROGRESS_HEARTBEAT_SEC=0` disables).
`watch` prints a JSON tick **each round** with `progress` + `new_events` (stderr human lines).
Initiator agents should **relay those ticks to the user** — prefer `create` then background
`run` + `watch`/`progress` poll when the chat must stay live; sync `create --run` still emits
`[ticket] progress · …` on stderr during the blocked call.

**Run observability (every headless worker run):** `_data/<id>/runs/<run>.{launch.json,stream.jsonl,json}`
— trigger chain (who/which session started it), content-addressed redacted initial prompt
(`prompts/<sha>.md`) + composition (template git blob, phase view), session reuse decision
(`resume` inside one role chain when the cache is warm / history small; one fresh retry if resume
fails), turns · tokens · cache hit · cost · peak RSS. Events get a global `seq`
(`~/.agent/tickets/events.jsonl`). Read it all through `"$D" api …` (JSON, `schema/*.json`):
`health · list · show --id · events --after N · run --run · prompt --sha · transcript --run · metrics --window`.
Agents print `进展：…` lines that stream as `milestone` events. Design + phases:
`docs/collab.md`.

**Multi-repo / multi-worktree work (`collab`):** when one intent needs changes in several repos,
or several independent slices of one repo, the initiating agent writes a contract (interfaces,
order, per-child `scope` globs) and fans it out instead of one long ticket:

```bash
P=$("$D" fanout plan --from . --title "…" --contract /tmp/contract.md | jq -r .id)
A=$("$D" fanout add --parent "$P" --to <repo> --title "…" --observed "…" --assumed "…" --scope 'src/a/**' | jq -r .id)
"$D" fanout add --parent "$P" --to <repo2> --title "…" --depends-on "$A" --scope 'pkg/**'
"$D" fanout run --parent "$P" --detach        # scheduler: caps, path overlap, mem gate, merge + fresh verify
"$D" fanout status --parent "$P"              # children, scheduler pid, integration
```

Children are normal tickets (challenge / reply still apply; rerun `ticket fanout run` after a reply or a
merge-conflict fix). Disjoint scopes in the same repo run in parallel worktrees; overlapping
scopes serialize. Every queue/dispatch/merge/verify decision is an event on the parent.

Policy for **Mode 3**: **no objection after research → start implement**; **objection → human `reply` then continue**. Filing with `--run` means the initiator is blocked — prefer `watch` so work resumes when the ball returns. Use `--mock` offline.

If a ticket is already **session-claimed** (`owner=human`), `run` / `reply --continue` / `watch` **will not** steal the lease unless the user explicitly asks to force headless (`run --steal`). Prefer developing in the claiming TUI.

**Prompt injection (token trim):** workers embed a **phase view**, not the full ticket.
Omit only high-noise / phase-irrelevant sections — **never** the hop’s contract.
Both phases keep Summary + Assumptions; `implement` also gets Verification + Decision
(+ Implement if present). `Thread` / `events.jsonl` stay on disk under `_data/<id>/`
(and `.ticket/ticket.md`) for on-demand Read only.

Headless workers call shared `scripts/dev/host-agent-invoke/` (`write` mode), set
`AGENT_ATTENTION_SKIP=1` / `TICKET_HEADLESS`, and (Claude) `disableAllHooks` so they
**must not** appear in the human attention badge / `Alt+/` list. Scheduling map:
`docs/agent-scheduling.md`.

## Resolve TOOL_HOME (first hit wins)

```text
1. $CROSS_REPO_TICKET_HOME or $TICKET_HOME
2. directory of this SKILL.md if run.sh is co-located
3. $HOME/.agents/skills/agent-collab   # usual after link
4. $WEZDECK_ROOT/skills/agent-collab
5. $HOME/github/wezterm-config/skills/agent-collab
```

```bash
TOOL_HOME=…   # dir that contains run.sh
D="$TOOL_HOME/run.sh"
# If `ticket` is on PATH (install-cli), you may use it; otherwise always $D.
```

**Never** assume the skill lives only under the TARGET repo (TOOL ≠ TARGET).

## One-time (only if missing)

```bash
"$D" init
# optional PATH: "$D" install-cli   # installs short name `ticket`
```

If `~/.agent/tickets/config.yml` lacks the target, add it (path + aliases) before create.

## Agent procedure

### A) Mode 1 — File a ticket (initiator project cwd)

1. Resolve TOOL_HOME; confirm `"$D"` is executable.
2. Infer `--to <allowlist_key>` from the user; use `--from .` when cwd is the source project (or an explicit source key).
3. Write **observed** + **assumed** from the user’s finding (required).
4. Run:

```bash
"$D" create \
  --to <target_key> \
  --from . \
  --title "<short>" \
  --observed "<what you saw>" \
  --assumed "<what target should guarantee>" \
  [--snippet-ref "path:line"] \
  [--summary "…"] [--source-pr "#…"]
```

5. Report the printed `id` to the user. Do **not** commit the ticket into any git tree.  
   Do **not** add `--run` unless the user asked for Mode 3 (委托开发).

### B) Mode 2 — Inbox / claim / develop in this session (receiving project cwd)

```bash
"$D" inbox --to .
"$D" next --to .
"$D" claim --id <id>    # owner=human, mode=session
"$D" show --id <id>
```

`--to .` / `--from .` resolve the allowlist key from cwd via the **primary**
git worktree root (`git rev-parse --git-common-dir`), so a linked worktree
(`…/.worktrees/<repo>/dev-…`) counts as the same repo as the primary checkout —
never as the worktree slug basename.

Read the **full** ticket, then **edit code in the current worktree/TUI**.  
If claim returns lease held → stop; do not dual-write.  
**Do not** call `"$D" run` after a successful session claim.

### C) Mode 3 — Create and ticket development

Only when the user explicitly wants a background worker:

```bash
"$D" create … --run [--backend claude|codex|grok]
# or later:
"$D" run --id <id> --phase auto
"$D" watch --id <id>   # initiator blocked on worker; each round → progress tick
"$D" progress --id <id>  # one-shot snapshot for chat updates
```

While Mode 3 runs, **report milestones to the user** (researching / implement / waiting_initiator /
shipped) from `watch` ticks or `progress` — do not leave them staring at a silent block.

### D) Challenge (target) → reply (initiator)

```bash
"$D" challenge --id <id> \
  --measured "…" --impact "…" --recommended "…" [--needs "…"] \
  [--questions '[{"question":"…","options":[{"label":"…","description":"…"},{"label":"…"}],"multi_select":false}]']
# initiator side:
"$D" reply --id <id> --decision "…" --status waiting_target
# Mode 3 worker-owned only:
"$D" reply --id <id> --decision "…" --continue
```

Session-claimed tickets: after `reply`, the **claiming TUI** continues implement — no `--continue`.

**Structured questions.** When the decision is a choice between concrete options, pass
`--questions` (≤4 questions, 2–6 options each, recommended first; research workers put the same
array in `worker-result.json` `questions`). The initiator taps them on the phone (ticket detail)
and the picks arrive as an ordinary `reply` decision (`问题 → 选项`); `reply` archives them to
`questions-history.jsonl`. `ticket api show` exposes them as `questions` while
`waiting_initiator`. Keep `--needs` as the plain-text version. Open-ended asks: no `--questions`.

**Take over in tmux.** When a tap is not enough:

```bash
"$D" attach --id <id> [--role research|worker] [--select] [--dry-run]
```

resumes the ticket's newest agent session (`sessions.<role>`) in a new window of the target repo's
tmux session via `agent-launcher.sh` + `WEZDECK_RESUME_SESSION_ID` (cwd = ticket worktree, else
the transcript's cwd; research run in a removed temp worktree → target repo main checkout, Claude
transcript copied over). An open ticket is session-claimed (`claimed_by=tmux:<pane>`), so
`reply --continue` / `run` refuse instead of writing into the same conversation. Refuses while a
headless run is in flight (`--force` overrides) or when the repo has no tmux session open.

### E) Close

```bash
"$D" close --id <id> --doc <topic-doc-in-target-repo>
# or explicit skip:
"$D" close --id <id> --no-doc "<reason>"
# keep Mode 3 worktree (rare):
"$D" close --id <id> --no-doc "<reason>" --keep-worktree
```

`close` also reclaims the Mode 3 `ticket-<id>` worktree when `meta.worktree` is set
(strips `.ticket/**`, keeps the local branch). Failure to reclaim does **not** undo close.

### F) Inspect Mode 3 worktrees (decision table)

```bash
"$D" worktrees                 # JSON + stderr skim (suggest/dirty/ahead/age)
"$D" worktrees --alive         # only trees still on disk
"$D" worktrees --to .          # filter by target allowlist key
```

### G) GC leftover Mode 3 worktrees

```bash
"$D" gc --dry-run
"$D" gc --execute --status closed,rejected,failed
"$D" gc --execute --include-shipped --min-age 7d
"$D" gc --execute --force --id <id>   # discard non-.ticket dirt
```

Update/create the **topic solution doc** in the target repo yourself; never commit `~/.agent/tickets/**` into the project.

## Status (authoritative)

`submitted` · `in_progress` · `waiting_initiator` · `waiting_target` · `shipped` · `closed` · `rejected` · `failed`  

`owner`: `worker` | `initiator` | `human`  

- `human` = Mode 2 session claim (main TUI develops)  
- `worker` = Mode 3 headless path  

Use `"$D" next --id <id>` when unsure whose turn it is.

## Don't

- Don’t ask the human to run CLI as the main path
- Don’t commit tickets into project git / `docs/decisions/`
- Don’t invent a second OpenClaw-only ticket store — same skill
- Don’t skip `--observed` / `--assumed` on create
- Don’t close without `--doc` or `--no-doc`
- Don’t start a second claim while a lease is active
- Don’t treat Ticket-headless as C3 ACP (or the reverse); OpenClaw Main picks **执行通道** — see `openclaw/docs/agent-interaction.md` §6
- **Don’t** after `claim` (session) call `run` / spawn `ticket-*` worktree / headless worker
- **Don’t** use `--run` / `run` unless the user asked to 委托 / 后台 / 派工人 (Mode 3)
- **Don’t** replace Modes 1–3 with a standing multi-dir mount from the source repo into the target (“context is better if I edit both”) — tickets own delegation; mounts are tactical same-intent co-edits only

## Tests (operators / CI — not the user path)

```bash
"$TOOL_HOME/test.sh"    # isolated MOCK fs; no LLM; no ~/.agent pollution
```

## Related

- Runner: `run.sh` · lib: `lib/` (`lifecycle.sh` = claim/run/reply; `progress.sh` = watch/progress) · offline: `test.sh`
- Link: `scripts/dev/link-platform-skills.sh`
- Sibling: `adversarial-review`, `brainstorm`
- Scheduling: `docs/agent-scheduling.md` (ticket vs multi-dir: `#ticket-vs-multi-dir-mount`)
