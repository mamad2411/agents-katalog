---
name: ship
description: "用户触发 /ezfl:ship 或要求 ship / 交付 / 完结一个 change 时必须使用本 skill。执行终验、分支管理、worktree 合回，并询问用户后调用 /opsx:archive 把 OpenSpec change 目录归档。"
---

# ship

<HARD-GATE>
禁止跳过 Step 0(ship lock)。禁止跳过 Step 3.4.5(harness-sync)直接进入 3.5(worktree remove)。禁止未询问用户就执行 /opsx:archive。archive 失败不阻断 ship。
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: ship — 使用 easy-flow:ship skill。`

## 遵守的 Hard Stops

H8(状态行)、H9(worktree 合回必须)、H11(ship lock 串行)。

## 输入

读取 `.harness/workflow.yaml: active_changes` 定位 `change_id` 和 `worktree_path`：
- **唯一匹配**：取其 `change_id`
- **多个匹配**：用 `ask_followup_question` 让用户选择
- **零匹配**：阻断，提示"未找到 design 阶段的 active change，请先执行 /ezfl:design"

读 `.harness/changes/<change_id>/state.yaml`（worktree 模式下从 worktree 内读）：取 `worktree.*`、`audit.*`
- `audit.blocked == true` → **入口阻断**：直接停止本 skill，提示"audit 处于 blocked 状态，请先回到 /ezfl:audit 处理后再 ship"，不进入 Step 1
- `worktree.created_by_easy_flow == true` → 触发本 skill 的 worktree 合回分支

## 执行流程

### Step 0：获取 ship lock（串行保护）

`read_file ./policies/ship-lock.md` 并按其规定在主仓 `.harness/.locks/ship.lock` 上获取互斥锁；失败即阻断 ship。锁内容含 `change_id`、PID、启动时间；`trap EXIT INT TERM HUP` 自动释放；> 30min 视为 stale 由用户显式确认清理（HARD STOP H11）。

### Step 1：终验

调用 `superpowers:verification-before-completion`，等待全部检查通过。

任一检查失败 → 阻断并要求用户修复后重新触发 `/ezfl:audit`（从 audit 重新跑），audit 通过后再回到 `/ezfl:ship`。

### Step 2：分支管理（核心）

调用 `superpowers:finishing-a-development-branch`，让其呈现 PR / merge / cleanup 三选项给用户。等待其返回。

### Step 3：worktree 产物合回 + git 合回 + 清理（仅当本流程创建过 worktree）

**条件**：`state.yaml: worktree.created_by_easy_flow == true`。顺序不可调换：3.1–3.4 判断合并状态 → 3.4.5 产物合回 → 3.5 清理。

#### 3.1 读取 worktree 元信息

从 `worktree` 块取 `path`、`branch`、`origin_repo`。

#### 3.2 脏检查 + 合并状态

```bash
bash "$PLUGIN_ROOT/hooks/worktree-merge-status.sh" "$WORKTREE_PATH" "$ORIGIN_REPO" "$BRANCH"
case $? in
  0) ALREADY_MERGED=1 ;;       # 干净 + 已合并 → 跳到 3.4.5
  1) ALREADY_MERGED=0 ;;       # 干净 + 未合并 → 进 3.3
  2) exit 1 ;;                 # 脏 → stderr 已含阻断话术
  *) exit 1 ;;                 # 参数/环境异常
esac
```

#### 3.3 若未合并：询问用户

通过 `ask_followup_question` 呈现 worktree 路径/分支，并提供三选项：A. 已通过 PR 合并 / 不需本地合并 → 仅清理；B. 本地 rebase 到主干后 fast-forward 合入；C. 暂不处理，保留 worktree。

#### 3.4 选项 B：本地 rebase + ff 合入

```bash
bash "$PLUGIN_ROOT/hooks/worktree-rebase-ff.sh" "$WORKTREE_PATH" "$ORIGIN_REPO" "$BRANCH"
# 退出码: 0=成功 / 1=rebase 冲突(worktree 留中间态,要求用户手动 git rebase --continue 后重跑 /ezfl:ship) / 2=ff merge 失败 / 3=环境异常
```

#### 3.4.5 + 3.5 产物合回 → 清理 worktree（合并执行，不可拆分）

**A/B 共用**（C 跳过整个块）。必须按顺序在同一步执行——先合回再清理：

```bash
# ━━━ 第一步：harness-sync（合回产物到 archive）━━━
PLUGIN_ROOT="$(cat .harness/.cache/.plugin_root)"
SYNC_RESULT=$(bash "$PLUGIN_ROOT/hooks/harness-sync.sh" "$WORKTREE_PATH" "$ORIGIN_REPO" "$change_id")
SYNC_EXIT=$?
# 退出码:0=synced,1=partial_failure,2=archive冲突(弹三选项重调),3=skipped_no_source

# ━━━ 第二步：清理 worktree（仅在第一步完成后执行）━━━
cd "$ORIGIN_REPO"
git worktree remove "$WORKTREE_PATH"
if [ "$ALREADY_MERGED" = "1" ] || git merge-base --is-ancestor "$BRANCH" HEAD; then git branch -d "$BRANCH"; fi
rmdir "$(dirname "$WORKTREE_PATH")" 2>/dev/null || true
```

- SYNC_EXIT=2 → 先弹三选项重调脚本解决冲突,再继续第二步
- worktree remove 失败 → 提示用户 `git worktree remove --force`
- **禁止跳过第一步直接执行第二步**

#### 3.6 选项 C：保留 worktree

不执行 3.4.5/3.5。标注 `worktree.status: abandoned`、`ship.harness_sync: skipped_worktree_retained`，提醒用户后续清理前先手动合回产物。

### Step 4：状态写入

更新 `.harness/changes/<change_id>/state.yaml`（worktree 模式下写 worktree 内的；非 worktree 模式下写主仓的；档案的归档与游标移除由 Step 6.1 完成，本步**不在此处删除**——Step 5/6 仍需 change_id）：

```yaml
ship:
  status: "shipped"
  finished_at: "<ISO>"
  merge_strategy: "<rebase-ff|pr-only|abandoned>"
  harness_sync: "<synced|partial_failure|skipped_no_source|skipped_worktree_retained|deferred_archive_conflict|n/a>"
  archive_dir: ".harness/archive/<change_id>"   # 仅 harness_sync ∈ {synced, partial_failure} 时有值
worktree: { status: "<merged|abandoned>" }   # 仅 created_by_easy_flow=true 时更新
current_verb: idle
```

`harness_sync = "n/a"`：本次未创建 worktree，无需合回。

### Step 5：调用 `/opsx:archive` 归档（强制询问，主代理直接执行）

**前提**：本步在 Step 4 写入 `ship.status=shipped` **之后**执行——这样即使 archive 跳过或失败，已完成的 ship 状态不会丢失。

#### 5.1 询问用户是否归档

通过 `ask_followup_question` 呈现当前 `change_id` 与 `ship.status=shipped` 状态，并提供三选项：A. 立即归档（推荐）；B. 暂不归档（PR 仍在 review / 中途暂停后续手动）；C. 跳过归档（实验性变更）。归档将把 `openspec/changes/<change_id>/` 移动到 `openspec/changes/archive/YYYY-MM-DD-<change_id>/`。

#### 5.2 用户选 A — 主代理执行 `/opsx:archive`

```bash
openspec-cn archive "$change_id" --yes
```

加 `--yes` 跳过 openspec 内部的 confirm 交互。**archive 失败(exit ≠ 0) → 立即阻断 ship**,输出错误信息,禁止继续进入 Step 6。

#### 5.3 归档结果处理

| archive 返回 | 处理 |
|--------------|------|
| `Archive Complete` | 记录 `ship.archive = "archived"`、`ship.archive_path = "<archived path>"`；进入 Step 6 |
| `Archive Complete (with warnings)` | 同上,但额外把警告追加到 Step 6 摘要 |
| exit ≠ 0 / 任何错误 | **阻断**：输出 `[easy-flow] 阻断：archive 失败,ship 中止。` + 错误信息,等待用户排查后重试 `/ezfl:ship` |

#### 5.4 用户选 B / C — 跳过归档

- 选 B（暂不归档）→ 记录 `ship.archive = "deferred"`，提示用户"完成后手动执行 `/opsx:archive <change_id>` 完成归档"
- 选 C（跳过归档）→ 记录 `ship.archive = "skipped"`，无后续提示

`changes/<change_id>/state.yaml` 追加：`ship: { archive: "<archived|deferred|skipped|failed>", archive_path: "<仅 archived 时有值>", archive_error: "<仅 failed 时有值>" }`

### Step 6：交付摘要输出

```
[easy-flow] ship 完成：

  change_id     : <change-name>
  tier          : <tier>
  分支          : <feature/...>
  worktree      : <已合回并清理 / 已保留 / 未创建>
  harness 产物  : <已合回主仓 .harness/archive/<change_id>/ | 未合回（worktree 保留）| 部分失败：<失败项> | n/a>
  audit 总分    : <X>/100
  涉及文件数    : <N>
  archive       : <已归档于 <archive_path> | 已延迟（用户选 B）| 已跳过（用户选 C）| 失败：<archive_error>>

后续：可以直接进行下一个 `/ezfl:design`；或 `/ezfl:reflect` 查看本次度量（含本次合回的 metrics）。
```

#### 6.1 主仓游标重置 + 清理（必做）

摘要输出后调用 `ship-cleanup.sh`（删 active_changes entry + rm -rf changes/<id>{,.snapshot}）：

```bash
bash "$PLUGIN_ROOT/hooks/ship-cleanup.sh" "$change_id" "$ORIGIN_REPO" || exit 1
```

输出 `[easy-flow] workflow: entry removed, active changes: <N>`。
