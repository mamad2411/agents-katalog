---
name: paper-analysis
description: Deep analysis of AI research papers with type-specific prompts. Covers benchmark papers, methodology papers, and survey/position/blog posts. Use when the user asks to read, analyze, review, or summarize a research paper, or mentions 论文分析、论文阅读、paper review、benchmark analysis、方法论分析.
---

# Paper Analysis

对 AI 研究论文进行"极致剖析"（Extreme Analysis），根据论文类型自动路由到对应的分析框架。

## 论文类型判定与路由

收到论文后，首先判定类型，然后读取对应的 prompt 文件：

**Benchmark 论文** → 读取 [prompts/benchmark.md](prompts/benchmark.md)
特征：提出新的评测数据集或评估框架，核心贡献是数据集构建和评估协议设计。

**方法/算法论文** → 读取 [prompts/methodology.md](prompts/methodology.md)
特征：提出新的模型架构、训练策略、推理方法或算法，核心贡献是技术创新。

**综述/观点/博客** → 读取 [prompts/survey-opinion.md](prompts/survey-opinion.md)
特征：Survey、Position Paper、Technical Blog、Opinion Piece，核心贡献是知识综合或观点论述。

如果论文兼具多种特征（如提出新方法同时构建了 benchmark），以其**主要贡献**为准选择框架，并在分析中补充次要贡献维度的关键信息。

### 期刊/顶刊叠加判定（正交于上面三类）

在选定上面的技术 route 之后，**再判断一次载体**：若论文发表于（或投向）**Nature Portfolio / Science / Cell 系及其子刊等公认顶刊**，或用户明确提到"期刊""正刊""子刊""顶刊"，则**额外叠加** [prompts/journal-nature.md](prompts/journal-nature.md)。

- 技术内核仍走 benchmark.md / methodology.md（不得省略）；
- journal-nature.md 的 A–F 节叠加在技术剖析**之后**，补充"顶刊叙事产品构造 + 传播机制"这一层会议论文框架不覆盖的维度；
- **硬性禁令**：paper-analysis 的产出是「对他人论文的阅读剖析」，禁止夹带「给自己论文投稿的写作借鉴/句式仿写清单」——那属于写作类工具的职责，不写进阅读产出。

## 用户输入

用户只需提供论文标识（URL / PDF / 标题 / DOI）。所有其他资源（GitHub 仓库、Hugging Face、相关论文、作者信息）由 agent 主动搜索定位。

## 共享指令（适用于所有类型）

### 写作风格

以段落叙述为主体，仅在数据表格、代码示例和指标公式处使用结构化格式。段落间需有清晰的逻辑衔接，如同撰写高质量技术综述。关键概念和术语使用**加粗**标注。

### 术语规范

使用专业、准确的中文术语，关键英文术语在括号中保留原文。

### 穷尽式文献网络构建

将论文视为"节点"，沿引用关系向外辐射。**必须追溯**的：所有直接对比的基线方法/benchmark 的原始论文。**应当检索**的：同期或更晚发表的解决相同问题的工作。**可选追溯**的：泛泛引用的背景工作。搜索是否有同期或后续工作也在解决相同问题，以判断本文的时效性和独特性。

检查官方 GitHub 仓库的 README、核心代码/评估脚本、关键 issue 和 discussion。若有 Hugging Face 页面，检查 dataset card、实际样本和社区讨论。

### 核心贡献者溯源

调查核心作者（第一作者、通讯作者）的学术轨迹：Google Scholar 主页、个人网站、过往发表记录、社交媒体（Twitter/X）上关于本工作的讨论。理解这项工作在作者研究脉络中的位置——是长期研究线的延伸还是全新探索？哪些前序工作为本文奠定了基础？融入"概览"部分。

### 社区采纳度与影响力

检查论文的引用量和增长趋势。是否被后续重要工作（如主流模型技术报告）采纳？在 GitHub 上的 star 数和社区活跃度如何？是否有知名研究者的公开评价？

### 指标详尽解释

对所有评估指标提供 LaTeX 公式（$...$ 或 $$...$$），逐一解释公式中所有符号，适用时结合具体例子演示计算过程。

### 资源不可用时的降级策略

若论文未开源代码，明确声明并指出这本身是可复现性的风险。若数据集有访问限制，说明限制条件。若无法获取真实数据样本，构造功能等价的最小示例并明确标注为"构造示例"。禁止虚构不存在的资源。

### Agent 能力边界

若单次对话无法完成所有引用论文的深度阅读，优先覆盖：(1) 直接对比的基线工作 (2) 作者声称改进的具体缺陷的验证 (3) 核心实验结果的解读。在报告中注明哪些引用论文未能深度覆盖。
