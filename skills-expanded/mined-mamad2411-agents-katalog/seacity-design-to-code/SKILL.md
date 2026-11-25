---
name: seacity-design-to-code
description: 设计图驱动代码生成 Skill — 把 Figma/Sketch 等设计文件导入 Pencil，通过 MCP 读取精确设计数据，自动生成 UI 代码，目标相似度 95%+。自动适配运行环境：Claude Code 用并行 Agent 团队流程，其他模型降级为线性单线程流程。触发场景："还原设计稿"、"从 Figma 生成代码"、"Pencil 文件"、"UI 高保真实现"、"把设计图做成 App"。
---

# Seacity Design-to-Code Skill

一个基于 Pencil MCP 的设计图→代码自动化工作流。把 Figma/Sketch 设计文件导入 Pencil 后，通过 6 阶段流程生成高精度 UI 代码。

**核心特性：自动适配运行环境**。在 Claude Code 等支持并行 Agent 的环境下用多 Agent 团队模式，在其他模型/环境下降级为线性模式，**同一份 Skill 两种使用方式**。

## 第一步：检测运行环境

**在执行任何工作之前，必须先检测当前环境是否支持并行 Agent**。

### 检测方法

按顺序检查以下能力是否可用：

| 能力 | 检测方式 | 代表环境 |
|------|---------|---------|
| **Full Agent Mode** | 能使用 `Agent` 或 `subagent` 工具派遣子代理 | Claude Code, Claude CLI |
| **Task Mode** | 能使用 `TaskCreate`/`TaskUpdate` 管理任务 | Claude Code with plan tools |
| **Linear Mode** | 只能按顺序执行工具调用 | Cursor, Aider, 普通 LLM API |

### 分支决策

```
IF 可用工具包含 Agent/subagent → 走 FULL AGENT MODE
ELSE IF 可用工具包含 TaskCreate → 走 TASK MODE（半并行）
ELSE → 走 LINEAR MODE（单线程顺序执行）
```

在对话开头运行一次检测，把结果告知用户：

```
✅ 检测到 Claude Code + Agent 工具 → 进入 FULL AGENT MODE
   本次将使用并行 Agent 团队，预计 30-60 分钟完成
```

或：

```
⚠️ 当前环境不支持并行 Agent → 降级到 LINEAR MODE
   将按 6 阶段顺序执行，预计 2-4 小时完成
   质量相同，只是耗时更长
```

## 执行模式详解

### FULL AGENT MODE（Claude Code 推荐）

6 阶段完整并行流程：

| Phase | 并行度 | 内容 |
|-------|--------|------|
| Phase 0 | 1 Agent | 设计情报提取 |
| Phase 1 | 1 Agent | 通用组件层建设 |
| Phase 2 | 4-6 Agents | 屏幕规格生成（并行） |
| Phase 3 | 4-6 Agents | 代码实现（并行） |
| Phase 4 | 4-6 Agents | 差分审计（并行独立） |
| Phase 5 | 按需 N Agents | 最终攻坚 |

完整模板见 `templates/phase*_*.md`。

### TASK MODE（半并行）

没有 Agent 工具但有任务管理能力。把每个 Agent 的工作转为 Task：

- Phase 2 时创建 N 个 Task，主循环依次处理每个 Task
- 不能真正并行，但保留了清晰的模块化

### LINEAR MODE（无并行能力的降级方案）

单线程顺序执行：

```
Phase 0: 情报提取                    [串行]
  ↓
Phase 1: 通用组件层                  [串行]
  ↓
Phase 2: 模块1规格 → 模块2规格 → ...  [串行，逐模块]
  ↓
Phase 3: 模块1实现 → 模块2实现 → ...  [串行]
  ↓
Phase 4: 模块1审计 → 模块2审计 → ...  [串行]
  ↓
Phase 5: 修复逐项进行
```

关键点：**流程结构不变，只是没有并行**。最终质量相同，仅耗时更长。

**Linear mode 下必须更严格遵守**：
- 每屏都要完整读取 spec 再写代码
- 不能跳过 Phase 2 直接写 code
- 每改完一屏立即编译验证（因为没有并行 Agent 互相兜底）

## 适用场景

- 用户手里有设计稿（Figma/Sketch/XD），需要实现成 App
- 已有项目 UI 还原度低，需要大幅提升相似度
- 新项目从 0 开始按设计图生成完整代码

## 前置条件检查

**开始前必须确认**：

1. **Pencil MCP 可用** — 当前会话能看到 `mcp__pencil__*` 工具
2. **设计文件已导入** — 用户已经把 Figma/Sketch 等文件拖入 Pencil 画板
3. **工程构建工具可用** — iOS 需要 Xcode，Android 需要 Gradle 等

如果没有 Pencil MCP，引导用户阅读 `reference/setup_pencil.md` 完成一次性安装。

## 核心原则（两种模式都适用）

1. **指挥官不下场**（Full Agent Mode）/ **工作者保持纪律**（Linear Mode）
2. **激进并行**（Full Agent Mode）/ **严格分阶段**（Linear Mode）
3. **数据优先于视觉** — 用 `batch_get` 取 JSON 精确数值，不依赖截图目测
4. **审计与修复分离** — 独立审计轮次，避免"既是运动员又是裁判"
5. **先建设施再盖楼** — Phase 1 先把通用组件建完
6. **每阶段都要编译** — 每轮结束必跑 build + simulator 截图验证
7. **规格先行** — Phase 2 产出 spec 后 Phase 3 才能写代码

## 6 阶段工作流

### Phase 0: 设计情报提取

**目标**：在写一行代码之前，把所有"要知道的事"都整理出来。

产出：
- `design_intel.md` — 总报告
- `color_tokens.json`、`typography.json`、`spacing.json`、`shadow_tokens.json`
- `component_catalog.json` — 识别的可复用组件
- `variant_groups.json` — 相同结构的多状态屏幕分组
- `asset_manifest.json` — 图片资源清单
- 所有图片资源已导出到 Assets

详见 `templates/phase0_intel.md`。

### Phase 1: 通用组件层建设

**目标**：屏幕开发开始前，所有可复用组件必须就位，包括弹窗系统。

产出：
- 设计 Token 文件（Colors、Fonts、Spacing 宏/常量）
- 所有通用组件独立文件
- 弹窗系统（基类 + 工厂）
- 基础架构（Base VC / Nav / Tab / Router）

详见 `templates/phase1_common.md`。

### Phase 2: 屏幕规格生成

**目标**：每屏的精确规格文档，作为 Phase 3 编码依据。

产出：
- `specs/{module}.md` — 每模块的规格文档
- `specs/_index.md` — 索引
- `consolidated_specs.md` — 跨屏一致性总览

详见 `templates/phase2_spec.md`。

### Phase 3: 代码实现

**目标**：严格按 spec 实现代码，不得凭感觉写数值。

契约机制：代码里必须标注 spec 字段：
```objc
// spec: loan_confirm.amount_cell.pill_bg = #2A2A2A
container.backgroundColor = kInputBackgroundColor;
```

详见 `templates/phase3_impl.md`。

### Phase 4: 差分审计

**目标**：找出代码和设计的真实差异，不是"觉得不像"。

评分标准：
- >95% = 达标，可进 Phase 6
- 90-95% = 可接受，记录 nice-to-have
- <90% = 必须进 Phase 5

详见 `templates/phase4_audit.md`。

### Phase 5: 最终攻坚

只针对 Phase 4 标记为必须修复的项。完成后重跑 Phase 4 验证。

详见 `templates/phase5_polish.md`。

### Phase 6: Build + Run 验证

- 编译（iOS/Android/Web/Flutter 自适应）
- 启动模拟器/浏览器
- 对每屏截图
- 产出 `FINAL_REPORT.md`

## Agent 分工规则（Full Agent Mode）

按功能模块切分，**永远不要**按"按钮由A改、文字由B改"这种横向切分。推荐切法：

| 模块类型 | 示例 | Agent 数 |
|---------|------|---------|
| 认证流程 | Splash + Login | 1 |
| 主页 + Tab 架构 | Home + TabBar + Nav | 1 |
| 列表页 | Order / 消息 | 1 |
| 个人中心 | Me / Profile + Settings | 1 |
| 业务流程（多步） | KYC / 下单 / 充值 | 1 |
| 业务详情 | Loan / Product / Detail | 1 |
| 次要页面集合 | About / Contact / Feedback 等 | 1 |
| 弹窗/通用 | 在 Phase 1 处理 | 0 |

## 反模式

详见 `reference/anti_patterns.md`。核心要点：

❌ 一个 Agent 搞定所有屏幕 → 结果 17% 相似度
❌ 只看截图对比 → 漏掉精确数值
❌ Phase 2 跳过直接写代码 → 结构错误，Phase 4 才发现
❌ 同 Agent 既修又审 → 盲点
❌ 跨模块修改文件 → 冲突、回滚风险
❌ 弹窗留到最后 → 通用组件不稳导致屏幕反复改
❌ 不编译就宣称完成 → 崩溃到用户面前

## 成功标准

- 整体相似度 ≥ 95%
- 编译零错误
- 主要交互流程可走通
- 所有通用组件可复用
- 代码遵守项目约定

## 迭代预期

| 模式 | 首次生成 | 加审计+攻坚 | 总工时 |
|------|---------|------------|--------|
| Full Agent Mode | ~88% | ~95%+ | 30-60 分钟 |
| Task Mode | ~85% | ~93% | 1-2 小时 |
| Linear Mode | ~83% | ~92% | 2-4 小时 |

## 进一步阅读

- `templates/phase0_intel.md` 到 `phase5_polish.md` — 每 Phase 的 prompt 模板
- `reference/setup_pencil.md` — Pencil MCP 一次性安装指南
- `reference/import_from_figma.md` — Figma 导入 Pencil 步骤
- `reference/anti_patterns.md` — 踩坑经验
- `reference/ios_conventions.md` — iOS 项目约定
- `reference/execution_modes.md` — 三种执行模式详解
- `examples/seacity_loan_app.md` — 完整案例参考
