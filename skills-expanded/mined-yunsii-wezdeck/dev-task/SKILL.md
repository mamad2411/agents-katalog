---
name: dev-task
description: >
  Allowlisted development (wezdeck (+ optional team roots in local config)) under OpenClaw: wezdeck defaults
  to primary master; claw worktrees when parallel/isolation needed; 团队仓
  still prefers claw-*; human/Claw rails (H1/H2, C1/C2/C3), ACP access layer.
---

# Dev task (allowlisted repos)

## When

Write work only under allowlist (see `AGENTS.md`). Pure Q&A: skip. Other repos: refuse.

| Logical | Roots |
| --- | --- |
| 团队仓 | `$HOME/work/team-repo`, `$HOME/work/.worktrees/team-repo` |
| wezdeck | `$HOME/github/wezterm-config` (primary), optional `.worktrees` |

## cwd policy (L0-12/13)

**Core:** personal projects → default mainline. **wezdeck** is the local instance.

| Repo | Default | Worktree when |
| --- | --- | --- |
| **wezdeck** (personal) | **primary `master`** | parallel, long experiment, isolated agent cwd, user asks |
| **团队仓** (team-ish) | **claw-\*** under `dirname(primary)/.worktrees/<repo>/` | default isolation unless user overrides |

Path formula (when used): `dirname(realpath(primary))/.worktrees/<basename(primary)>/<slug>/`.

Architecture: `openclaw/docs/agent-architecture.md`.

## Checklist

Same steps as `AGENTS.md` Write-task checklist (wezdeck may skip assess/create).
Scripts: `dev-task-ledger.sh`, `claw-worktree.sh`, `claw-run.sh`.

## Assess → create (only when isolation/parallel needed)

```bash
./openclaw/scripts/claw-worktree.sh assess \
  --title "<subject>" --domain "<area>" --scope "<hint>" [--days N] \
  --cwd "$HOME/github/wezterm-config"
./openclaw/scripts/claw-worktree.sh create \
  --title "…" --lifecycle task|dev|hotfix --domain "…" \
  --cwd "$HOME/github/wezterm-config"
```

- Prefer-reuse same domain; never human `dev-*`/`task-*` as write targets.
- **Reclaim never automatic** after close (only if a worktree was used).

## Rails & modes (user-facing)

| 轨 | 方式 | 旧 | Who codes | Main does |
| --- | --- | --- | --- | --- |
| 人工 | H1 人直接 | A | User IDE | Ledger/验收 only |
| 人工 | H2 原生 Agent | A | Host grok/claude/codex | Assist only |
| Claw | C1 Main 自写 | B | Main (Main-Grok) | Implement + verify |
| Claw | C2 Handoff | C | Host CLI after handoff | **Stop coding** that cwd |
| Claw | C3 ACP 后端 | E | ACP → claude \| codex | Spawn/close; single writer |
| Claw | Ticket-headless | — | `ticket` host headless | 跑同一 skill `agent-collab`；票在 `~/.agent/tickets/` |
| — | D | D | — | **Forbidden** |

**ACP** = access layer only; backends are Claude/Codex. No `spawn grok`.
**Ticket-headless** = 跨仓契约工人（research→implement），不是 ACP 会话；不要另建 OpenClaw 私有票库。
Do not rewrite host `~/.codex` / `~/.grok` defaults when fixing ACP
(use `~/.openclaw/acpx/codex-home` for ACP Codex).
选型：`docs/agent-scheduling.md`（平台）+ `openclaw/docs/agent-interaction.md` §6（Claw 交互细节）。

### Handoff (C2)

```text
## Handoff
- task_id / cwd / branch / goal / non-goals / acceptance
- 开发方式: C2 本机原生 handoff（C）
- constraints: no force-push; no push main without yes
- after: 本机做完 → 飞书摘要 → main close + reclaim ask
- 本机: cd <cwd> && claude --continue
```

## 开发方式推荐卡（必发）

**Full names required** (never bare "Codex"/"Claude" alone):

| Full name | Meaning |
| --- | --- |
| Claude-TUI | host `claude` (H2/C2) |
| Claude-ACP | C3 `agentId=claude` |
| Codex-TUI | host `codex` + `~/.codex` |
| Codex-ACP | C3 `agentId=codex` + isolated CODEX_HOME |
| Codex-Grok-profile | host `codex -p grok` |
| Main-Grok | OpenClaw main model |
| Grok-native | host `grok` CLI |

Before code or ACP, post and wait:

```text
## 开发方式（请抉择）
- 轨: 人工 | Claw
- 推荐: H1 | H2 (Claude-TUI|Codex-TUI|Grok-native) | C1 Main-Grok |
        C2 handoff | C3 (Claude-ACP|Codex-ACP) | Ticket-headless (ticket)
- 执行通道: ACP | Ticket-headless | Handoff/TUI | Main自写
- 执行者 / 后端全名: …
- 理由: …（含限制/degraded；跨仓契约优先 Ticket-headless）
- 备选: …
- 平台约束: 单写者、claw-*、确认前不写码；不改原生默认配置；工单不另建票库
- 审查建议: review-claude × review-grok | 跳过（理由）
- cwd / task_id: …
请确认。确认前不改代码 / 不 spawn ACP / 不 kick ticket implement。
```

Heuristics: **C1** small/clear; **Claude-ACP** multi-file + 飞书 steer; **Ticket-headless**
cross-repo contract / research→implement; **C2/H2** need TUI; **H1** already coding;
**Codex-ACP** explicit Codex stack.

## C3 ACP spawn constitution (prepend to task)

```text
[OpenClaw C3 constitution — non-negotiable]
1. Single writer: only you write this cwd; no parallel Main/TUI on same tree.
2. cwd is the path Main gave (wezdeck may be primary master or claw-*).
3. No force-push; wezdeck may push master per owner policy; other repos need explicit yes.
4. Prefer reasonable logical commits (compress by change boundary; no hard 1–3 cap); no secret leakage.
5. On completion report: changed files, summary, blockers; honest fail if blocked.
6. You are Claude-ACP or Codex-ACP (access layer), not a replacement for host TUI config.
7. Do not participate in the host interactive attention badge (WezDeck Alt+/ ●/▲).
   ACP is delegated; wrappers must set AGENT_ATTENTION_SKIP / OPENCLAW_ACP
   (see `openclaw/scripts/patch-acpx-attention-skip.sh`).
```

Before spawn: reject if cwd missing or outside allowlist. wezdeck may be primary master; 团队仓 usually claw-*.
After C3: prefer structured report `changed_files` / `summary` / `blockers` / `commits`.

Probe: `openclaw/scripts/agent-matrix-status.sh`.

## 实现方案块

Always restate mode even if user named it.

```text
## 理解 / 合理性（批判）
## 实现方案（请确认）
- 最小交付: …
- 可选结构/复用: … | 无
- 影响范围: 代码… | 人… | 团队/流程… | 无额外
- 推荐: 仅最小 | 最小+轻复用 | 先结构后功能（可附内部代号）
```

## 落实 / commits

On 落实: review → implement → verify → 按变更边界整洁提交（数量不强制 1–3）→ push agreed branch → report.
**wezdeck:** default work on **primary master**; after green checks **commit + push `master`** (L0-12/13/20). If a task branch/worktree was used, ff-only into master then push.
Other repos: push main/master only with explicit yes.
Shell via `claw-run` when required by exec-risk.

### Feishu report default (brevity)

- Progress while working: **1–3 lines**, not tool play-by-play.
- Final report: **精简【结果】卡** below by default.
- Do **not** default-paste full acceptance tables, long path lists, full adversarial disclosure, or multi-block bash.
- User says 展开/全文/细节 → then **完整卡**.
- Failures: 4-line closed-loop first (失败/原因/处置/影响).
- Material failure never re-run green → 状态不得为 **成功**.

#### 精简【结果】卡（飞书首条默认）

```text
## 结果
- 状态: 成功 | 失败 | 部分完成
- 一句话: …
- 锚点: <hash> <subject> · 分支… ·（可选 task_id）
- 开发方式: 中文轨+全名后端（如 Claw·C1 Main-Grok）
- 决策动作: 无 | 请确认… | 是否回收 worktree？
- 失败闭环: （仅失败时）失败/原因/处置/影响

细节回「展开」。
```

#### 完整卡（用户要展开/排障时）

```text
## 结果
- 状态: 成功 | 失败 | 部分完成
- 摘要: …（人话；避免只有内部代号）
- task_id: …
- 开发方式: 中文轨+全名后端（如 Claw·C1 Main-Grok / C3 Codex-ACP）
- 仓库 cwd: /absolute/…
- 分支: …
- 最近 commit: <hash> <subject>
- 验收:
  - <cmd> → pass | fail | not run | re-run pass (after …)
- 性能/体验: 未测 | 基线…→现… | 必要开销说明… | 劣化原因与处置…
- 影响范围: 代码… | 人… | 团队/流程… | 无额外
- 宪法同步: 无 L0 变更 | 已同步 agent-profiles | 未同步（须说明）
- 对抗审查: 未做 | 见「对抗审查披露」（默认只写结论+是否阻塞；全文按需）
- 失败记录: 无 | 逐条 失败/原因/处置/影响/结果或备选
- 风险/未做: …

## Worktree
- 类型: task|dev|hotfix · 是否建议回收: … · 请回复是否回收

## 审查 / Resume
- 按**实际开发方式**写主路径：
  - Main 自写（C1）: 飞书本线程（主路径）；可选 cd <cwd> 旁观
  - 本机 handoff（C2）/ 用户自写（H1）: cd <cwd> && claude --continue  # 或 codex resume --last
  - ACP（C3）: 飞书本线程 / ACP 续跑说明（写清 agent 与 cwd）
```

### Git author & trailer (mandatory)

| Rule | Detail |
| --- | --- |
| Author | Always repo owner. wezdeck: `Yuns <yuns.xie@qq.com>`. **Never** bot Author names / `yuns@local`. |
| Do not | `git -c user.name=<bot>` or other bot identity overrides. |
| Trailer | `Assisted-by: OpenClaw (backend=…, model=…)` |
| C1 Main | `backend=main`, `model=<short model id>` e.g. `grok-4.5` (not `grok-proxy/…` unless debugging) |
| C2/C3 write | `backend=<full name>` e.g. `Claude-ACP`, `Codex-ACP` + that backend's model |
| Editorial only | `Assisted-by: OpenClaw (editorial-only)` or omit |
| Integrate | wezdeck already on master → push; else rebase → `merge --ff-only` → push; **no** default `--no-ff` |

Example message:

```text
feat(scope): subject

- bullet why/what

Assisted-by: OpenClaw (backend=main, model=grok-4.5)
```

## Adversarial review (agent runs it)

**Do not** ask the human to run `run.sh`. On review intent or acceptance:

1. **Load** `skills/adversarial-review/SKILL.md`
2. **Run** `$REPO/skills/adversarial-review/run.sh <BASE> --writer <family> --mode strict`
3. **Report** L0-21 disclosure (writer / form / reviewer / refuter / conclusions)

「对抗审查」= multi-role (find+refute minimum). Same agent twice with opposite
stance is OK if labeled SINGLE-MODEL. Solo Main monologue = **设计批判** only.
Writer-aware selection: `--writer main|claude|codex|human` (strategy B).

## Constitution (all agents)

Usage may differ by rail/limits; **criteria do not**: L0, skills, scripts,
single-writer, honest pass/fail, no fake green, secret hygiene, error closed-loop
(`Process failed` / `Exec failed` same-turn plain language).
