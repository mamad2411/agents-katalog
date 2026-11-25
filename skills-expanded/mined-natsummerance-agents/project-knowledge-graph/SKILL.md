---
name: project-knowledge-graph
description: |
  基于 graphify（Graphify-Labs/graphify，多模态知识图谱生成器）做项目/语料的知识图谱
  构建：当用户接手陌生大型代码库要先摸清结构枢纽、要把代码+文档+论文+截图等异构语料
  织成统一概念网络、或要给后续 agent 会话留下可增量更新的 wiki/图谱导航层时触发。
  边界：不做动态对话记忆与用户画像、不做经验 SOP 沉淀；小语料（≤6 文件）收益有限需
  如实告知。
source_project: Graphify-Labs/graphify
tags: [knowledge-graph, codebase-onboarding, multimodal, tree-sitter, leiden, wiki]
---

# project-knowledge-graph

## R | 引用

> "Fully multimodal. Drop in code, PDFs, markdown, screenshots, diagrams, whiteboard
> photos — graphify uses Claude vision to extract concepts and relationships from all of
> it and connects them into one graph. … 71.5x fewer tokens per query vs reading the raw
> files, persistent across sessions, honest about what it found vs guessed."

来源：<https://raw.githubusercontent.com/Graphify-Labs/graphify/main/README.md>（2026-08-25 抓取）

## I | 骨架

- 定位一句话：对「死的语料」做一次性+可持续的结构化——把文件堆变成可查询的概念网络，与对话型记忆四兄弟正交。
- 入口形态：Claude Code skill，`/graphify .` 对任意文件夹生效（代码库、笔记、论文皆可）。
- 多模态抽取矩阵：代码 = tree-sitter AST + call-graph pass（无需 LLM）；docs = Claude 概念抽取；PDF = 引用挖掘 + 概念抽取；图片 = Claude vision（含非英文图内文字）。
- 边来源三级诚实标注：每条边标 `EXTRACTED` / `INFERRED` / `AMBIGUOUS`——永远分得清「找到的」和「猜的」。
- 五件产物（graphify-out/）：graph.html 交互图、obsidian/ vault、wiki/（agent 可爬的 index.md + 社区文章）、GRAPH_REPORT.md（god nodes、surprising connections、suggested questions）、graph.json + SHA256 cache。
- 增量机制：`--update` 只重处理变更文件并合并；`--watch` 后台自动同步（代码改动秒级纯 AST 重建）；`graphify hook install` post-commit 自动重建。
- 导出与查询：query / path / explain 子命令；--svg/--graphml/--neo4j(cypher)/--mcp。
- 技术栈：NetworkX + Leiden 社区检测 + vis.js，全本地运行，不需要 Neo4j。

## A1 | 案例

接手一份陌生混合语料：52 个文件 = 若干 Karpathy 仓库源码 + 5 篇论文 + 4 张架构截图。动作：

1. `pip install graphifyy && graphify install` 装好 Claude Code skill；
2. `/graphify . --mode deep` 首跑，产出 GRAPH_REPORT.md；
3. 读报告：god node 是 attention 机制（几乎所有节点经由它相连），一条 surprising connection 把仓库里的优化器代码连到了某篇论文的 3.2 节；
4. 抽检 INFERRED 边：发现两条过度连接，降档重跑确认；
5. `--wiki` 生成 index.md，交给下一个会话的 agent 导航，全程不再通读原文件。

验收：README 实测同规模语料查询 token 缩减 71.5x；新 agent 仅凭 wiki 能答出模块职责与关键枢纽。

## A2★ | 适用判定

情境一（触发）：「刚接手一个巨大的陌生代码库，先帮我搞清楚核心模块和关系」——onboarding 摸底是第一触发场景。
情境二（触发）：「把这批异构材料（代码+论文+白板照片）织成一张概念网络，找出跨域联系」——多模态统一建图独此一家。
情境三（触发）：「给项目留一个后续每个 agent 会话都能接着用的导航层」——wiki/graph.json + watch/hook 增量归口在此。

语言信号（命中任意一条即倾向触发）：
- 「知识图谱」「codebase 结构图」「模块依赖关系」「god node」
- 「概念网络」「跨文档联系」「graphify」
- 「项目 wiki」「agent 可爬的知识库」「大仓库 onboarding」

与兄弟区分：
- 本组另外三个兄弟全部面向「活的交互」（用户偏好 mem0-memory-layer、对话事实召回 hindsight-retrieval、操作经验沉淀 agent-experience-persistence）；本 skill 只处理静态语料。
- 反向判别：用户说「让 agent 记住这个项目」必须追问——记「结构」→ 本 skill；记「和我聊过什么/干过什么」→ 兄弟。

## E | 执行步骤

1. 圈定语料：范围目录清单 + 文件类型分布。完成标准：体量估计完成，并据此判断建图收益（≤6 文件如实提示收益有限）。
2. 安装：`pip install graphifyy && graphify install`（PyPI 暂名 graphifyy）。完成标准：Claude Code 内 `/graphify` 可识别；Windows PATH 问题按 README 处理。
3. 首跑建图：`/graphify .`（深挖用 --mode deep）。完成标准：graphify-out/ 五件套齐全无报错。
4. 校验报告：读 GRAPH_REPORT.md 的 god nodes 与 surprising connections 是否符合直觉。完成标准：写出「符合/意外 + 为什么」短评。
5. 边来源抽检：统计 EXTRACTED/INFERRED/AMBIGUOUS 比例，人工复核高推断边。完成标准：抽检记录落盘；失真严重则降 mode 重跑。
6. 挂增量机制：`--watch` 或 `graphify hook install` 二选一。完成标准：修改一个文件后图更新且 cache 只处理了变更项。
7. 交棒产出：`--wiki` 生成导航层。完成标准：新开一个会话仅凭 index.md 能正确回答 2 个结构问题。

## B | 边界

不适用：
- 动态对话记忆/用户画像/经验 SOP 沉淀 → 分别转 `mem0-memory-layer`、`hindsight-retrieval`、`agent-experience-persistence`。
- 微型语料（≤6 文件）：README 自认此时压缩比 ≈1x，价值仅剩结构清晰——应直接阅读而非建图。

局限：
- INFERRED 边存在过度连接风险，必须人工抽检，不能盲信报告。
- LLM/vision 抽取按调用量计费，大语料首跑成本可观。
- 上游活跃仓库实为 safishamsi/graphify（v1 分支），Graphify-Labs 镜像同步时效需留意，安装名暂为 graphifyy。

## 相关 skills

- `mem0-memory-layer`：动态用户偏好记忆（与本 skill 静静动动互补）
- `hindsight-retrieval`：动态事实召回
- `agent-experience-persistence`：操作经验持久化

## 审计信息

- V1✓ 来源核验：main 通道成功抓取全文 README；注意上游 badge 指向 safishamsi/graphify，已在局限中披露
- V2✓ 结构完整：R/I/A1/A2/E/B/相关/审计八节齐备，frontmatter 四要素齐全
- V3✓ 测试通过：test-prompts.json 共 7 条推演全 PASS，见 test-results.md
- 审计日期：2026-08-25
- 来源 URL：<https://raw.githubusercontent.com/Graphify-Labs/graphify/main/README.md>
