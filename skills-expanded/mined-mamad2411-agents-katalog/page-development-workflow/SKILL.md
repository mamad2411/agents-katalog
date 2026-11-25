---
name: page-development-workflow
description: 从零开发功能页面的标准化工作流。包含需求分析、技术调研、设计文档、实现计划、编码实现和测试验收的完整流程。适用于任何技术栈的页面开发场景。当需要开发新页面、实现设计稿、或按照规范创建功能模块时使用。
---

# 页面开发工作流

通用的功能页面开发标准化流程，适用于任何前端技术栈和项目类型。

## 铁律（不可违反）

1. **禁止跳阶段** — 必须按 Phase 1 → 2 → 3 → 4 → 5 顺序执行，不得跳过任何阶段
2. **禁止直接写代码** — Phase 4 之前不得编写任何业务代码（类型定义、常量、组件、页面均算代码）
3. **每阶段必须等用户确认** — 每个 Phase 完成后，必须向用户展示该阶段产出并等待用户明确确认（如「继续」「可以」「下一步」）才能进入下一个 Phase
4. **无产出不停留** — 每个 Phase 必须产出该阶段规定的交付物，不能空过

> 如果用户说「帮我开发 XX 页面」「实现这个设计稿」「按这个需求写页面」等触发词，**从 Phase 1 开始**，不得直接写代码。

## 快速开始

```
Phase 1: 需求分析 → [用户确认] → Phase 2: 设计文档 → [用户确认] → Phase 3: 实现计划 → [用户确认] → Phase 4: 编码实现 → Phase 5: 测试验收
```

每个 `[用户确认]` 是一个硬性门控：展示当前阶段产出 → 等待用户回复 → 才能进入下一阶段。

## 标准工作流

### Phase 1: 需求分析与技术调研

**收集信息：**
- 设计稿或原型图（Figma、Sketch、Axure 等）
- 产品需求文档（PRD）或功能说明
- 接口文档或 API 规范
- 项目技术栈和开发规范

**确认关键点：**
1. 页面路由路径和文件位置
2. UI 组件库选择（优先复用项目已有组件）
3. 交互逻辑和用户操作流程
4. 数据结构与接口字段映射
5. 状态枚举值与展示映射关系

**技术决策：**
- 是否需要封装独立模块/Hook？
- 使用哪些核心组件？
- API 服务如何组织？
- 状态管理方案选择

**Phase 1 完成标志（必须全部产出）：**
- [ ] 已列出收集到的信息来源（设计稿/PRD/API 文档等）
- [ ] 已确认 5 个关键点并向用户展示
- [ ] 已做出技术决策并向用户说明

> **⛔ 门控：** 向用户展示以上产出，等待用户确认后才能进入 Phase 2。不得自行假设用户同意。

#### GitNexus 代码探索（已有索引的项目）

在需求分析阶段，用 GitNexus 快速了解现有代码结构，避免重复造轮子：

```
1. READ gitnexus://repo/{name}/context    → 检查索引是否最新
2. gitnexus_query({query: "<业务概念>"})  → 找到相关的现有模块和执行流
3. gitnexus_context({name: "<现有组件>"}) → 了解可复用的组件、Hook、服务
```

**用途：**
- 发现可复用的组件、Hook、工具函数
- 了解现有的状态管理模式和 API 服务组织方式
- 避免与现有模块产生命名冲突或职责重叠

**索引状态检查：**

| 情况 | 判断方式 | 处理 |
|------|---------|------|
| 索引不存在 | context 返回 "No index found" | 跑 `npx gitnexus analyze` 建立索引 |
| 索引过期 | context 返回 "Index is stale" | 跑 `npx gitnexus analyze` 重建索引 |
| 索引最新 | context 返回正常数据 | 直接使用 |

> 可用 `npx gitnexus status` 查看索引时间和符号数量，判断是否需要重建。
> 重建后重新 READ `gitnexus://repo/{name}/context` 验证索引已加载。

#### MCP 工具集成

在需求分析阶段，根据用户提供的资源类型，使用对应的 MCP 工具获取详细信息。

详细的工具参数和示例见 `references/mcp-integration.md`。

- **Swagger/API 接口文档** → 使用 `lm-mcp-server` 的 `get_swagger_mcp` 获取接口详情
- **Figma 设计稿** → 使用 `Framelink Figma MCP Server` 的 `get_figma_data` 获取 UI 数据

### Phase 2: 技术方案设计

**用户提供技术文档时：** 审阅并补充实现层面的细节（不重复创建已有内容）。

**用户未提供技术文档时：** 使用 `writing-doc` 技能按「前端功能技术文档模板」创建新文档。

**审阅/补充要点：**

1. **确认路由和文件位置** — 根据项目目录规范确认页面文件路径
2. **细化组件拆分** — 基于页面架构图，明确每个组件的 props、状态和职责边界
3. **确认 hooks 和 utils** — 明确哪些逻辑封装为内部 hook、哪些提取为公共 hook/utils
4. **确认常量和类型** — 检查状态映射、枚举值、TypeScript 类型是否完整
5. **确认接口字段** — 核对 API 请求参数和响应字段的类型定义

**Phase 2 完成标志：**
- [ ] 技术文档已创建或已审阅补充完毕
- [ ] 组件拆分、hooks/utils、常量类型、接口字段均已明确

> **⛔ 门控：** 向用户展示技术文档（或补充内容），等待用户确认后才能进入 Phase 3。

### Phase 3: 制定实现计划

将 Phase 2 的技术文档作为 spec，使用 `superpowers:writing-plans` 技能创建详细的实现计划。

**页面开发的任务顺序（作为 writing-plans 的输入）：**

1. 创建类型定义（TypeScript 接口/类型）
2. 创建常量配置（状态映射、选项列表等）
3. 创建 API 服务层（接口请求封装）
4. **TDD 循环** → 创建数据管理模块（状态管理、业务逻辑）
5. **TDD 循环** → 创建 UI 组件（列表项、卡片等）
6. **TDD 循环** → 实现页面主入口（整合所有组件）
7. 路由配置验证

> **TDD 循环** = 执行此任务时必须使用 `superpowers:test-driven-development` 的红-绿-重构循环（写失败测试 → 最少代码通过 → 重构），无论哪种执行方式。

#### GitNexus 影响面评估（已有索引的项目）

编码前评估新模块对现有代码的影响：

```
gitnexus_impact({target: "<要修改或依赖的现有符号>", direction: "upstream"})
→ d=1（直接破坏）：必须同步更新
→ d=2（可能影响）：需要测试
→ d=3（传递效应）：需要关注
```

**什么时候跑：** 新页面需要修改现有模块（共享组件、服务层、状态管理）时，先评估爆炸半径再动手。

**Phase 3 完成标志：**
- [ ] 实现计划已生成，任务列表包含上述 7 个步骤
- [ ] 执行方式已由用户选择（子代理驱动 / 内联执行 / 直接实现）

> **⛔ 门控：** 向用户展示实现计划，等待用户确认后才能进入 Phase 4。

### Phase 4: 编码实现

**前置条件检查（缺一不可）：**
- ✅ Phase 1 需求分析已完成且用户已确认
- ✅ Phase 2 技术文档已创建/审阅且用户已确认
- ✅ Phase 3 实现计划已生成且用户已确认

> 如果以上任一条件不满足，**禁止编写代码**，回到对应阶段补齐。

按 Phase 3 生成的实现计划逐步执行。执行方式在 writing-plans 的执行交接时由用户选择：

- **子代理驱动**（推荐）— 委托 `superpowers:subagent-driven-development`
- **内联执行** — 委托 `superpowers:executing-plans`
- **简单场景** — 直接按计划步骤顺序实现

**编码纪律：**
- TDD 任务必须按红-绿-重构循环（委托 `superpowers:test-driven-development`）
- 类型定义、常量配置、API 声明等声明式代码按计划直接编写
- 代码示例见 `references/code-examples.md`

### Phase 5: 测试验收

#### 自动化测试门控

使用 `superpowers:verification-before-completion` 的完整门控方法论（运行命令 → 阅读输出 → 带证据陈述结论）。

**页面验收必跑命令：**

```bash
npm test src/pages/page-name/ -- --coverage   # 单元测试
npx tsc --noEmit                                # 类型检查
npx eslint src/pages/page-name/ --fix           # 代码规范
# 有 GitNexus 索引：gitnexus_detect_changes({scope: "staged"})
```

#### 验收清单

**自动化验证（必须有输出证据）：**
- [ ] 所有单元测试通过（0 failures）
- [ ] TDD 红-绿-重构循环已遵循（见 `superpowers:test-driven-development` 验证清单）
- [ ] 覆盖了边界情况（空数据、错误状态、加载状态）
- [ ] TypeScript 类型检查通过（0 errors）
- [ ] ESLint 检查通过（0 errors, 0 warnings）
- [ ] 构建通过（exit 0）

**UI 手动验证：**

#### 步骤 1：给出手动测试入口

说明：[写清楚用户应该访问哪个页面、点击哪个入口、进入哪个模块。]

#### 步骤 2：列出核心测试点

说明：用户至少需要检查这些点：

- [ ] 页面或模块是否能正常打开
- [ ] 文案、标题、按钮、提示信息是否正确
- [ ] 关键交互是否正常，例如点击、切换、展开、关闭、提交
- [ ] 关键状态是否完整，例如默认态、禁用态、空态、错误态
- [ ] 是否存在明显视觉问题，例如错位、遮挡、溢出、闪动
- [ ] UI 还原度符合设计稿
- [ ] 搜索/筛选功能正常
- [ ] 分页/加载更多正常
- [ ] 响应式布局在不同屏幕尺寸下正常
- [ ] hover 状态交互正常
- [ ] loading 状态展示合理
- [ ] empty 空态处理完整
- [ ] error 错误态处理完整
- [ ] 键盘可达性和焦点顺序正确

#### 步骤 3：给出手动验收方式

说明：[写清楚用户如何记录结果，例如"通过/不通过 + 问题截图 + 复现步骤"。]

#### 步骤 4：更新验收结果记录

记录：[说明哪些点已由用户确认，哪些点还需要继续调整。]

红线信号见 `superpowers:verification-before-completion` 和 `superpowers:test-driven-development` 技能。

> **验收失败时：** 回到 Phase 4 修复问题，重新走 Phase 4 → Phase 5 循环，直到所有验收项通过。

#### 代码审查（验收通过后）

验收通过后、进入 Phase 6 之前，使用 `superpowers:requesting-code-review` 派遣 code-reviewer 子代理对页面代码做质量审查。

- Critical/Important 问题修复后，重新走验收 → 审查循环
- Minor 问题记录到 `// TODO(review)` 注释，集中清理

<!-- ### Phase 6: 收尾

验收通过后，使用 `git-commit-conventions` 提交代码，使用 `git-finishing-development-branch` 完成分支集成（合并/PR）。 -->

## 技能集成

### 关联技能

- `superpowers:test-driven-development` — TDD 红-绿-重构纪律的完整方法论；Phase 4 的 TDD 任务委托此技能
- `superpowers:writing-plans` — 实现计划的完整方法论；Phase 3 调用，生成详细计划并引导执行方式选择
- `superpowers:subagent-driven-development` — 子代理驱动执行；Phase 4 推荐方式
- `superpowers:executing-plans` — 内联执行；Phase 4 可选方式
- `superpowers:verification-before-completion` — 提交前验证门控；Phase 5 内联执行
- `superpowers:requesting-code-review` — 代码质量审查；Phase 5 验收通过后调用
- `writing-doc` — 设计文档规范；Phase 2 调用
- `git-commit-conventions` — Git 提交规范；Phase 6 调用
- `git-finishing-development-branch` — 分支集成收尾；Phase 6 调用

### GitNexus 技能集成

当项目已有 GitNexus 索引时，以下技能在各阶段提供增强能力：

| 阶段 | GitNexus 技能 | 用途 |
|------|-------------|------|
| Phase 1 需求分析 | `gitnexus-exploring` | 探索现有代码结构，发现可复用组件 |
| Phase 3 实现计划 | `gitnexus-impact-analysis` | 评估新模块对现有代码的影响范围 |
| Phase 4 编码实现 | `gitnexus-refactoring` | 需要修改现有模块时的安全重构 |
| Phase 5 测试验收 | `gitnexus-cli` | 检查索引状态、验证变更范围 |

> GitNexus 工具参数和示例见 `superpowers:systematic-debugging` 技能的 `references/gitnexus-toolkit.md`。

## 通用规范要点

### 目录结构

```
src/
├── services/              # API 服务层（按业务模块组织）
│   └── module-name/
│       ├── index.ts       # 接口请求方法
│       └── types.ts       # 接口类型定义
└── pages/
    └── page-name/
        ├── index.tsx              # 页面入口
        ├── types.ts               # 页面类型定义
        ├── constants.ts           # 页面常量配置
        ├── hooks/                 # 页面私有逻辑
        │   └── useXxxData.ts
        └── components/            # 页面私有组件
            └── ItemCard/
                ├── index.tsx
                └── types.ts
```

### 设计原则

- **职责分离**：UI 组件、业务逻辑、API 服务分离
- **类型安全**：所有数据流转使用明确的类型定义
- **组件复用**：抽取通用组件，避免重复代码
- **统一规范**：遵循项目代码风格和命名约定
- **样式类名规范**：优先使用 Tailwind 内置类（如 `p-3`、`rounded-xl`、`text-sm`），避免任意值写法（如 `p-[12px]`）；仅当内置类无法精确表达时才使用任意值

### 代码组织

- API 服务统一管理，按业务模块分类
- 类型定义集中维护，避免散落
- 常量配置独立文件，方便维护
- 组件封装适度，避免过度设计

## 适用场景

- 从零开发任何类型的前端页面
- 实现 UI 设计稿（Figma、Sketch、XD 等）
- 按照团队规范创建功能模块
- 重构现有页面结构

## 技术栈参考

本工作流是通用的，代码示例以 **React + TypeScript** 为参考。核心流程适用于：
- React / Vue / Angular 等框架
- Web / 移动端 / 桌面端应用
- TypeScript / JavaScript 项目
- 任何组件库和样式方案
