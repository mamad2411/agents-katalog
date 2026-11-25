---
name: dart-open-source-projects
description: 筛选高质量的纯 Dart（非 Flutter）开源项目，按上手难易程度排列，每个项目对应一个 Dart 主题技能，帮助学习者在真实项目中巩固 Dart 知识。
metadata:
  model: deepseek-v4-pro
  last_modified: 2026-05-11T13:00:00Z
---

# 纯 Dart 开源项目技能集合

## 项目筛选标准

只收录 **纯 Dart 开发（不依赖 Flutter 框架）** 的开源项目：

- 使用 `language:Dart NOT flutter` 搜索 GitHub
- 排除移动端 UI 框架项目（Flutter widget/packages）
- 优先收录可独立运行的 CLI 工具、服务端框架、通用库

## 难度分级总览

| 等级 | 项目 | GitHub | 关联技能 |
|------|------|--------|---------|
| **L1 入门** | dart-for-beginners-course | [链接](https://github.com/Yczar/dart-for-beginners-course) | [dart-fundamentals](../dart-fundamentals/SKILL.md) |
| **L1 入门** | design-patterns-in-dart | [链接](https://github.com/scottt2/design-patterns-in-dart) | [dart-classes-objects](../dart-classes-objects/SKILL.md) |
| **L1 入门** | google-translator | [链接](https://github.com/gabrielpacheco23/google-translator) | [dart-fundamentals](../dart-fundamentals/SKILL.md) |
| **L1 入门** | common_utils | [链接](https://github.com/Sky24n/common_utils) | [dart-core-libraries](../dart-core-libraries/SKILL.md) |
| **L2 进阶** | formz | [链接](https://github.com/VeryGoodOpenSource/formz) | [dart-type-system](../dart-type-system/SKILL.md) |
| **L2 进阶** | fresh | [链接](https://github.com/felangel/fresh) | [dart-async-concurrency](../dart-async-concurrency/SKILL.md) |
| **L2 进阶** | talker | [链接](https://github.com/Frezyx/talker) | [dart-core-libraries](../dart-core-libraries/SKILL.md) |
| **L2 进阶** | dson | [链接](https://github.com/dart-league/dson) | [dart-core-libraries](../dart-core-libraries/SKILL.md) |
| **L3 高级** | very_good_cli | [链接](https://github.com/VeryGoodOpenSource/very_good_cli) | [dart-packages-pub](../dart-packages-pub/SKILL.md) |
| **L3 高级** | mason | [链接](https://github.com/felangel/mason) | [dart-packages-pub](../dart-packages-pub/SKILL.md) |
| **L3 高级** | dart_frog | [链接](https://github.com/dart-frog-dev/dart_frog) | [dart-async-concurrency](../dart-async-concurrency/SKILL.md) |
| **L3 高级** | image | [链接](https://github.com/brendan-duncan/image) | [dart-core-libraries](../dart-core-libraries/SKILL.md) |

## 推荐学习路线

```
L1 基础语法入门
  → dart-oss-beginners-course (配合 dart-fundamentals)
  → dart-oss-design-patterns (配合 dart-classes-objects)

L2 库与工具进阶
  → dart-oss-common-utils / dart-oss-google-translator
  → dart-oss-formz (类型系统) / dart-oss-fresh (异步)

L3 实战项目
  → dart-oss-dart-frog (后端框架)
  → dart-oss-very-good-cli (CLI 工具)
  → dart-oss-mason (模板引擎)
  → dart-oss-image (底层算法)

## 维护指南

不定期搜索 GitHub 上新出现的纯 Dart 开源项目，手动添加到本集合。

### 搜索策略

**主搜索查询**（GitHub 搜索框或 API）：

```
language:Dart NOT flutter stars:>30
```

**分类搜索**：

| 类别 | 查询 |
|------|------|
| Dart 库/包 | `language:Dart topic:dart-package stars:>30` |
| Dart CLI 工具 | `language:Dart topic:cli topic:dart stars:>10` |
| Dart 服务端 | `language:Dart topic:dart-server stars:>10` |
| 最近更新 | `language:Dart NOT flutter pushed:>2026-01-01 sort:updated` |
| 新兴项目 | `language:Dart NOT flutter stars:10..100 created:>2025-01-01` |

**API 搜索**（获取结构化结果）：

```
https://api.github.com/search/repositories?q=language:Dart+NOT+flutter+stars:>50&sort=stars&order=desc&per_page=30
```

### 筛选规则

| 条件 | 操作 |
|------|------|
| Flutter 项目（含 `flutter` topic / 依赖 flutter SDK） | **排除** |
| 纯 Dart 项目且 Stars > 20 | 加入候选列表 |
| 代码量 < 50 行或仅 README | 排除 |
| 项目已归档（archived） | 排除 |
| 超过 2 年未更新 | 降低优先级 |

### 添加新项目的步骤

#### Step 1: 评估项目

```bash
# 克隆项目，快速评估
git clone --depth 1 <project_url> /tmp/project-eval
# 检查是否依赖 flutter
grep -r "flutter" /tmp/project-eval/pubspec.yaml
# 估算代码量
find /tmp/project-eval -name "*.dart" | xargs wc -l | tail -1
```

#### Step 2: 分级与映射

| 评判维度 | L1 入门 | L2 进阶 | L3 高级 |
|---------|---------|---------|---------|
| 核心代码行数 | < 500 | 500-3000 | > 3000 |
| 依赖复杂度 | 无/少依赖 | 中等 | Monorepo/多包 |
| Dart 特性覆盖 | 基础语法 | 泛型/异步/核心库 | 全栈/底层算法 |
| 架构复杂度 | 单文件/少量文件 | 多模块 | 框架级 |

映射到最相关的 Dart 主题 skill（dart-fundamentals / dart-async-concurrency / dart-core-libraries 等）。

#### Step 3: 创建 Skill 目录和文件

```bash
# 目录命名：dart-oss-<project-key>
mkdir -p skills/dart-open-source-projects/dart-oss-<name>
```

SKILL.md 格式（参见已有文件）：

```yaml
---
name: dart-oss-<name>
description: 学习 <author/project> 开源项目，通过 <描述> 理解 <关联的 Dart 技能>。
metadata:
  model: deepseek-v4-pro
  last_modified: <date>
  related_skills:
    - <dart-topic-skill>
  project:
    url: https://github.com/<author>/<repo>
    stars: <N>
    difficulty: beginner|intermediate|advanced
    category: library|cli|tutorial|framework|patterns
---

# 学习 <Project Name> 项目

## Contents
- [项目概览](#项目概览)
- [与 <related-skill> 的关联](#与-xxx-的关联)
- [项目架构分析](#项目架构分析)
- [核心实现详解](#核心实现详解)
- [Workflow: <学习目标>](#workflow-xxx)
- [Examples](#examples)

## 项目概览
<!-- GitHub 链接、Stars、难度、项目简介 -->

## 与 <related-skill> 的关联
<!-- 用表格列出项目代码中使用的 Dart 特性与对应 skill 主题的映射 -->

## 项目架构分析
<!-- 核心模块、类层级图、数据流 -->

## 核心实现详解
<!-- 关键代码片段和设计模式分析 -->

## Workflow: <学习目标>
<!-- Task Progress 步骤 + 条件逻辑 -->

## Examples
<!-- 从项目中学到的模式 + 延伸练习 -->
```

#### Step 4: 更新集合文件

1. 在 `skills/dart-open-source-projects/SKILL.md` 的难度分级表中添加新行
2. 在 `README.md` 的"纯 Dart 开源项目技能"表中添加新行
3. 运行 `dart analyze` 确认无错误

#### Step 5: 验证清单

- [ ] `dart analyze` 通过
- [ ] SKILL.md 包含正确的 YAML frontmatter（name、description、metadata）
- [ ] 项目确实为纯 Dart（不依赖 Flutter SDK）
- [ ] GitHub 链接有效，Stars 数字准确
- [ ] 映射的关联技能合理
- [ ] README.md 已同步更新
```
