---
description: "Use when tasks involve code collection, module analysis, code generation, build/test — 强制采用 subagent-driven 工作流；任何不确定或需用户决定的情形必须通过 vscode_askQuestions (ask_question) 提问并等待用户答复；任务完成与反馈的唯一确认方式为 ask_question。关键词：subagent, ask_question, Explore, Analyze, Patch, Runner"
name: "Subagent-Driven 执行规范"
applyTo: "**"
---

# Subagent-Driven 执行规范

适用范围：当代理/技能将要执行下列任一类工作时生效：

- 代码搜集（搜索/收集文件）
- 模块/接口理解（依赖/接口分析）
- 代码生成/补丁（实现或修改源代码）
- 编译/构建与测试运行
- 重构或其他会修改代码的操作

## 强制性原则（必须遵守）

1. 子任务必须以子代理（subagent）执行：
   - `Explore`: 搜集与定位相关文件
   - `Analyze`: 模块/接口/依赖分析
   - `Patch`: 生成补丁或代码实现
   - `Runner`: 编译、构建与执行测试
   - `Review`: 静态检查与格式化

2. 每个子代理应返回可审计的产物：文件清单、diff、构建/测试日志、以及可供主代理合并的明确输出。

3. 并行化：对互不冲突的子任务可并行运行子代理；禁止并行写入同一文件。主代理负责检测冲突并在需要时序列化写入。

4. Subagent的模型和推理等级默认和主代理一致；如需调整，必须在调用时明确指定。针对gpt系列 一般采用gpt5.4或更高版本以确保能力匹配 推理等级xhigh 而claude系列模型 一般采用opus 4.7 推理等级max。

## 不确定性与用户确认（强制流程）

- 任何可能影响公共接口、存在多实现方案、或带来数据/回滚风险的情形，必须立刻使用 `vscode_askQuestions`（ask_question）向用户提问并等待答复。提问必须提供：操作影响、推荐选项、以及自由文本输入框以接收用户自定义指示。

## 任务完成与后续确认（唯一通道）

- 任务完成后，唯一允许的用户确认与后续指示渠道为 `vscode_askQuestions`（ask_question）。该提问应列出更改摘要、受影响文件、验证步骤、风险点与推荐下一步，并允许自由文本输入。

## 输出、审计与证据

- 子代理必须产出可审计证据：搜索结果（含上下文/行号）、补丁（diff）、构建与测试日志（含命令与退出码）。所有修改应通过可审计方式应用并记录在 `manage_todo_list`。

## 实践建议

- 请采用标准子代理命名：`Explore`, `Analyze`, `Patch`, `Runner`, `Review`。
- 在多步工作前，用 `manage_todo_list` 跟踪步骤与状态；并在每次子代理开始/完成时记录其动作与产物。

## 覆盖与例外

- 如需覆盖本规范，可在目标路径添加局部 `.instructions.md` 文件并以“Overrides subagent-driven rules”标注理由。

---

**示例提示（供主代理使用）**:

- "Use subagent-driven: run `Explore` to collect files matching `TODO`; run `Analyze` to extract module interfaces; run `Patch` to generate diffs; run `Runner` to execute tests. If a decision is required, call `vscode_askQuestions` and pause."
