---
name: dart-book-distillation
description: 将 Dart 主题书籍蒸馏为一组可执行的 Agent Skills，让书中方法论真正用起来。基于 cangjie-skill 的 book2skill 元技能，适配 Dart 学习生态。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-14T10:00:00Z
---
# 蒸馏 Dart 书籍为一组可执行 Skills

基于 cangjie-skill 的 book2skill 元技能，将 Dart/Flutter 主题书籍中的方法论、最佳实践、设计模式和编程范型，拆解为一组**原子化、可被 agent 在真实场景下调用**的 skills。

## Contents
- [何时调用此技能](#何时调用此技能)
- [输入要求](#输入要求)
- [核心方法论](#核心方法论)
- [输出结构](#输出结构)
- [执行流程](#执行流程)
- [Dart 领域引导](#dart-领域引导)
- [Workflow: 蒸馏一本 Dart 书籍](#workflow-蒸馏一本-dart-书籍)
- [Examples](#examples)

## 何时调用此技能

用户说类似：
- "帮我把《Dart Apprentice》拆成 skills"
- "蒸馏这本 Flutter 书"
- "把这本 Dart 书的方法论做成可用 skill"
- "distill this dart book into skills"

## 输入要求

在开始前**必须**从用户处确认：
1. **书的文本来源**：PDF / EPUB / TXT 文件路径，或可访问的纯文本。**不要**在没有文本的情况下凭记忆拆书。
2. **书名 + 作者 + 出版年**：用于目录命名和审计。
3. **是否首次试点**：建议先拆 1 本验证流程再批量。

## 核心方法论：RIA-TV++

一个六阶段 + 并行提取 + 三重验证 + 压力测试的流水线：

```
阶段 0: Adler 整书理解     → BOOK_OVERVIEW.md
阶段 1: 5 个 agent 并行提取 → 候选方法论单元池
阶段 1.5: 三重验证筛选       → 通过的单元
阶段 2: RIA++ 构造 skill     → 每个 skill 的 SKILL.md
阶段 3: Zettelkasten 链接    → INDEX.md（单书索引）
阶段 4: 压力测试             → test-prompts.json + 回炉淘汰
```

**边界**：
- 做：方法论 / 决策框架 / 清单 / 原则 / 概念体系的蒸馏
- 不做：书摘 / 读后感 / 作者人设角色扮演

## 输出结构

```
books/<book-slug>/
├── BOOK_OVERVIEW.md           # 阶段 0 产出：主旨/骨架/术语/批判
├── INDEX.md                   # 阶段 3 产出：skill 总览 + 引用图
├── candidates/                # 阶段 1 产出：原始候选池（审计用）
├── rejected/                  # 阶段 1.5 淘汰的单元 + 原因（审计用）
├── <skill-slug-1>/
│   ├── SKILL.md
│   └── test-prompts.json
├── <skill-slug-2>/
│   └── ...
```

## 执行流程

### 阶段 0 — 整书理解

1. 读取用户提供的书本文本。大文件分块阅读。
2. 执行 Adler 四步阅读法（结构 → 解释 → 批判 → 应用）。
3. 输出 `books/<slug>/BOOK_OVERVIEW.md`，包含：
   - **主旨**：用 1-3 句话概括全书核心论点
   - **骨架**：章节结构 + 逻辑脉络（用 Mermaid 流程图或列表）
   - **术语表**：关键概念的原文 + 解释
   - **批判**：本书的局限性、作者可能存在的盲点、与其他 Dart 资源的互补关系
4. 展示产出给用户确认："骨架理解对了吗？有没有希望重点突出的方向？"

### 阶段 1 — 5 个 Sub-Agent 并行提取

**并行启动** 5 个提取器，各自独立读书并输出到 `books/<slug>/candidates/`：

| 提取器 | 职责 | 产出文件 |
|--------|------|----------|
| 框架提取器 | 决策框架 / 思维模型 / 设计模式 | `framework.md` |
| 原则提取器 | 原则 / 清单 / 编码规则 | `principle.md` |
| 案例提取器 | 作者亲自使用过的实例（带代码） | `case.md` |
| 反例提取器 | 失败模式 / 反模式 / 警告 | `counter-example.md` |
| 术语提取器 | 领域术语词典 | `glossary.md` |

### 阶段 1.5 — 三重验证筛选

对每个候选单元执行三道验证：

- **V1 跨域验证**：书中至少 2 个独立段落有佐证？
- **V2 预测力验证**：能用它回答一个书里没明说的新问题吗？
- **V3 独特性验证**：不是任何 Dart 开发者都能想出的常识吗？

通过的进入阶段 2。不通过的写入 `books/<slug>/rejected/` 并附原因，保留审计轨迹。

### 阶段 2 — RIA++ 构造 Skill

对每个通过的单元，构建 SKILL.md：

- **R (Reading)**：原文引用（≤150 字/段）
- **I (Interpretation)**：用自己的话重写方法论骨架
- **A1 (Past Application)**：书中作者用过的案例
- **A2 (Future Trigger)** ★：用户什么情境下会需要 → skill 的 `description` 字段
- **E (Execution)**：1-2-3 可执行步骤
- **B (Boundary)**：什么时候不适用 / 作者盲点

每个 SKILL.md 遵循 studydart-skills 格式规范：

```yaml
---
name: dart-book-<book-slug>-<skill-slug>
description: ...
metadata:
  model: deepseek-v4-pro
  last_modified: ...
  tags: [dart, <domain-tag>]
  source_book: <book-slug>
---
# 标题

## Contents
## 方法论说明
## Workflow
## Examples
```

### 阶段 3 — 知识链接

为蒸馏出的所有 skills 生成 `books/<slug>/INDEX.md`，包含：
- 所有 skill 名称和描述
- 引用关系图（哪几个 skill 相互依赖或补充）
- Dart 领域标签映射

同时更新全局索引 `books/INDEX.md`，新增本书条目。

### 阶段 4 — 压力测试

1. 为每个 skill 生成 `test-prompts.json`，包含 3-5 个测试用例
2. 使用 agent 运行测试：给定 prompt → 调用 skill → 验证输出是否可用
3. 不通过的 skill 标注问题并回炉修正
4. 三次修正仍不通过的标记为 `[遗留]` 并说明原因

## Dart 领域引导

### 推荐蒸馏书单

参考 `resources/dart_books.yaml` 获取推荐书单。适合蒸馏的 Dart/Flutter 书籍特征：
- 有明确的方法论和可操作模式（而非 API 速查手册）
- 包含作者的实际决策案例
- 有独特的见解（非主流共识的复述）

### 领域标签映射

蒸馏产出的 skills 自动附加 Dart 领域标签，与现有学习技能对齐：

| 标签 | 对应技能 | 触发特征 |
|------|----------|----------|
| `fundamentals` | dart-fundamentals | 变量、控制流、函数、库 |
| `type-system` | dart-type-system | 泛型、Record、类型别名、类型安全 |
| `classes-objects` | dart-classes-objects | 类设计、继承、mixin、扩展方法 |
| `pattern-matching` | dart-pattern-matching | 模式匹配、switch 表达式、解构 |
| `null-safety` | dart-null-safety | 空安全、nullable、null-aware |
| `async-concurrency` | dart-async-concurrency | Future、Stream、Isolate、并发 |
| `collections-iterables` | dart-collections-iterables | 集合操作、迭代器、数据变换 |
| `core-libraries` | dart-core-libraries | dart:io、dart:convert、dart:math |
| `packages-pub` | dart-packages-pub | 包管理、发布、工作空间 |
| `effective-dart` | dart-effective-dart | 代码风格、文档、API 设计 |

### 蒸馏过程中的领域提示

- **识别 Dart 版本**：区分 Dart 2.x 和 Dart 3.x 的特性（如模式匹配、sealed class 在 Dart 3 才引入）
- **关联官方文档**：在 SKILL.md 中添加 `resources:` 引用 dart.cn 对应章节
- **避免过时模式**：如果书中的代码示例使用了已被替代的写法（如 `new` 关键字），在 SKILL.md 中标注并给出 Dart 3 等效写法

## Workflow: 蒸馏一本 Dart 书籍

### Task Progress

- [ ] **Step 1: 收集信息。** 确认书名、作者、出版年、文本来源。从 `resources/dart_books.yaml` 查找是否已有引导信息。
- [ ] **Step 2: 阶段 0 — 整书理解。** 分块读取全书文本，输出 `BOOK_OVERVIEW.md`（主旨 + 骨架 + 术语表 + 批判）。
- [ ] **Step 3: 用户确认。** 展示 BOOK_OVERVIEW，确认骨架理解正确，获取重点方向。
- [ ] **Step 4: 阶段 1 — 并行提取。** 同时启动 5 个提取器（框架/原则/案例/反例/术语），各自输出到 `candidates/`。
- [ ] **Step 5: 阶段 1.5 — 验证筛选。** 对每个候选执行三重验证，通过的进入阶段 2，淘汰的写入 `rejected/`。
- [ ] **Step 6: 阶段 2 — 构造 Skill。** 对每个通过单元，按 RIA++ 框架生成 `SKILL.md`，附加 Dart 领域标签。
- [ ] **Step 7: 阶段 3 — 知识链接。** 生成 `INDEX.md`（单书索引），更新 `books/INDEX.md`（全局索引）。
- [ ] **Step 8: 阶段 4 — 压力测试。** 生成 `test-prompts.json`，运行测试，回炉修正或标记遗留。
- [ ] **Step 9: 展示成果。** 汇总产出：N 个 skill 通过 / M 个回炉 / K 个淘汰。提示用户后续使用方式。

### 条件逻辑

- **如果用户未提供文本来源**：停止并提示要求。不凭记忆拆书。
- **如果文本超过 10 万字符**：分批处理，每批 2-3 万字，阶段间汇报进度。
- **如果候选单元少于 5 个**：提示用户这本书可能不适合蒸馏（或让用户指定关注章节）。
- **如果蒸馏的 skill 与现有 skills/ 下的主题重叠**：在 INDEX.md 中标注关联关系，提示用户对比。
- **如果书籍是面向 Flutter 的**：额外使用 `flutter` 标签，关联 Flutter 相关知识图谱。
- **如果书籍代码使用 Dart 2.x 语法**：在 SKILL.md 中标注并给出 Dart 3 等效写法。

## Examples

### 蒸馏《Dart Apprentice》示例命令

```bash
# 用户在 agent 中说：
帮我蒸馏 books/Dart_Apprentice.pdf，这是一本Dart入门书

# Agent 执行：
1. 阶段 0 → books/dart-apprentice/BOOK_OVERVIEW.md
2. 确认骨架
3. 阶段 1 → books/dart-apprentice/candidates/{framework,principle,case,...}.md
4. 阶段 1.5 → 验证筛选，淘汰常识性内容
5. 阶段 2 → books/dart-apprentice/{dart-var-final-const,dart-null-safety-intro,...}/SKILL.md
6. 阶段 3 → books/dart-apprentice/INDEX.md + 更新 books/INDEX.md
7. 阶段 4 → 压力测试，通过 8 个 / 回炉 2 个 / 淘汰 3 个
```

### SKILL.md 产出示例（节选）

```yaml
---
name: dart-book-dart-apprentice-var-declaration
description: 根据场景选择正确的变量声明方式（var/final/const/late），避免类型推断陷阱
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-14T10:00:00Z
  tags: [dart, fundamentals]
  source_book: dart-apprentice
---
# 变量声明选择指南

## 选择矩阵

| 场景 | 推荐声明 |
|------|----------|
| 局部可变变量 | `var` |
| 局部不可变量 | `final` |
| 编译时常量 | `const` |
| 延迟初始化 | `late` |

## Workflow: 选择正确的变量声明

- [ ] 1. 变量值会变？ → `var`
- [ ] 2. 运行时确定但不变？ → `final`
- [ ] 3. 编译时已知？ → `const`
- [ ] 4. 延迟初始化？ → `late`

## Examples

// 来自书中案例并给出 Dart 3 等效写法
```
