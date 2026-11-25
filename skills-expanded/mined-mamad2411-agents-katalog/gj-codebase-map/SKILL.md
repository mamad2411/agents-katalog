---
name: gj-codebase-map
description: Map an existing repository into AI-readable project context. Use when onboarding a GitLab project, refreshing docs/codebase, deriving docs/context and docs/modules, generating .gj/context.yml drafts, or scanning changed paths after major refactors.
---

# GJ 代码库建图

## 工作流程

1. 使用 `rg --files` 了解仓库结构。
2. 从四个视角扫描：
   - 技术：技术栈、运行时、依赖、外部集成。
   - 架构：入口、分层、数据流、模块边界。
   - 质量：约定、测试、CI、错误处理。
   - 风险：安全、脆弱区域、性能、未知项。
3. 创建或更新：
   - `docs/codebase/STACK.md`
   - `docs/codebase/INTEGRATIONS.md`
   - `docs/codebase/ARCHITECTURE.md`
   - `docs/codebase/STRUCTURE.md`
   - `docs/codebase/CONVENTIONS.md`
   - `docs/codebase/TESTING.md`
   - `docs/codebase/CONCERNS.md`
4. 生成当前上下文草稿：
   - `docs/context/current-state.md`
   - `docs/context/module-map.md`
   - `docs/context/glossary.md`
   - `docs/modules/*.md`
   - `.gj/context.yml`
   从 `.gj/doc-templates/module.md` 创建模块文档，使用语义化模块名，包含通用元数据契约，
   并明确区分已观察事实和推断。
5. 标记所有需要人工确认的推断。
6. 暂存或分享前扫描生成内容中的秘密信息。

## 规则

- `docs/codebase/*` 只记录已观察事实，不代表已批准的业务规则。
- 未经确认，不要把观察到的行为转为当前状态规则。
- 发现 Token、私钥、密码或连接字符串时停止，并要求人处理。

## 输出格式

```markdown
## 代码库建图摘要

扫描路径：

创建/更新的文档：

已观察事实：

待确认推断：

风险和关注点：

秘密扫描：
```

## 参考资料

需要查看小型示例建图时，读取 `references/demo-run.md`。
