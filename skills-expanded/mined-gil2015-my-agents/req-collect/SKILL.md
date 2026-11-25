---
name: req-collect
description: 当需要在开始 UI 开发前，从指定文件夹中收集并整理需求资料时使用
---

# 需求收集

## 概述

从指定来源收集、结构化并验证需求，生成下游可直接消费的 `req.md`，并在可确定时补齐当前 mission 的 `module.name`。这个阶段不写业务代码，但要把需求边界、澄清问题和模块标识先收干净。

**核心原则：** 需求必须明确、可测试、无歧义。没有明确证据时，不假设产品意图，也不猜模块目录名。

**违反规则的字面意思就是违反规则的精神。**

## 适用场景

**必须使用：**
- 启动一个新功能模块
- 从产品、PM 或设计侧接到新需求
- 开发过程中需求发生变更或更新
- 需要整合来自多个文件或多轮补充的需求

**例外情况（需征询开发者）：**
- 一次性原型，需求只通过口头传达且不会进入正式模块体系
- 紧急修复（Hotfix），且开发者已明确给出范围和处理方式

觉得“这个需求我已经理解了”？停下来。照样把它结构化。

## 铁律

```text
EVERY UNCLEAR REQUIREMENT MUST BE FLAGGED - NEVER ASSUME PRODUCT INTENT
```

发现了一条模糊的需求？把它标记到 `.ai/missions/{missionId}/reqDocs/issues.md` 中。不要猜测他们的意思，也不要用“常识”补齐模块目录名。

**没有例外：**
- 不要假设“显而易见”的验收标准，让需求方来定义
- 不要自行解读模糊描述，先标记等待澄清
- 不要跳过“看起来很简单”的需求，它们同样需要结构化
- `module.name` 不明确时，不要在 step1 里自创目录名再交给 step2

## 违反后果

若跳过澄清直接进入开发，后续阶段（`ui-dev`、`api-integrate`、`module-test`、`bug-fix`）必须中止并回退到本技能；先补齐 `.ai/missions/{missionId}/reqDocs/req.md`，并让 `config.json.module.name` 达到可用状态后再继续。

## 执行流程

1. `LOAD`：读取 `config.json`、历史 `req.md` / `issues.md`、来源文件和当前轮补充输入。
2. `PARSE`：按模板结构化需求，并尝试确定 `module.name` / `module.displayName`。
3. `VERIFY`：逐条检查需求是否完整、可测试、无歧义。
4. `FLAG`：把所有澄清项写入 `issues.md`，并显式标出未定模块信息。
5. `OUTPUT`：增量更新 `req.md`、按需生成 `issues.md`，并在确认后回写 `config.json.module`。

### 第 1 步：LOAD - 读取需求范围与配置

优先读取以下信息：
- `.ai/missions/{missionId}/config.json`：读取 `reqDocSources`、`moduleRoot`、`module.name`、`module.displayName`
- `.ai/missions/{missionId}/reqDocs/req.md`：如已存在，读取历史 REQ 和顶部模块信息
- `.ai/missions/{missionId}/reqDocs/issues.md`：如已存在，读取历史澄清项
- `reqDocSources` 中配置的文件或目录：需求原文、补充说明、设计文档
- 用户当前提供的文本、图片说明或补充上下文

必须先确认：
- 本轮是首次收集，还是在已有 `req.md` 上增量更新
- `reqDocSources` 中的路径是否真实存在；缺失路径不能被静默忽略
- 当前 mission 是否已经有明确的 `module.name`
- 如果 `module.name` 为空，当前输入里是否已经能唯一确定真实模块目录名

**若上下文来自 mission 目录，至少执行：**
- `test -f ".ai/missions/{missionId}/config.json"`
- `find ".ai/missions/{missionId}" -maxdepth 3 -type f | sort`

**当需求来源来自文件系统时，至少执行：**
- `test -d "{source-folder}"`
- `find "{source-folder}" -type f | sort`
- `find "{source-folder}" -type f -size 0`

### 第 2 步：PARSE - 结构化需求并确定模块标识

将原始内容转换为结构化需求格式，模板参见 `../../references/doc-templates/req-doc-template.md`。

针对每条需求：
- 分配顺序编号：`REQ-001`、`REQ-002`……
- 提取：标题、描述、优先级、UI 参考、API 依赖
- 制定验收标准：每条必须可测试（`AC-001`、`AC-002`……）
- 标记初始状态：`CLEAR` 或 `NEEDS_CLARIFICATION`

模块信息处理规则：
- `config.json.module.name` 已存在时，默认沿用；除非本轮输入明确要求改模块目标
- 当前输入里已给出明确模块目录名时，同步写回 `config.json.module.name`
- 只有业务中文名、页面标题或口头简称时，可填写 `module.displayName`，但不要擅自推导 `module.name`
- `module.name` 仍无法唯一确定时，必须在 `issues.md` 中单独建澄清项，并以 `DONE_WITH_CONCERNS` 收口

### 第 3 步：VERIFY - 检查需求质量

逐条审查结构化后的需求：

| 检查项 | 关注点 |
|-------|-------|
| 完整性 | 是否包含验收标准？ |
| 具体性 | 描述是否足够具体，可以直接实现？ |
| 可测试性 | 每条验收标准能否用“是/否”验证？ |
| 歧义性 | 是否包含“应该”“可能”“理想情况下”“大概”“etc.”“等”？ |
| 范围 | 是否为单一职责，而非多个功能的捆绑？ |
| UI 清晰度 | 是否明确影响哪个页面、组件或交互区域？ |
| 模块信息 | `module.name` 是否已确定，且与已有文档保持一致？ |

### 第 4 步：FLAG - 记录澄清项

对任何标记为 `NEEDS_CLARIFICATION` 的需求：
- 撰写具体问题，不写泛泛的“你什么意思？”
- 在适用时提供可能的解读方案
- 在 `.ai/missions/{missionId}/reqDocs/issues.md` 中按需求分组列出问题

对模块信息未定的情况：
- 单独记录“模块目录名待确认”
- 说明当前已知的业务名称、页面范围和候选信息
- 明确这是阻塞 step2 / step3 的上下文缺口，而不是可以忽略的小问题

### 第 5 步：OUTPUT - 写入需求文档

将结果写入 `.ai/missions/{missionId}/reqDocs/`：

1. `req.md`：所有结构化需求，顶部 `模块名` 与 `模块显示名` 需与 `config.json.module` 保持一致
2. `issues.md`：仅在存在待澄清项时生成或更新

同时维护 `config.json`：
- 只增量更新 `module.name` / `module.displayName`
- 不覆盖其他配置字段
- 如果 `module.name` 仍未确定，保留空值并通过结果状态显式提示

## 速查表

| 阶段 | 关键活动 | 完成标准 |
|------|---------|---------|
| LOAD | 读取配置、旧文档和来源文件 | 需求范围、历史上下文和模块信息清楚 |
| PARSE | 结构化需求、尝试确定模块标识 | 每条需求都有编号和验收标准 |
| VERIFY | 检查清晰度和完整性 | 每条已标记为 `CLEAR` 或 `NEEDS_CLARIFICATION` |
| FLAG | 记录澄清项与模块缺口 | 不清晰项和未定模块信息都已显式建档 |
| OUTPUT | 写入 `req.md` / `issues.md` 并同步 `config.json` | 下游可消费，且不会误用 `missionId` 代替模块名 |

## 常见借口

| 借口 | 现实 |
|------|------|
| “这个需求很明显” | 如果真的明显，结构化它只需几十秒 |
| “写代码时再澄清” | 不清晰的需求会导致返工，先澄清再动手 |
| “设计稿已经说明了” | 设计稿展示的是 UI，不是业务逻辑和边界条件 |
| “先随手起个模块目录名，后面再改” | 目录名一旦进入 step2 / step3，就会扩散到代码和文档 |
| “mission 目录名看起来就能当模块名” | `missionId` 只是任务编号，不代表真实模块目录 |

## 危险信号 - 立即停下来

- 你在凭想象编写 PM 从未描述过的用户场景作为验收标准
- 你没有认真检查就把所有需求标记为 `CLEAR`
- 你因为“这看起来是第 2 阶段的事”而跳过模块标识确认
- 你在没有真实依据的情况下自行发明 `module.name`
- 你把多个独立功能合并成了一条 `REQ`

## 参考文档

| 主题 | 文件 |
|------|------|
| 通用规则 | `../../references/rules/common-rules.md` |
| 需求文档模板 | `../../references/doc-templates/req-doc-template.md` |

## 集成关系

- **输出被以下阶段消费：** `ui-dev`、`api-integrate`、`module-test`、`bug-fix`
