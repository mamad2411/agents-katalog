---
name: dev-memory-setup
description: 把 unsorted.md 里未分类内容整理到结构化文件。触发词："整理 dev-memory"、"初始化 dev-memory"、"记忆规整下"。
---

# Dev Memory Setup

在 v2 里，setup **不再是前置门禁**。任何 `dev-memory-capture` 写入都会自动把骨架建起来，内容先落到 unsorted.md（如果 heuristic 不确定）或直接落到对应分类文件。

Setup 的新职责是一个 **promotion 动作**：

1. 读 unsorted.md 里 lazy init 期间积累的未分类条目
2. 和用户一起按 decisions/progress/risks/glossary 分类
3. merge 到目标文件，清空 unsorted.md
4. 收集仍然缺的元信息（目标、范围、阶段、约束、源资料入口）
5. 标 `manifest.setup_completed = true`，此后 capture 的 heuristic 默认从 unsorted 兜底切到 progress 兜底

**Workspace mode：** 始终针对单个仓库。cwd 是多 repo workspace 时，必须通过 `--repo <basename>` 明确指定目标仓库。

**Announce at start:** 用一句简短的话说明将先扫 unsorted 条目展示给用户，再分类 merge 到结构化文件。

## DO / DON'T

**Do:**

- 用户明确说"整理一下 dev-memory"、"初始化 dev-memory"、"规整下这个仓库的记忆"
- `context show` 显示 `setup_completed=false` 且 `unsorted.md` 有 ≥5 条内容
- unsorted.md 累积 ≥20 条时 SessionStart 主动提示过一次，用户确认要整理

**Don't:**

- 已 setup 且 unsorted.md 空（没东西可 merge）
- 批量给多个仓库无差别 setup（必须 `--repo <basename>` 明确一个）
- 用户只是要写一条内容（那是 capture 的职责，不是 setup）
- 把原本该直接分类的内容硬塞进 unsorted —— setup 不是中转站

## Workflow

### Step 1: init（永远安全，幂等）

```bash
npx dev-memory-cli setup init \
  [--repo <repo-path>] [--branch <branch-name>]
```

输出里包含：
- `unsorted_entries`：unsorted.md 当前的条目列表
- `unsorted_count`：条数
- `setup_completed`：当前 setup 状态
- `files`：所有路径

### Step 2: 和用户一起分类

把 `unsorted_entries` 列给用户，让用户说每条进哪个分类（或 skip）。如果 LLM 能高置信度分类，主动 propose，用户只需确认/修正。

支持的 kind（和 capture 的 KIND_MAP 对齐）：

| Kind | 去哪里 |
|---|---|
| `decision` | branch/decisions.md "关键决策与原因" |
| `progress` | branch/progress.md "当前进展" |
| `next` | branch/progress.md "下一步" |
| `risk` | branch/risks.md "阻塞与注意点" |
| `glossary` | branch/glossary.md "当前有效上下文" |
| `source` | branch/glossary.md "分支源资料入口" |
| `shared-decision` | repo/decisions.md "跨分支通用决策" |
| `shared-context` | repo/glossary.md "长期有效背景" |
| `shared-source` | repo/glossary.md "共享入口" |
| `skip` | 丢弃（比如过时 / 没价值的条目） |

### Step 3: 生成 plan.json 写 merge

plan.json 格式：

```json
{
  "classifications": [
    {"entry": "原条目文本", "kind": "decision"},
    {"entry": "另一条...", "kind": "shared-context"},
    {"entry": "过时了...", "kind": "skip"}
  ],
  "clear_unsorted_on_done": true
}
```

运行 merge：

```bash
npx dev-memory-cli setup merge-unsorted \
  --plan-file /tmp/dev-memory-merge-plan.json \
  [--repo <repo-path>]
```

执行后：
- 条目按 kind 分组 append 到目标 section
- unsorted.md 重置为空模板（默认 `clear_unsorted_on_done=true`）
- `manifest.setup_completed = true`

### Step 4: 补缺失元信息

setup 之后仍可能有空模板，走 capture 填：

- `--kind overview` → 当前目标
- `--kind scope` → 范围边界
- `--kind stage` → 当前阶段
- `--kind constraint` → 关键约束
- `--kind shared-source` → 共享源文档入口

### 只标完成不整理（极简路径）

如果 unsorted 是空的，但你想切换默认分类策略（从"不确定 → unsorted"切到"不确定 → progress"），直接跑：

```bash
npx dev-memory-cli setup mark-completed \
  [--repo <repo-path>]
```

## Intake Rules（问用户时的原则）

- 主动问用户要源文档或链接，不要让用户把整份文档手打一遍
- branch 层只留当前分支有效记忆
- repo 层只留跨分支共享资料和长期背景
- 零散信息整理成当前有效摘要再写

## Always / Never

**Always:**

- 先跑 init 看 unsorted_entries
- merge 时尊重用户选择的分类，不擅自修改
- setup_completed = true 后告诉用户 heuristic 兜底已切换

**Never:**

- 拒绝写入（v2 capture 永远 lazy init；如果 setup 没跑过，capture 会用 unsorted 兜底）
- 继续复制整份 prd/review/frontend/backend/test 正文
- 把仓库工作区当成本地记忆主目录
