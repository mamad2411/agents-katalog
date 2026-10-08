---
name: super-dev
description: Activate the Super Dev pipeline inside Codex CLI.
when_to_use: Use when the user says /super-dev, super-dev:, or super-dev： followed by a requirement. Activate the Super Dev pipeline for research-first, commercial-grade project delivery.
version: 2.4.0
---
# super-dev for Codex CLI

## 关键约束提醒（每次操作前必读）

以下规则在整个开发过程中始终有效，不得以任何理由违反：

1. **图标系统**: 功能图标只能来自 Lucide / Heroicons / Tabler 图标库。绝对禁止使用 emoji 表情 作为功能图标、装饰图标或临时占位。如果你发现自己即将输出包含 emoji 的 UI 代码，停下来，改用图标库组件。

2. **AI 模板化禁令**: 禁止紫/粉渐变主色调、禁止 emoji 图标、禁止无信息层级的卡片墙、禁止默认系统字体直出。

3. **代码即交付**: 不允许“先用 emoji 顶上后面再换”。图标库必须在第一行 UI 代码前就锁定。

4. **自检规则**: 在向用户展示任何 UI 代码或预览前，必须自检源码中不存在任何 emoji 字符（Unicode range U+2600-U+27BF, U+1F300-U+1FAFF）。发现后先替换为正式图标库再继续。

## Direct Activation Rule（强制）

- If this skill is invoked, Super Dev pipeline mode is already active.
- Do not spend a turn saying you will read the skill first, explain the skill, or decide whether to enter the workflow.
- Do not answer with variants of "我先读取 skill 再判断流程".
- If this file is loaded from `~/.codex/skills`, treat it as the compatibility mirror of the same Super Dev contract.

## 触发方式（强制）

- Treat `super-dev: <需求描述>` and `super-dev：<需求描述>` as the AGENTS-driven natural-language fallback entry point.
- Treat `$super-dev` as the explicit official Skill mention when the Codex host exposes skills by name.
- In Codex desktop/app, if the slash list shows this enabled skill, selecting `/super-dev` from that list is valid because it resolves to this Skill rather than a custom project slash command.
- Do not treat it as ordinary chat.
- 当前宿主负责调用模型、工具、终端与实际代码修改。
- Super Dev 不是大模型平台，也不提供自己的代码生成 API。

## Runtime Contract（强制）

- Super Dev 由两部分组成：
  1. 当前项目内的本地 Python CLI 工具
  2. 当前宿主里的规则/Skill/命令映射
- 当前宿主负责调用模型、联网、终端、编辑器与实际代码修改。
- 当用户通过 Codex App/Desktop 的 `/super-dev` skill 入口、Codex CLI 的 `$super-dev`，或 `super-dev: ...` / `super-dev：...` 回退入口触发时，都意味着你必须进入 Super Dev 流水线。
- 需要研究、设计、编码、运行、调试时，优先使用 Codex 自身的 web/search/terminal/edit 能力。
- 需要做治理动作时，才使用本地 `super-dev` CLI。

## 宿主交互边界

普通用户只需要记住 3 个终端命令：

```bash
super-dev
super-dev update
super-dev uninstall
```

普通用户优先只记住这些宿主表达：

```text
/super-dev <goal>
/super-dev-seeai <goal>
继续当前流程
现在下一步是什么
```

文本回退宿主优先使用：

```text
super-dev: <goal>
super-dev-seeai: <goal>
```

维护/治理场景才显式进入：

```text
/super-dev-work <mode> <goal>
/super-dev-run <stage|resume|status|next>
/super-dev-review <target> <action>
```

工作模式固定为：

- `new`：从 0 到 1
- `evolve`：已有项目增量迭代
- `variant`：从现有项目派生新版本
- `patch`：在现有项目上修 bug / 做整改
- `resume`：继续当前中断流程

硬规则：

- `new` 才能直接从 `research -> docs` 开始
- `evolve / variant / patch` 必须先 `baseline`
- baseline 必须先分析现有功能、架构、代码、路由/API、UI 与约束，再进入差量 research 和三文档
- `resume` 是默认场景，不是异常场景

恢复是默认场景，不是补充场景。优先理解这些表达：

- `继续当前流程`
- `现在下一步是什么`
- `/super-dev 继续当前流程`

内部 CLI 能力仍可存在，但不应再被当成普通用户主心智。

## 首轮响应契约（强制）

- 首次触发时第一轮回复必须说明：流水线已激活，当前阶段是 `research`。
- 先读取 `.super-dev/WORKFLOW.md` 与 `output/*-bootstrap.md`（若存在）。
- 说明固定顺序：research -> 三份核心文档 -> 等待确认 -> Spec/tasks -> 前端优先 -> 后端/测试/交付。
- 三份核心文档完成后暂停等待确认；未经确认不创建 Spec 也不编码。

### research 双引擎

**引擎 1: 本地知识发现** — 优先读取 `knowledge/` 和 knowledge-bundle.json，并在当前宿主里把结论沉入 `output/*-research.md`。

**引擎 2: 宿主联网研究** — WebFetch/WebSearch 搜索同类产品、竞品和官方文档，写入 `output/*-research.md`。

两个引擎的结果都必须在 PRD/架构/UIUX 文档中被继承。

## 本地知识库契约（强制）

- 存在 `knowledge/` 时，research 与文档阶段优先读取相关知识文件。
- 存在 `output/knowledge-cache/*-knowledge-bundle.json` 时，先读取 local_knowledge / web_knowledge / research_summary。
- 命中的知识是项目约束（标准/检查清单/反模式/场景包/质量门禁），必须继承到 PRD、架构、UIUX、Spec 和实现阶段。
- 未经用户确认禁止创建 `.super-dev/changes/*` 或开始编码。
- 产物必须真实写入项目文件，不能只在聊天中口头描述。

## 编码前门禁（Spec 确认后、编码开始前必须执行）

跳过任何一步都会导致大量返工：

### 第 1 步：技术栈预研（最关键）
- 读取项目依赖文件（package.json / requirements.txt / go.mod 等），找到主要依赖的精确版本号
- 用 WebFetch 查阅每个主要框架的官方文档：Getting Started、Migration Guide、API Reference
- **不确定 API 写法时，先查官方文档再写代码，永远不要猜**

### 第 2 步：读取项目配置
- `super-dev.yaml` 确认技术栈选择
- 框架配置文件、tsconfig.json、.env.example
- 已有代码目录结构

### 第 3 步：声明 UI 工具链
- 声明并确认图标库（Lucide/Heroicons/Tabler）和组件库已安装
- 不声明 = 不允许写 UI 代码

### 第 4 步：确认 API 契约和设计 token
- 读取 output/*-architecture.md 中的 API 定义
- 读取 output/*-uiux.md 中的设计 token

### 第 5 步：在宿主里建立页面结构与共享类型并验证构建
- 按 `output/*-architecture.md` 与 `output/*-uiux.md` 直接在宿主里生成/更新页面结构、组件实现参考与共享类型
- 运行宿主原生构建命令确认零错误后才开始写业务代码


## 会话连续性契约（强制）

- 若存在 `.super-dev/SESSION_BRIEF.md`，每次继续前必须先读取。
- 用户在确认门/返工门说"改/补充/确认/继续"等，属于流程内动作，不退回普通聊天。
- 修改后留在当前门里，总结变化并再次等待确认。
- UI 不满意 -> 先更新 `output/*-uiux.md`，再重做前端 + UI review。
- 架构不合理 -> 先更新 `output/*-architecture.md`，再调整 Spec/实现。
- 质量不达标 -> 先修复，重新执行 quality gate + proof-pack。
- 启用 policy 时不得默认建议降低治理强度。

## 实现闭环契约（强制）

- 每轮修改后先做最小 diff review 再汇报完成。
- 运行 build / type-check / test / runtime smoke。
- 新增代码必须接入真实调用链；未接入则删除，禁止留 unused code。
- 新增日志/告警/埋点必须验证会在真实路径触发。

## 编码阶段持续治理

读取 `.super-dev/pipeline-state.json` 了解当前在哪个阶段。
根据阶段调整你的工作重点：research 阶段侧重调研，frontend 阶段侧重 UI 实现，quality 阶段侧重测试和门禁。

每次进入新阶段时宣告: `Super Dev | [N/9] 阶段名 开始 | 主导专家: XXX`

### 每次写文件前自检
- [ ] "use client" 是否需要？（Next.js）
- [ ] 图标来自声明的图标库？（不是 emoji）
- [ ] 颜色来自设计 token？（不是硬编码 hex）
- [ ] import 路径正确？API 路径与架构文档一致？

### 每完成一个功能后
1. build 无错误 2. lint 无 error 3. 无控制台红色错误
4. 对比 output/*-uiux.md 视觉一致 5. 运行 validate-superdev.sh（如有）

## Required behavior

1. First reply: say Super Dev pipeline mode is active and the current phase is `research`.
2. Before the first reply, read `.super-dev/WORKFLOW.md` and `output/*-bootstrap.md` when present and treat them as the explicit bootstrap contract for this repository.
3. Read `knowledge/` and `output/knowledge-cache/*-knowledge-bundle.json` when present.
4. Use Codex native web/search/edit/terminal capabilities to produce:
   - `output/*-research.md`
   - `output/*-prd.md`
   - `output/*-architecture.md`
   - `output/*-uiux.md`
5. Write the required artifacts into the repository workspace. Chat-only summaries do not count as completion.
6. Stop after the three core documents and wait for explicit confirmation.
7. Only after confirmation, create `.super-dev/changes/*/proposal.md` and `.super-dev/changes/*/tasks.md`, then continue with frontend-first implementation.
8. If the user says the UI is unsatisfactory, requests a redesign, or says the page looks AI-generated, first update `output/*-uiux.md`, then redo the frontend, rerun frontend runtime and UI review, and only then continue.
9. If the user says the architecture is wrong or the technical plan must change, first update `output/*-architecture.md`, then realign Spec/tasks and implementation before continuing.
10. If the user says quality or security is not acceptable, first fix the issues, rerun the quality gate, refresh any delivery evidence the reports ask for, and only then continue.

## Never do this

- Never jump straight into coding after `super-dev:` or `super-dev：`.
- Never create Spec or implementation work before the documents are confirmed.
- 未经用户明确确认，禁止创建 `.super-dev/changes/*`。
- Use local `super-dev` CLI for governance actions only; keep research, drafting, coding, and debugging inside Codex.

## 宿主常犯错误速查（每次编码前扫一眼）

### 错误 1: 使用 emoji 作为图标
```tsx
// ❌ <button>🔍 搜索</button>
// ✅ import { Search } from 'lucide-react'
//    <button><Search size={16} /> 搜索</button>
```

### 错误 2: 紫色渐变 AI 模板
```tsx
// ❌ bg-gradient-to-r from-purple-500 to-pink-500
// ✅ 使用 output/*-uiux.md 定义的品牌色: bg-primary + text-heading-1
```

### 错误 3: 前后端 API 路径不一致
```
// ❌ 架构文档写 /api/users，后端实际是 /api/v1/users
// ✅ 编码前先确认 output/*-architecture.md 中的 API 路径
```

## 错误恢复策略

遇到错误时按以下优先级恢复：

**阶段 1 -- 便宜恢复（不丢失上下文）**
- Token 超限？注入"继续，不要回顾"然后重试
- 工具失败？注入错误详情 + 备选方案，继续
- 权限拒绝？说明允许什么，继续

**阶段 2 -- 上下文重建（可能丢失细节）**
- Prompt 过长？压缩旧上下文，保留最近内容
- 多次失败？丢弃非关键历史，只保留关键决策

**阶段 3 -- 暴露错误（无法恢复）**
- 提供: 什么失败了 + 为什么 + 下一步建议
- 回到终端重新运行 `super-dev` 校验宿主接入；若本地版本或注入面不一致，再执行 `super-dev update`

永远不要在尝试阶段 1-2 之前就暴露错误给用户。

## Agent Teams 协作（支持 Teams 功能的宿主）

如果宿主支持 Agent Teams（如 Claude Code 的 /teams），可以让多位 Super Dev 专家并行工作：

**研究阶段**: PM + ARCHITECT 并行调研
**文档阶段**: PRD / Architecture / UIUX 可并行起草
**编码阶段**: 前端 + 后端可并行开发（注意 API 契约对齐）
**质量阶段**: Security + QA + Performance 并行审查

使用 Teams 时的约束：
- 每个 teammate 必须声明自己的专家角色
- teammates 之间通过共享文件（output/*.md）传递上下文
- 修改同一文件前必须协调（避免冲突）
- 质量门禁结果必须等所有 teammates 完成后汇总

## Super Dev System Flow Contract

- SUPER_DEV_FLOW_CONTRACT_V1
- PHASE_CHAIN: research>docs>docs_confirm>spec>frontend>preview_confirm>backend>quality>delivery
- DOC_CONFIRM_GATE: required
- PREVIEW_CONFIRM_GATE: required
- HOST_PARITY: required
