---
name: CodexCleanUp
description: 检查当前 Codex 会话是否属于正确的 Project，并在用户选择推荐分组后，使用官方 Codex App 能力在目标 Project 下创建一个带压缩上下文的交接会话。保留原会话、原标题和原归属，不关闭 App，不修改本地私有状态。用户说“整理当前会话”“这个会话该放哪个 Project”“帮我调整分组”“清理 Codex 会话”“codex clean up”“CodexCleanUp”或明确要求把当前会话交接到另一个 Project 时使用。
---

# Codex Clean Up

## Contract

使用“创建交接会话”模型，不使用“原地移动会话”模型。

- 原会话保持原样：不改 Project、标题、内容、归档状态或 pinned 状态。
- 目标 Project 下创建一条新的 Codex 会话，并把当前会话压缩成可继续工作的上下文写入新会话。
- 不关闭 Codex/ChatGPT App，不修改 `~/.codex/.codex-global-state.json`、SQLite 或其他私有状态文件。
- 不删除、归档、fork 原会话；只使用官方 Codex App 工具创建新会话。
- 创建失败、标题更新失败或目标 Project 无法确认时，不声称已完成。

## 可用工具与边界

优先使用当前 Codex App 提供的官方工具：

- `codex_app__list_projects`：读取可创建会话的 Project 及其 `projectId`。
- `codex_app__list_threads`：需要核对近期会话标题时读取摘要；当前 App 版本只传 `limit`，且不超过 50，不要传 `query`，在返回结果中自行筛选。
- `codex_app__create_thread`：在目标 Project 下创建新会话。
- `codex_app__set_thread_title`：创建成功后设置交接标题。
- `codex_app__read_thread`：创建后有线程 ID 时做只读回读验证。

`codex_app__list_projects` 可能同时返回 `projectKind: "chatgpt"` 的云端 Project。它们不是本 Skill 的目标；只选择可由 `codex_app__create_thread` 创建的 Codex local Project，remote Project 只有在工具明确支持对应 target 时才使用。

如果这些官方工具不可用，停止并报告“当前环境无法创建 Project 内新会话”；不要退回私有状态写入方案。

## 工作流

### 1. 只读诊断

先判断当前会话的主题、当前 Project、标题和会话 ID。优先使用当前线程上下文；需要核对时使用 `codex_app__list_threads`。无法确认当前会话 ID 或当前归属时，明确标记为未知，不猜测。

使用 `codex_app__list_projects` 获取最新 Project 列表。结合以下证据评估候选：

- 当前会话主题和目标/产品实体；
- Project 名称、根目录和近期会话标题；
- 当前会话工作目录（只能作为证据之一，不能单独覆盖主题判断）；
- 已知的用户 Project 画像或本轮读取到的项目上下文。

不要因为当前 cwd 落在某个目录，就直接认定该 Project 一定合理。先判断主题是否一致。

如果当前归属合理，只报告合理性和依据，不创建交接会话。

### 2. 候选与用户选择

仅展示推荐度不低于 60 分的候选。

- 最高候选明显领先时，只展示最高候选。
- 分值接近时最多展示 3 个候选。
- 始终提供 `N. 都不是`。
- 使用 `A/B/C/N` 选择，不要求用户重复输入 Project 全名。

输出格式：

```text
当前会话归属：<Project 或未分组>（依据：<证据>）
当前判断：需要创建交接会话

A. <Project> —— <分数>/100
   依据：<具体证据>
   不确定性：<缺失信息>

N. 都不是

回复 A/B/C/N。
```

用户选择 `N` 时停止，不创建会话。用户可以随后直接指定 Project 名称。

### 3. 交接计划与执行

用户选择 `A/B/C` 本身就是对该推荐分组的最终确认，不再要求第二次 `OK`。收到有效选择后，立即生成交接计划并执行创建。计划必须包含：

- 原会话标题、线程 ID、当前归属；
- 目标 Project 名称和将使用的 `projectId`；
- 新会话标题：`迁移｜<原会话标题>`；
- 将写入新会话的压缩摘要；
- 明确说明原会话不会改变。

计划只作为本轮执行前的内部检查；不要因为已经展示过计划，再向用户索要 `OK`。如果用户只回复“可以”“确认”但没有对应的 `A/B/C`，而候选存在歧义，先要求选择候选；如果用户明确指定了唯一 Project 名称，则视为有效选择。

### 4. 生成交接摘要

使用 [handoff-template.md](references/handoff-template.md) 的结构。摘要应足够让新会话继续工作，但不要复制完整 transcript。至少包括：

- 当前目标和问题背景；
- 已确认事实、关键决策和约束；
- 已完成工作与验证证据；
- 未完成事项、风险和下一步；
- 相关文件、路径、线程 ID 或链接；
- 明确区分事实、推断和未知。

摘要开头保留来源信息，便于两边对照：

```text
本会话由 Codex Clean Up 从以下会话交接而来：
- 原会话标题：...
- 原线程 ID：...
- 原 Project：...
- 交接原因：...
```

### 5. 创建目标会话

收到 `A/B/C` 或唯一 Project 名称后，重新调用 `codex_app__list_projects`，按精确 `projectId` 选择目标，避免 Project 改名或列表变化导致误投。

对本机 local Project，调用：

```text
codex_app__create_thread({
  target: {
    type: "project",
    projectId: "<目标 projectId>",
    environment: { type: "local" }
  },
  prompt: "<完整交接摘要>"
})
```

不要使用 worktree，除非用户明确要求新 worktree。对当前工具不支持的 remote Project，不猜测 `environment`，报告无法创建并保持原会话不变。

创建成功返回新线程 ID 后，调用：

```text
codex_app__set_thread_title({
  threadId: "<新线程 ID>",
  title: "迁移｜<原会话标题>"
})
```

标题设置失败时，不删除新线程；如实报告“会话已创建，但标题仍为自动标题”。如果返回了线程 ID，可用 `codex_app__read_thread` 做只读回读；不要为了验证重新创建。

### 6. 原会话回执

在原会话中报告：

- 新会话已创建或明确失败；
- 目标 Project 名称；
- 新会话标题和线程 ID；
- 摘要已写入；
- 原会话仍保留在原位置、原标题和原内容未改动。

只有 `codex_app__create_thread` 成功返回线程 ID 才能说“已创建”。

## 失败处理

- 无法列出 Project：停止，不读取或写入私有状态文件。
- 当前会话或目标 Project 不确定：停止，不猜测。
- 用户未选择候选：只保留诊断结果，不创建。
- 创建工具失败：报告具体错误，原会话不变。
- 创建成功但标题设置失败：保留新会话并报告部分成功，不重复创建。
- 不要把“准备创建”“工具调用已发起”说成“已创建”。

## 禁止事项

- 不执行任何私有状态移动脚本（包括 `move.py`、`rename.py` 或任何 `--confirm` 写入）。
- 不编辑 `.codex-global-state.json`、`state_5.sqlite` 或其他私有状态。
- 不要求用户关闭 App。
- 不修改原会话的 Project、标题、内容、归档或 pinned 状态。
- 不删除原会话，不创建新 Project，不把当前会话的完整 transcript 原样复制到目标会话。
