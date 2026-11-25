---
name: tt-defer
description: "将任务推送到滴答清单任务池，支持自然语言触发和命令触发。触发词：推到待办、丢到池子、明天再做、tt-defer、推任务、推迟任务。"
---

# tt-defer

将任务推送到滴答清单「任务池」，供远程服务器自动执行。

> **IMPORTANT**: 执行前必须先读取 `references/task-format.md` 了解任务格式规范。

<gsd:workflow>
  <gsd:meta>
    <name>tt-defer</name>
    <trigger>推到待办、丢到池子、明天再做、tt-defer、推任务、推迟任务、放到池子里、稍后执行</trigger>
    <requires>tt CLI (npm install -g @wangjs-jacky/ticktick-cli), Bash, AskUserQuestion</requires>
    <checkpoints>
      <checkpoint order="0">tt CLI 可用且已登录</checkpoint>
      <checkpoint order="1">任务池清单已确认存在</checkpoint>
      <checkpoint order="2">推送内容确认后执行</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>Phase 0 必须首先执行，检测 tt CLI 和任务池清单</constraint>
      <constraint>所有任务只推送到「任务池」清单，不推到其他清单</constraint>
      <constraint>标题必须简短（≤15字），详细内容写入 content</constraint>
      <constraint>必须为每个任务打上类型 tag（plan-exec / spec-dev / research / article / code-task）</constraint>
      <constraint>content 必须包含完整的执行上下文（原始背景、执行环境、执行计划）</constraint>
      <constraint>禁止硬编码 projectId，首次通过 tt project-list 获取</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>将当前对话中的任务上下文完整推送到滴答清单任务池</gsd:goal>

  <gsd:phase name="前置检测" order="0">
    <gsd:step>检测 tt CLI 是否已安装（tt --version）</gsd:step>
    <gsd:step>检测是否已登录（tt whoami）</gsd:step>
    <gsd:step>检测或创建「任务池」清单</gsd:step>
  </gsd:phase>

  <gsd:phase name="上下文提取" order="1">
    <gsd:step>识别触发来源（自然语言 / 命令 / plan-spec 完成后）</gsd:step>
    <gsd:step>提取当前会话中的 plan / spec / 文章 / 任务描述</gsd:step>
    <gsd:step>推断任务类型 tag</gsd:step>
    <gsd:step>组装任务格式</gsd:step>
  </gsd:phase>

  <gsd:phase name="推送任务" order="2">
    <gsd:step>确认推送内容（展示标题 + tag + 执行时间）</gsd:step>
    <gsd:step>执行 tt task-add 推送到任务池</gsd:step>
    <gsd:step>确认推送结果</gsd:step>
  </gsd:phase>
</gsd:workflow>

## Tag 推断规则

| 上下文特征 | 推断 Tag |
|-----------|---------|
| 当前会话生成了 plan 文件 | `plan-exec` |
| 当前会话生成了 spec/设计文档 | `spec-dev` |
| 用户提供 URL 或文章链接 | `article` |
| 描述涉及"调研"、"研究"、"分析" | `research` |
| 以上均不匹配 | `code-task` |
| 用户手动指定 | 用户指定（最高优先级） |

## 配置管理

配置文件：`~/.config/tt-auto/config.json`

首次运行自动创建，缓存 `poolProjectId`。检测流程：
1. 读取 config.json 中的 poolProjectId
2. 无则运行 `tt project-list` 查找名为「任务池」的清单
3. 找不到则在 TickTick 中创建新清单，写入 config.json

## CLI 命令

```bash
# 创建任务（带 tag）
tt task-add "简短标题" -p <poolProjectId> --tag <tag> --content "<markdown content>" --start-date <date> --due-date <date>

# 查看任务池中所有任务
tt project-tasks <poolProjectId> --json
```

## 输出风格

延续 tt skill 的轻松语气：
- 推送成功："已丢进池子，远程会处理"
- 带 tag 和时间："已推到任务池 [plan-exec] 明天执行"
- 推迟无聊任务："好的，先泡在池子里等着吧~"

## Check List

- [ ] tt CLI 已安装且已登录
- [ ] 任务池清单已检测/创建，projectId 已缓存
- [ ] 任务标题 ≤15 字
- [ ] 已打上正确的类型 tag
- [ ] content 包含完整上下文（原始背景 + 执行环境 + 执行计划）
- [ ] 推送前已确认内容
