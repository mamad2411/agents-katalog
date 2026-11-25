---
name: propose
description: "用户触发 /ezfl:propose 或要求基于 pre_design.md 生成 OpenSpec 四件套时必须使用本 skill。本 skill 串接三件事：(1) 在入口提示用户决策是否创建 worktree（非阻断）；(2) 定位并校验 design 阶段产出的 pre_design.md（缺失时回退用用户原始 prompt）；(3) 由主代理 inline 调用 /opsx:propose，并做出口合规校验。是 design → lock 之间的唯一承接点，且兼任 worktree 决策入口。"
---

# propose

<HARD-GATE>
- **禁止**未读取或未确认 `pre_design.md` 的存在/内容就调用 `/opsx:propose`
- **禁止**跳过 worktree 提示直接进入 propose 主流程（提示是非阻断的：用户可选不创建并继续，但**不能不问**）
- **禁止**主代理在调用 `/opsx:propose` 之前未 `read_file templates/tasks-template.md`
- **禁止**通过 `superpowers:using-git-worktrees` 创建 worktree——必须由本 skill Step 1.3.A 直接执行 git 命令完成
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: propose — 使用 easy-flow:propose skill。`

## 流程（按顺序执行，每一步未完成不得进入下一步）

### Step 0：定位 change_id

读取 `.harness/workflow.yaml: active_changes`，筛选 `phase=design` 的 entry：
- **唯一匹配**：直接取其 `change_id`
- **多个匹配**：用 `ask_followup_question` 列出所有候选让用户选择
- **零匹配**：阻断，提示"未找到 design 阶段的 active change，请先执行 /ezfl:design"

### Step 1：Worktree 决策（提示性，非阻断）

**1.1 前置自检**：读 `.harness/changes/<change_id>/state.yaml: worktree.created_by_easy_flow`。已存在非空值 → 跳过本步，输出 `[easy-flow] worktree: 已决策（<...>），跳过本次询问。` 后进入 Step 2。

**1.2 询问用户**（统一文案，不按 tier 区分）：

> 即将进入 propose 阶段，会落盘 OpenSpec 四件套并改动仓库。是否为本次变更建立独立的 git worktree？
>
> A. 是，创建 worktree
> B. 否，留在当前工作目录

#### 1.3.A 用户选 A — 创建 worktree（脚本执行）

```bash
PLUGIN_ROOT="$(cat .harness/.cache/.plugin_root)"
main_repo_root="$(git rev-parse --show-toplevel)"
WT_RESULT=$(bash "$PLUGIN_ROOT/hooks/worktree-create.sh" "$change_id" "$main_repo_root")
WT_EXIT=$?
```

- exit 0 → `$WT_RESULT` 含 JSON(`target_path` / `target_branch` / `snapshot_path`)；继续下方 workflow 更新
- exit 1 → **阻断**，stderr 有错误信息

**同步主仓 workflow.yaml**(脚本内含锁/写后校验,见 H12):

```bash
bash "$PLUGIN_ROOT/hooks/workflow-entry.sh" update-active --skill propose \
  --where-change-id "$change_id" --set phase=propose --set worktree-path="$target_path"
```

输出 `[easy-flow] worktree: created at <target_path> on branch <target_branch>`。

#### 1.3.B 用户选 B — 留在主仓库

不动 git。更新主仓 `.harness/changes/<change_id>/state.yaml`：写 `worktree.created_by_easy_flow: false`、`current_verb: propose`。同步 workflow.yaml(phase 切到 propose,worktree_path 仍为空):

```bash
bash "$PLUGIN_ROOT/hooks/workflow-entry.sh" update-active --skill propose \
  --where-change-id "$change_id" --set phase=propose
```

输出 `[easy-flow] worktree: not created, staying in <cwd>`。

### Step 2：定位并校验 `pre_design.md`

**2.1 定位**：worktree 模式（1.3.A）下取 `<target_path>/.harness/changes/<change_id>/pre_design.md`；主仓模式（1.3.B）下取 `<main_repo_root>/.harness/changes/<change_id>/pre_design.md`。

**2.2 文件存在性 + 完整性**：

| 情况 | 处理 |
|---|---|
| **文件不存在** | fallback：把用户调用 `/ezfl:propose` 时的原始消息作为 propose 输入；输出 `[easy-flow] 未找到 pre_design.md，使用用户原始 prompt 作为 propose 输入。` 后跳到 Step 3.2 |
| **文件存在** | 调 `bash "$PLUGIN_ROOT/hooks/pre-design-validate.sh" <pre_design_path>`(8 节必含清单与 `templates/pre-design-template.md` 同源):exit 0 通过 / exit 2 缺节(stderr 已含统一阻断话术) / exit 1 文件不存在(理论不会命中) |

**2.3 用户最终确认**（防御性，防陈旧 pre_design.md）：完整路径下输出预览 + 询问 `A. 确认 / B. 暂停回到 design`，仅 A 进入 Step 3。

### Step 3：调用 `/opsx:propose`

**3.1 强制前置**：调用前必须 `read_file templates/tasks-template.md` 并显式输出 `[easy-flow propose] 已 read_file templates/tasks-template.md（version: <模板顶部第一行>）`。

**3.2 组装输入**：完整路径 → `pre_design.md` 全文整段嵌入（不要总结）；fallback 路径 → 用户调用时的原始消息。

**`pre_design.md` 节 → OpenSpec 四件套映射**（仅完整路径适用）：

| `pre_design.md` 节 | 写入位置 |
|---|---|
| `## Reframe 历程` | `proposal.md` 的 "Why / Context" 节 |
| `## Constitution Alignment` | `design.md` 的 `## Constitution Alignment` 节（逐条对齐 Core Principle） |
| `## Premises` | `design.md` 的 `## Premises` 节 |
| `## Decisions`（架构 + 技术选型） | `design.md` 的 `## Decision` / `## Architecture` 节 |
| `## Alternatives` | `design.md` 的 `## Alternatives` 节 |
| `## 任务范围 / Scope` | `tasks.md` 任务划分的范围依据 |
| `## Open Questions` | `proposal.md` 的 `## Open Questions` 节 |

`tasks.md` 严格按 `templates/tasks-template.md` 规则生成；`change_id` 来自 Step 0 定位结果。

**3.3 执行**：主代理在自己会话内调用 `/opsx:propose <change_id>`，把 3.2 的输入作为命令上下文。

### Step 4：出口校验

> fallback 模式（用户原始 prompt 作输入）下若 propose 未生成第 2/3/4 项要求的节，可放宽不阻断、仅在摘要中标记 `(fallback)`。

`/opsx:propose` 返回后校验：

1. 四件套均生成：`openspec/changes/<change_id>/` 下含 `proposal.md` / `design.md` / `specs/` / `tasks.md`
2. `design.md` 含 `## Constitution Alignment` 节，且逐条覆盖 Core Principle
3. `design.md` 含 `## Alternatives` 节，逐条说明未选方案及拒绝理由
4. `design.md` 含 `## Premises` 节
5. `tasks.md` 合规检查(**必须跑脚本,禁止脑补核对**):

```bash
PLUGIN_ROOT="$(cat .harness/.cache/.plugin_root)"
LINT_RESULT=$(bash "$PLUGIN_ROOT/hooks/tasks-lint.sh" "openspec/changes/$change_id/tasks.md")
LINT_EXIT=$?
```

   exit 0 → 通过;exit 1 → **阻断**,输出 `$LINT_RESULT`(JSON violations),要求修正 tasks.md 后重新跑本校验
6. 本 skill 在调用前已显式输出 "已 read_file `templates/tasks-template.md`" 声明

校验通过 → 输出 `[easy-flow] propose 完成：四件套已落盘到 openspec/changes/<change_id>/。下一步建议 /ezfl:lock。`；任一项不满足 → 阻断并输出失败原因。
