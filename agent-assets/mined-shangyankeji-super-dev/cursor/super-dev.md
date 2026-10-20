---
description: "Super Dev pipeline governance - research-first commercial-grade delivery. Activates when user says /super-dev or super-dev:"
alwaysApply: true
---

# Super Dev Cursor 规范模板

## 项目上下文

此项目使用 Super Dev 进行规范驱动开发。

**文档位置**:
- PRD: `output/*-prd.md`
- 架构设计: `output/*-architecture.md`
- UI/UX 设计: `output/*-uiux.md`
- Spec 规范: `.super-dev/specs/`

**核心原则**:
1. 所有代码实现必须基于生成的文档
2. 严格遵循 PRD 中定义的功能需求
3. 实现架构文档中的技术设计
4. 使用 UI/UX 文档中的设计系统

## 代码生成规范

### 功能实现
- ✅ 必须实现 PRD 中的所有功能需求
- ✅ 遵循架构文档中的技术栈选择
- ✅ 使用 UI/UX 文档中的设计 tokens
- ❌ 不要添加 PRD 中未明确的功能
- ❌ 不要偏离架构文档的核心设计

### 代码质量
- 遵循红队审查报告中的安全建议
- 达到质量门禁 80+ 分标准
- 修复所有高危和中危问题
- 添加完整的错误处理

### 测试要求
- 单元测试覆盖率 > 80%
- 集成测试覆盖关键路径
- 使用项目选定的测试框架
- 所有测试必须通过

### 代码风格
- 遵循项目现有的代码风格
- 使用有意义的变量和函数名
- 添加必要的代码注释
- 函数长度不超过 50 行

## 提交规范

遵循 Conventional Commits:
```
feat: 新功能
fix: Bug 修复
docs: 文档更新
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

## 优先级规则

当文档之间存在冲突时，按以下优先级处理:

1. **安全 > 性能 > 可维护性**
2. **文档中的明确要求 > 一般最佳实践**
3. **项目特定规范 > 通用编码规范**
4. **PRD > 架构 > UI/UX** (功能优先)

## 快速开始

使用 Super Dev 生成项目后:

```bash
# 1. 生成项目资产
super-dev pipeline "功能描述" --platform web --frontend react

# 2. 在 Cursor Composer 中 (Cmd+I)
# 粘贴 output/*-ai-prompt.md 的内容

# 3. 点击 Generate，AI 会根据所有文档生成代码

# 4. 审查生成的代码，确保符合所有规范
```

## 注意事项

- ⚠️ 如果文档中有不明确的地方，先询问用户
- ⚠️ 不要假设需求，严格按照文档实现
- ⚠️ 生成的代码应该可以直接运行
- ⚠️ 包含必要的配置文件和依赖说明


# Super Dev Pipeline Rules
- When the user triggers `/super-dev ...`, enter Super Dev pipeline mode immediately.
- Start with research and write output/*-research.md as a real file in the repository.
- Always read and maintain output/*-prd.md, output/*-architecture.md, and output/*-uiux.md as source-of-truth project files.
- Summarize the three core documents to the user and wait for user confirmation before creating Spec/tasks or writing code.
- Create Spec/tasks only after confirmation.
- Execute frontend-first delivery before backend/database tasks, then run quality gate before release.
- Before any UI implementation, first lock the icon library, typography, design token system, component ecosystem, and page skeleton from output/*-uiux.md.
- Do not use emoji as functional icons or placeholders.
- For non-conversational AI products, avoid Claude / ChatGPT-style sidebar chat shells unless the UI plan explicitly justifies them.
- Keep using the component ecosystem and design token direction defined in output/*-uiux.md rather than switching ad hoc.
- If `.super-dev/SESSION_BRIEF.md` exists, read it before responding and keep the current Super Dev gate active across follow-up edits.

## Coding Constraints (active during ALL coding phases)
- Before writing ANY code, run `cat package.json` to check framework versions. If unsure, read official docs first.
- Icons MUST come from Lucide/Heroicons/Tabler. No emoji as icons. No purple/pink gradient themes.
- Frontend fetch URLs must exactly match backend route definitions.
- Before writing each file: correct imports, no emoji, colors from tokens only.
- After completing a feature, run build + lint. Fix errors before moving on.

## Super Dev System Flow Contract
- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
