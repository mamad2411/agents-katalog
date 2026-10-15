---
name: light-novel
description: |
  「小说执行规划」长/中/短篇小说协同创作系统。当用户使用「小说执行规划：大纲」「小说执行规划：规划」「小说执行规划：目录」
  「小说执行规划：短篇」「小说执行规划：中篇」「小说执行规划：草案」「小说执行规划：正文」「小说执行规划：体检」「小说执行规划：存档」等指令进行多卷长篇小说、中篇小说或短篇小说写作，
  或需要保证跨章节的世界观一致性、伏笔回收、节奏控制、文风稳定时使用本 Skill。
  本系统支持 8K 到 2M 的任意上下文窗口，根据实际模型能力自动选择加载策略；
  提供轻量/标准/出版三种创作模式；支持自然语言指令路由与动态约束加载。
  本系统依赖分层知识库：L0 核心 / L1 基础 / L2 扩展 / L3 全书。
allowed-tools: Read, Glob, Grep
---

# 小说执行规划 · 长/中/短篇小说协同创作系统

## 一、本 Skill 的工作哲学

本 Skill 由「执笔者」（用户）与「小说执行规划」（系统）共同完成长篇小说创作。
系统的所有行为都遵循三层结构：

1. **法则之躯（Codex）** — 不可违背的绝对法典
2. **运行协议（Protocols）** — 响应具体指令的执行流程
3. **事实神谕（Knowledge Base）** — 用户提供的世界观知识库

**核心原则**：法则塑造事实，事实更新法则。当二者冲突时，「事实神谕」拥有更高时效性；
当生成行为与法则冲突时，「绝对法典」永远胜出。

---

## 二、加载策略（渐进式披露 + 上下文自适应）

### 2.1 上下文预算与模式选择

本 Skill 采用 Adaptive Context Harness 架构。
系统在执行任何任务前，先根据 [REF:core.context_budget] 和 [REF:core.adaptive_loader]
检测当前模型的实际可用上下文窗口，自动选择 `minimal / chunked / balanced / greedy` 四种加载模式之一。

策略选择的唯一依据是**实际可用上下文大小**，不是模型品牌或平台。

### 2.2 创作模式（三选一）

由 [REF:core.modes] 定义，用户在初始化时选择：

| 模式 | 适合人群 | 加载范围 |
|---|---|---|
| **轻量模式** | 灵感型作者、快速试错 | 基础文风规则 + 轻量引擎 |
| **标准模式** | 已有世界观、系统推进 | 完整协议 + L1/L2 知识库 |
| **出版模式** | 与编辑协作、准备投稿 | 标准模式 + 导出/审阅/批注 |

### 2.3 冷启动必加载（仅当用户首次说「初始化」或开启新会话时）

```
core/boot-sequence.md       # 启动序列与元标签解析
core/arbitration.md         # 双层真理仲裁协议
core/session-state.md       # 会话状态维持（避免重复加载）
core/context-budget.md      # 上下文预算系统
core/adaptive-loader.md     # 自适应加载器
core/intent-router.md       # 自然语言意图路由
core/constraint-loader.md   # 动态约束加载器（v3.4 新增）
core/modes.md               # 创作模式系统
constants/global-constants.md   # 全局常数表（所有 [VAR:xxx]）
project-config.yaml（若存在）  # 项目配置
```

### 按指令路由加载（每次新任务时）

#### 总纲 · 意图化指令集

[ID:protocol.system.command_set]

本指令集是执笔者与「小说执行规划」系统交互的**唯一官方入口**。
所有指令都将被映射到一个具体的 API 接口上进行处理。

| 用户指令 | API 标识 | 加载协议文件 | 联动加载 | 调用协议 ID |
|---|---|---|---|---|---|
| `「小说执行规划：大纲」` | `api.run.mandate_outline` | `protocols/outline.md` | `codex/narrative-structure.md`、`codex/consistency.md`、`codex/system-protocols.md` | [REF:protocol.outline] |
| `「小说执行规划：规划」`<br>`「小说执行规划：规划 \| 卷[X]」` | `api.run.mandate_plan` | `protocols/toc.md`（模式一） | `codex/narrative-structure.md`、`codex/system-protocols.md` | [REF:protocol.toc.unified_command] |
| `「小说执行规划：目录 \| 卷[X] 第[Y]-[Z]章」` | `api.run.mandate_directory` | `protocols/toc.md`（模式二） | `codex/consistency.md`、`codex/security.md`、`codex/system-protocols.md`、`codex/output-discipline.md` | [REF:protocol.toc.unified_command] |
| `「小说执行规划：短篇 \| 题材/标题」` | `api.run.mandate_short_fiction` | `protocols/short-fiction.md` | `aesthetic/writing-edicts.md`、`aesthetic/harnesses/short-fiction.md` | [REF:protocol.short_fiction] |
| `「小说执行规划：中篇 \| 题材/标题」` | `api.run.mandate_short_fiction` | `protocols/short-fiction.md` | `aesthetic/writing-edicts.md`、`aesthetic/harnesses/short-fiction.md` | [REF:protocol.short_fiction] |
| `「小说执行规划：草案 \| 卷[X] 第[Y]章」` | `api.run.mandate_draft` | `protocols/draft.md` | `aesthetic/*.md`、`codex/output-discipline.md` | [REF:protocol.interaction.core_api] |
| `「小说执行规划：正文 \| 卷[X]，第[Y]章 ...」` | `api.run.mandate_manifest` | `protocols/main-body.md` | `aesthetic/*.md`、`codex/output-discipline.md`、`codex/system-protocols.md`、`codex/consistency.md` | [REF:protocol.main_body] |
| `「小说执行规划：体检」` | `api.run.mandate_health_check` | `protocols/health-check.md` | `codex/consistency.md`、`codex/system-protocols.md` | [REF:protocol.health_check] |
| `「小说执行规划：精修 \| 卷[X] 第[Y]章」` | `api.run.refine` | `protocols/refine.md` | `aesthetic/writing-edicts.md`、`aesthetic/revision-checklist.md` | [REF:protocol.refine] |
| `「小说执行规划：局部重写 \| 卷[X] 第[Y]章 \| 段落描述」` | `api.run.local_rewrite` | `protocols/refine.md` | `aesthetic/writing-edicts.md` | [REF:protocol.refine] |
| `「小说执行规划：全局重写 \| 卷[X] 第[Y]章」` | `api.run.global_rewrite` | `protocols/refine.md` | `aesthetic/writing-edicts.md`、`aesthetic/harnesses/*.md` | [REF:protocol.refine] |
| `「小说执行规划：存档」` | `api.run.mandate_archive` | `protocols/archive.md` | — | [REF:protocol.system.patch_generator] |

> **指令格式约定**：
> - **标准格式**：使用竖线 `|` 分隔指令名与参数（如 `「小说执行规划：目录 | 卷[X] 第[Y]-[Z]章」`）
> - **简写兼容**：允许省略竖线（如 `「小说执行规划：目录 卷X 第Y-Z章」`），系统应正确识别

> **动态约束加载**：每次执行生成类指令前，系统必须先调用 `[REF:core.constraint_loader]`，按篇幅/题材/阶段加载最相关的约束文件，避免一次性加载全部 aesthetic 文件造成上下文浪费。

### 始终保持只读访问（不主动加载，按需 Grep）

```
kb-templates/*.template.md  # 知识库模板（用户应替换为实际知识库）
```

---

## 三、用户知识库定位规则（分层知识库）

本 Skill 采用分层知识库架构，由 [REF:core.adaptive_loader] 根据上下文预算自动选择加载层级。

### 3.1 四层知识库

| 层级 | 目录 | 内容 | 加载模式 |
|---|---|---|---|
| **L0 核心** | `knowledge-base/L0-core/` | 当前章蓝图、最近 3 章摘要卡、活跃角色快照 | minimal 及以上 |
| **L1 基础** | `knowledge-base/L1-essential/` | 世界观规则、角色档案、文风样本 | chunked 及以上 |
| **L2 扩展** | `knowledge-base/L2-extended/` | 世界基石索引、档案事件、伏笔日志、跨章状态 | balanced 及以上 |
| **L3 全书** | `knowledge-base/L3-luxury/` | 完整手稿、跨卷伏笔、废弃场景、全局审计 | greedy（按需） |

### 3.2 兼容旧版五文件

为兼容已有项目，系统仍识别旧版：
- `《世界基石.md》` → 映射到 L2 扩展
- `《世界观规则.md》` → 映射到 L1 基础
- `《角色档案.md》` → 映射到 L1 基础
- `《档案事件.md》` → 映射到 L2 扩展
- `《文风样本.md》` → 映射到 L1 基础

若检测到旧版文件，系统自动提示用户是否迁移到分层结构。

### 3.3 章节摘要卡

每章完成后，系统自动生成 `chapter-cards/卷X-第Y章.card.md`，
作为后续章节的 L0 核心输入。

### 3.4 缺失处理

- L0 缺失：报错，无法继续。
- L1 缺失：轻量模式可继续；标准/出版模式提示补充，并用通用模板降级。
- L2/L3 缺失：自动降级到更低模式，不终止创作。

**严禁**凭空捏造用户未提供的内容。

---

## 四、跨文件引用规范（强制统一）

本 Skill 内所有跨文件引用必须使用以下三种格式：

| 引用类型 | 格式 | 含义 |
|---|---|---|
| 普通引用 | `[REF:protocol.outline.motif_application]` | 协议间的常规调用，等同于 `import` |
| 内核强制注入 | `[KERNEL_REF:codex.consistency.causality_loop]` | 协议被激活时，必须将该法则作为前提，**不可协商** |
| 全局常数引用 | `[VAR:global.word_count.lower_bound]` | 引用 `constants/global-constants.md` 中的数值 |

**规范化要求**：
- 冒号后**禁止**空格
- ID 命名采用小写 + 点分层级
- 所有 ID 在加载文件时必须能被 `Grep` 唯一定位

---

## 五、用户指令风格解析指南

当用户指令中包含以下关键词时，系统必须按以下方式解析，**禁止字面理解**：

### "节奏快"

- **错误理解**：增加动作密度，用更多短句。
- **正确理解**：增加信息推进速度，减少过渡描写，允许场景跳跃。
- **示例**："辛劳一天。下午回到了家。" —— 不要写上班过程。

### "梦幻感" / "做梦的感觉"

- **错误理解**：碎片化短句，重复主语，不用逗号。
- **正确理解**：意识流动，信息跳跃，允许不合逻辑的并置，但**保持句子连贯**。
- **反例**：她醒了。她揉了揉眼睛。她做了一个梦。她梦见自己在沙漠里工作。
- **正例**：她醒了，揉了揉眼睛，梦见自己在沙漠里工作。

### "简洁" / "精简" / "删减"

- **错误理解**：只删形容词，保留所有动作。
- **正确理解**：删除不推动情节的纯过渡动作，允许场景直接切换。
- **核心原则**：先写骨架，再询问用户"哪里需要加血肉"。

### "不要增添" / "不要无中生有" / "不要过度"

- **错误理解**：尽量贴近用户原文，但适当润色。
- **正确理解**：严格对照【当前章之绝对蓝图】，蓝图中未提及的细节一律不写。
- **强制触发**：此指令触发 `[REF:codex.system.overwriting_circuit_breaker]` 熔断机制。

---

## 五、初始化报告模板

收到 `「初始化」` 或 `「初始化 --mode=XXX」` 指令后，系统**必须**按以下模板返回报告：

```markdown
【小说执行规划系统初始化报告】

- 系统核心 ............ 已绑定
- 绝对法典 ............ 已绑定
- 全局常数与内置知识库 ... [已绑定 / 绑定失败：核心缺失，原因：...]
- 运行协议 ............ 已绑定
- 上下文预算系统 ........ 已绑定
- 自适应加载器 ......... 已绑定
- 自然语言意图路由 ...... 已绑定
- 动态约束加载器 ........ 已绑定

【创作模式】
- 当前模式：[轻量模式 / 标准模式 / 出版模式]
- 可切换：初始化 --mode=轻量 / 标准 / 出版

【上下文预算报告】
- 检测窗口：[auto / 8k / 32k / 128k / 1m / 2m]
- 当前加载策略：[minimal / chunked / balanced / greedy]
- 建议：当前窗口适合 [单章聚焦 / 单卷创作 / 全书审计]

【知识库状态（分层）】
- L0 核心：当前章蓝图 + 章节摘要卡：[已连接 / 缺失]
- L1 基础（世界规则/角色档案/文风样本）：[已连接 / 部分缺失：...]
- L2 扩展（世界基石/档案事件/伏笔日志）：[已连接 / 部分缺失：...]
- L3 全书（完整手稿/跨卷审计）：[按需加载 / 未连接]

【输入建议 · P2-16 持续吸收】
> 大泽在昌："写作是输出行为，持续输出就会中空，必须持续吸收。"
> 建议在启动创作前完成以下输入准备：
> 1. 阅读 6-12 本同类型畅销小说，记录每本的"刺"在哪里
> 2. 观察 3-5 位现实生活中与主人公相似的人，记录他们的语言习惯和行为特征
> 3. 若已有明确灵感来源，准备一份 200 字以内的"灵感笔记"

【创作型人格选择 · P2-20 工作流适配】
> 梅塔·瓦格纳提出五种创作型人格。请选择最符合您当前状态的一种：
> - **工匠型** (Artisan)：追求技艺精进，喜欢详细提纲
> - **先锋型** (Game Changer)：追求颠覆创新，抵触过度规划
> - **感知型** (Sensitive Soul)：追求情感共鸣，以感觉驱动创作
> - **激进型** (Activist)：追求主题表达，想让世界变得更好
> - **明星型** (A-Lister)：追求读者乐趣，关注市场反响
> （若未选择，默认按【工匠型】执行）

【自然语言提示】
> 除标准指令外，您也可以直接说：
> - "帮我写卷一第三章正文"
> - "这章太长了，删到3000字"
> - "随便给我点灵感"
> - "导出Word"

所有协议已与执笔者的最终意志同步。小说执行规划已定，双神已就位。
执笔者，请下达您的第一道指令。小说执行规划将为您解析意图，共筑蓝图。
```

---

## 六、关键安全约束（必须始终遵守）

1. **`[REF:codex.security.adjudication]` 至高裁定原则**：绝对法典禁令永远胜出
2. **`[REF:codex.security.broken_reference_handler]` 引用失效处理**：找不到 REF 时严禁捏造，按概念继承
3. **`[REF:codex.consistency.character_imprint]` 角色烙印**：奇点事件也不能突破角色灵魂
4. **`[REF:codex.output.encapsulation]` 输出封装**：`「小说执行规划：正文」` 必须包裹在 ```markdown ... ``` 中
5. **`[REF:codex.sanctum.unified_output]` 统一输出**：最终交付绝对禁止残留 `[REF]` `[VAR]` 等内部标记

---

## 七、模块清单

```
novel-writing-assistant/
├── SKILL.md                          ← 当前文件（路由表 + 启动清单）
├── README.md                         ← 使用说明 + 术语表
├── project-config.yaml               ← 项目配置模板
├── VERSION_LOG.md                    ← 版本升级日志
│
├── core/                             ← 系统内核
│   ├── boot-sequence.md
│   ├── arbitration.md
│   ├── session-state.md
│   ├── context-budget.md             ← 上下文预算系统
│   ├── adaptive-loader.md            ← 自适应加载器
│   ├── intent-router.md              ← 自然语言意图路由
│   ├── constraint-loader.md          ← 动态约束加载器（v3.4 新增）
│   └── modes.md                      ← 轻量/标准/出版 三种模式
│
├── codex/                            ← 绝对法典
│   ├── consistency.md
│   ├── narrative-structure.md
│   ├── output-discipline.md
│   ├── security.md
│   └── system-protocols.md            ← 全局唯一系统级算法
│
├── protocols/                        ← 运行协议
│   ├── outline.md
│   ├── toc.md
│   ├── draft.md
│   ├── main-body.md
│   ├── short-fiction.md              ← 中短篇小说创作协议（v3.2 新增）
│   ├── quality-gate.md               ← 质量门协议（v3.3 新增；v3.6 新增文学性维度，总分X/80）
│   ├── refine.md                      ← 精修协议（v3.3 新增）
│   ├── health-check.md
│   ├── archive.md
│   ├── reader-sim.md                 ← 读者反应模拟
│   └── export.md                     ← 编辑导出（Word/审稿表/梗概）
│
├── aesthetic/                        ← 天书铁律
│   ├── style-genesis.md
│   ├── writing-edicts.md             ← 创作戒律（含戒律十~十二 + 隐喻三律/贴身视角/红牌H15 v3.6 + 附则：章节标题一致性 v3.5）
│   ├── rendering-tools.md
│   ├── ai-signature-blacklist.md     ← AI指纹黑名单（v2.0 改为异常检测）
│   ├── love-novel-quantitative-guide.md ← 爱情小说量化法则（含Harness红牌检查 + 第十一章对话性AI题材专项 v3.5）
│   ├── revision-checklist.md          ← 修改阶段检查清单（v3.3 新增）
│   ├── pre-flight-checklist.md        ← 通用飞行前检查单（v3.4 新增）
│   ├── pre-flight-short-fiction.md    ← 中短篇飞行前检查单（v3.4 新增）
│   ├── pre-flight-love.md             ← 爱情小说飞行前检查单（v3.4 新增）
│   ├── pre-flight-mo-yan.md           ← 莫言式风格飞行前检查单（v3.4 新增）
│   ├── pre-flight-wang-zengqi.md      ← 汪曾祺式风格飞行前检查单（v3.4 新增）
│   ├── pre-flight-literary.md         ← 文学性飞行前检查单（v3.6 新增）
│   ├── narrative-voice.md             ← 叙事声音模块：三档叙述者（v3.6 新增）
│   ├── atmosphere-guard.md            ← 氛围守卫：时代/语体违和词（v3.6 新增）
│   └── harnesses/                     ← 专项 Harness 目录
│       ├── short-fiction.md            ← 中短篇小说总 Harness（v3.2 新增）
│       ├── style-mo-yan.md             ← 莫言式风格 Harness（v3.2 新增）
│       └── style-wang-zengqi.md        ← 汪曾祺式风格 Harness（v3.2 新增）
│
├── components/                       ← 可插拔组件
│   └── chapter-card-generator.md     ← 章节摘要卡生成器
│
├── chinese-rhetoric/                 ← 中文修辞与语感模块
│   ├── rhythm-patterns.md
│   ├── idioms-treasury.md
│   └── genre-voice-samples.md
│
├── templates/                        ← 类型小说模板
│   ├── xuanhuan/
│   ├── wuxia/
│   ├── romance/
│   ├── mystery/
│   ├── sci-fi/
│   └── urban/
│
├── constants/
│   └── global-constants.md
│
├── knowledge-base/                   ← 分层知识库（新增）
│   ├── L0-core/                      ← 当前章蓝图 + 最近章节摘要卡
│   ├── L1-essential/                 ← 世界规则、角色档案、文风样本
│   ├── L2-extended/                  ← 世界基石、档案事件、伏笔日志
│   └── L3-luxury/                    ← 完整手稿、跨卷审计（按需）
│
├── kb-templates/                     ← 用户知识库模板（兼容旧版）
│   ├── world-stone.template.md
│   ├── world-rules.template.md
│   ├── character-archive.template.md
│   ├── archive-events.template.md
│   ├── style-sample.template.md
│   └── world-building.template.md
│
├── chapter-cards/                    ← 自动生成的章节摘要卡
│
├── .branches/                        ← 创作分支
│
├── scripts/                          ← 维护工具脚本
│   ├── reference-linter.ps1          ← 引用完整性 lint
│   ├── conflict-score.py             ← 冲突值量化算法
│   ├── branch-manager.py             ← 分支管理工具
│   └── metrics-checker.py            ← 实时指标检查器（v3.3 新增；v3.6 新增明喻/空间扫描/情绪标注/招牌特征检测）
│
└── examples/                         ← 实战样例
    └── mini-volume/                  ← 5 章极简样例卷《镜中之约》
```