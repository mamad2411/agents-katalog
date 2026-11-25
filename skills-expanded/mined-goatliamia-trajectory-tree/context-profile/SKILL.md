---
name: context-profile
description: 分析当前上下文和工具配置，结合实际使用判断保留与调整。
---

选择一个可确认的切点，解释模型此刻获得了哪些材料和能力、它们怎样支持当前任务，并给出明确的保留、精简或启停出口。

Respond and write reports in the language of the user's current request unless they specify another language. Preserve native evidence, paths, identifiers and arguments verbatim.

## 取证入口

- **从 Eval 加载项或文本对照选区进入**：草稿已内联所选加载项的来源、加载阶段、token 估算及相同文本片段的行号与摘录。对带有本地文件路径的条目（如 `AGENTS.md`、个人/项目 `SKILL.md`），直接按行号读取源文件核对上下文；需要查看动态注入或未展开项的完整快照正文时，再读取草稿给出的选区快照 JSON。
- **从会话直接进入**：使用 `trajectory_inspect` 的 `view: "cost"`（配合 `groupBy: "definition"` 查看工具声明体积、版本变化与调用次数）和 `view: "context"`（查看七类上下文构成、压缩边界与 Skill 加载记录），必要时用 `trajectory_read` 读取对应请求头或指令记录。

## 分析步骤与三类明确出口

**1. 还原当前有效供给并对应用途。** 区分常驻系统提示、全局与项目 `AGENTS.md`、已激活工具声明、Skill 目录（常驻）与 Skill 正文（按需加载）、运行时动态注入。核对主要材料承担的是硬性约束、环境事实、操作规程还是示例，以及近期关联任务中的实际使用情况。

**2. 按问题类型收口到具体出口：**
- **文本重合与冲突（Overlap 出口）**：对照双方的加载阶段与职责：
  - *常驻 × 常驻重复*（如个人指令与项目指令、或两份常驻说明重复）→ **合并去重**：指明保留哪一处、删除哪一处的具体文件路径与行号区间；
  - *常驻 × 按需 Skill 正文重复* → **常驻瘦身**：常驻位置只保留 1 句触发条件与 Skill 名称索引，详细执行步骤下沉到 Skill 正文按需加载；
  - *条款冲突或过期* → **对齐事实**：以当前代码库和运行环境为准，直接给出改写或移除过期条款的 diff 草案。
- **工具与插件启停（Capability 启停出口）**：
  - **严禁建议修改宿主官方工具的源码、参数定义或内置工具说明（不得改动官方工具语义）**；
  - 对观察窗口内未见使用或常驻占用较高的官方/插件工具，**必须先向用户阐述清楚该工具的核心职责、主流适用任务与低频兜底场景，在明确用户的真实任务需求后，给出关闭（停用）或保留该工具的建议**；
  - 对项目自有工具，可建议精简定义或调整返回结构。
- **Skill 整理与发现优化（Skill 出口）**：
  - *有相关任务但未被触发* → 将真实任务中的高频特征词补入 `description` / `whenToUse`；
  - *目录常驻描述过长* → 压缩 `description` / `whenToUse`，将长正文拆入 `references/`；
  - *当前工作范围不再承担该类任务* → 阐述该 Skill 职责后，建议在当前配置中关闭。

通用处置原则参考[处置与知识保留](../trace-analysis/references/disposition.md)，动态材料更新参考[上下文持续使用](../trace-analysis/references/context.md)，工具开销参考[用量与能力投入](../trace-analysis/references/cost.md)，验证方法沿用[综合诊断的验证方法](../trace-analysis/SKILL.md#验证改法)。需要交付独立报告时按[报告写作](../../report/WRITING.md)组织。
