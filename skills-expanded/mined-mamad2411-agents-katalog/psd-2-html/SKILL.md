---
name: psd-2-html
description: Generate and execute @xfe/psd-to-html CLI commands from user intent with minimal questions. Use when users ask to convert PSD files to HTML/React templates, need missing psd parameters completed, want workspace-aware command recommendations, or need precheck/install guidance for the psd command.
---

# psd-2-html

## Core Objective

将用户的 PSD 转换需求转成可直接执行的 `psd` 命令，并在最少提问下补全必要参数。

## Hard Rules

1. 先做前置检查，再做参数补全：
- 必跑 `command -v psd`。
- 可选补充 `psd --version`。
- 若未安装，停止后续流程，仅提供内网源安装命令：
  - `npm install -g @xfe/psd-to-html --registry=http://npm-registry.seasungame.com/`
  - `npm install @xfe/psd-to-html --registry=http://npm-registry.seasungame.com/`

2. 默认最少提问：
- 仅在缺少或冲突时提问。
- 每轮只问 1 个问题。
- 提问优先给 3-5 个选项，并标注 `(Recommended)`。

3. 执行前必须确认：
- 先回显最终命令，再问 `请确认是否执行？(yes/no)`。
- 仅当用户明确说“直接执行/自动执行/无需确认”时，才可跳过确认。

4. 语言策略：
- 说明文字默认简体中文。
- 命令、路径、错误日志保留英文原文。

5. 候选命令必须可读：
- 每条候选命令后，补一段“参数解释（自然语言）”。
- 至少解释 `-s`、`-d`、`--prefix`、`--html-template-type`。
- 解释面向不熟悉 CLI 的用户，避免仅复述参数名。
- 候选命令展示默认使用“卡片式”结构：`命令`、`适用`、`参数白话`、`下一步`。
- 长命令必须独立成行，不要把命令断行后塞进说明段落。

## Entry Modes

### Mode A: Bare Invocation

当用户只输入 `$psd-2-html` 或没有给出有效参数时：

1. 先做 `psd` 命令可用性检查。
2. 扫描 workspace 线索：
- PSD 文件：`rg --files -g '*.psd'`
- React 线索：`package.json` 中是否出现 `react` 依赖。
3. 输出 3-5 条候选完整命令，包含 1 条推荐项。
4. 追加一个最小问题，让用户选命令编号或提供自定义 `-s`。

推荐优先模板：
- `psd -s quiz-rewards.psd -d quiz-rewards --prefix quiz-rewards --html-template-type=react`

若发现当前 workspace 有更合适 PSD（例如 `selling-point.psd`），优先给基于该文件的推荐命令。

### Mode B: Partial Input

当用户给了部分参数或自然语言需求时：

1. 先提取用户已给参数。
2. 按顺序补全：`-s` -> `-d` -> `--prefix` -> `--html-template-type`。
3. 采用积极型默认推断：
- `-s`：若仅一个 `.psd`，直接采用；多个则给 3-5 选项。
- `-d`：默认 `basename(<source>)`。
- `--prefix`：默认同 `-d`。
- `--html-template-type`：若是 React 项目，默认 `react`；否则 `auto`。
4. 只在必要时问一个问题补齐关键缺口。

### Mode C: Full Command Input

当用户已经提供完整 `psd ...` 命令：

1. 先检查命令可用性。
2. 回显命令并说明将执行内容。
3. 默认二次确认后执行。

## Option Prompt Template

当需要用户选择时，使用以下格式（3-5 选项）：

`可选命令（完整可执行）：`
`Option A (Recommended)`
- `命令`：`psd -s selling-point.psd -d selling-point --prefix selling-point --html-template-type=auto`
- `适用`：当前未识别 React 项目，先用 `auto` 最稳妥。
- `参数白话`：`-s` 是“基于哪个 PSD 生成”；`-d` 是“输出目录”；`--prefix` 是“类名前缀”；`--html-template-type=auto` 是“自动选择模板类型”。
- `下一步`：回复 `A` 使用该命令。

`Option B`
- `命令`：`psd -s selling-point.psd -d selling-point --prefix selling-point --html-template-type=react`
- `适用`：直接产出 React 模板。
- `参数白话`：`--html-template-type=react` 表示强制生成 React 模板，其余参数含义同 Option A。
- `下一步`：回复 `B` 使用该命令。

`Option C`
- `命令`：`psd -s selling-point.psd -d selling-point --prefix selling-point --html-template-type=mobile`
- `适用`：明确是移动端模板。
- `参数白话`：`mobile` 表示按移动端模板生成。
- `下一步`：回复 `C` 使用该命令。

`Option D`
- `命令`：`psd -s selling-point.psd -d selling-point --prefix selling-point --html-template-type=pc`
- `适用`：明确是 PC 端模板。
- `参数白话`：`pc` 表示按 PC 模板生成。
- `下一步`：回复 `D` 使用该命令。

只保留与当前环境真实存在的数据；不要编造文件。
命令列表后必须加一条轻量引导：
- `你可以输入 A/B/C/D；输入“参数说明”查看详细参数；或直接说你的想法（例如“要 React，输出目录改成 output”）。`

## Parameter Help Mode

当用户输入“参数说明/详细参数/help”时，给简明参数解释：

- `-s, --source <string>`：要转换的 PSD 文件路径（必填）。
- `-d, --dist <string>`：生成结果输出目录（默认会自动推断）。
- `--prefix <string>`：CSS/类名前缀，减少命名冲突。
- `--html-template-type <string>`：模板类型，常用 `auto`、`react`、`mobile`、`pc`。
- `--dry-run <bool>`：只预检查，不生成文件。

## Command Assembly Rules

最终命令应为完整可执行命令，默认包含以下参数：
- `-s <source.psd>`
- `-d <dist-dir>`
- `--prefix <css-prefix>`
- `--html-template-type <react|auto|pc|mobile|react-styled-jsx|react-css-modules>`

常用输出示例：
- React:
  - `psd -s selling-point.psd -d selling-point --prefix selling-point --html-template-type=react`
- Auto:
  - `psd -s selling-point.psd -d selling-point --prefix selling-point --html-template-type=auto`

## Failure Handling

1. `psd` 不存在：输出安装步骤并结束当前轮补全。
2. source 不存在：给出“文件不存在”并重新提供 3-5 个候选。
3. 运行报错：先贴英文错误原文，再给中文解释和下一步建议。
4. 可提醒 PSD 约束：图层不能有蒙版、不能有样式、锁定图层不会生成。

## Output Contract

交付给用户的内容应满足：

1. 有前置检查结论（已安装/未安装）。
2. 有完整最终命令（不是半截参数）。
3. 有确认步骤（除非用户已明确授权自动执行）。
4. 若为引导模式，有 3-5 个选项和推荐项。
