---
name: dart-book-distillation
description: 将 Dart/Flutter 主题书籍蒸馏为一组可执行的 Agent Skills，让书中方法论真正用起来。基于 cangjie-skill 的 book2skill 元技能。
license: MIT
compatibility: Requires book text source (PDF/EPUB/TXT).
metadata:
  author: studydart-skills
  version: "1.0"
  based_on: cangjie-skill (book2skill)
---
# 蒸馏 Dart 书籍为一组可执行 Skills

基于 cangjie-skill 的 book2skill 元技能，将 Dart/Flutter 主题书籍中的方法论、最佳实践、设计模式和编程范型，拆解为一组**原子化、可被 agent 在真实场景下调用**的 skills。

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
   - **骨架**：章节结构 + 逻辑脉络
   - **术语表**：关键概念的原文 + 解释
   - **批判**：本书的局限性、作者盲点、与 Dart 资源的互补关系
4. 展示产出给用户确认后再进入阶段 1。

### 阶段 1 — 5 个 Sub-Agent 并行提取

并行启动 5 个提取器，各自独立读书并输出到 `books/<slug>/candidates/`：

| 提取器 | 职责 | 产出文件 |
|--------|------|----------|
| 框架提取器 | 决策框架 / 思维模型 / 设计模式 | `framework.md` |
| 原则提取器 | 原则 / 清单 / 编码规则 | `principle.md` |
| 案例提取器 | 作者使用过的实例（带代码） | `case.md` |
| 反例提取器 | 失败模式 / 反模式 / 警告 | `counter-example.md` |
| 术语提取器 | 领域术语词典 | `glossary.md` |

### 阶段 1.5 — 三重验证筛选

- **V1 跨域验证**：书中至少 2 个独立段落有佐证？
- **V2 预测力验证**：能回答书里没明说的新问题吗？
- **V3 独特性验证**：不是任何 Dart 开发者都能想到的常识吗？

通过的进入阶段 2。不通过的写入 `books/<slug>/rejected/` 并附原因。

### 阶段 2 — RIA++ 构造 Skill

对每个通过的单元构建 SKILL.md（R=原文引用, I=用自己的话解释, A1=书中案例, A2=触发情境, E=可执行步骤, B=边界条件）。产出的 SKILL.md 遵循 studydart-skills 格式规范。

### 阶段 3 — 知识链接

生成单书索引 `books/<slug>/INDEX.md` 并更新全局索引 `books/INDEX.md`。

### 阶段 4 — 压力测试

为每个 skill 生成测试用例，运行验证，不通过的标记回炉。

## Dart 领域引导

蒸馏时根据书籍内容自动附加领域标签。推荐蒸馏书单见 `resources/dart_books.yaml`。

| 标签 | 对应技能 | 触发特征 |
|------|----------|----------|
| `fundamentals` | dart-fundamentals | 变量、控制流、函数、库 |
| `type-system` | dart-type-system | 泛型、Record、类型安全 |
| `classes-objects` | dart-classes-objects | 类设计、继承、mixin |
| `pattern-matching` | dart-pattern-matching | 模式匹配、switch 表达式 |
| `null-safety` | dart-null-safety | 空安全、nullable |
| `async-concurrency` | dart-async-concurrency | Future、Stream、Isolate |
| `collections-iterables` | dart-collections-iterables | 集合操作、Iterable |
| `core-libraries` | dart-core-libraries | dart:io、dart:convert |
| `packages-pub` | dart-packages-pub | 包管理、发布 |
| `effective-dart` | dart-effective-dart | 代码风格、API 设计 |

### 蒸馏提示

- **识别 Dart 版本**：区分 Dart 2.x 和 Dart 3.x 特性
- **关联官方文档**：在 SKILL.md 中引用 dart.cn 对应章节
- **避免过时模式**：标注已替代的写法并给出 Dart 3 等效写法
- **不凭记忆拆书**：没有文本来源就停下来问用户要
- **保留审计轨迹**：candidates/ 和 rejected/ 都要留

## 最佳实践

- **先试点 1 本** — 除非用户明确说批量
- **阶段之间主动汇报进度** — 不要静默跑完再 dump 结果
- **永远先确认骨架** — 阶段 0 产出必须经用户确认再继续
