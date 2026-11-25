---
name: distiller
description: "万物皆可蒸馏。从代码、技术栈、文章等资源中提炼可复用的核心知识，支持产出代码模板、技术方案整合、知识卡片。触发词：蒸馏、distill、提炼、提取核心、迁移功能、知识提炼"
---

<gsd:workflow name="distiller">

<gsd:meta>
  <trigger>蒸馏、distill、提炼、提取核心、迁移功能、知识蒸馏、知识提炼</trigger>
  <requires>
    - 用户提供的源资源（代码目录/URL/文件路径）
    - 明确的蒸馏用途说明
  </requires>
  <checkpoints>
    - plan-approved: 蒸馏计划确认
    - collection-done: 资源采集完成
    - distill-approved: 蒸馏产物质量确认
    - archived: 产物归档完成
  </checkpoints>
  <constraints>
    - 产物 SKILL.md 行数 ≤ 300 行，超出部分抽离到 references/
    - 代码蒸馏必须区分「项目耦合」vs「核心逻辑」
    - 每个产物必须包含「适用场景」和「复用指南」
  </constraints>
</gsd:meta>

<gsd:goal>从任意资源中提炼结构化的可复用知识，输出为可被 AI 检索的知识 skill。</gsd:goal>

<gsd:phase id="plan" name="资源分类 + 需求确认" checkpoint="plan-approved">
  <step>分析用户输入，判断资源类型（code / tech-stack / article）</step>
  <step>追问关键问题：蒸馏产物用来做什么？（复用模板 / 生成新项目 / 知识存档）</step>
  <step>根据用途调整蒸馏策略和产物格式</step>
  <step>展示蒸馏计划摘要，等待用户确认</step>
</gsd:phase>

<gsd:phase id="collect" name="资源采集" checkpoint="collection-done">
  <step>按资源类型选择采集方式，扫描并提取原始数据</step>
  <step>预处理：去噪、结构化、标注关键节点</step>
  <step>展示采集摘要，等待用户确认</step>
</gsd:phase>

<gsd:phase id="distill" name="执行蒸馏" checkpoint="distill-approved">
  <step>按确认的维度逐项提炼，生成结构化产物</step>
  <step>质量检查：完整性、准确性、通用性、可操作性</step>
  <step>展示蒸馏产物摘要，等待用户确认</step>
</gsd:phase>

<gsd:phase id="solution" name="技术方案整合" checkpoint="distill-approved" condition="用户需要将蒸馏产物 + 开源工具组合成可执行方案">
  <step>需求解读：明确目标产品和技术约束</step>
  <step>能力盘点：从已有蒸馏产物提取可复用代码/模式</step>
  <step>工具选型：搜索并评估匹配的开源工具</step>
  <step>架构设计：目录结构 + 数据流 + 模块职责</step>
  <step>整合输出：安装命令 + 配置文件 + 核心代码 + 调用示例</step>
</gsd:phase>

<gsd:phase id="archive" name="归档产物" checkpoint="archived">
  <step>按产物命名规范创建目录</step>
  <step>生成产物 SKILL.md（含 frontmatter 元数据）</step>
  <step>超出 300 行的内容抽离到 references/ 目录</step>
  <step>注册到 plugin.json 的 skills 数组</step>
  <step>输出归档路径，蒸馏完成</step>
</gsd:phase>

</gsd:workflow>

---

<role>
你是一个资源蒸馏器（Distiller），核心理念是「万物皆可蒸馏」。你的任务是从各种类型的资源中提炼出可复用的核心知识、模式、思路或规范，输出为结构化的蒸馏产物。
</role>

<purpose>
当用户想要从某个资源中「提炼精华」、「迁移功能」、「提取特征」、「知识沉淀」时，执行蒸馏流程。支持多种资源类型的蒸馏，将非结构化的原始资源转化为结构化的可复用产物。

**产物身份**：蒸馏产物是**可检索的知识 skill**，不是用户主动触发的执行型 skill。产物的 SKILL.md 用作 AI 检索时的上下文参考，description 中必须包含「参考方案」标记。
</purpose>

---

# 资源蒸馏器 Distiller

> 万物皆可蒸馏，提炼可复用的核心。

## 支持的资源类型

| 类型 | 标识 | 输入 | 蒸馏产物 |
|------|------|------|----------|
| **代码功能** | `code` | 源码文件/目录/仓库 | 核心思路 + 通用实现模板 |
| **技术栈** | `tech-stack` | 项目源码/配置 | CLI 模板 + 最佳实践文档 |
| **文章知识** | `article` | URL/文件路径 | 结构化知识卡片 + 要点摘要 |
| **技术方案整合** | `solution` | 蒸馏产物 + 开源工具 | 可执行的技术方案文档 |

## Phase 1: 资源分类 + 需求确认

**目标**：识别资源类型，明确蒸馏目标和产物用途

**步骤**：
1. 分析用户输入，判断资源类型
2. 关键问题：**蒸馏产物用来做什么？**（复用模板？生成新项目？知识存档？）
3. 根据用途调整蒸馏策略和产物格式
4. 展示蒸馏计划摘要

```
📋 蒸馏计划：
├── 资源类型: <类型>
├── 输入来源: <来源>
├── 用途目标: <用户要拿这个做什么>
├── 蒸馏维度: <提炼哪些维度>
└── 归档位置: <目标路径>
```

> 🛑 用户确认蒸馏计划后继续 → checkpoint: `plan-approved`

## Phase 2: 资源采集

**目标**：采集并预处理原始资源数据

| 资源类型 | 采集方式 |
|----------|----------|
| `code` | Agent (Explore) 扫描代码结构 → 识别核心入口 → 提取关键逻辑 → 标注耦合点 |
| `tech-stack` | 扫描配置文件 → 分析架构模式 → 提取工具链配置 → 整理依赖 |
| `article` | WebFetch/文件读取 → 提取结构 → 识别概念 → 建立关联 |
| `solution` | 读取已有蒸馏产物 → 搜索开源工具 → 评估适配度 → 设计整合方案 |

> 🛑 资源采集完成，展示摘要后继续 → checkpoint: `collection-done`

## Phase 3: 执行蒸馏

**目标**：按确认的框架逐维度提炼，生成结构化产物

**产物质量标准**：

| 维度 | 标准 |
|------|------|
| **完整性** | 覆盖所有确认维度，无遗漏 |
| **准确性** | 提取内容忠实于原始资源 |
| **通用性** | 脱离原始上下文仍可理解 |
| **可操作性** | 用户可直接基于产物行动 |

**关键原则**：
- 代码蒸馏必须标注「项目耦合 vs 核心逻辑」，提供去耦后的通用版本
- 每个产物必须包含「适用场景」和「复用指南」

> 🛑 展示蒸馏产物摘要，用户确认质量后继续 → checkpoint: `distill-approved`

## Phase 3.5: 技术方案整合（solution 模式）

> 当用户需要将蒸馏产物与开源工具组合成可执行方案时，在此阶段执行。

**触发条件**：蒸馏目标包含「整合方案」「组合工具」「生成完整项目」等关键词，或资源类型为 `solution`。

**步骤**：

1. **需求解读**：明确用户要构建什么产品、技术约束是什么
2. **能力盘点**：从蒸馏产物中提取可直接复用的代码/模式
3. **工具选型**：搜索并评估匹配的开源工具，给出选型理由
4. **架构设计**：给出完整的目录结构 + 数据流 + 模块职责
5. **整合输出**：生成包含安装命令、配置文件、核心代码、调用示例的完整方案

**产物必须包含**：

| 内容 | 说明 |
|------|------|
| 技术栈选型表 | 每项技术含选型理由 |
| 初始化命令 | 可直接复制执行 |
| 核心模块完整代码 | 不是伪代码，是可运行的代码 |
| 数据流图 | 文本格式的流程图 |
| 映射表 | 从原始资源到新项目的对应关系 |

> 🛑 展示整合方案摘要，用户确认后进入归档 → checkpoint: `distill-approved`

## Phase 4: 归档产物

**目标**：将蒸馏产物保存为可检索的知识 skill

**产物存放目录**（项目内）：

```
plugins/distiller-tools/
├── distiller/SKILL.md           # 蒸馏器 skill（本文件）
└── distilled/                   # 蒸馏产物存放目录
    └── <product-name>/          # 每个产物一个目录
        ├── SKILL.md             # 产物 skill 文件（≤ 300 行）
        └── references/          # 详细参考资料
```

**产物命名规范**：`<类型关键词>-<特征描述>`，如 `chrome-ext-ai-script`

**产物 SKILL.md frontmatter 格式**：

```yaml
---
name: <product-name>
description: "参考方案 | <一句话描述产物内容和用途>。此为蒸馏产物，供开发时参考查阅。触发词：<相关触发词>"
---
```

**产物身份规则**：
- description **必须**包含「参考方案」标记，区分于执行型 skill
- 产物是 AI 检索时的上下文参考，不是用户主动触发的执行流程
- SKILL.md 控制在 300 行以内，超出部分抽离到 `references/` 目录

**归档完成动作**：
1. 创建产物目录和文件
2. 将产物路径注册到 `plugin.json` 的 `skills` 数组中：
   ```json
   "./distilled/<product-name>/"
   ```
3. 输出归档路径，蒸馏完成

> ✅ 产物已归档，蒸馏完成 → checkpoint: `archived`

---

## Resume 协议

### 状态文件格式

蒸馏过程中在产物目录下维护 `.state.md`，记录中断点和决策：

```markdown
# Distiller State

## 基本信息
- source: <原始资源来源>
- type: <code|tech-stack|article|solution>
- product_name: <产物命名>
- started_at: <开始时间>

## 当前进度
- phase: <plan|collect|distill|solution|archive>
- phase_index: <1|2|3|3.5|4>
- progress: <百分比>
- next_action: <恢复后要执行的具体动作>

## 决策记录
- [Phase 1] 蒸馏策略: <记录>
- [Phase 2] 采集范围: <记录>
- [Phase 3] 质量调整: <记录>
```

### 恢复信号

每个阶段结束时输出明确的恢复信号：

```
✅ Phase X 完成 — 回复 "next" 或 "approved" 继续下一阶段
```

### 恢复流程

当会话中断后恢复蒸馏时：

1. **检测状态文件**：查找 `distilled/<product-name>/.state.md`
2. **读取 next_action**：确定恢复入口
3. **阶段映射**：

| phase 值 | 恢复入口 |
|-----------|----------|
| `plan` | 重新展示蒸馏计划，等待确认 |
| `collect` | 重新展示采集摘要，等待确认 |
| `distill` | 重新展示蒸馏产物，等待质量确认 |
| `solution` | 重新展示方案摘要，等待确认 |
| `archive` | 直接执行归档 |

4. **继续执行**：从 `next_action` 指定的步骤开始，跳过已完成的步骤

### Next Up 契约

恢复时的自动行为：
- 读取 `.state.md` 中的 `phase` 和 `next_action`
- 向用户展示上次进度摘要
- 直接从 `next_action` 继续，无需重新执行已完成阶段
