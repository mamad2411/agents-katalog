---
name: tt-worker
description: "读取滴答清单任务池中的任务并自动执行。触发词：执行任务池、tt-worker、处理待办、跑任务池、自动执行。"
---

# tt-worker

读取滴答清单「任务池」中的任务，根据 tag 自动执行。

> **IMPORTANT**: 执行前必须先读取 `references/task-format.md` 了解任务格式规范。

<gsd:workflow>
  <gsd:meta>
    <name>tt-worker</name>
    <trigger>执行任务池、tt-worker、处理待办、跑任务池、自动执行、处理池子</trigger>
    <requires>tt CLI (npm install -g @wangjs-jacky/ticktick-cli), Bash</requires>
    <checkpoints>
      <checkpoint order="0">tt CLI 可用且已登录，任务池清单存在</checkpoint>
      <checkpoint order="1">任务列表读取完成，确认执行范围</checkpoint>
      <checkpoint order="2">每个任务执行前后记录状态</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>Phase 0 必须首先执行，检测 tt CLI 和任务池清单</constraint>
      <constraint>只从「任务池」清单读取任务，不读其他清单</constraint>
      <constraint>单次最多执行 maxTasksPerRun 个任务（默认 5，可在 config.json 配置）</constraint>
      <constraint>单个任务超时 taskTimeoutMinutes 分钟（默认 30），超时保留进度不标记完成</constraint>
      <constraint>内容不完整或仓库不存在的任务跳过，不标记完成</constraint>
      <constraint>每个任务执行完后在 content 末尾追加执行记录</constraint>
      <constraint>使用简洁日志风格输出，不用轻松语气</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>自动读取并执行滴答清单任务池中的待办任务</gsd:goal>

  <gsd:phase name="前置检测" order="0">
    <gsd:step>检测 tt CLI（tt --version）</gsd:step>
    <gsd:step>检测登录状态（tt whoami）</gsd:step>
    <gsd:step>读取 config.json 获取任务池 projectId</gsd:step>
  </gsd:phase>

  <gsd:phase name="任务读取" order="1">
    <gsd:step>读取任务池中所有未完成任务（tt project-tasks poolProjectId --json）</gsd:step>
    <gsd:step>按优先级/到期时间排序</gsd:step>
    <gsd:step>展示任务列表（标题 + tag + 到期时间）</gsd:step>
  </gsd:phase>

  <gsd:phase name="任务执行" order="2">
    <gsd:step>逐个执行任务（不超过 maxTasksPerRun）</gsd:step>
    <gsd:step>读取 tag 确定执行策略</gsd:step>
    <gsd:step>解析 content 中的执行计划</gsd:step>
    <gsd:step>执行任务</gsd:step>
    <gsd:step>追加执行记录到 content</gsd:step>
    <gsd:step>标记任务为已完成</gsd:step>
  </gsd:phase>

  <gsd:phase name="执行报告" order="3">
    <gsd:step>输出本次执行汇总</gsd:step>
  </gsd:phase>
</gsd:workflow>

## 执行策略映射（基于 tag）

| Tag | 执行动作 | 完成标志 |
|-----|---------|---------|
| `plan-exec` | 读取 content 中的 plan，逐步执行 | plan 中所有步骤完成 |
| `spec-dev` | 读取 content 中的 spec，按 spec 开发 | 代码提交 + 测试通过 |
| `research` | 搜索资料、分析、输出报告 | 报告文档生成 |
| `article` | 抓取文章内容、提炼要点 | 摘要写入 Obsidian |
| `code-task` | 根据 content 描述直接编码 | 代码提交 |

## 任务状态追踪

每个任务执行过程中，在 content 末尾维护执行记录：

```markdown
## 执行记录（tt-worker 自动维护）
- [x] 步骤 1：xxx - 完成
- [ ] 步骤 2：xxx - 进行中...
```

**恢复机制**：重新运行时检查 `## 执行记录`，跳过已完成步骤（`[x]`），从第一个未完成步骤继续。

## 安全机制

| 机制 | 说明 |
|------|------|
| 任务上限 | 单次最多 N 个（可配置，默认 5） |
| 超时保护 | 超时后保留进度、不标记完成 |
| 跳过策略 | 格式不完整/仓库不存在 → 跳过 + 记录原因 |
| 执行报告 | 最终输出：成功 N / 跳过 N / 失败 N |

## 配置管理

配置文件：`~/.config/tt-auto/config.json`

```json
{
  "poolProjectId": null,
  "poolProjectName": "任务池",
  "remoteServer": null,
  "maxTasksPerRun": 5,
  "taskTimeoutMinutes": 30
}
```

## 输出风格

简洁日志风格（非轻松语气）：
- `[完成] 按plan重构auth模块 - 产出: 3 commits`
- `[跳过] 仓库不存在: /path/to/repo`
- `[失败] 超时: 30分钟未完成`
- `本次执行: 3 成功, 1 跳过, 0 失败`

## CLI 命令

```bash
# 读取任务池任务
tt project-tasks <poolProjectId> --json

# 读取单个任务详情
tt task-find <taskId>

# 更新任务（追加执行记录）
tt task-update <taskId> -p <poolProjectId> --content "<updated content>"

# 标记完成
tt task-done <poolProjectId> <taskId>
```

## Check List

- [ ] tt CLI 已安装且已登录
- [ ] 任务池 projectId 已从 config.json 读取
- [ ] 只读取「任务池」清单中的任务
- [ ] 执行任务数不超过 maxTasksPerRun
- [ ] 每个任务根据 tag 使用正确的执行策略
- [ ] 执行记录已追加到 content
- [ ] 成功的任务已标记为已完成
- [ ] 最终输出了执行报告汇总
