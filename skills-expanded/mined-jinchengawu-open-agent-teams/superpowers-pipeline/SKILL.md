---
name: superpowers-pipeline
description: 团队已配置 .cursor/superpowers-pipeline.json 时——会话开始或阶段切换前显式 Read 该 JSON，按 steps/after/triggers 对齐 skill 门禁顺序（声明式 SSOT，非自动脚本）
---

# Superpowers Pipeline（声明式编排）

## 何时用

- 业务仓库根或 `.cursor/` 下存在 **`superpowers-pipeline.json`**（常见路径：`.cursor/superpowers-pipeline.json`）。
- 需要与团队约定「**何时**应 Read **哪些** skill」一致，减少终端内置规则与 skills 的排异。

## 必须行为

1. **显式 Read**：在按流水线工作时，先 **Read** `superpowers-pipeline.json` 全文，再调度其中列出的 `skillDirectory`（对应 `.cursor/skills/<name>/SKILL.md` 等）。
2. **依赖顺序**：对每个 `step`，仅在其 `after` 中列出的 `id` 已满足后再进入该 step。
3. **Triggers**：将 `triggers[].kind` 理解为**语义标签**（如每轮门禁、完成前、提交前）；具体是否执行仍由你与用户上下文决定，但以 JSON 为团队对齐口径。

## 与校验脚本的关系

- 包内或 CI 可对 JSON 做结构校验（DAG、id 唯一）：`node packages/web3-fe-superpowers/scripts/validate-superpowers-pipeline.mjs --file <路径>`。
- Schema：`packages/web3-fe-superpowers/schemas/superpowers-pipeline.schema.json`。
- 示例模板：`packages/web3-fe-superpowers/templates/superpowers-pipeline.example.json`。

## 与侧车意图的关系

长对话可压缩回复，但**意图与证据**应按 **`superpowers-intent-trace`** skill 写入 `debug/superpowers-intent/`，便于审计与复盘。
