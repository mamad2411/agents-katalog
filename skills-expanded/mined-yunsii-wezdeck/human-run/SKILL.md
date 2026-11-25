---
name: human-run
description: >
  Mandatory handoff when a human (not the agent) must run a script/command.
  Agent loads this skill, ensure-env, emits staged chat (preparing → ready with
  peek header → after-run), propose.sh --no-wait then wd-run wait, then
  continues follow-up itself. Handoff script bodies must be non-blocking
  kickoffs (trigger/async ack) — never wait for CI/deploy inside x. Never paste
  multi-line scripts into chat. Agent self-exec is out of scope. Use when you
  would otherwise ask the user to paste/run a script, or the command needs TTY
  / host secrets / out-of-sandbox privileges.
---

# human-run (platform skill — single source)

**Who runs the script:** the **human**, via shell command `x`.  
**Who prepares it:** the **agent**, via this skill’s `ensure-env.sh` + `propose.sh`.  
**Never** paste a multi-line script into chat as the execution channel.  
**Never** wrap agent self-exec through this skill — tools already run those.

Runtime CLI lives in the same wezdeck tree as this skill:
`scripts/runtime/cli/{wd-run,x}` + `agent-run-lib.sh`.  
Docs: `docs/agent-run.md`. Profile: `agent-profiles` → `reporting.md`.

## Who runs what

| Actor | Duty |
| --- | --- |
| **Human** | In a real terminal: `x` (peek → Enter=run / other=cancel → run in recorded cwd) |
| **Any agent** | **Load skill → ensure-env → 会话①准备中 → propose --no-wait → 会话②就绪(复述 peek 头) → wait → 会话③结果** |
| **Agent tools** | Self-runnable work — do **not** call this skill |

## When to load (mandatory)

Load whenever **any** of these is true:

- You are about to ask the human to run / paste / copy a shell script or multi-line command
- The command needs a real TTY, GUI, host secret the agent must not hold, or privileges outside the agent sandbox
- The human must read and approve the exact script before it runs

**Do not load** when you can run it with tools, or when the snippet is illustrative only (mark 勿粘贴执行).

## Resolve TOOL_HOME

```text
1. directory of this SKILL.md (follow symlinks; ~/.agents/skills/human-run → …)
2. $HUMAN_RUN_HOME if set
3. else fail — re-run link-platform-skills.sh from a wezdeck that has human-run

The source checkout may be declared explicitly with `WEZDECK_REPO=/absolute/path`.
Do not use the logical `~/.agents/skills/human-run` path to derive the repo root.
```

## Environment check + init (mandatory first step)

**Do not** hand-roll path guessing in the chat. Always:

```bash
TOOL_HOME="$(readlink -f "${HUMAN_RUN_HOME:-$HOME/.agents/skills/human-run}")"
"$TOOL_HOME/ensure-env.sh"
```

`ensure-env.sh` is idempotent. It:

1. Verifies this skill’s wezdeck tree has `wd-run` / `x` / `agent-run-lib.sh`
2. If `$WEZDECK_REPO/scripts/runtime/cli` lacks them, **symlinks** from the skill tree (so `wezdeck-env` PATH and human `x` work even when that clone’s HEAD is behind)
3. Writes/updates `~/.wezterm-x/agent-tools.env` with a working `wd_run=`
4. Smokes the binary; prints the absolute `wd-run` path on stdout

If ensure-env fails → **fail closed** (report the ensure-env stderr). Do **not** paste scripts into chat.

## Script body contract (non-blocking kickoff)

`x` only covers the **human-gated moment**. The script must finish quickly so
`wd-run wait` returns and **you** resume ownership of the long tail.

| Put in the `x` script | Keep out of the `x` script (agent after wait) |
| --- | --- |
| Trigger / fire-and-forget (start deploy, enqueue job, open privileged CLI that submits then exits) | Poll CI / pipeline / rollout until green |
| Print a clear “triggered” ack + any id/url the agent will need | `sleep` loops, `gh run watch`, `kubectl rollout status` waits |
| Fail fast if trigger rejected | Multi-stage verification the agent can do with tools |

**Rule:** prefer async trigger + exit 0 once accepted. If a tool has sync vs async
modes, choose async for the handoff body. After wait returns,
the agent polls / verifies / retries with its own tools.

Anti-patterns (do **not** ship in handoff body):

```bash
# BAD — blocks the human and the agent's wait on CI
gh run watch "$id" --exit-status
while ! curl -fsS "$health"; do sleep 5; done
```

```bash
# GOOD — trigger only; agent continues after wait
gh workflow run deploy.yml -f ref=…
echo "triggered workflow=deploy.yml"   # agent scrapes / lists runs next
```

## Agent procedure (staged — mandatory)

Do **not** ask the human to run `x` before HEAD holds this handoff.
A single `propose --wait` call cannot insert the ready chat line between write
and block — **split** propose and wait so session② can fire.

1. **Decide** this is human-only (if you can self-run → do that; skip this skill).
2. **Split the work:** handoff body = non-blocking kickoff; post-wait = agent-owned follow-up.
3. **Ensure env:** `"$TOOL_HOME/ensure-env.sh"` (required). Tool-only; do **not** tell the human to run `x` yet.
4. **Choose cwd** — existing directory; never omit `--cwd`.
5. **Require a human-readable `--summary`** (≤80, title the human will see in `x` peek). Do **not** omit it and rely on body-first-line fallback.
6. **会话① 准备中（硬要求，在 propose 之前）** — 独立可见一行；**禁止**在此阶段说「请跑 `x`」：

   ```text
   ⏳ 正在准备人工执行脚本：{summary}（写入中，先不要跑 x）。
   ```

7. **Propose without waiting:**

   ```bash
   "$TOOL_HOME/propose.sh" --no-wait \
     --cwd "/abs/workdir" \
     --actor "${AGENT_NAME:-agent}" \
     --summary "short human title ≤80" \
     --stdin <<'EOF'
   # non-blocking kickoff only
   EOF
   ```

   Capture stdout `id=…`. stderr prints an `agent-run: ready` block whose fields
   match the `x` peek page header (`id` / `status` / `actor` / `cwd` / `summary`).

8. **会话② 已就绪（硬要求，在 wait 之前；唯一允许说跑 `x` 的时机）** — 复述 peek 页眉，**不要**贴脚本正文：

   ```text
   ⏸ 脚本已就绪，跑 `x` 时你会先看到：
     id:      {id}
     status:  pending
     actor:   {actor}
     cwd:     {cwd}
     summary: {summary}
   请在本机终端运行 `x` 预览正文后回车执行；其它键取消。我这边挂起等待。
   若终端 peek 头与上表不一致（尤其 id / summary），先取消、勿回车。
   ```

   禁止只把「跑 `x`」写进工具描述 / 内部备注而不出现在对用户可见的会话正文。
   不依赖 attention 徽章或其它 UI 角标来传达「在等你」。

9. **Wait** for that id (short human action timeout — minutes, not CI duration):

   ```bash
   WD_RUN="$("$TOOL_HOME/ensure-env.sh")"
   "$WD_RUN" wait --id "$id" --timeout 600
   ```

   Or: `propose.sh` without `--no-wait` only when the host cannot split tool
   calls — then session① must say「就绪前不要跑 x」, and you accept that
   session② cannot appear mid-flight (race-prone; avoid).

10. **会话③ 结果 + continue** — scrape `agent-run: done id=… status=… exit=…`
    from wait stderr when present:

    ```text
    ✓ `x` 已完成（summary={summary} · id={id} · exit={n}）。接下来我会…
    ✗ `x` 未执行成功（summary={summary} · id={id} · reason={cancelled|superseded|timeout|exit n}）。…
    ```

    Then handle CI/status/verification with tools. Do not ask the human to sit
    in `x` until a pipeline ends.

## Don't

- Don't tell the human to run `x` before propose has written HEAD (session① must not say 请跑 x)
- Don't start wait without a prior user-visible session② that restates the peek header
- Don't omit `--summary` or use a cryptic body-first-line as the title
- Don't put long waits / CI watches inside the handoff script body
- Don't paste multi-line runnable scripts into chat (including as “preview”)
- Don't skip `ensure-env.sh` / `propose.sh` and call a guessed `wd-run` path
- Don't `propose` work you can run with tools
- Don't omit `--cwd`
- Don't ask the human to run `wd-run` as the primary path — that is `x`
- Don't confuse shell `x` with WezTerm **`Alt+x`**

## Related

- `ensure-env.sh`, `propose.sh`, `lib/resolve-wd-run.sh` (this dir)
- Runtime: `scripts/runtime/cli/wd-run`, `scripts/runtime/cli/x`
- Docs: `docs/agent-run.md`
- Install links: `scripts/dev/link-platform-skills.sh`
