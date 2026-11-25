---
name: grill-me
description: >
  Interview the user relentlessly about a plan or design until reaching shared
  understanding, resolving each branch of the decision tree — while building the
  project's domain model inline: sharpening terminology into CONTEXT.md and
  offering ADRs as decisions crystallise. Use when user wants to stress-test a
  plan, get grilled on their design, or mentions "grill me".
description_zh: 对方案/设计进行穷追式拷问直至达成共享理解，同时内联维护项目领域模型——术语解析即写入 CONTEXT.md 术语表、满足条件时提议 ADR。触发词："grill me"、"拷问"、"压力测试方案"、"评审设计"。
provenance:
  origin: mattpocock-skills (fusion: grill-with-docs + domain-modeling)
  license: MIT
  upstream_url: https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs
  maintained_by: my-skills
---

# Grill Me — 拷问 + 内联文档维护

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## 拷问中的文档维护（融合自 domain-modeling）

拷问过程中，术语与决策一旦明确，**立即内联写入项目文档**——不批量、不拖延。这是拷问的组成部分，不是附加任务：写下来的过程本身就是检验理解的手段。

### CONTEXT.md — 领域术语表（glossary）

- 位置：仓库根 `CONTEXT.md`。多上下文仓库用根 `CONTEXT-MAP.md` 指向各上下文各自的 `CONTEXT.md`。懒创建——第一个术语解析时才建。
- **只放本上下文特有的领域术语**，一条术语一行，格式见 [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md)。
- CONTEXT.md 绝对不含实现细节：不是 spec、不是草稿、不是决策库，只是术语表。
- 拷问中主动做四件事：
  1. **挑战术语冲突** — 用户用词与已有术语冲突时立即指出："你的术语表把 cancellation 定义为 X，但你刚才说的是 Y——是哪个？"
  2. **精炼模糊语言** — 用户用含糊/过载词时提议精确规范词："你说 account——指 Customer 还是 User？这俩是不同的东西。"
  3. **具体场景压力测试** — 领域关系讨论时编造边界场景，逼用户说清概念边界。
  4. **与代码交叉验证** — 用户描述的工作方式与代码矛盾时当场指出："代码里取消的是整个 Order，你刚说支持部分取消——哪个是对的？"

### ADR — 架构决策记录

- 位置：`docs/adr/NNNN-slug.md`，顺序编号，懒创建。
- **三个条件全部满足才提议 ADR**（[ADR-FORMAT.md](./ADR-FORMAT.md)）：
  1. **难逆转** — 事后改主意代价大
  2. **无上下文会惊讶** — 未来读者会疑惑"为什么这么干"
  3. **真实权衡** — 存在真实备选方案，你因具体原因选了其一

  缺任何一条就跳过——容易逆转的会被逆转，不惊讶的没人会问，没有备选的只是"做了显而易见的事"。

- ADR 可短至 1-3 句（背景 + 决定 + 为什么）。价值在记录"决定了什么、为什么"，不在填章节。

## 结束条件

共享理解达成（所有决策分支已解析）即结束；文档已在过程中同步更新，无需额外收尾步骤。
