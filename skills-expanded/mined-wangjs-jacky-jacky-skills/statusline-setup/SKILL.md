---
name: statusline-setup
description: "交互式配置 Claude Code 状态栏，支持多种方案切换。触发词：状态栏、statusline、配置状态栏"
---

<role>
你是一个 Claude Code 配置管理专家，负责状态栏方案的配置和切换。
</role>

<purpose>
当用户需要配置或切换 Claude Code 终端状态栏时，提供交互式方案选择并完成配置。
</purpose>

<trigger>
配置状态栏
statusline
状态栏
glm-coding-plan-statusline
omc-hud
</trigger>

<yolo:config>
  <yolo:mode>auto-advance</yolo:mode>
  <yolo:safety-gates>
    <gate>修改 settings.json 中 statusLine 以外的字段</gate>
  </yolo:safety-gates>
</yolo:config>

<gsd:workflow>
  <gsd:meta>
    <name>statusline-setup</name>
    <trigger>状态栏、statusline、配置状态栏</trigger>
    <requires>Read, Edit, AskUserQuestion</requires>
    <constraints>
      <constraint>仅修改 settings.json 中的 statusLine 字段</constraint>
      <constraint>YOLO 模式下安全门仍需人工确认</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>根据用户选择，将 settings.json 的 statusLine 字段配置为指定方案</gsd:goal>

  <gsd:phase name="detect" order="1">
    <gsd:step>读取 ~/.claude/settings.json</gsd:step>
    <gsd:step>检测当前 statusLine 配置，识别已激活的方案</gsd:step>
  </gsd:phase>

  <gsd:phase name="select" order="2">
    <gsd:step>使用 AskUserQuestion 展示可选方案（标注当前方案）</gsd:step>
    <gsd:step>收集用户选择</gsd:step>
  </gsd:phase>

  <gsd:phase name="apply" order="3">
    <gsd:step>根据选择更新或删除 statusLine 字段</gsd:step>
    <gsd:step>确认配置结果</gsd:step>
  </gsd:phase>
</gsd:workflow>

# 状态栏配置

> 🚀 **YOLO 模式** — 自动推进，低风险操作跳过确认。

## 可选方案

| 方案 | 命令 | 说明 |
|------|------|------|
| **GLM Coding Plan** | `npx @wangjs-jacky/glm-coding-plan-statusline@latest` | 编码计划实时状态 |
| **OMC HUD** | `node $HOME/.claude/hud/omc-hud.mjs` | oh-my-claudecode HUD |
| **关闭状态栏** | _(删除 statusLine)_ | 不显示 |

## 执行流程

### Phase 1: 检测当前配置

**目标**：读取并识别当前状态栏方案

**步骤**：
1. 使用 Read 读取 `~/.claude/settings.json`
2. 检查 `statusLine.command` 字段：
   - 包含 `glm-coding-plan-statusline` → 当前为 GLM Coding Plan
   - 包含 `omc-hud` → 当前为 OMC HUD
   - 无 `statusLine` 字段 → 当前已关闭

### Phase 2: 交互式选择

**目标**：让用户选择目标方案

使用 AskUserQuestion，格式如下：

- **question**: "选择要使用的状态栏方案？"
- **header**: "StatusLine"
- **multiSelect**: false
- **options**:
  - label: "GLM Coding Plan" / description: "编码计划实时状态" + "（当前）" 如已激活
  - label: "OMC HUD" / description: "oh-my-claudecode HUD" + "（当前）" 如已激活
  - label: "关闭状态栏" / description: "不显示" + "（当前）" 如已关闭

### Phase 3: 应用配置

**目标**：写入用户选择的方案

**步骤**：
1. 根据用户选择，使用 Edit 更新 `statusLine` 字段：
   - **GLM Coding Plan**：
     ```json
     "statusLine": { "type": "command", "command": "npx @wangjs-jacky/glm-coding-plan-statusline@latest" }
     ```
   - **OMC HUD**：
     ```json
     "statusLine": { "type": "command", "command": "node $HOME/.claude/hud/omc-hud.mjs" }
     ```
   - **关闭**：删除整个 `statusLine` 字段（含其前一行逗号）
2. 告知用户配置完成，新状态栏下次启动时生效

## 验证

- 确认 Edit 后 settings.json 中仅 `statusLine` 字段被修改
- 若用户选择关闭，确认 `statusLine` 字段已完全移除
