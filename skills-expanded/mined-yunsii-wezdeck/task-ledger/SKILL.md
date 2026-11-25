---
name: task-ledger
description: >
  Ledger development tasks to Feishu Base via dev-task-ledger.sh.
  Write roots from ~/.openclaw/tasks-allowlist.json (per agent). Use on
  accept/confirm/close of coding/ops work; not for pure Q&A.
---

# Development task ledger (Feishu Base)

## Hard rules

1. Development tasks **must** target an **allowlisted** root for the active
   agent (see Path guard / `tasks-allowlist.json`). main → wezdeck|team-repo;
   pm → FE1 (ops). Do not hard-code another machine's `/home/...` in commits.
2. If the user asks for another repo: **do not** `open` a ledger row as accepted
   work; refuse and explain allowlist policy.
3. When accepted, **time loop must close**:
   - `open` → (user confirms plan/初评/开发方式) → **`confirm`** if
     `--confirm-required 1` → work → `close`
   - `close --status done` **fails** if still 需确认 and never `confirm`ed
   - `cancelled` / `blocked` / `failed` may close without confirm
4. Never write secrets into the ledger.
5. Final reply **must** include `task_id`.
6. If CLI fails, say so; do not invent `task_id`.
7. When the request has a clear **需求提出人** (product / user who asked):
   record them on open/update with `--requester-id <ou_…>` (preferred).
   Feishu person field name: **需求提出人**. Do not leave it blank when known.
8. **Order with worktree:** `open` first; after claw worktree exists, `update`
   cwd/分支; after user confirms 初评+开发方式, **`confirm`**; then implement.
9. Pure Q&A: do not open a row. As soon as the user accepts **implementation**,
   open before assess/create (same turn is OK if open is first).
10. **Test hygiene:** after every smoke / CLI self-test that `open`s a row,
    **`delete`** that row (and local index entry). Do **not** leave
    `smoke` / `time-loop` / `*-test` rows in the production Base table.
    Soft `close` is not enough for pure tests — use hard `delete`.

## Path guard

- **Config file (authoritative):** `~/.openclaw/tasks-allowlist.json`
  (from `openclaw/config/tasks-allowlist.json.example`).
- Resolver: `openclaw/scripts/tasks-allowlist.py` (`show` / `check` / `roots`).
- Agent: `OPENCLAW_TASKS_AGENT` or default `main` (paths come from config, not env).
- CLI allowlists **local** `--cwd` / path-form `--repo` only (not remote URLs).
- Base field **`仓库`** = **https web URL** (clickable in Feishu); **`cwd`** = local path.
  CLI rewrites `git@…` / `ssh://…` / `….git` → `https://host/org/repo`.

## CLI

```bash
# from wezterm-config checkout, or $WEZDECK_REPO if set
# --repo: local path (→ origin → https web URL in 仓库) or any git remote form
# --cwd: local path only → Base field cwd
./openclaw/scripts/dev-task-ledger.sh open \
  --title "…" \
  --repo "$HOME/work/team-repo" \
  --cwd "$HOME/work/team-repo" \
  --scope "packages/… or apps/…" \
  --acceptance "pnpm --filter … test" \
  --risk low|medium|high \
  --source feishu \
  --confirm-required 1 \
  --requester-id ou_xxx   # 需求提出人 (Feishu open_id); optional --requester "显示名"

./openclaw/scripts/dev-task-ledger.sh update \
  --task-id <uuid> \
  --requester-id ou_xxx

./openclaw/scripts/dev-task-ledger.sh confirm --task-id <uuid>

./openclaw/scripts/dev-task-ledger.sh close \
  --task-id <uuid> \
  --status done|failed|cancelled|blocked \
  --summary "…" \
  --branch "…" \
  --commits "abc1234" \
  --mr "https://…"

# Hard-delete a row (smoke/test cleanup — preferred over leaving closed test rows)
./openclaw/scripts/dev-task-ledger.sh delete --task-id <uuid>
# or: ./openclaw/scripts/dev-task-ledger.sh delete --record-id recXXXX
```

### Test / smoke cleanup (mandatory)

| After | Do |
| --- | --- |
| Any agent/CLI smoke that called `open` | `delete --task-id …` (or `--record-id …`) |
| Mistaken `open` | `delete`, not only `close --status cancelled` |
| Real work finished | `close` (keep the audit row) |

Do **not** accumulate `*smoke*`, `*time-loop*`, `*-test` titles in Base.

### 需求提出人

| CLI | Base 列 | 类型 |
| --- | --- | --- |
| `--requester-id ou_…` | `需求提出人` | 人员（单选） |
| `--requester "姓名"` | 仅当没有 open_id 时写入 `record_note` 兜底 | 文本 |

- Prefer open_id from Feishu mention / contact lookup.
- Owner who chats with OpenClaw is **not** automatically the requester; set when the asker is named (e.g. product feedback).

Config: `~/.config/shell-env.d/openclaw-tasks.env` (local only; never commit filled file).

## Time fields (Base) — closed loop

All times are **local clock strings with second precision**:
`YYYY-MM-DD HH:MM:SS` (from `date '+%Y-%m-%d %H:%M:%S'`).

In Feishu Base, **开始时间 / 确认时间 / 结束时间 must be 文本 (text)**, not
`datetime`. Feishu `datetime` display formats only go to the **minute**
(`yyyy-MM-dd HH:mm` max) — there is no `…:ss` enum — so a date-only or
datetime column will drop seconds (or show only the day). Text keeps the
full string the CLI writes.

| Column | When set | Meaning |
| --- | --- | --- |
| **开始时间** | `open` | Ledger row created / task accepted into the table |
| **需确认** | `open` true if `--confirm-required 1`; **unchecked after `confirm`** (or false from open if `0`) | **Live gate only** — still waiting for plan/初评/开发方式 yes. Not history. Not 验收/merge |
| **确认时间** | `confirm`, or `open` when confirm-required=0 (same as 开始时间) | User approved plan / 初评 / 【开发方式】 |
| **结束时间** | `close` | **Ledger closed** (`done`/`failed`/`cancelled`/`blocked`) — **not** auto PR-merge time |

**需确认 after confirm:** clearing the checkbox is correct. “Was confirmed” is recorded by **确认时间** (non-empty), not by leaving 需确认 checked.

**开始时间 vs 确认时间:** they are **not** always equal.
- Default (`--confirm-required 1`): open writes 开始时间; later `confirm` writes 确认时间 → usually **later**.
- `--confirm-required 0`: no gate → 确认时间 **=** 开始时间 at open.
- Do **not** reuse 需确认 for 待验收 / 待 merge; put that in 结果摘要 / MR / 状态.

**结束时间 ≠ PR merge 时间。**  
- 结束时间 = 在台账上结案的时刻（agent 跑 `close` 的秒级时间戳）。  
- PR/MR 用字段 **`MR`**（链接）+ 可选摘要说明 merge；若以后要单独记 merge 时刻，再加列，不要占用 结束时间。

## Flow

1. Path guard → allowlist (团队仓 | wezdeck).
2. `open` → writes **开始时间** + **需确认**; capture `task_id`.
3. Plan / worktree 初评 + 【开发方式】→ user yes → **`confirm`**
   (writes **确认时间**, 需确认=false, 状态=in_progress).
4. Create/reuse **`claw-*` worktree**; `update` ledger **cwd** (local) + **分支**;
   **仓库** stays remote URL.
5. Implement (B/C/E/A); main still owns close.
6. `close` → **结束时间** + 终态; `done` requires prior confirm when required.
7. **Ask** reclaim (never auto).
