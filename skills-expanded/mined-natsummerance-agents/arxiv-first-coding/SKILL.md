---
name: arxiv-first-coding
description: |
  编码前先查 arXiv 先行文献：把要实现的技术机制（缓存/共识/检索/排序/训练技巧等）映射到 arXiv 类目，真实抓取论文、逐篇隔离阅读、打分聚类，收敛为一条带引用的实现路径（含第一步、承重风险与避坑清单）。触发场景：动手实现非平凡算法或机制前问"有没有人解决过/state of the art 是什么/我是不是在重新造轮子"；用户显式要求查 prior art 或搜相关论文。不适用于：整个项目的技术栈/供应商/成本选型（走 advise-project-approach）、学术论文文本润色（走 academic-humanizer）、CRUD 胶水代码或用户已点名具体方案"就按简单方式做"的已收敛请求。
source_project: UditAkhourii/neuroarxiv
tags: [arxiv, prior-art, literature-review, architecture-decision, research-before-code]
---

# arxiv-first-coding（编码前 arXiv 先行文献检索）

## R (Reading) — 源项目核心设计

> "Real papers, fetched over real HTTP, read in isolation so no source anchors another, converged into ONE recommendation — cited, with a first step and the known ways this has already gone wrong for somebody else."
> "NeuroArxiv caught a withdrawn proof it had cited and declined to rely on it... Cold and web-search both produced real, reasonable answers — neither produced that."

（来源：`README.md`；评测细节见 `EVALS.md`）

## I (Interpretation) — 方法论骨架

核心洞察：开发者浪费的时间大多不是不会写代码，而是在没查过"难题是否已被发表并踩过坑"的情况下直接开写。本方法不是搜索封装——搜索给你一堆来源，它强制你基于来源做出**一个决定**。

1. **预检三问**：有技术机制可研究吗？要投入真实精力吗？方法还开放吗？任一为否即放弃全流程。
2. **分类映射**：问题 → 3~5 个 arXiv 类目 + 3~6 个机制词（"cache invalidation"，不是"caching system"）。
3. **真实抓取**：对 export.arxiv.org 发真 HTTP 请求，字段照录不生成——每条 id/标题/摘要都是真实元数据。
4. **隔离发散**：每篇论文一个并行独立读，只见这一篇的摘要——见过邻居摘要的读会开始总结"集合"而非扎根于眼前那篇。
5. **打分聚类**：relevance / practicality / rigor 三维评分 + trap/strength 配对，按底层架构角度聚类。
6. **收敛一条路**：拒绝"给你 4 篇你自己挑"，承诺单一推荐路径 + 落选簇的真实取舍 + 从**所有**论文 limitation 汇总的避坑清单。

## A1 (Past Application) — 源项目的典型应用

### 案例: LLM 补全社会化缓存机制选型
- **输入**: `"cache LLM completions across requests without serving stale answers"`（上游 quickstart 原题）。
- **做法**: 映射到 cs.DC/cs.DB/cs.LG 等类目逐个抓取 → 每篇并行隔离读出 approach/borrow/limitation → 打分聚成"失效策略派/免共识派/学习式索引派"等簇 → 选 relevance×practicality 最强的一簇收敛。
- **结果**: 输出 THE PATH：4~8 句实现草图 + 真实引文（id+标题+url+角色）+ 第一步 + 承重风险 + 取自全部 limitation 的 avoid 清单；评测中同类流程曾抓住"已撤回证明"与"仅在单上下文长度验证过的 benchmark 结果"并在推荐前标记。

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. 实现前查新："我要写一个分布式限流/一致性哈希/重排算法，有没有现成的学术方案？不想自己重新踩坑"——猜错的代价是重构而不是 typo。
2. 架构拍板焦虑："这个机制是不是已经有人解决了？state of the art 到哪了？我在造轮子吗？"——需要文献证据支撑 go/no-go。
3. 显式调用：用户点名 `/arxiv-first-coding` 或明说"先帮我查查相关论文再动手"——跳过预检直接进流程。

### 语言信号
- "有没有人做过 / 已经解决过这个问题吗 / 我是不是在造轮子"
- "state of the art / SOTA / 先行研究 / prior art"
- "实现之前先看看相关论文 / 查查文献"
- "XX 机制有什么已有方案 / 学术界怎么解这个问题"
- "设计缓存/共识/检索/排序/训练策略，怕踩已知的坑"

### 与兄弟 skill 的区分
- vs `advise-project-approach`: 本 skill 处理**单一技术机制的文献决策**——读论文、收敛一条实现路径；advise-project-approach 处理**项目级工程判断**——约束分析、可比项目、技术栈/供应商/成本与 build plan。问"这个算法怎么实现最好、有没有论文"来这里，问"我该项目用什么栈怎么规划"去那里。
- vs `academic-humanizer`: 论文文本的表达润色完全归 academic-humanizer；本 skill 只检索和消化文献做工程决策，不改任何写作。

## E (Execution) — 可执行步骤

1. **预检三问** — 有技术机制吗？要投入真实精力吗（会锚定架构、返工昂贵）？方法开放吗（用户未点名算法/库）？完成标准: 三问全过进入 Phase 1，任一不过则放弃并最多附一句"可用 /arxiv-first-coding <problem> 显式检查"。
2. **分类映射** — 把问题映射到 3~5 个 arXiv 类目 id 和 3~6 个机制级搜索词。完成标准: 类目与搜索词成对列出且均为机制词，纯商业框架问题也给出尽力技术角度。
3. **真实抓取** — 用 WebFetch 对 export.arxiv.org API 逐类目串行请求（间隔数秒），逐 `<entry>` 照录 id/标题/摘要/作者/日期/链接；某类目不足 2 条时去掉搜索词重试一次。完成标准: 零虚构条目，结果稀薄时如实报告而非凑数。
4. **隔离发散** — 每篇论文一个并行独立 Agent 读，只喂"问题+该篇摘要"，产出 `{approach, borrow, limitation, relevanceNote}` JSON，禁止连续引用超几个词。完成标准: 任一读出现"compared to the other papers"类交叉污染表述即废弃单独重跑。
5. **打分聚类** — 每篇按 relevance/practicality/rigor 评 0~10 并配 `[rel8 prac6 rig7]` 式分数；trap 必须与 strength 配对；按架构角度聚成 3~6 簇。完成标准: 每篇有分数，每簇有架构角度命名（非关键词分组）。
6. **收敛一条路** — 选一簇输出：4~8 句实现草图、引文清单（id+标题+url+角色）、第一个具体步骤、承重风险、取自**所有**论文 limitation 的 avoid 清单、每个落选簇一句话真实取舍、一个开放问题。完成标准: THE PATH 六要素齐备，禁止以"这里有 3 个好选项你挑"收尾。
7. **反幻觉自查** — 核对所有数字/主张均可溯源到抓取到的摘要原文，拿不准的重抓而非凭标题推断。完成标准: 引文与抓取记录一一对应，无任何超出摘要支撑面的结论。

## B (Boundary) — 边界

### 不适用场景（≥2条）
- 项目级选型与规划（技术栈对比、供应商成本、repo review、build plan）→ 走 `advise-project-approach`：那是多准则工程判断，不是单机制文献检索。
- CRUD、胶水代码、变量命名、接两个现成 SDK，或用户已点名具体算法/库/说"just 用简单方式实现"→ 方法已收敛，重开文献流程纯属浪费。
- 学术论文/提案的文本润色与去 AI 痕迹 → 走 `academic-humanizer`。

### 已知局限 / 失败模式（≥1条真实的）
- **只读摘要不读全文**: borrow/avoid 结论停留在摘要可支撑的层面，实现细节仍需回到原文核实。
- **arXiv-only 检索网较窄**: 上游自评承认 5 题中 2 题引文广度输给通用 web search；工程实践类问题可能需补充官方文档检索。
- **成本高**: 约 N+4 次 Agent 调用（N 通常 12~20）加串行 HTTP 抓取，不适合每个小决策，只用于"错了要重建"级别的选择。
- **无网络不可运行核心循环**: 抓不到时如实报告无法检索，绝不凭记忆编造论文。

## 相关 skills
- contrasts-with: advise-project-approach（单机制文献决策 vs 项目级选型规划；互设诱饵：项目选型让位给它）
- contrasts-with: academic-humanizer（文献检索消化 vs 论文表达润色）

---

## 审计信息
- **验证**: V1 ✓ / V2 ✓ / V3 ✓
- **蒸馏时间**: 2026-08-25；**来源**: local `vendor/UditAkhourii__neuroarxiv/` 下 `README.md`、`skills/neuroarxiv/SKILL.md`（评测结论引自 README 对 `EVALS.md` 的汇总）
