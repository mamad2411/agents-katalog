---
name: paper-factory
version: 1.0.0
description: 端到端学术论文生成工厂，支持从选题到定稿的全流程自动化
author: tzukwan
---

# Paper Factory — 论文工厂技能

## 描述

Paper Factory 是 tzukwan-cli 的旗舰技能，提供从研究选题、文献调研、实验设计、结果分析到完整论文写作的端到端自动化流水线。内置 5 大工作流，覆盖期刊论文、硕士学位论文、博士学位论文三种类型，并深度集成 awesome-public-datasets 数据集库与多个开放数据源，确保每篇生成的论文均基于真实数据支撑。

## 功能列表

- **5 大核心工作流**：选题生成 → 文献综述 → 实验方案 → 结果分析 → 完整论文写作
- **多种论文类型**：期刊短文（journal）、硕士学位论文（master）、博士学位论文（phd）
- **多学科支持**：计算机科学、生物信息学、统计学、物理学、经济学、医学、环境科学等
- **真实数据集集成**：从 awesome-public-datasets（GitHub）实时拉取并推荐最适配数据集
- **PIVOT/REFINE 决策逻辑**：实验结果不佳时自动评估是否调整假设（PIVOT）或优化方法（REFINE）
- **结构化输出**：生成完整的 LaTeX 或 Markdown 文稿，含图表占位符、引用格式化
- **论文复现**：从已有论文的方法部分生成可运行的复现代码骨架

## 命令

- `generate`
- `monitor`
- `analyze`
- `reproduce`
- `review`

## 工作流详细描述

### 工作流 1：generate — 端到端论文生成

完整执行 5 个阶段，输出可提交的论文草稿：

**阶段 1 — 选题与问题定义（Topic & Problem Formulation）**
- 根据研究领域、关键词、目标期刊/会议生成研究问题列表
- 评估各问题的新颖性、可行性、影响力（基于近 3 年 arXiv 引用热度）
- 输出：研究问题陈述（Research Question Statement）+ 贡献声明草稿

**阶段 2 — 文献综述（Literature Review）**
- 调用 `literature-review` 技能检索多源文献
- 构建研究脉络图（时间线 + 方法演进）
- 识别研究空白（Research Gaps）作为论文切入点
- 输出：综述章节草稿 + 参考文献列表（BibTeX）

**阶段 3 — 数据集与实验设计（Dataset & Experiment Design）**
- 调用 `dataset-hub` 技能推荐匹配的公开数据集
- 生成实验方案（基线方法、评估指标、消融实验设计）
- 输出：数据集 manifest + 实验设计文档

**阶段 4 — 实验执行与结果分析（Experiment & Analysis）**
- 调用 `experiment` 技能执行或模拟实验
- PIVOT/REFINE 决策：若主要结果未达预期，自动分析原因并建议调整策略
- 生成图表脚本（matplotlib/seaborn/R ggplot2）
- 输出：结果数据表 + 分析叙述 + 图表代码

**阶段 5 — 论文写作与格式化（Writing & Formatting）**
- 按论文类型和目标期刊模板生成完整章节
- 引用格式化（APA / IEEE / GB-T-7714 等）
- LaTeX 模板适配（ACM、IEEE、Elsevier、Nature、NeurIPS、ICML 等）
- 输出：完整论文 `.tex` 文件 + `references.bib` + 摘要英文版

---

### 工作流 2：monitor — 研究领域实时监控

- 持续监控 arXiv、PubMed、Semantic Scholar 中与当前论文主题相关的新发表
- 自动评估新论文是否对当前工作构成竞争或可作为引用补充
- 生成每日/每周摘要报告推送到终端或 Telegram

---

### 工作流 3：analyze — 论文质量深度分析

- 逻辑一致性检查（假设 ↔ 实验 ↔ 结论 三角自洽）
- 统计显著性验证（实验结果的置信区间、p 值合理性）
- 引用覆盖度评估（关键相关工作是否遗漏）
- 图表与正文对应性检查
- 输出：质量评估报告（Markdown）+ 修改建议列表

---

### 工作流 4：reproduce — 论文复现

- 输入：arXiv ID 或 PDF 路径
- 解析论文方法部分，提取算法伪代码、超参数设置、数据预处理步骤
- 生成 Python 实现骨架（PyTorch / scikit-learn / numpy）
- 匹配原始数据集，生成完整的 `reproduce.py` + `README.md`
- 输出：可运行的复现代码目录

---

### 工作流 5：review — 同行评审模拟

- 模拟 3 位虚拟审稿人（Reviewer 1/2/3）分别从技术深度、写作质量、实验充分性角度打分
- 生成结构化审稿意见（Major/Minor Revision 分类）
- 提供针对每条审稿意见的 Response to Reviewer 草稿
- 输出：审稿意见 Markdown 文档 + Response 草稿

## 使用示例

```bash
# 生成一篇关于联邦学习隐私保护的期刊论文（中文）
tzukwan paper-factory generate \
  --topic "federated learning privacy" \
  --type journal \
  --language zh \
  --domain cs.CR \
  --output ./my-paper/

# 生成生物信息学方向的博士论文大纲
tzukwan paper-factory generate \
  --topic "single-cell RNA-seq trajectory inference" \
  --type phd \
  --domain bioinformatics \
  --outline-only

# 复现 arXiv 上一篇论文
tzukwan paper-factory reproduce 2312.09876 --output ./reproduced/

# 对已有论文草稿进行同行评审模拟
tzukwan paper-factory review ./my-paper/draft.tex

# 监控联邦学习领域最新进展
tzukwan paper-factory monitor --topic "federated learning" --interval 24h
```

### 对话触发示例

```
用户：帮我写一篇关于大语言模型幻觉检测的论文
用户：生成一篇硕士论文，研究方向是图神经网络
用户：复现这篇 arXiv 论文：2401.12345
用户：帮我审阅这篇论文草稿，指出不足
用户：监控一下我研究领域的最新论文
```

## 触发词

- `write paper`
- `generate paper`
- `写论文`
- `生成论文`
- `论文写作`
- `paper factory`
- `学术写作`
- `reproduce paper`
- `复现论文`
- `paper review`
- `论文审稿`

## 支持的论文类型

| 类型标识 | 描述 | 典型章节结构 |
|----------|------|--------------|
| `journal` | 期刊/会议短文（4–12 页） | Abstract, Introduction, Related Work, Method, Experiments, Conclusion |
| `master` | 硕士学位论文（50–100 页） | 摘要, 绪论, 文献综述, 研究方法, 实验结果, 讨论, 结论, 参考文献 |
| `phd` | 博士学位论文（100–300 页） | 摘要, 绪论, 背景综述, 方法章(×3), 综合讨论, 结论与展望, 附录 |

## 支持的学科领域

- `cs.AI` — 人工智能
- `cs.LG` — 机器学习
- `cs.CL` — 计算语言学 / NLP
- `cs.CV` — 计算机视觉
- `cs.CR` — 密码学与安全
- `cs.SE` — 软件工程
- `bioinformatics` — 生物信息学
- `stat.ML` — 统计机器学习
- `q-bio` — 定量生物学
- `physics` — 物理学
- `econ` — 经济学
- `med` — 医学 / 临床研究
- `env` — 环境科学

## 数据源/API 依赖

| 服务 | 用途 | 认证 |
|------|------|------|
| arXiv API | 文献检索与引用 | 无需 |
| Semantic Scholar API | 引用网络、影响力数据 | 可选 |
| PubMed E-utilities | 生物医学文献 | 无需 |
| OpenAlex API | 开放学术图谱 | 无需 |
| awesome-public-datasets (GitHub) | 数据集推荐 | 无需（公开仓库） |
| GitHub API | 代码仓库搜索 | 可选（提升速率限制） |

## 输出格式

所有输出文件保存到 `--output` 指定目录（默认 `./tzukwan-output/paper-factory/`）：

```
output/
├── paper.tex              # 完整 LaTeX 论文
├── paper.md               # Markdown 版本（同步生成）
├── references.bib         # BibTeX 参考文献
├── abstract_en.txt        # 英文摘要（用于投稿）
├── figures/               # 图表生成脚本
│   ├── fig1_results.py
│   └── fig2_ablation.py
├── data/                  # 数据集 manifest 和预处理脚本
│   └── dataset_manifest.json
├── code/                  # 实验代码骨架
│   ├── model.py
│   ├── train.py
│   └── evaluate.py
└── review_report.md       # 同行评审模拟报告（review 命令）
```
