# Superpowers Core Workflow Specification

> Love Diary 项目开发必须严格遵循以下 Superpowers 核心工作流。
> 任何功能开发、Bug 修复、重构都必须按顺序走完五个阶段，不允许跳步。

---

## Phase 1: Brainstorm（头脑风暴）

**目标**：充分理解需求，探索可能的实现方向，明确约束与边界。

- 用自然语言描述需求，明确「做什么」而非「怎么做」。
- 列出所有不确定点，主动向用户/stakeholder 澄清。
- 至少写出 2 个备选方案，标注各自的优缺点。
- 确认技术约束：兼容性要求、性能指标、依赖限制。
- 产出物：头脑风暴纪要（可内嵌在 SPEC.md 的「背景与方案选型」章节中）。

**出口条件**：需求边界清晰，方案方向已选定，没有模糊地带。

---

## Phase 2: Write SPEC.md（编写规格说明书）

**目标**：将需求固化为可执行、可验收的规格文档。

在 `docs/specs/` 目录下创建 `SPEC-<feature-name>.md`，必须包含以下章节：

1. **概述 (Overview)** — 一句话说明要做什么、为什么做。
2. **用户故事 (User Stories)** — 用 Gherkin 格式编写验收条件：
   ```gherkin
   Feature: <功能名>
     Scenario: <场景描述>
       Given <前置条件>
       When <触发动作>
       Then <预期结果>
   ```
3. **技术方案 (Technical Approach)** — 从 Phase 1 选定的方案，含架构图/数据流描述。
4. **API / 数据模型 (Contracts)** — 接口签名、数据表结构、组件 Props 定义。
5. **边界与异常处理 (Edge Cases & Errors)** — 空状态、加载态、错误态、极限数据量。
6. **验收标准 (Acceptance Criteria)** — 可勾选的 checklist，每一条可被 TDD 测试覆盖。
7. **非功能需求 (Non-Functionals)** — 性能、可访问性 (a11y)、SEO、包体积等。

**出口条件**：任何开发者拿到 SPEC 都能独立完成实现，无需回头问需求方。

---

## Phase 3: Write TASKS.md（编写任务计划表）

**目标**：将 SPEC 拆解为可估算、可按需执行的原子任务。

在 `docs/specs/` 目录下创建 `TASKS-<feature-name>.md`，必须包含：

| 字段 | 说明 |
|---|---|
| **Task ID** | `T-001`, `T-002` ... 全局唯一编号 |
| **描述** | 一句话说明任务内容 |
| **依赖** | 前置 Task ID，无则写 `—` |
| **预估时间** | 用 T-shirt sizing：XS (<1h) / S (1-3h) / M (3-8h) / L (1-2d) |
| **优先级** | P0 (阻塞性) / P1 (高) / P2 (中) / P3 (低) |
| **关联 SPEC 章节** | 可追溯的文档引用 |
| **状态** | Todo / In Progress / Done |

排序规则：P0 > P1 > P2 > P3，同优先级按依赖拓扑排序。

**出口条件**：任务粒度达到「一个任务 = 一个可独立提交的 commit」。

---

## Phase 4: TDD — Test-Driven Development（测试驱动开发）

**目标**：先写失败的测试，再写让测试通过的代码，最后重构。

### Red-Green-Refactor 循环

```
┌──────────────────────────────────────┐
│  RED: Write a failing test          │
│       ↓                             │
│  GREEN: Write minimal code to pass  │
│       ↓                             │
│  REFACTOR: Clean up, keep it green  │
│       ↓                             │
│  (repeat until AC met)              │
└──────────────────────────────────────┘
```

### 规则

- **测试先行**：每写一个任务 (T-XXX)，先写对应的测试用例。
- **最小实现**：只写让测试通过的最少代码，不过度设计。
- **测试分层**：
  - 单元测试：覆盖纯逻辑、工具函数、数据转换。
  - 组件测试：覆盖 UI 渲染、交互行为、Props 组合。
  - 集成测试：覆盖关键用户流程（happy path + 至少 1 条错误路径）。
- **覆盖率要求**：核心业务逻辑 ≥ 80%，UI 组件 ≥ 60%。
- 测试文件与源文件同目录或镜像目录结构。

**出口条件**：所有测试绿色，新增功能有对应的测试覆盖。

---

## Phase 5: Double Self-Review（双重代码自审）

**目标**：在提交 PR 前，开发者自己对代码做两次独立审查。

### Review Pass #1：功能正确性（30 分钟后执行）

换一个视角，假装自己是 Code Reviewer：

- [ ] 对照 SPEC.md 的 Acceptance Criteria，逐条验证是否满足。
- [ ] 手动跑一遍 happy path + 至少 2 条 edge case。
- [ ] 检查 console / error log 是否有未预期的输出。
- [ ] 确认所有 TASKS.md 中的任务状态已更新为 Done。

### Review Pass #2：代码质量（Pass #1 完成后执行）

专注于代码本身的可维护性：

- [ ] **命名**：变量、函数、文件名是否自解释、符合项目惯例。
- [ ] **单一职责**：每个函数/组件只做一件事。
- [ ] **无冗余**：是否引入了不必要的抽象、未使用的 import、死代码。
- [ ] **安全**：用户输入是否校验、XSS/注入是否防护、敏感信息是否泄露。
- [ ] **性能**：是否有不必要的 re-render、重复请求、内存泄漏风险。
- [ ] **可访问性**：语义化 HTML、ARIA 标签、键盘导航、焦点管理。
- [ ] **一致性**：是否遵循 `DESIGN.md` 设计系统规范、项目目录结构约定。

**出口条件**：两份 Review Checklist 全部打勾，方可提交 PR。

---

## Workflow State Machine

```
START
  │
  ▼
[Brainstorm] ──→ [SPEC.md] ──→ [TASKS.md] ──→ [TDD Impl] ──→ [Double Review] ──→ DONE
     │               │              │               │                │
     └── 可回退 ────→┴── 可回退 ───→┴── 可回退 ────→┴── 可回退 ──────┘
```

- 任何时候发现上游有遗漏/错误，允许回退到对应阶段补充。
- 回退必须在 SPEC.md 或 TASKS.md 中留下修订记录。

---

## File Naming & Directory Convention

```
project-root/
├── docs/
│   └── specs/
│       ├── SPEC-<feature-name>.md
│       └── TASKS-<feature-name>.md
├── src/
│   ├── __tests__/          # 或与源文件同目录的 *.test.ts
│   └── ...
├── DESIGN.md               # 设计系统规范
├── CLAUDE.md               # 项目使用手册
└── .clinerules             # 本文件 (Superpowers 工作流)
```

---

*本规范强制执行，不接受例外。如有特殊情况需要跳过某阶段，必须在 commit message 中明确说明原因并获得 Reviewer 认可。*
