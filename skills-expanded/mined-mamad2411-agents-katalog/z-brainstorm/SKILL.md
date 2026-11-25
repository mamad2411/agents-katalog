---
name: z-brainstorm
description: 为需要跨会话或多步骤推进的工作，调查代码库、逐题确认需求并落地一份可持久化的规划文档。用于显式调用 z-brainstorm。简单的一次性任务、纯问答或可直接完成的改动不适用，交给代理自身能力即可。
---

# 规划需求

把用户请求转成一份经过确认的规划文档。规划期间可以调查仓库、维护领域词汇，但不修改产品代码。

先解析 Zyes 项目根目录：读取仓库 `AGENTS.md`/`CLAUDE.md` 的 `<!-- zyes:start -->` 受控块。

**未检测到有效配置时不要自动初始化。** 用一句话询问用户：是否要初始化 Zyes 来持久化这次规划？

- 用户同意 → 转 `z-init`，完成后回到本 skill。
- 用户拒绝或只想快速处理 → **停止本 skill**，不创建任何 Zyes 文件，直接用代理自身能力处理需求。

规划文档保存在 `<ZYES_PROJECT_ROOT>/plans/active/`。

## 1. 调查与追问

1. 读取与请求相关的代码、测试、配置、项目文档。
2. 读取 `<ZYES_PROJECT_ROOT>/knowledge/CONTEXT.md`（若存在）和相关 ADR，沿用已定义的领域词汇。
3. 存在需要用户拍板的**实质决策**时，套用 [z-grilling](../z-grilling/SKILL.md) 的规则：一次只问一个问题、能查的事实自己查、每个问题都给推荐答案、达成共同理解前不落地。没有实质决策时不要制造问题。

## 2. 落地规划文档

决策收敛后，向用户展示一份规划摘要（背景、范围、关键决策、验收标准、执行步骤），推荐路径并询问是否落地。用户确认后写入单个文件：

```text
<ZYES_PROJECT_ROOT>/plans/active/YYYY-MM-DD-<slug>.md
```

`slug` 由标题规范化为小写 kebab-case；日期用当前本地日期。同名文件已存在时让用户选择继续该文件或换名，不覆盖。使用以下固定结构；没有内容的小节写 `none`：

```markdown
---
status: ready          # planning | ready | in-progress | done | cancelled
created: YYYY-MM-DD
slug: <slug>
---
# <标题>

## 背景与目标
问题、目标、范围内、范围外。

## 关键决策
- D1: <决策> — 理由（来自追问）

## 验收标准
- [ ] AC1: <可观察的结果>

## 执行步骤
- [ ] 1. <可独立验证的垂直切片>
- [ ] 2. ...

## 进度日志
- （执行阶段由 z-implement 追加：日期 (会话/agent)：做了什么；验证结果；下一步）
```

执行步骤按可独立验证的垂直切片拆分，不要为了凑数拆成琐碎步骤。刚落地、尚未开始执行时 `status` 写 `ready`；仍在追问、决策未定时写 `planning`。

## 3. 维护领域知识（按需）

规划中出现稳定的新业务术语、与既有 glossary 冲突，或产生难以反转的承重架构决策时：

- 术语写入 `<ZYES_PROJECT_ROOT>/knowledge/CONTEXT.md`（只记稳定的业务词汇、含义、边界，不记实现细节或任务范围）。
- 难反转且有实际替代方案的承重决策写入 `knowledge/adr/NNNN-<slug>.md`，记录 Context / Decision / Alternatives / Consequences。普通实现取舍不建 ADR。
- 文件和目录按需懒创建，没有内容时静默跳过。

## 衔接

落地文档后报告文件绝对路径和 `status`，说明可用 `z-implement` 开始执行。实现开始后若出现实质范围变化，新建一份规划文档，不改写已在执行或已完成的旧文档。
