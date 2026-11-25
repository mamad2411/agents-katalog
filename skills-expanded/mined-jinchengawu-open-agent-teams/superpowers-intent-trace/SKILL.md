---
name: superpowers-intent-trace
description: 侧车模式——在 debug/superpowers-intent/ 下按需求 ID 维护意图与对齐证据（SSOT），与对话内简短回复并行，便于审计、PR 复盘与提示词调试
---

# Superpowers Intent Trace（侧车意图）

## 目的

对话里可以**短答、摘要**；但**意图、约束、证据链接**应在仓库内有一份**可检索 SSOT**，与聊天解耦，便于：

- 审计（谁在什么前提下承诺了什么）
- PR / MR 复盘
- 提示词与门禁调试

## 路径约定

在业务仓库（或 monorepo 子包）下使用统一目录：

```text
debug/superpowers-intent/
  <requirementId>.md
```

- **`requirementId`**：与需求绑定一致，如 `REQ-2026-0424`、`JIRA-XXX`；字符建议 `[A-Za-z0-9._-]+`。
- 若仓库已有 `docs/requirements/` 等规范，**仍建议**将「AI 侧结构化意图」放在 `debug/superpowers-intent/`，与需求全文外链互补。

## 文件内容建议（Markdown）

每条需求一个文件，至少包含：

1. **元信息**：需求 ID、分支、PR 链接、负责人、时间戳（可引用 `templates/requirement-binding.template.md` 字段）。
2. **意图 SSOT**：当前任务目标、非目标、验收口径（用户原话可摘要 + 链接）。
3. **对齐证据**：关键决策、选用的 skills、门禁是否已执行（ checklist ）。
4. **与流水线关系**：若使用 `superpowers-pipeline.json`，记录已 Read 的 pipeline 版本或 hash（可选）。

## Git 与隐私

- 若含内网链接或敏感信息：将 `debug/superpowers-intent/` 加入 **`.gitignore`**，或仅提交脱敏副本。
- 团队规范允许时：纳入版本库以便 PR 讨论引用具体文件路径。

## 与 superpowers-pipeline 的配合

- **Pipeline** 回答「按什么顺序 Read 哪些 skill」。
- **Intent trace** 回答「**为什么**这样做、**对齐了哪些证据**」；两者均为文件系统侧事实，不依赖模型上下文长度。
