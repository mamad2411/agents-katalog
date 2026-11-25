---
name: research-paper-writing
title: Research Paper Writing Pipeline
description: "Write ML papers for NeurIPS/ICML/ICLR: design→submit."
version: 1.1.0
author: Orchestra Research
license: MIT
dependencies: [semanticscholar, arxiv, habanero, requests, scipy, numpy, matplotlib, SciencePlots]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Research, Paper Writing, Experiments, ML, AI, NeurIPS, ICML, ICLR, ACL, AAAI, COLM, LaTeX, Citations, Statistical Analysis]
    category: research
    related_skills: [arxiv, ml-paper-writing, subagent-driven-development, plan]
    requires_toolsets: [terminal, files]

---

# 研究论文撰写流程

这是一个端到端的完整流程，用于协助撰写可直接投稿的机器学习/AI研究论文，目标期刊包括**NeurIPS、ICML、ICLR、ACL、AAAI和COLM**。该技能涵盖了整个研究生命周期：实验设计、执行、监控、分析、论文撰写、审稿、修改以及投稿。

这并非**线性流程**，而是一个循环迭代的过程。实验结果会催生新的实验，审稿意见又会引发进一步分析。智能体需要能够处理这些反馈循环。
```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH PAPER PIPELINE                  │
│                                                             │
│  Phase 0: Project Setup ──► Phase 1: Literature Review      │
│       │                          │                          │
│       ▼                          ▼                          │
│  Phase 2: Experiment     Phase 5: Paper Drafting ◄──┐      │
│       Design                     │                   │      │
│       │                          ▼                   │      │
│       ▼                    Phase 6: Self-Review      │      │
│  Phase 3: Execution &           & Revision ──────────┘      │
│       Monitoring                 │                          │
│       │                          ▼                          │
│       ▼                    Phase 7: Submission               │
│  Phase 4: Analysis ─────► (feeds back to Phase 2 or 5)     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
## 何时使用此技能

在以下情况下可使用此技能：
- 基于现有代码库或创意**启动新的研究论文撰写**
- **设计并执行实验**以支撑论文中的论点
- **撰写或修改**研究论文的任意部分
- 为向特定会议或研讨会**提交论文做准备**
- 通过补充实验或修改内容来**回应审稿意见**
- 在不同会议格式之间**转换论文**
- 撰写**非实证类论文**——理论论文、综述论文、基准测试论文或立场文件（参见[超越实证机器学习的论文类型](#paper-types-beyond-empirical-ml)）
- 为自然语言处理、人机交互或对齐研究**设计人工评估方案**
- 准备**论文被接收后的交付物**——海报、演讲材料、代码发布等

## 核心理念

1. **主动出击**。提供完整的初稿，而非提出问题。科学家们时间紧张——先给出他们可以据此反馈的具体内容，再逐步优化。
2. **绝不可编造引用**。人工智能生成的引用错误率约为40%。务必通过编程方式获取引用信息。将无法验证的引用标记为 `[CITATION NEEDED]`。
3. **论文是一个故事，而非实验的集合**。每篇论文都需用一句话清晰阐述其核心贡献。若无法做到这一点，则说明论文尚未成熟。
4. **实验应为论点服务**。每个实验都必须明确说明其所支持的论点。切勿进行与论文整体逻辑无关的实验。
5. **尽早提交，频繁提交**。每次完成一批实验、每次更新论文初稿，都应附上描述性信息后进行提交。Git日志就是实验的历史记录。

### 主动性与协作

**默认原则：主动出击。先撰写初稿，再基于初稿提出问题。**

| 自信度等级 | 应采取的行动 |
|------------|--------------|
| **高**（代码库结构清晰，贡献点明确） | 撰写完整初稿，提交后根据反馈进行优化 |
| **中**（存在部分模糊之处） | 撰写初稿并标注不确定的内容，随后继续完善 |
| **低**（存在重大未知因素） | 通过 `clarify` 提出1-2个针对性问题，之后再撰写初稿 |

| 章节 | 是否可自主撰写初稿 | 是否需在初稿中标注问题 |
|------|-------------------|--------------------------|
| 摘要 | 是 | “将核心贡献表述为X——如需调整请告知” |
| 引言 | 是 | “强调了问题Y——如有错误请修正” |
| 方法部分 | 是 | “已包含A、B、C等细节——请补充缺失内容” |
| 实验部分 | 是 | “突出了1、2、3号实验结果——如需调整顺序请告知” |
| 相关工作部分 | 是 | “已引用X、Y、Z等论文——请补充我遗漏的文献” |

**仅在以下情况暂停并等待输入**：目标会议不明确、存在多种相互矛盾的表述、实验结果似乎不完整，或收到明确要求先进行审阅的指示。

---

## 阶段0：项目准备

**目标**：搭建工作环境，了解现有研究，明确论文的贡献点。

### 步骤0.1：探索代码库

```bash
# Understand project structure
ls -la
find . -name "*.py" | head -30
find . -name "*.md" -o -name "*.txt" | xargs grep -l -i "result\|conclusion\|finding"
```

请查找以下文件：
- `README.md` — 项目概述与功能说明
- `results/`、`outputs/`、`experiments/` — 现有的研究结果
- `configs/` — 实验配置参数
- `.bib` 文件 — 现有的参考文献
以及各类草稿文档或笔记。

### 步骤 0.2：整理工作空间

建立统一的工作空间结构：

```
workspace/
  paper/               # LaTeX source, figures, compiled PDFs
  experiments/         # Experiment runner scripts
  code/                # Core method implementation
  results/             # Raw experiment results (auto-generated)
  tasks/               # Task/benchmark definitions
  human_eval/          # Human evaluation materials (if needed)
```

### 步骤 0.3：配置版本控制

```bash
git init  # if not already
git remote add origin <repo-url>
git checkout -b paper-draft  # or main
```

**Git 使用规范**：每批完成后的实验数据都需通过提交操作进行保存，并附上描述性说明。示例如下：
```
Add Monte Carlo constrained results (5 runs, Sonnet 4.6, policy memo task)
Add Haiku baseline comparison: autoreason vs refinement baselines at cheap model tier
```

### 步骤 0.4：明确贡献点

在开始撰写任何内容之前，先清晰阐述以下三点：
- **核心贡献是什么**：这篇论文究竟带来了什么独特的价值？
- **依据是什么**：有哪些证据可以支撑这一观点？
- **为何重要**：为什么读者应该关注它？

> 可向科研人员提出如下建议：“据我理解，本文的主要贡献在于：[一句话概括]。关键研究结果为[Y]。这样的表述是否符合您的预期？”

### 步骤 0.5：制定待办清单

使用 `todo` 工具来创建结构化的项目计划：

```
Research Paper TODO:
- [ ] Define one-sentence contribution
- [ ] Literature review (related work + baselines)
- [ ] Design core experiments
- [ ] Run experiments
- [ ] Analyze results
- [ ] Write first draft
- [ ] Self-review (simulate reviewers)
- [ ] Revise based on review
- [ ] Submission prep
```

请在整个项目中统一更新此内容。它将作为跨会话的持久化状态保存下来。

### 步骤 0.6：估算计算预算

在开始实验之前，先预估总成本与所需时间：

```
Compute Budget Checklist:
- [ ] API costs: (model price per token) × (estimated tokens per run) × (number of runs)
- [ ] GPU hours: (time per experiment) × (number of experiments) × (number of seeds)
- [ ] Human evaluation costs: (annotators) × (hours) × (hourly rate)
- [ ] Total budget ceiling and contingency (add 30-50% for reruns)
```

在实验运行过程中实时追踪实际支出情况：
```python
# Simple cost tracker pattern
import json, os
from datetime import datetime

COST_LOG = "results/cost_log.jsonl"

def log_cost(experiment: str, model: str, input_tokens: int, output_tokens: int, cost_usd: float):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "experiment": experiment,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": cost_usd,
    }
    with open(COST_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
```

**预算紧张时**：在开展全面测试之前，先进行小规模试点实验（使用1-2个样本及部分任务）。在调试流程时可选用成本较低的模型，最终运行时再切换为目标模型。

### 步骤0.7：多作者协作

大多数论文的作者数量为3至10人。建议尽早确定协作流程：

| 协作流程 | 工具 | 适用场景 |
|----------|------|----------|
| **Overleaf** | 基于浏览器的工具 | 多位作者需同时编辑，且团队没有Git使用经验 |
| **Git + LaTeX** | 配备`.gitignore`规则用于管理辅助文件的`git` | 技术团队，需要基于分支的代码审查功能 |
| **Overleaf + Git同步** | Overleaf高级版 | 结合两者的优势——支持实时协作并保留版本历史记录 |

**章节负责制**：为每个章节指定一名主要作者，其他成员仅可发表评论，不得直接修改内容。这样可以避免合并冲突及风格不一致的问题。

```
Author Coordination Checklist:
- [ ] Agree on section ownership (who writes what)
- [ ] Set up shared workspace (Overleaf or git repo)
- [ ] Establish notation conventions (before anyone writes)
- [ ] Schedule internal review rounds (not just at the end)
- [ ] Designate one person for final formatting pass
- [ ] Agree on figure style (colors, fonts, sizes) before creating figures
```

**需提前确定的 LaTeX 格式规范**：
- 使用 `\method{}` 宏以确保方法名称的一致性
- 引用格式：区分 `\citet{}` 与 `\citep{}` 的使用方式
- 数学符号：向量用小写粗体，矩阵用大写粗体等
- 英式拼写与美式拼写的选择

---

## 第一阶段：文献综述

**目标**：查找相关研究、确定基准方法、收集引用文献。

### 步骤 1.1：筛选初始参考论文

从代码库中已存在的参考文献开始入手：

```bash
# Via terminal:
grep -r "arxiv\|doi\|cite" --include="*.md" --include="*.bib" --include="*.py"
find . -name "*.bib"
```

### 步骤 1.2：搜索相关研究

**加载 `arxiv` 技能**以实现结构化论文检索：调用 `skill_view("arxiv")`。该技能支持通过 arXiv REST API 进行搜索，还能提供 Semantic Scholar 的引文图谱、作者资料以及 BibTeX 格式生成功能。

如需进行广泛检索，可使用 `web_search`；若要获取特定论文，则可使用 `web_extract`：

```
# Via web_search:
web_search("[main technique] + [application domain] site:arxiv.org")
web_search("[baseline method] comparison ICML NeurIPS 2024")

# Via web_extract (for specific papers):
web_extract("https://arxiv.org/abs/2303.17651")
```

可尝试的其他搜索查询：

```
Search queries:
- "[main technique] + [application domain]"
- "[baseline method] comparison"
- "[problem name] state-of-the-art"
- Author names from existing citations
```

**推荐**：为实现实时学术搜索，请安装 **Exa MCP**：
```bash
claude mcp add exa -- npx -y mcp-remote "https://mcp.exa.ai/mcp"
```

### 步骤 1.2b：深入搜索（先广度后深度）

单纯的单一轮查询往往难以发现重要的相关研究成果。建议采用受深度研究流程启发的迭代式“先广度后深度”搜索策略：

```
Iterative Literature Search:

Round 1 (Breadth): 4-6 parallel queries covering different angles
  - "[method] + [domain]"
  - "[problem name] state-of-the-art 2024 2025"
  - "[baseline method] comparison"
  - "[alternative approach] vs [your approach]"
  → Collect papers, extract key concepts and terminology

Round 2 (Depth): Generate follow-up queries from Round 1 learnings
  - New terminology discovered in Round 1 papers
  - Papers cited by the most relevant Round 1 results
  - Contradictory findings that need investigation
  → Collect papers, identify remaining gaps

Round 3 (Targeted): Fill specific gaps
  - Missing baselines identified in Rounds 1-2
  - Concurrent work (last 6 months, same problem)
  - Key negative results or failed approaches
  → Stop when new queries return mostly papers you've already seen
```

**何时停止搜索**：如果某一轮次返回的论文中有超过80%已存在于您的收藏中，说明搜索已达到饱和状态。通常2-3轮即可完成目标，而对于综述类论文，则可能需要4-5轮。

**针对基于智能体的工作流**：可通过`delegate_task`函数并行处理每一轮的查询任务。收集所有结果后进行去重处理，再根据汇总到的信息生成下一轮的查询条件。

### 第1.3步：验证每条引用

**绝不可凭记忆生成BibTeX格式，必须通过编程方式获取。**

对于每条引用，都必须遵循以下5个必经步骤：

```
Citation Verification (MANDATORY per citation):
1. SEARCH → Query Semantic Scholar or Exa MCP with specific keywords
2. VERIFY → Confirm paper exists in 2+ sources (Semantic Scholar + arXiv/CrossRef)
3. RETRIEVE → Get BibTeX via DOI content negotiation (programmatically, not from memory)
4. VALIDATE → Confirm the claim you're citing actually appears in the paper
5. ADD → Add verified BibTeX to bibliography
If ANY step fails → mark as [CITATION NEEDED], inform scientist
```

```python
# Fetch BibTeX via DOI
import requests

def doi_to_bibtex(doi: str) -> str:
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"}
    )
    response.raise_for_status()
    return response.text
```

如果您无法验证某条引用：

```latex
\cite{PLACEHOLDER_author2024_verify_this}  % TODO: Verify this citation exists
```

**务必告知科研人员**：“我已将[X]处引用标记为需要验证的占位符。”

如需完整的API文档及`CitationManager`类的详细信息，请参阅[references/citation-workflow.md](references/citation-workflow.md)。

### 第1.4步：整理相关研究

按方法论对论文进行分组，而非逐篇处理：

**正确示例**：“有一类研究采用了X的假设[refs]，而我们选择使用Y的假设，原因是……”
**错误示例**：“Smith等人提出了X。Jones等人提出了Y。我们将两者结合使用。”

---

## 第2阶段：实验设计

**目标**：设计能够直接支撑论文论点的实验。每个实验都必须回答一个具体问题。

### 第2.1步：将论点与实验对应起来

建立明确的映射关系：

| 论点 | 实验 | 预期证据 |
|-------|-----------|-------------------|
| “我们的方法优于基线方法” | 主要对比实验（表1） | 胜率、统计显著性 |
| “在较弱模型上效果更显著” | 模型规模扩展研究 | 单调改进曲线 |
| “收敛需要满足特定约束条件” | 有约束与无约束对比 | 收敛速度比较 |

**规则**：如果某个实验无法对应到任何论点，则不应执行该实验。

### 第2.2步：设计基线方法

出色的基线方法是区分被接收论文与被拒论文的关键。审稿人会询问：“他们是否与X进行了对比？”

常见的基线类型包括：
- **朴素基线**：最简单的可行方案
- **强基线**：目前已知的最优方法
- **消融基线**：去掉您方法中的一个组件后的版本
- **计算资源匹配基线**：使用相同的计算资源，但分配方式不同

### 第2.3步：明确评估方案

在开始任何实验之前，需明确以下内容：
- **指标**：要测量的内容，以及方向性符号（数值越高/越低越好）
- **结果聚合方式**：如何将多次运行/任务的结果合并
- **统计检验方法**：用于判断显著性水平的测试类型
- **样本量**：需要进行的运行次数/问题数量/任务数量

### 第2.4步：编写实验脚本

参考成功的研究流程中的模式进行编写：

**逐步保存数据**——在每一步之后保存结果，以便在出现故障时能够恢复数据：
```python
# Save after each problem/task
result_path = f"results/{task}/{strategy}/result.json"
if os.path.exists(result_path):
    continue  # Skip already-completed work
# ... run experiment ...
with open(result_path, 'w') as f:
    json.dump(result, f, indent=2)
```

**工件保留**——保存所有中间输出结果：
```
results/<experiment>/
  <task>/
    <strategy>/
      final_output.md          # Final result
      history.json             # Full trajectory
      pass_01/                 # Per-iteration artifacts
        version_a.md
        version_b.md
        critic.md
```

**职责分离**——将生成、评估与可视化功能分开处理：
```
run_experiment.py              # Core experiment runner
run_baselines.py               # Baseline comparison
run_comparison_judge.py        # Blind evaluation
analyze_results.py             # Statistical analysis
make_charts.py                 # Visualization
```

如需了解完整的设计模式、定时监控及错误恢复方案，请参阅[references/experiment-patterns.md](references/experiment-patterns.md)。

### 第2.5步：设计人工评估（如适用）

许多自然语言处理、人机交互及对齐领域的论文都要求以人工评估作为主要或补充性证据。在开展自动化实验之前，应先完成此项设计——因为人工评估往往需要更长的准备时间（如伦理委员会审批、标注员招募等）。

**何时需要进行人工评估：**
- 自动化指标无法衡量您关注的关键维度（流畅性、实用性、安全性）
- 您的研究成果侧重于面向人类的质量特性（可读性、用户偏好、信任度）
- 自然语言处理领域的学术会议（如ACL、EMNLP）要求生成类任务必须进行人工评估

**关键设计决策：**

| 决策项 | 可选方案 | 建议 |
|--------|----------|------|
| **标注员类型** | 专家、众包人员、最终用户 | 根据研究需求选择合适的标注员类型 |
| **评分方式** | 利克特量表（1-5分）、成对比较、排序 | 对于大语言模型输出，成对比较比利克特量表更可靠 |
| **样本量** | 每位标注员的评估数量及总评估项数 | 建议通过功效分析确定样本量，至少100项评估，3名以上标注员 |
| **一致性指标** | 科恩卡帕值、克里彭多夫阿尔法值、ICC系数 | 当标注员超过2人时使用克里彭多夫阿尔法值；同时需报告原始一致性数据 |
| **平台选择** | Prolific、MTurk、内部团队 | 追求高质量评估可选择Prolific；追求大规模评估可使用MTurk；需要领域专业知识的任务可选用内部团队 |

**标注指南检查清单：**
```
- [ ] Clear task description with examples (good AND bad)
- [ ] Decision criteria for ambiguous cases
- [ ] At least 2 worked examples per category
- [ ] Attention checks / gold standard items (10-15% of total)
- [ ] Qualification task or screening round
- [ ] Estimated time per item and fair compensation (>= local minimum wage)
- [ ] IRB/ethics review if required by your institution
```

**报告要求**（审核人员需核查所有内容）：
- 注释人员的数量及其资质
- 不同注释人员之间的一致性，需提供具体指标与数值
- 报酬明细（金额、预计时薪）
- 注释界面描述或截图（附于文档末尾）
- 总注释时长

如需包含针对人工评估数据的统计检验方法、众包质量控制策略以及机构审查委员会相关指导的完整指南，请参阅 [references/human-evaluation.md](references/human-evaluation.md)。

---

## 第三阶段：实验执行与监控

**目标**：可靠地运行实验，监控进展，并从故障中恢复。

### 步骤 3.1：启动实验

对于需要长时间运行的实验，建议使用 `nohup` 命令来运行。

```bash
nohup python run_experiment.py --config config.yaml > logs/experiment_01.log 2>&1 &
echo $!  # Record the PID
```

**并行执行**：可同时运行多个独立的实验，但需注意 API 的调用频率限制。同一 API 上同时进行的实验数量超过 4 个时，会导致所有实验的运行速度变慢。

### 第 3.2 步：设置监控（Cron 表达式）

对于需要长时间运行的实验，应设置定期的状态检查。Cron 表达式应遵循以下格式：

```
Monitor Prompt Template:
1. Check if process is still running: ps aux | grep <pattern>
2. Read last 30 lines of log: tail -30 <logfile>
3. Check for completed results: ls <result_dir>
4. If results exist, read and report: cat <result_file>
5. If all done, commit: git add -A && git commit -m "<descriptive message>" && git push
6. Report in structured format (tables with key metrics)
7. Answer the key analytical question for this experiment
```

**静默模式**：如果自上次检查以来没有发生变化，则回复 `[SILENT]` 以隐藏对用户的通知。仅在有新变化时才进行报告。

### 第 3.3 步：处理故障

常见的故障类型及恢复方法：

| 故障类型 | 检测方式 | 恢复方法 |
|---------|-----------|----------|
| API 速率限制/额度耗尽 | 日志中出现 402/429 错误 | 等待片刻后重新运行（脚本会跳过已完成的工作） |
| 进程崩溃 | 进程 PID 失踪，结果不完整 | 从上一个检查点重新运行 |
| 复杂问题超时 | 进程卡住，无日志进度更新 | 终止进程并跳过该任务，在结果中记录说明 |
| 模型 ID 错误 | 日志中出现模型名称相关的错误 | 更正 ID 后重新运行 |

**要点**：脚本应始终检查是否存在已有结果，并跳过已完成的工作。这样既能确保重新运行的安全性，又能提高效率。

### 第 3.4 步：提交已完成的结果

在每个实验批次完成后：

```bash
git add -A
git commit -m "Add <experiment name>: <key finding in 1 line>"
git push
```

### 第 3.5 步：维护实验日志

Git 提交记录了所发生的一切，但无法体现**探索路径**——即根据已有经验做出的下一步尝试决策。因此，建议维护一份结构化的实验日志，用以记录这一探索路径。

```json
// experiment_journal.jsonl — append one entry per experiment attempt
{
  "id": "exp_003",
  "parent": "exp_001",
  "timestamp": "2025-05-10T14:30:00Z",
  "hypothesis": "Adding scope constraints will fix convergence failure from exp_001",
  "plan": "Re-run autoreason with max_tokens=2000 and fixed structure template",
  "config": {"model": "haiku", "strategy": "autoreason", "max_tokens": 2000},
  "status": "completed",
  "result_path": "results/exp_003/",
  "key_metrics": {"win_rate": 0.85, "convergence_rounds": 3},
  "analysis": "Scope constraints fixed convergence. Win rate jumped from 0.42 to 0.85.",
  "next_steps": ["Try same constraints on Sonnet", "Test without structure template"],
  "figures": ["figures/exp003_convergence.pdf"]
}
```

**为何要使用日志而非仅依赖 Git？** Git 用于追踪文件的变化，而日志则用于记录思考过程：为何尝试了某种方法 X、从中获得了哪些经验，以及这些经验对后续实验有何启示。在撰写论文时，这样的记录对于“方法”部分（如“我们观察到了 X，这促使我们提出了 Y”）以及如实报告失败情况具有不可替代的价值。

**选择最佳路径**：当日志显示出分支结构（exp_001 → exp_002a、exp_002b、exp_003）时，应挑选最能支撑论文论点的路径。将那些无法继续推进的分支作为消融实验或负面结果记录在附录中。

**为每个实验保存代码快照**：每次运行实验后，都复制对应的脚本文件。
```bash
cp experiment.py results/exp_003/experiment_snapshot.py
```
即便后续对代码进行修改，该机制也能确保结果的一致性。

---

## 第四阶段：结果分析

**目标**：提取分析结果、计算统计数据，并明确核心问题所在。

### 步骤 4.1：汇总结果

编写分析脚本，实现以下功能：
1. 加载批次处理中的所有结果文件
2. 计算每项任务的指标以及总体汇总指标
3. 生成汇总表格

```python
# Standard analysis pattern
import json, os
from pathlib import Path

results = {}
for result_file in Path("results/").rglob("result.json"):
    data = json.loads(result_file.read_text())
    strategy = result_file.parent.name
    task = result_file.parent.parent.name
    results.setdefault(strategy, {})[task] = data

# Compute aggregate metrics
for strategy, tasks in results.items():
    scores = [t["score"] for t in tasks.values()]
    print(f"{strategy}: mean={np.mean(scores):.1f}, std={np.std(scores):.1f}")
```

### 第4.2步：统计显著性分析

务必计算以下内容：
- **误差条**：标准差或标准误，需明确说明使用哪种
- **置信区间**：关键结果需给出95%置信区间
- **成对检验**：用于比较两种方法的McNemar检验
- **效应量**：用于体现实际意义，可选择Cohen’s d或h值

关于McNemar检验、自助法置信区间以及Cohen’s h值的完整实现方式，请参阅[references/experiment-patterns.md](references/experiment-patterns.md)文档。

### 第4.3步：明确研究核心内容

分析完成后，需明确回答以下问题：
1. **主要研究发现是什么？** 用一句话概括。
2. **有哪些意外发现？** 出乎意料的结果往往能造就最优秀的论文。
3. **哪些实验失败了？** 失败的实验往往最具参考价值。如实报告失败情况能提升论文质量。
4. **还需要进行哪些后续实验？** 研究结果常常会引发新的问题。

#### 如何处理阴性或无效结果

当假设错误或研究结果无明确结论时，可采取以下三种方案：

| 情况 | 应对措施 | 适合发表的会议/期刊 |
|------|----------|---------------------|
| 假设错误，但分析**原因**具有价值 | 围绕对原因的分析来构建论文框架 | NeurIPS、ICML（前提是分析严谨） |
| 方法虽未优于基准方法，但**揭示了新见解** | 将研究贡献聚焦于对现象的理解与分析 | ICLR（重视理论理解）、各类研讨会论文 |
| 对某流行观点得到明确的阴性结果 | 将其整理成文——领域内需要了解这些信息 | NeurIPS数据集与基准测试会议、TMLR、各类研讨会 |
| 结果无明确结论，缺乏清晰的研究主线 | 调整方向——开展不同的实验或重新构思研究框架 | 不要强行撰写本不该存在的论文 |

**如何撰写阴性结果论文：**
- 首先阐述学界当前的观点，以及为何需要对这些观点进行验证
- 详细描述严谨的研究方法（必须逻辑严密——审稿人会更加严格审查）
- 用统计证据清晰呈现无效结果
- 分析**为何**未出现预期结果
- 探讨该结果对所在领域的影响

**明确欢迎阴性结果的会议/期刊**：NeurIPS（数据集与基准测试分会场）、TMLR、《机器学习可复现性挑战》以及各大会议的研讨会。部分研讨会还会专门征集阴性结果论文。

### 第4.4步：制作图表

**图表绘制要求**：
- 所有图表均需使用矢量图形格式（PDF）保存：`plt.savefig('fig.pdf')`
- 选择对色盲人群友好的配色方案，如Okabe-Ito或Paul Tol方案
- 图表标题需具备独立性——读者无需阅读正文即可理解其含义
- 图表内不应出现标题——这一功能由图表标题承担

**表格制作要求**：
- 使用`booktabs` LaTeX包格式化表格
- 每项指标的最佳值需用粗体标出
- 添加方向符号（表示“更高/更低”为更好）
- 保持小数位数一致

```latex
\usepackage{booktabs}
\begin{tabular}{lcc}
\toprule
Method & Accuracy $\uparrow$ & Latency $\downarrow$ \\
\midrule
Baseline & 85.2 & 45ms \\
\textbf{Ours} & \textbf{92.1} & 38ms \\
\bottomrule
\end{tabular}
```

### 第4.5步：决策——继续实验还是开始撰写？

| 情况 | 后续操作 |
|-----------|----------|
| 核心论点得到支持，且结果具有显著性 | 进入第5阶段（撰写） |
| 结果尚不明确，需要更多数据 | 回到第2阶段（设计） |
| 出现意外发现，提示新的研究方向 | 回到第2阶段（设计） |
| 缺少某个消融实验，审稿人会要求补充 | 先完成该实验，再进入第5阶段 |
| 所有实验均已完成，但部分实验失败 | 记录失败情况，然后进入第5阶段 |

### 第4.6步：撰写实验日志（通往报告的桥梁）

在开始撰写论文之前，需先创建一份结构化的实验日志，用于将实验结果转化为文字描述。这是连接实验与论文内容的最重要纽带——若没有这份日志，撰写工具就不得不从原始结果文件中重新梳理研究过程。

请按照以下结构创建 `experiment_log.md` 文件：

```markdown
# Experiment Log

## Contribution (one sentence)
[The paper's main claim]

## Experiments Run

### Experiment 1: [Name]
- **Claim tested**: [Which paper claim this supports]
- **Setup**: [Model, dataset, config, number of runs]
- **Key result**: [One sentence with the number]
- **Result files**: results/exp1/final_info.json
- **Figures generated**: figures/exp1_comparison.pdf
- **Surprising findings**: [Anything unexpected]

### Experiment 2: [Name]
...

## Figures
| Filename | Description | Which section it belongs in |
|----------|-------------|---------------------------|
| figures/main_comparison.pdf | Bar chart comparing all methods on benchmark X | Results, Figure 2 |
| figures/ablation.pdf | Ablation removing components A, B, C | Results, Figure 3 |
...

## Failed Experiments (document for honesty)
- [What was tried, why it failed, what it tells us]

## Open Questions
- [Anything the results raised that the paper should address]
```

**为何这很重要**：在撰写初稿时，智能体（或被委托的子智能体）可以同时加载 `experiment_log.md` 与 LaTeX 模板，从而基于实际实验结果生成初稿。若没有这一桥梁，写作智能体就必须解析原始的 JSON/CSV 文件并自行推断内容——而这正是导致数据失真或错误报告的常见原因。

**Git 使用规范**：将日志文件与其描述的结果一起提交。

---

## 逐步优化：策略选择

该流程中的任何输出——论文初稿、实验脚本、分析报告——均可通过迭代方式不断优化。Autoreason 研究提供了实证数据，说明每种优化策略在何种情况下有效，又在何种情况下失效。请参考本节内容选择合适的策略。

### 快速决策表

| 您的情况 | 推荐策略 | 原因 |
|---------|----------|------|
| 中等性能模型 + 有约束的任务 | **Autoreason** | 此类场景下，模型生成能力与自我评估能力之间的差距最大，基准方法能有效削弱模型较差的输出结果。 |
| 中等性能模型 + 开放式任务 | 带有范围限制的 **Autoreason** | 通过添加固定事实、结构或交付要求，限定优化空间。 |
| 最先进模型 + 有约束的任务 | **Autoreason** | 即使使用最先进的模型，在有约束的任务中也能在三分之二的案例中取得良好效果。 |
| 最先进模型 + 无约束任务 | **批判与修订** 或 **单次处理** | 此类情况下 Autoreason 效果较差，因为模型自身的自我评估能力已经足够优秀。 |
| 具体技术任务（如系统设计） | **批判与修订** | 直接的“发现问题-修正问题”循环效率更高。 |
| 填充模板型任务（仅需正确结构） | **单次处理** 或 **保守策略** | 决策空间极小，迭代无法带来额外价值。 |
| 包含测试用例的代码 | **Autoreason（代码变体）** | 先分析代码失败的原因，再针对性修复，恢复率为 62%，而传统方法仅为 43%。 |
| 非常弱的模型（如 Llama 8B 级别） | **单次处理** | 模型能力太弱，无法生成多样化的候选方案，应优先提升生成质量。 |

### 生成能力与评估能力之间的差距

**核心观点**：Autoreason 的价值取决于模型生成能力与其自我评估能力之间的差距大小。

```
Model Tier        │ Generation │ Self-Eval │ Gap    │ Autoreason Value
──────────────────┼────────────┼───────────┼────────┼─────────────────
Weak (Llama 8B)   │ Poor       │ Poor      │ Small  │ None — can't generate diverse candidates
Mid (Haiku 3.5)   │ Decent     │ Poor      │ LARGE  │ MAXIMUM — 42/42 perfect Borda
Mid (Gemini Flash)│ Decent     │ Moderate  │ Large  │ High — wins 2/3
Strong (Sonnet 4) │ Good       │ Decent    │ Medium │ Moderate — wins 3/5
Frontier (S4.6)   │ Excellent  │ Good      │ Small  │ Only with constraints
```

这一差距是结构性而非暂时的。随着成本下降，如今的先进方案明日便可能沦为中等水平，但最佳解决方案始终存在，只是位置会发生变化。

### Autoreason 循环（概述）

每次循环都会从全新的独立智能体中生成三个候选方案：

1. **批评者** → 找出现有方案A的问题（不提供修复方案）
2. **作者B** → 根据批评意见修改方案A
3. **合成器** → 合并方案A和B（标签随机分配）
4. **评审小组** → 3名盲评的思维链评审员通过博尔达计分法对A、B及AB组合进行评分
5. **收敛判定** → 若方案A在连续k=2次循环中胜出，则流程结束

**关键参数：**
- k=2次收敛判定（k=1则收敛过早，k=3则成本过高且无法提升质量）
- 始终使用思维链评审员（可使收敛速度提升3倍）
- 作者的随机温度值为0.8，评审员的为0.3
- 保守的平局处理规则：现有方案在平局中获胜
- 每个角色均为全新的智能体，彼此之间没有共享上下文

### 在论文初稿中的应用

通过autoreason优化论文本身时：
- **为批评者提供真实依据**：实际的实验数据、结果JSON文件及统计输出。若缺乏这些信息，模型可能会编造虚假的消融实验和伪置信区间。
- **至少使用3名评审智能体**：若某个评审解析器出现故障，不会仅产生噪声，而是会导致整个系统无法达到平衡状态。
- **明确限定修改范围**：应指定“解决这些具体缺陷”，而非笼统地要求“改进论文”。

### 失效模式

| 失效类型 | 检测方式 | 解决方案 |
|---------|---------|---------|
| 无法收敛（方案A始终未胜出） | 20次以上循环后方案A的得分提升仍低于15% | 为任务添加更明确的范围约束 |
| 合成结果偏离 | 文字量无限制增长 | 对结构及最终输出结果设置限制 |
| 性能低于单次循环水平 | 基线模型的得分高于迭代后的输出 | 改为单次循环处理；可能是模型能力不足 |
| 过拟合（代码场景） | 公开测试通过率很高，但私有测试通过率很低 | 采用结构化分析方法，而非仅依赖测试反馈 |
| 评审智能体故障 | 解析失败导致评审小组人数少于3人 | 在继续之前先修复解析器 |

如需完整的提示词、博尔达计分规则、模型选择指南、范围约束设计模式及计算资源预算参考，可查看[references/autoreason-methodology.md](references/autoreason-methodology.md)文档。

---

## 第5阶段：论文撰写

**目标**：撰写出完整且可直接投稿的论文。

### 大型项目的上下文管理

一个包含50多个实验文件、多个结果目录以及大量文献注释的论文项目，其上下文窗口很容易被超出。需主动采取管理措施：

**每项撰写任务应加载到上下文中的内容：**

| 撰写任务 | 应加载到上下文的内容 | 不应加载的内容 |
|---------|----------------------|----------------|
| 撰写引言部分 | `experiment_log.md`、研究贡献说明以及5-10篇最相关的论文摘要 | 原始结果JSON文件、完整的实验脚本及所有文献注释 |
| 撰写方法部分 | 实验配置、伪代码及架构描述 | 原始日志文件、其他实验的结果 |
| 撰写结果部分 | `experiment_log.md`、结果汇总表及图表列表 | 完整的分析脚本及中间数据 |
| 撰写相关工作部分 | 已整理好的引用笔记（步骤1.4的输出）及.bib文件 | 实验文件、原始PDF文档 |
| 修订环节 | 完整的论文初稿及特定审稿人的意见 | 其他所有内容 |

**基本原则：**
- **`experiment_log.md`是主要的上下文桥梁**——它无需加载原始数据文件，即可汇总撰写所需的所有信息（详见步骤4.6）
- 在分配任务时，**每次仅加载一个部分的上下文**。负责撰写方法部分的子智能体无需了解文献综述内容。
- **应进行总结而非直接包含原始文件**。对于200行的结果JSON文件，只需加载10行的汇总表；对于50页长的相关论文，只需加载5句话的摘要以及你对其相关性的2行评价。
- **针对非常大的项目**：可创建`context/`目录，存放预先压缩好的摘要文件：
  ```
  context/
    contribution.md          # 1 sentence
    experiment_summary.md    # Key results table (from experiment_log.md)
    literature_map.md        # Organized citation notes
    figure_inventory.md      # List of figures with descriptions
  ```

### 叙事原则

**最核心的洞察**：你的论文并非一系列实验的简单堆砌——而是一个有明确贡献、并用证据支撑的故事。

每一篇成功的机器学习论文都围绕 Neel Nanda 所说的“叙事”展开：一个简短、严谨、基于证据的技术故事，且能给读者带来有价值的启示。

**三个核心要素（在引言部分结束时必须清晰明确）：**

| 核心要素 | 描述 | 验证方式 |
|----------|------|----------|
| **是什么** | 1-3个具体的创新性观点 | 能用一句话概括吗？ |
| **为什么** | 严谨的实证证据 | 实验是否证明了你的假设优于其他替代方案？ |
| **意义何在** | 为何读者应关注此研究 | 它是否解决了学术界公认的问题？ |

**如果无法用一句话概括你的贡献，那就还称不上是一篇论文。**

### 这一指导原则的来源

该技能整合了那些在顶级学术期刊上发表过多篇论文的研究人员所提出的写作理念。这些写作理念最初由 [Orchestra Research](https://github.com/orchestra-research) 以 `ml-paper-writing` 技能的形式整理而成。

| 来源 | 核心贡献 | 链接 |
|------|----------|------|
| **Neel Nanda**（谷歌 DeepMind） | 叙事原则以及“是什么/为什么/意义何在”框架 | [如何撰写机器学习论文](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers) |
| **Sebastian Farquhar**（DeepMind） | 五句话摘要公式 | [如何撰写机器学习论文](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) |
| **Gopen & Swan** | 读者期待的7项原则 | [科学写作的科学](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) |
| **Zachary Lipton** | 词汇选择与避免含糊表述 | [科学写作的启发式方法](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) |
| **Jacob Steinhardt**（加州大学伯克利分校） | 精确性与时态一致性 | [写作技巧](https://bounded-regret.ghost.io/) |
| **Ethan Perez**（Anthropic） | 微观层面的清晰度提升技巧 | [简易论文写作技巧](https://ethanperez.net/easy-paper-writing-tips/) |
| **Andrej Karpathy** | 聚焦单一核心贡献 | 多篇演讲内容 |

**如需深入了解上述任何内容，请参阅：**
- [references/writing-guide.md](references/writing-guide.md) —— 包含示例的完整解释
- [references/sources.md](references/sources.md) —— 完整参考文献列表

### 时间分配建议

建议将大致**相等的时间**分配给以下各部分：
1. 摘要
2. 引言
3. 图表
4. 其余所有内容之和

**原因何在？** 大多数审稿人在阅读到方法部分之前就已经形成了初步判断。而读者阅读论文的顺序通常是：标题 → 摘要 → 引言 → 图表 → 可能再阅读其余部分。

### 写作工作流程

```
Paper Writing Checklist:
- [ ] Step 1: Define the one-sentence contribution
- [ ] Step 2: Draft Figure 1 (core idea or most compelling result)
- [ ] Step 3: Draft abstract (5-sentence formula)
- [ ] Step 4: Draft introduction (1-1.5 pages max)
- [ ] Step 5: Draft methods
- [ ] Step 6: Draft experiments & results
- [ ] Step 7: Draft related work
- [ ] Step 8: Draft conclusion & discussion
- [ ] Step 9: Draft limitations (REQUIRED by all venues)
- [ ] Step 10: Plan appendix (proofs, extra experiments, details)
- [ ] Step 11: Complete paper checklist
- [ ] Step 12: Final review
```

### 两轮润色法

在使用 AI 智能体撰写文档时，可采用**两轮润色法**（该方法在 SakanaAI 的 AI-Scientist 工作流中已被证明非常有效）：

**第一轮——逐节撰写并立即润色：**
针对每个章节，先完成整篇草稿的撰写，随后立即在相同上下文中进行润色。这样能在内容尚新鲜时及时发现局部问题，如表达清晰度、行文流畅性以及内容完整性等方面的缺陷。

**第二轮——结合整篇文档背景进行全局润色：**
在所有章节都撰写完成后，以整篇文档的视角重新审视每一节。此步骤有助于发现跨章节的问题，例如内容重复、术语不一致、叙事逻辑不连贯，以及某些章节承诺的内容与另一章节未能实现的情况之间的矛盾。

```
Second-pass refinement prompt (per section):
"Review the [SECTION] in the context of the complete paper.
- Does it fit with the rest of the paper? Are there redundancies with other sections?
- Is terminology consistent with Introduction and Methods?
- Can anything be cut without weakening the message?
- Does the narrative flow from the previous section and into the next?
Make minimal, targeted edits. Do not rewrite from scratch."
```

### LaTeX错误检查清单

请在每个优化提示中附上此清单。这些是大型语言模型在编写LaTeX时最常出现的错误：

```
LaTeX Quality Checklist (verify after every edit):
- [ ] No unenclosed math symbols ($ signs balanced)
- [ ] Only reference figures/tables that exist (\ref matches \label)
- [ ] No fabricated citations (\cite matches entries in .bib)
- [ ] Every \begin{env} has matching \end{env} (especially figure, table, algorithm)
- [ ] No HTML contamination (</end{figure}> instead of \end{figure})
- [ ] No unescaped underscores outside math mode (use \_ in text)
- [ ] No duplicate \label definitions
- [ ] No duplicate section headers
- [ ] Numbers in text match actual experimental results
- [ ] All figures have captions and labels
- [ ] No overly long lines that cause overfull hbox warnings
```

### 第5.0步：标题

标题是论文中被阅读最多的部分，它决定了是否有人会继续点击查看摘要。

**优秀的标题**：
- 直接说明研究贡献或发现：“Autoreason：迭代式大语言模型优化何时有效以及为何失败”
- 突出令人惊讶的结果：“扩展数据受限的语言模型”（暗示该方法可行）
- 明确方法名称及其功能：“DPO：语言模型的直接偏好优化”

**糟糕的标题**：
- 过于笼统：“一种改进语言模型输出的方法”
- 过长：字数超过15词
- 全是专业术语：“迭代式随机策略优化的渐近收敛性”（这类标题对谁有意义？）

**撰写规则**：
- 如果有自定义方法名称，请务必包含（便于引用）
- 置入1-2个审稿人常用的关键词
- 尽量避免使用冒号，除非前后两部分都有实际含义
- 进行测试：仅通过标题，审稿人能否了解该研究的领域及其贡献？

### 第5.1步：摘要（五句结构公式）

出自DeepMind的Sebastian Farquhar：

```
1. What you achieved: "We introduce...", "We prove...", "We demonstrate..."
2. Why this is hard and important
3. How you do it (with specialist keywords for discoverability)
4. What evidence you have
5. Your most remarkable number/result
```

**删除**诸如“大型语言模型已取得显著成就……”这类泛化的开头语。

### 第5.2步：图1

图1是除摘要之外，大多数读者最先关注的第二个内容。应在撰写引言之前先草拟它——这能迫使你明确核心思想。

| 图1类型 | 适用场景 | 示例 |
|---------|----------|------|
| **方法示意图** | 新架构或新流程 | 用TikZ绘制的系统结构图 |
| **结果预览图** | 一个突出的结果即可说明全部要点 | 柱状图：展示“本方法与基准方法的对比”，并清晰显示差距 |
| **问题示意图** | 问题本身不易理解时使用 | 展示问题出现前后的状态，以体现你解决的问题 |
| **概念性图表** | 抽象的贡献需要可视化支撑时使用 | 方法特性的2×2矩阵图 |

**规则**：仅凭图1本身就应能让人理解其含义。图注应足以传达核心思想。使用颜色要有目的性——切勿仅为装饰。

### 第5.3步：引言（最多1-1.5页）

必须包含以下内容：
- 明确的问题陈述
- 简要的方法概述
- 2-4项贡献列表（每项最多1-2行，采用双栏格式）
- 方法部分应从第2-3页开始

### 第5.4步：方法部分

为便于复现，需提供：
- 方法的概念性概要或伪代码
- 所有超参数的清单
- 足以用于复现的架构细节
- 需明确说明最终的设计决策；实验部分再介绍各种消融实验

### 第5.5步：实验与结果

对于每个实验，需明确说明：
- **该实验支持何种论点**
- 它与主要贡献之间的关联
- 需观察的内容：“蓝线显示了X，这证明了Y”

要求包括：
- 带有计算方法的误差条（标准差与标准误）
- 超参数的搜索范围
- 计算基础设施信息（GPU类型、总计算时长）
- 种子设置方法

### 第5.6步：相关工作

应按方法论而非单篇论文的顺序进行组织。需大量引用相关文献——审稿人很可能也撰写过相关论文。

### 第5.7步：局限性分析（必填）

所有重要会议都要求此项内容。诚实的态度有助于：
- 审稿人被要求不要因作者诚实地承认局限性而扣分
- 通过提前指出缺陷来避免后续批评
- 解释为何这些局限性不会动摇核心论点

### 第5.8步：结论与讨论

**结论部分**（必填，0.5-1页）：
- 用一句话重述贡献内容（表述方式需与摘要不同）
- 用2-3句话总结关键发现（不要以列表形式）
- 讨论意义：这对该领域有何影响？
- 后续工作：列出2-3项具体的下一步计划（避免使用“我们将在未来工作中解决X”这类模糊表述）

**讨论部分**（可选，有时与结论合并）：
- 超出直接结果的更广泛意义
- 与其他子领域的关联
- 对该方法何时有效、何时无效的客观评估
- 实际部署时的考虑因素

**切勿**在结论部分引入新的结果或论点。

### 第5.9步：附录编写策略

所有重要会议都允许使用无限数量的附录，且附录对于实现研究复现至关重要。附录结构如下：

| 附录章节 | 内容 |
|---------|------|
| **证明与推导** | 过于冗长的完整证明。正文中可仅陈述定理，并注明“证明见附录A” |
| **额外实验** | 消融实验、性能变化曲线、各数据集的详细分析、超参数敏感性分析 |
| **实现细节** | 完整的超参数表、训练细节、硬件规格、随机种子信息 |
| **数据集文档** | 数据收集过程、标注指南、许可协议、预处理步骤 |
| **提示词与模板** | 所使用的具体提示词（针对基于LLM的方法）、评估模板 |
| **人工评估相关内容** | 标注界面截图、给标注人员的指导说明、伦理审查委员会相关文件 |
| **其他图表** | 各任务的详细分析结果、行为轨迹可视化图、失败案例示例 |

**规则**：
- 正文必须具备自含性——审稿人无需阅读附录
- 绝不能将关键证据仅放在附录中
- 需进行交叉引用，例如“完整结果见表5（附录B）”，而不仅仅是“参见附录”
- 应使用`\appendix`命令，然后依次使用`\section{A: Proofs}`等格式

### 页面篇幅管理

当超出页数限制时：

| 缩减策略 | 节省的页数 | 风险 |
|---------|-----------|------|
| 将证明内容移至附录 | 0.5-2页 | 低——这是常规做法 |
| 精简相关工作描述 | 0.5-1页 | 中——可能会遗漏重要引用 |
| 合并表格与子图 | 0.25-0.5页 | 低——通常能提升可读性 |
| 适度使用`\vspace{-Xpt}`命令 | 0.1-0.3页 | 若调整得当风险较低，否则可能影响排版 |
| 删除定性示例 | 0.5-1页 | 中——审稿人通常喜欢示例内容 |
| 缩小图表尺寸 | 0.25-0.5页 | 风险较高——图表仍需保持可读性 |

**切勿**：缩小字体大小、更改页边距、删除必填部分（如局限性分析、更广泛的影响分析），或对正文使用`\small`/`\footnotesize`格式。

### 第5.10步：伦理与更广泛影响声明

目前大多数会议都要求或强烈建议提交伦理/更广泛影响声明。这并非套话——审稿人会仔细阅读，若发现伦理问题可能会直接导致论文被拒收。

**应包含的内容**：

| 组件 | 内容 | 要求提交的会议 |
|-------|------|--------------|
| **积极的社会影响** | 你的工作如何造福社会 | NeurIPS、ICML |
| **潜在的负面影响** | 滥用风险、双重用途问题、失效情况 | NeurIPS、ICML |
| **公平性与偏见** | 你的方法或数据是否存在已知偏见？ | 所有会议（虽未明说，但需体现） |
| **环境影响** | 大规模训练所产生的碳排放 | ICML，NeurIPS也越来越重视此项内容 |
| **隐私问题** | 你的工作是否涉及或可能用于处理个人数据？ | ACL、NeurIPS |
| **LLM使用披露** | 在写作或实验过程中是否使用了人工智能？ | ICLR（强制要求）、ACL |

**撰写声明时需注意**：

```latex
\section*{Broader Impact Statement}
% NeurIPS/ICML: after conclusion, does not count toward page limit

% 1. Positive applications (1-2 sentences)
This work enables [specific application] which may benefit [specific group].

% 2. Risks and mitigations (1-3 sentences, be specific)
[Method/model] could potentially be misused for [specific risk]. We mitigate
this by [specific mitigation, e.g., releasing only model weights above size X,
including safety filters, documenting failure modes].

% 3. Limitations of impact claims (1 sentence)
Our evaluation is limited to [specific domain]; broader deployment would
require [specific additional work].
```

**常见错误：**
- 写出“我们预计不会产生任何负面影响”（这几乎从不对——审稿人对此深感怀疑）
- 表述含糊：仅称“这可能被滥用”却未说明具体方式
- 未考虑大规模任务所带来的计算成本
- 在要求披露的场合忘记说明使用了大语言模型

**计算碳足迹**（针对训练数据量庞大的论文）：
```python
# Estimate using ML CO2 Impact tool methodology
gpu_hours = 1000  # total GPU hours
gpu_tdp_watts = 400  # e.g., A100 = 400W
pue = 1.1  # Power Usage Effectiveness (data center overhead)
carbon_intensity = 0.429  # kg CO2/kWh (US average; varies by region)

energy_kwh = (gpu_hours * gpu_tdp_watts * pue) / 1000
carbon_kg = energy_kwh * carbon_intensity
print(f"Energy: {energy_kwh:.0f} kWh, Carbon: {carbon_kg:.0f} kg CO2eq")
```

### 第5.11步：数据集说明文档与模型卡片（如适用）

如果您的论文介绍了**新的数据集**或**发布了新模型**，请提供结构化的文档。审稿人越来越期望看到此类内容，NeurIPS的数据集与基准测试跟踪系统也要求必须提交。

**数据集的说明文档**（Gebru等人，2021年）——可放入附录中：

```
Dataset Documentation (Appendix):
- Motivation: Why was this dataset created? What task does it support?
- Composition: What are the instances? How many? What data types?
- Collection: How was data collected? What was the source?
- Preprocessing: What cleaning/filtering was applied?
- Distribution: How is the dataset distributed? Under what license?
- Maintenance: Who maintains it? How to report issues?
- Ethical considerations: Contains personal data? Consent obtained?
  Potential for harm? Known biases?
```

**模型卡片**（Mitchell等人，2019年）——应作为模型使用许可的附录内容包含在内：

```
Model Card (Appendix):
- Model details: Architecture, training data, training procedure
- Intended use: Primary use cases, out-of-scope uses
- Metrics: Evaluation metrics and results on benchmarks
- Ethical considerations: Known biases, fairness evaluations
- Limitations: Known failure modes, domains where model underperforms
```

### 写作风格

**句子层面的清晰度（Gopen与Swan提出的7项原则）：**

| 原则 | 规则 |
|------|------|
| 主语与动词靠近 | 将主语和动词置于相近位置 |
| 重音位置 | 将强调部分放在句子末尾 |
| 主题优先 | 先介绍背景信息，再呈现新内容 |
| 旧信息在前，新信息在后 | 先阐述已知内容，再介绍未知内容 |
| 一个单元，一个功能 | 每段只阐述一个观点 |
| 动词体现动作性 | 使用动词，而非名词化表达 |
| 先铺垫背景，再引入新内容 | 在呈现新内容前先做好背景铺垫 |

**词汇选择（Lipton与Steinhardt的建议）：**
- 表述要具体：使用“准确性”而非“性能”
- 避免含糊用语：除非确实不确定，否则不要使用“可能”这类词
- 全文术语保持一致
- 避免渐进式词汇表达：使用“开发”而非“组合”

**包含示例的完整写作指南**：请参阅[references/writing-guide.md](references/writing-guide.md)

### 使用LaTeX模板

**务必先复制整个模板目录，然后再在其中进行编写。**

```
Template Setup Checklist:
- [ ] Step 1: Copy entire template directory to new project
- [ ] Step 2: Verify template compiles as-is (before any changes)
- [ ] Step 3: Read the template's example content to understand structure
- [ ] Step 4: Replace example content section by section
- [ ] Step 5: Use template macros (check preamble for \newcommand definitions)
- [ ] Step 6: Clean up template artifacts only at the end
```

**步骤 1：复制完整模板**

```bash
cp -r templates/neurips2025/ ~/papers/my-paper/
cd ~/papers/my-paper/
ls -la  # Should see: main.tex, neurips.sty, Makefile, etc.
```

请复制整个目录，而不仅仅是 .tex 文件。模板中包含样式文件（.sty）、参考文献样式文件（.bst）、示例内容以及 Makefile。

**步骤 2：首先验证模板能否正常编译**

在进行任何修改之前：
```bash
latexmk -pdf main.tex
# Or manual: pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

如果未经修改的模板无法编译，请先解决该问题（通常是由于缺少TeX相关包——可通过`tlmgr install <package>`进行安装）。

**步骤3：将模板内容保留作为参考**

请勿立即删除示例内容，应将其注释掉并用作格式参考：
```latex
% Template example (keep for reference):
% \begin{figure}[t]
%   \centering
%   \includegraphics[width=0.8\linewidth]{example-image}
%   \caption{Template shows caption style}
% \end{figure}

% Your actual figure:
\begin{figure}[t]
  \centering
  \includegraphics[width=0.8\linewidth]{your-figure.pdf}
  \caption{Your caption following the same style.}
\end{figure}
```

**第4步：逐部分替换内容**

请按顺序进行操作：标题/作者 → 摘要 → 引言 → 方法 → 实验 → 相关工作 → 结论 → 参考文献 → 附录。每完成一个部分后及时进行整合。 

**第5步：使用模板宏**

```latex
\newcommand{\method}{YourMethodName}  % Consistent method naming
\newcommand{\eg}{e.g.,\xspace}        % Proper abbreviations
\newcommand{\ie}{i.e.,\xspace}
```

### 模板使用常见问题

| 问题类型 | 具体表现 | 解决方案 |
|---------|---------|----------|
| 仅复制 `.tex` 文件 | 缺少 `.sty` 文件，导致无法编译 | 需复制整个目录 |
| 修改 `.sty` 文件 | 破坏会议要求的格式规范 | 绝不对样式文件进行编辑 |
| 添加随机软件包 | 引发冲突，破坏模板结构 | 仅在必要时添加 |
| 过早删除模板内容 | 丢失格式参考信息 | 在完成全部内容前以注释形式保留 |
| 不频繁编译 | 错误逐渐累积 | 每写完一个章节后及时编译 |
| 使用光栅格式的 PNG 图片 | 打印输出时图像模糊 | 始终通过 `savefig('fig.pdf')` 生成矢量 PDF 格式图片 |

### 模板快速参考表

| 会议名称 | 主要文件 | 样式文件 | 页面限制 |
|----------|---------|---------|----------|
| NeurIPS 2025 | `main.tex` | `neurips.sty` | 9页 |
| ICML 2026 | `example_paper.tex` | `icml2026.sty` | 8页 |
| ICLR 2026 | `iclr2026_conference.tex` | `iclr2026_conference.sty` | 9页 |
| ACL 2025 | `acl_latex.tex` | `acl.sty` | 8页（长文版） |
| AAAI 2026 | `aaai2026-unified-template.tex` | `aaai2026.sty` | 7页 |
| COLM 2025 | `colm2025_conference.tex` | `colm2025_conference.sty` | 9页 |

**通用规则**：采用双盲评审机制，参考文献不计入页数限制，附录数量无上限，必须使用 LaTeX 格式。

所有模板均存放在 `templates/` 目录中。关于编译设置的相关信息（包括 VS Code、CLI、Overleaf 及其他集成开发环境的使用方法），请参阅 [templates/README.md](templates/README.md) 文件。

### 表格与图表

**表格格式**——建议使用 `booktabs` 包以实现专业级的排版效果：

```latex
\usepackage{booktabs}
\begin{tabular}{lcc}
\toprule
Method & Accuracy $\uparrow$ & Latency $\downarrow$ \\
\midrule
Baseline & 85.2 & 45ms \\
\textbf{Ours} & \textbf{92.1} & 38ms \\
\bottomrule
\end{tabular}
```

规则：  
- 用粗体标出各项指标的最佳数值；  
- 使用方向符号（$\uparrow$

```latex
% --- Professional Packages (add after conference style file) ---

% Typography
\usepackage{microtype}              % Microtypographic improvements (protrusion, expansion)
                                     % Makes text noticeably more polished — always include

% Tables
\usepackage{booktabs}               % Professional table rules (\toprule, \midrule, \bottomrule)
\usepackage{siunitx}                % Consistent number formatting, decimal alignment
                                     % Usage: \num{12345} → 12,345; \SI{3.5}{GHz} → 3.5 GHz
                                     % Table alignment: S column type for decimal-aligned numbers

% Figures
\usepackage{graphicx}               % Include graphics (\includegraphics)
\usepackage{subcaption}             % Subfigures with (a), (b), (c) labels
                                     % Usage: \begin{subfigure}{0.48\textwidth} ... \end{subfigure}

% Diagrams and Algorithms
\usepackage{tikz}                   % Programmable vector diagrams
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc, fit, backgrounds}
\usepackage[ruled,vlined]{algorithm2e}  % Professional pseudocode
                                     % Alternative: \usepackage{algorithmicx} if template bundles it

% Cross-references
\usepackage{cleveref}               % Smart references: \cref{fig:x} → "Figure 1"
                                     % MUST be loaded AFTER hyperref
                                     % Handles: figures, tables, sections, equations, algorithms

% Math (usually included by conference .sty, but verify)
\usepackage{amsmath,amssymb}        % AMS math environments and symbols
\usepackage{mathtools}              % Extends amsmath (dcases, coloneqq, etc.)

% Colors (for figures and diagrams)
\usepackage{xcolor}                 % Color management
% Okabe-Ito colorblind-safe palette:
\definecolor{okblue}{HTML}{0072B2}
\definecolor{okorange}{HTML}{E69F00}
\definecolor{okgreen}{HTML}{009E73}
\definecolor{okred}{HTML}{D55E00}
\definecolor{okpurple}{HTML}{CC79A7}
\definecolor{okcyan}{HTML}{56B4E9}
\definecolor{okyellow}{HTML}{F0E442}
```

**注意事项：**
- `microtype` 是对视觉质量提升效果最显著的包，它能在亚像素级别调整字符间距，因此务必加入。
- `siunitx` 可通过 `S` 列类型来实现表格中数值的对齐，从而无需手动调整间距。
- `cleveref` 必须在 `hyperref` 之后加载。由于大多数会议主题文件已包含 `hyperref`，因此应将 `cleveref` 放在最后。
- 请检查会议模板是否已预先加载了这些包中的任意一个（尤其是 `algorithm`、`amsmath`、`graphicx`），避免重复加载。

### siunitx 的表格对齐功能

`siunitx` 能显著提升包含大量数值的表格的可读性：

```latex
\begin{tabular}{l S[table-format=2.1] S[table-format=2.1] S[table-format=2.1]}
\toprule
Method & {Accuracy $\uparrow$} & {F1 $\uparrow$} & {Latency (ms) $\downarrow$} \\
\midrule
Baseline         & 85.2  & 83.7  & 45.3 \\
Ablation (no X)  & 87.1  & 85.4  & 42.1 \\
\textbf{Ours}    & \textbf{92.1} & \textbf{90.8} & \textbf{38.7} \\
\bottomrule
\end{tabular}
```

`S` 类型的列会自动以小数点为对齐基准。位于 `{}` 中的表头可避免受此对齐规则的影响。

### 子图

并排显示图表的标准格式：

```latex
\begin{figure}[t]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \centering
    \includegraphics[width=\textwidth]{fig_results_a.pdf}
    \caption{Results on Dataset A.}
    \label{fig:results-a}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \centering
    \includegraphics[width=\textwidth]{fig_results_b.pdf}
    \caption{Results on Dataset B.}
    \label{fig:results-b}
  \end{subfigure}
  \caption{Comparison of our method across two datasets. (a) shows the scaling
  behavior and (b) shows the ablation results. Both use 5 random seeds.}
  \label{fig:results}
\end{figure}
```

使用 `\cref{fig:results}` 表示“图1”，使用 `\cref{fig:results-a}` 表示“图1a”。

### 使用 algorithm2e 编写的伪代码

```latex
\begin{algorithm}[t]
\caption{Iterative Refinement with Judge Panel}
\label{alg:method}
\KwIn{Task $T$, model $M$, judges $J_1 \ldots J_n$, convergence threshold $k$}
\KwOut{Final output $A^*$}
$A \gets M(T)$ \tcp*{Initial generation}
$\text{streak} \gets 0$\;
\While{$\text{streak} < k$}{
  $C \gets \text{Critic}(A, T)$ \tcp*{Identify weaknesses}
  $B \gets M(T, C)$ \tcp*{Revised version addressing critique}
  $AB \gets \text{Synthesize}(A, B)$ \tcp*{Merge best elements}
  \ForEach{judge $J_i$}{
    $\text{rank}_i \gets J_i(\text{shuffle}(A, B, AB))$ \tcp*{Blind ranking}
  }
  $\text{winner} \gets \text{BordaCount}(\text{ranks})$\;
  \eIf{$\text{winner} = A$}{
    $\text{streak} \gets \text{streak} + 1$\;
  }{
    $A \gets \text{winner}$; $\text{streak} \gets 0$\;
  }
}
\Return{$A$}\;
\end{algorithm}
```

### TikZ 图表模板

TikZ 是机器学习论文中方法图的标准工具。常见图表模板包括：

**流程图/管道图**（在机器学习论文中最常用）：

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=1.8cm,
  box/.style={rectangle, draw, rounded corners, minimum height=1cm, 
              minimum width=2cm, align=center, font=\small},
  arrow/.style={-{Stealth[length=3mm]}, thick},
]
  \node[box, fill=okcyan!20] (input) {Input\\$x$};
  \node[box, fill=okblue!20, right of=input] (encoder) {Encoder\\$f_\theta$};
  \node[box, fill=okgreen!20, right of=encoder] (latent) {Latent\\$z$};
  \node[box, fill=okorange!20, right of=latent] (decoder) {Decoder\\$g_\phi$};
  \node[box, fill=okred!20, right of=decoder] (output) {Output\\$\hat{x}$};
  
  \draw[arrow] (input) -- (encoder);
  \draw[arrow] (encoder) -- (latent);
  \draw[arrow] (latent) -- (decoder);
  \draw[arrow] (decoder) -- (output);
\end{tikzpicture}
\caption{Architecture overview. The encoder maps input $x$ to latent 
representation $z$, which the decoder reconstructs.}
\label{fig:architecture}
\end{figure}
```

**对比/矩阵图**（用于展示不同的方法变体）：

```latex
\begin{tikzpicture}[
  cell/.style={rectangle, draw, minimum width=2.5cm, minimum height=1cm, 
               align=center, font=\small},
  header/.style={cell, fill=gray!20, font=\small\bfseries},
]
  % Headers
  \node[header] at (0, 0) {Method};
  \node[header] at (3, 0) {Converges?};
  \node[header] at (6, 0) {Quality?};
  % Rows
  \node[cell] at (0, -1) {Single Pass};
  \node[cell, fill=okgreen!15] at (3, -1) {N/A};
  \node[cell, fill=okorange!15] at (6, -1) {Baseline};
  \node[cell] at (0, -2) {Critique+Revise};
  \node[cell, fill=okred!15] at (3, -2) {No};
  \node[cell, fill=okred!15] at (6, -2) {Degrades};
  \node[cell] at (0, -3) {Ours};
  \node[cell, fill=okgreen!15] at (3, -3) {Yes ($k$=2)};
  \node[cell, fill=okgreen!15] at (6, -3) {Improves};
\end{tikzpicture}
```

**迭代循环图**（适用于具有反馈机制的方法）：

```latex
\begin{tikzpicture}[
  node distance=2cm,
  box/.style={rectangle, draw, rounded corners, minimum height=0.8cm, 
              minimum width=1.8cm, align=center, font=\small},
  arrow/.style={-{Stealth[length=3mm]}, thick},
  label/.style={font=\scriptsize, midway, above},
]
  \node[box, fill=okblue!20] (gen) {Generator};
  \node[box, fill=okred!20, right=2.5cm of gen] (critic) {Critic};
  \node[box, fill=okgreen!20, below=1.5cm of $(gen)!0.5!(critic)$] (judge) {Judge Panel};
  
  \draw[arrow] (gen) -- node[label] {output $A$} (critic);
  \draw[arrow] (critic) -- node[label, right] {critique $C$} (judge);
  \draw[arrow] (judge) -| node[label, left, pos=0.3] {winner} (gen);
\end{tikzpicture}
```

### 用于版本追踪的 LaTeXdiff 工具

在撰写反驳意见时不可或缺——该工具可生成带标记的 PDF 文件，清晰显示不同版本之间的差异：

```bash
# Install
# macOS: brew install latexdiff (or comes with TeX Live)
# Linux: sudo apt install latexdiff

# Generate diff
latexdiff paper_v1.tex paper_v2.tex > paper_diff.tex
pdflatex paper_diff.tex

# For multi-file projects (with \input{} or \include{})
latexdiff --flatten paper_v1.tex paper_v2.tex > paper_diff.tex
```

这样生成的PDF文件中，被删除的内容会以红色斜线标出，新增内容则用蓝色标示——这正是用于补充反驳材料的标准格式。

### 适用于matplotlib的SciencePlots库

安装该库后，即可生成符合出版要求的图表：

```bash
pip install SciencePlots
```

```python
import matplotlib.pyplot as plt
import scienceplots  # registers styles

# Use science style (IEEE-like, clean)
with plt.style.context(['science', 'no-latex']):
    fig, ax = plt.subplots(figsize=(3.5, 2.5))  # Single-column width
    ax.plot(x, y, label='Ours', color='#0072B2')
    ax.plot(x, y2, label='Baseline', color='#D55E00', linestyle='--')
    ax.set_xlabel('Training Steps')
    ax.set_ylabel('Accuracy')
    ax.legend()
    fig.savefig('paper/fig_results.pdf', bbox_inches='tight')

# Available styles: 'science', 'ieee', 'nature', 'science+ieee'
# Add 'no-latex' if LaTeX is not installed on the machine generating plots
```

**标准图表尺寸**（双栏格式）：
- 单栏：`figsize=(3.5, 2.5)` —— 适合单栏显示
- 双栏：`figsize=(7.0, 3.0)` —— 覆盖两栏
- 正方形：`figsize=(3.5, 3.5)` —— 适用于热力图和混淆矩阵

---

## 第6阶段：自我评审与修改

**目标**：在提交前模拟评审流程，及早发现不足之处。

### 步骤6.1：模拟多视角评审（集成模式）

从多个角度生成评审意见。自动化研究流程（尤其是SakanaAI的AI科学家工具）带来的重要启示是：**通过元评审员进行集成式评审，能够比单次评审获得更为精准的反馈。**

**步骤1：生成N份独立的评审意见**（N=3-5）

可使用不同的模型或温度参数。每位评审员仅查看论文本身，而无法看到其他人的评审意见。**默认采用负面倾向**——已有大量研究证明，大型语言模型在评估时存在明显的正面偏差。

```
You are an expert reviewer for [VENUE]. You are critical and thorough.
If a paper has weaknesses or you are unsure about a claim, flag it clearly
and reflect that in your scores. Do not give the benefit of the doubt.

Review this paper according to the official reviewer guidelines. Evaluate:

1. Soundness (are claims well-supported? are baselines fair and strong?)
2. Clarity (is the paper well-written? could an expert reproduce it?)
3. Significance (does this matter to the community?)
4. Originality (new insights, not just incremental combination?)

Provide your review as structured JSON:
{
  "summary": "2-3 sentence summary",
  "strengths": ["strength 1", "strength 2", ...],
  "weaknesses": ["weakness 1 (most critical)", "weakness 2", ...],
  "questions": ["question for authors 1", ...],
  "missing_references": ["paper that should be cited", ...],
  "soundness": 1-4,
  "presentation": 1-4,
  "contribution": 1-4,
  "overall": 1-10,
  "confidence": 1-5
}
```

**第2步：元评审（领域主席汇总）**

将所有N份评审意见提交给元评审员进行处理：

```
You are an Area Chair at [VENUE]. You have received [N] independent reviews
of a paper. Your job is to:

1. Identify consensus strengths and weaknesses across reviewers
2. Resolve disagreements by examining the paper directly
3. Produce a meta-review that represents the aggregate judgment
4. Use AVERAGED numerical scores across all reviews

Be conservative: if reviewers disagree on whether a weakness is serious,
treat it as serious until the authors address it.

Reviews:
[review_1]
[review_2]
...
```

**步骤3：反馈循环**（可选，进行2-3轮）

每位审稿人在查看元审评意见后，均可进一步优化自己的审稿内容。可设置提前终止条件：若审稿人回复“我已经完成”（即无需任何修改），则停止迭代。

**用于审稿的模型选择**：即便论文最初是用性能较低的模型撰写的，也建议使用当前最强大的模型来进行审稿。审稿模型应与写作模型分开选择。

**少样本校准**：如果条件允许，可提供1-2篇来自目标期刊的真实已发表审稿意见作为示例。这能显著提升评分的准确性。相关示例请参阅[references/reviewer-guidelines.md](references/reviewer-guidelines.md)。

### 步骤6.1b：视觉审阅环节（VLM）

仅基于文本的审稿会忽略一类问题：图表质量、排版问题以及视觉一致性。如果您拥有具备视觉处理能力的模型，可以对编译后的PDF文件进行独立的**视觉审阅**：

```
You are reviewing the visual presentation of this research paper PDF.
Check for:
1. Figure quality: Are plots readable? Labels legible? Colors distinguishable?
2. Figure-caption alignment: Does each caption accurately describe its figure?
3. Layout issues: Orphaned section headers, awkward page breaks, figures far from their references
4. Table formatting: Aligned columns, consistent decimal precision, bold for best results
5. Visual consistency: Same color scheme across all figures, consistent font sizes
6. Grayscale readability: Would the figures be understandable if printed in B&W?

For each issue, specify the page number and exact location.
```

该功能能够检测出基于文本的审查无法发现的問題：轴标签难以辨认的图表、距离首次引用位置有三页之远的插图、图2与图5之间不统一的颜色方案，或是明显宽于列宽的表格。

### 第6.1c步：声明验证通过

在完成模拟审查后，还需进行单独的验证流程。此举旨在发现审查人员可能遗漏的事实性错误：

```
Claim Verification Protocol:
1. Extract every factual claim from the paper (numbers, comparisons, trends)
2. For each claim, trace it to the specific experiment/result that supports it
3. Verify the number in the paper matches the actual result file
4. Flag any claim without a traceable source as [VERIFY]
```

在基于智能体的工作流中：可将验证任务委托给一个**全新的子智能体**，该子智能体仅接收论文文本和原始结果文件。全新的上下文环境能有效避免确认偏误——验证者不会“记住”结果本应是什么样的。

### 6.2步：确定反馈优先级

收集评审意见后，需对它们进行分类：

| 优先级 | 应采取的行动 |
|--------|------------|
| **紧急**（存在技术缺陷或缺失基准数据） | 必须立即修复。可能需要开展新的实验 → 回到第2阶段 |
| **高**（存在表述不清问题或缺少消融实验） | 应在本次修订中解决 |
| **中**（存在轻微的写作问题或需要额外实验） | 若时间允许则进行修复 |
| **低**（涉及风格偏好或无关建议） | 记录下来以便日后处理 |

### 6.3步：修订循环

针对每一项紧急/高优先级的问题：
1. 确定受影响的具体章节
2. 撰写修复方案
3. 验证修复方案不会破坏其他论点
4. 更新论文内容
5. 再次检查是否解决了评审者指出的问题

### 6.4步：撰写反驳意见

在提交论文后回应实际评审意见时，撰写反驳意见是一项与常规修订不同的专项技能：

**格式**：逐条回应。针对每位评审者的意见分别进行回复：
```
> R1-W1: "The paper lacks comparison with Method X."

We thank the reviewer for this suggestion. We have added a comparison with 
Method X in Table 3 (revised). Our method outperforms X by 3.2pp on [metric] 
(p<0.05). We note that X requires 2x our compute budget.
```

**规则**：
- 解决所有问题——若遗漏任何一点，审稿人都会察觉。
- 首先给出最有力的回应。
- 表达简洁直接——审稿人需要阅读大量反驳意见。
- 若在反驳期内进行了实验，需一并呈现新结果。
- 即使面对轻微的批评，也绝不可采取防御态度或予以忽视。
- 使用 `latexdiff` 生成标出修改处的 PDF 文件（详见“专业 LaTeX 工具”部分）。
- 对于具体且具有可操作性的反馈，应向审稿人表示感谢（而非泛泛的赞美）。

**禁忌事项**：无依据地声称“我们坚决不同意”；不加解释地称“这超出了研究范围”；仅回应优点而忽视缺点。

### 第 6.5 步：论文进展追踪

在关键节点保存文档快照：
```
paper/
  paper.tex                    # Current working version
  paper_v1_first_draft.tex     # First complete draft
  paper_v2_post_review.tex     # After simulated review
  paper_v3_pre_submission.tex  # Final before submission
  paper_v4_camera_ready.tex    # Post-acceptance final
```

## 第7阶段：投稿准备

**目标**：最终检查、格式调整及正式提交。

### 步骤7.1：会议专用清单

每个会议都要求填写特定的检查清单。请务必仔细填写——未完成的清单可能导致论文被直接拒收。

请参阅 [references/checklists.md](references/checklists.md) 以获取：
- NeurIPS会议的16项论文检查清单
- ICML会议的广泛影响力与可复现性相关要求
- ICLR会议的LLM披露政策
- ACL会议要求的限制条款部分
- 通用投稿前检查清单

### 步骤7.2：匿名化检查清单

双盲评审意味着审稿人无法知晓论文的作者身份。请逐一核对以下所有项目：

```
Anonymization Checklist:
- [ ] No author names or affiliations anywhere in the PDF
- [ ] No acknowledgments section (add after acceptance)
- [ ] Self-citations written in third person: "Smith et al. [1] showed..." not "We previously showed [1]..."
- [ ] No GitHub/GitLab URLs pointing to your personal repos
- [ ] Use Anonymous GitHub (https://anonymous.4open.science/) for code links
- [ ] No institutional logos or identifiers in figures
- [ ] No file metadata containing author names (check PDF properties)
- [ ] No "our previous work" or "in our earlier paper" phrasing
- [ ] Dataset names don't reveal institution (rename if needed)
- [ ] Supplementary materials don't contain identifying information
```

**常见错误**：补充代码中显示了 Git 提交信息、使用了机构工具添加水印的图表、残留了先前草稿中的致谢内容，以及在匿名期结束前就发布了 arXiv 预印本。 

### 第 7.3 步：格式校验

```
Pre-Submission Format Check:
- [ ] Page limit respected (excluding references and appendix)
- [ ] All figures are vector (PDF) or high-res raster (600 DPI PNG)
- [ ] All figures readable in grayscale
- [ ] All tables use booktabs
- [ ] References compile correctly (no "?" in citations)
- [ ] No overfull hboxes in critical areas
- [ ] Appendix clearly labeled and separated
- [ ] Required sections present (limitations, broader impact, etc.)
```

### 第 7.4 步：预编译验证

在尝试运行 `pdflatex` 之前，先执行这些自动检查。在此阶段发现错误，比之后调试编译器输出要高效得多。

```bash
# 1. Lint with chktex (catches common LaTeX mistakes)
# Suppress noisy warnings: -n2 (sentence end), -n24 (parens), -n13 (intersentence), -n1 (command terminated)
chktex main.tex -q -n2 -n24 -n13 -n1

# 2. Verify all citations exist in .bib
# Extract \cite{...} from .tex, check each against .bib
python3 -c "
import re
tex = open('main.tex').read()
bib = open('references.bib').read()
cites = set(re.findall(r'\\\\cite[tp]?{([^}]+)}', tex))
for cite_group in cites:
    for cite in cite_group.split(','):
        cite = cite.strip()
        if cite and cite not in bib:
            print(f'WARNING: \\\\cite{{{cite}}} not found in references.bib')
"

# 3. Verify all referenced figures exist on disk
python3 -c "
import re, os
tex = open('main.tex').read()
figs = re.findall(r'\\\\includegraphics(?:\[.*?\])?{([^}]+)}', tex)
for fig in figs:
    if not os.path.exists(fig):
        print(f'WARNING: Figure file not found: {fig}')
"

# 4. Check for duplicate \label definitions
python3 -c "
import re
from collections import Counter
tex = open('main.tex').read()
labels = re.findall(r'\\\\label{([^}]+)}', tex)
dupes = {k: v for k, v in Counter(labels).items() if v > 1}
for label, count in dupes.items():
    print(f'WARNING: Duplicate label: {label} (appears {count} times)')
"
```

在继续操作之前，请先解决所有警告信息。对于基于智能体的工作流：需将 chktex 的检测结果反馈给智能体，并给出仅进行最小程度修复的指示。

### 第 7.5 步：最终编译

```bash
# Clean build
rm -f *.aux *.bbl *.blg *.log *.out *.pdf
latexmk -pdf main.tex

# Or manual (triple pdflatex + bibtex for cross-references)
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# Verify output exists and has content
ls -la main.pdf
```

**如果编译失败**：请解析 `.log` 文件以定位首个错误。常见解决方案如下：
- “未定义的控制序列” → 缺少相关包或命令名称拼写有误
- “缺少插入的 $ 符号” → 数学符号出现在数学模式之外
- “文件未找到” → 图片路径错误或缺少 `.sty` 文件
- “引用未定义” → 缺少对应的 `.bib` 条目或未运行 bibtex 工具

### 7.6步：针对不同会议的特殊要求

| 会议名称 | 特殊要求 |
|---------|----------|
| **NeurIPS** | 需在附录中列出论文检查清单，若被录用还需提供通俗摘要 |
| **ICML** | 需提交更详细的“广泛影响声明”（置于结论部分，不计入字数限制） |
| **ICLR** | 需公开所使用的LLM信息，并签署互审协议 |
| **ACL** | 必须包含“局限性说明”章节以及“负责任NLP检查清单” |
| **AAAI** | 风格文件有严格规定——严禁进行任何修改 |
| **COLM** | 需明确阐述该语言模型对整个社区的贡献 |

### 7.7步：会议重投与格式转换

在更换会议模板时，**绝不可直接复制LaTeX文档的序言部分**：

```bash
# 1. Start fresh with target template
cp -r templates/icml2026/ new_submission/

# 2. Copy ONLY content sections (not preamble)
#    - Abstract text, section content, figures, tables, bib entries

# 3. Adjust for page limits
# 4. Add venue-specific required sections
# 5. Update references
```

| 从 → 到 | 页面调整 | 主要修改内容 |
|-----------|-------------|----------------|
| NeurIPS → ICML | 9 → 8 | 删除1页内容，增加“更广泛的影响力”相关描述 |
| ICML → ICLR | 8 → 9 | 扩展实验部分，补充大语言模型相关说明 |
| NeurIPS → ACL | 9 → 8 | 按自然语言处理领域的规范重新组织结构，补充“局限性”章节 |
| ICLR → AAAI | 9 → 7 | 大幅删减内容，严格遵循格式要求 |
| 任意方向 → COLM | 不固定 → 9 | 重新架构内容，突出语言模型的应用 |

在删减页面时：可将证明内容移至附录，精简相关研究综述，合并表格，使用子图。  
在扩充内容时：可增加消融实验，详细阐述局限性，补充更多基线模型，加入定性示例。

**被拒后**：在修改版本中回应审稿人的意见，但不要添加“修改说明”章节，也不要提及之前的投稿信息（因采用盲审机制）。

### 第7.8步：准备最终提交版本（录用后）

论文被录用后，需准备最终提交版本：

```
Camera-Ready Checklist:
- [ ] De-anonymize: add author names, affiliations, email addresses
- [ ] Add Acknowledgments section (funding, compute grants, helpful reviewers)
- [ ] Add public code/data URL (real GitHub, not anonymous)
- [ ] Address any mandatory revisions from meta-reviewer
- [ ] Switch template to camera-ready mode (if applicable — e.g., AAAI \anon → \camera)
- [ ] Add copyright notice if required by venue
- [ ] Update any "anonymous" placeholders in text
- [ ] Verify final PDF compiles cleanly
- [ ] Check page limit for camera-ready (sometimes differs from submission)
- [ ] Upload supplementary materials (code, data, appendix) to venue portal
```

### 第7.9步：arXiv与预印本发布策略

在机器学习领域，将论文发布到arXiv是一种常见做法，但在此过程中需特别注意时间选择与匿名性保障问题。

**时间选择决策树：**

| 情境 | 建议 |
|------|------|
| 向双盲评审会议投稿（如NeurIPS、ICML、ACL） | 应在提交截止日期**之后**才在arXiv上发布，切勿提前。虽然不同会议的执行标准有所差异，但提前发布可能在技术层面违反匿名性政策。 |
| 向ICLR投稿 | ICLR明确允许在提交前将论文发布到arXiv，但提交的论文文本中不得出现作者姓名。 |
| 论文已发布在arXiv上，现向其他会议投稿 | 大多数会议接受此类情况。但在审稿期间，切勿通过更新版本来加入针对审稿意见的修改内容。 |
| 工作坊论文 | 任何时间在arXiv上发布均可——因为工作坊通常不采用双盲评审机制。 |
| 希望抢占发表优先权 | 若担心被他人抢先发表，可立即发布，但需接受由此带来的匿名性牺牲。 |

**arXiv分类选择**（针对机器学习/人工智能论文）：

| 分类 | 代码 | 适用领域 |
|------|------|----------|
| 机器学习 | `cs.LG` | 通用机器学习方法 |
| 计算与语言 | `cs.CL` | 自然语言处理、语言模型 |
| 人工智能 | `cs.AI` | 推理、规划、智能体相关研究 |
| 计算机视觉 | `cs.CV` | 视觉模型 |
| 信息检索 | `cs.IR` | 搜索系统、推荐系统 |

**请选定一个主要分类，再补充1-2个相关的跨领域分类。** 分类越多，论文的曝光度越高，但只有真正相关的分类才建议同时列出。

**版本管理策略：**
- **v1**：初始提交版本（内容与会议提交的版本一致）
- **v2**：论文被接受后发布的最终版本，包含经过整理的修正内容（摘要中需注明“已被[会议名称]接收”）
- 在审稿期间，切勿发布包含针对审稿人意见的修改内容的v2版本。

```bash
# Check if your paper's title is already taken on arXiv
# (before choosing a title)
pip install arxiv
python -c "
import arxiv
results = list(arxiv.Search(query='ti:\"Your Exact Title\"', max_results=5).results())
print(f'Found {len(results)} matches')
for r in results: print(f'  {r.title} ({r.published.year})')
"
```

### 第 7.10 步：代码打包研究

发布整洁且可运行的代码，能够显著提升被引频率以及审稿人的信任度。请将代码与最终提交版本一同进行打包。

**仓库结构：**

```
your-method/
  README.md              # Setup, usage, reproduction instructions
  requirements.txt       # Or environment.yml for conda
  setup.py               # For pip-installable packages
  LICENSE                # MIT or Apache 2.0 recommended for research
  configs/               # Experiment configurations
  src/                   # Core method implementation
  scripts/               # Training, evaluation, analysis scripts
    train.py
    evaluate.py
    reproduce_table1.sh  # One script per main result
  data/                  # Small data or download scripts
    download_data.sh
  results/               # Expected outputs for verification
```

**研究代码的README模板：**

```markdown
# [Paper Title]

Official implementation of "[Paper Title]" (Venue Year).

## Setup
[Exact commands to set up environment]

## Reproduction
To reproduce Table 1: `bash scripts/reproduce_table1.sh`
To reproduce Figure 2: `python scripts/make_figure2.py`

## Citation
[BibTeX entry]
```

**预发布检查清单：**
```
- [ ] Code runs from a clean clone (test on fresh machine or Docker)
- [ ] All dependencies pinned to specific versions
- [ ] No hardcoded absolute paths
- [ ] No API keys, credentials, or personal data in repo
- [ ] README covers setup, reproduction, and citation
- [ ] LICENSE file present (MIT or Apache 2.0 for max reuse)
- [ ] Results are reproducible within expected variance
- [ ] .gitignore excludes data files, checkpoints, logs
```

**待审核时的匿名代码**：
```bash
# Use Anonymous GitHub for double-blind review
# https://anonymous.4open.science/
# Upload your repo → get an anonymous URL → put in paper
```

## 第8阶段：验收后的交付物

**目标**：通过展示材料与社区互动，最大化已获接受的论文的影响力。

### 8.1步骤：会议海报

大多数会议都要求设置海报展示环节。海报设计原则如下：

| 元素 | 设计指南 |
|------|----------|
| **尺寸** | 需符合会场要求（通常为24英寸×36英寸或A0竖版/横版） |
| **内容** | 标题、作者、一句话总结贡献、方法示意图、2-3项关键结果、结论 |
| **排版逻辑** | 从左上角到右下角（Z形排列）或分栏式 |
| **文字要求** | 标题需在3米距离处仍可清晰阅读，正文在1米距离处可读。不可使用完整段落，仅可使用项目符号 |
| **图表要求** | 使用更高分辨率的论文中已有图表，重点结果可放大展示 |

**常用工具**：LaTeX（`beamerposter`包）、PowerPoint/Keynote、Figma、Canva。

**制作时间**：建议在会议开始前2周以上完成。帆布材质的海报更轻便，便于携带。如今许多会议也支持虚拟/数字海报。

### 8.2步骤：会议演讲/焦点报告

若获得口头演讲或焦点报告机会：

| 演讲类型 | 时长 | 内容要点 |
|----------|------|----------|
| **焦点报告** | 5分钟 | 阐述问题、研究方法及一项关键结果。需严格控制在5分钟内完成 |
| **口头演讲** | 15-20分钟 | 完整阐述整个研究过程：问题提出、方法设计、关键结果、消融实验及局限性分析 |
| **研讨会报告** | 10-15分钟 | 需根据研讨会听众特点调整内容，可能需要补充更多背景信息 |

**幻灯片设计规则**：
- 每张幻灯片只呈现一个核心观点
- 尽量减少文字——详细内容需口头阐述，而非直接展示在幻灯片中
- 通过动画逐步展示关键图表，帮助听众逐步理解
- 结尾需添加一张“总结”幻灯片，用一句话概括论文的贡献
- 需准备备用幻灯片，以应对可能出现的提问

### 8.3步骤：博客文章/社交媒体发布

简洁易懂的总结能显著提升论文影响力：

- **Twitter/X系列推文**：5-8条推文。先展示核心结果，再介绍方法。需包含图1及关键结果图表
- **博客文章**：字数在800-1500字之间。面向机器学习实践者而非审稿人撰写，无需过多理论阐述，重点强调直观理解与实际应用价值
- **项目页面**：包含摘要、图表、演示视频、代码链接及BibTeX格式的HTML页面。建议使用GitHub Pages搭建

**发布时机**：在论文被收录到会议论文集或arXiv上可供下载后1-2天内发布。

---

## 研讨会论文与短篇论文

研讨会论文与短篇论文（如ACL短篇论文、Findings论文）遵循相同的处理流程，但存在不同的约束条件和期望标准。

### 研讨会论文

| 对比维度 | 研讨会论文 | 主流会议论文 |
|----------|------------|--------------|
| **页数限制** | 通常为4-6页 | 7-9页 |
| **评审标准** | 对完整性要求较低 | 需要内容完整、详尽 |
| **评审流程** | 通常为单盲或轻度盲审 | 双盲、严格评审 |
| **重视点** | 新颖想法、初步结果、行业观点类文章 | 完整的实证研究，且需有强有力基线对比 |
| **arXiv提交时间** | 可随时提交 | 有特定时间要求（需参考arXiv提交策略） |
| **贡献要求** | 具有新方向、有趣的负面结果或初步研究成果 | 需有重大进展，并有充分证据支撑 |

**何时选择提交研讨会论文**：
- 拥有处于早期阶段的想法，希望在撰写完整论文前获得反馈
- 得到负面结果，但内容不足以支撑8页以上的篇幅
- 想就某个热点话题发表观点或立场文章
- 进行复现研究或可重复性报告

### ACL短篇论文与Findings论文

ACL系列会议设有不同的投稿类型：

| 类型 | 页数 | 需要满足的要求 |
|------|------|----------------|
| **长篇论文** | 8页 | 需包含完整的研究内容、强有力的基线对比及消融实验 |
| **短篇论文** | 4页 | 需聚焦一个明确观点，并提供相应证据支持 |
| **Findings论文** | 8页 | 研究质量优异，但略逊于主流会议论文水平 |

**短篇论文写作策略**：仅选择一个核心论点并予以充分论证。切勿试图将长篇论文的内容压缩到4页内——应另起一篇更聚焦的论文。

---

## 非实证机器学习类的论文类型

上述主要流程适用于实证机器学习类论文。其他类型的论文则需要不同的结构与证据标准。关于各类论文的详细指导，请参阅[references/paper-types.md](references/paper-types.md)文档。

### 理论类论文

**结构**：引言 → 前提知识（定义、符号说明） → 主要结果（定理） → 证明概要 → 讨论 → 完整证明（附录）

**与实证类论文的主要区别**：
- 贡献形式为定理、界或反例结论，而非实验数据
- 方法部分被“前提知识”和“主要结果”替代
- 证明是核心证据，而非实验数据（不过理论结果的实证验证也是可取的）
- 文本中给出证明概要，完整证明放在附录中，这是标准做法
- 实验部分为可选内容，但若能验证理论预测，则可增强论文说服力

**证明写作原则**：
- 以正式方式陈述定理，并明确列出所有假设条件
- 在正式证明之前先给出直观解释（例如：“核心思路是……”）
- 证明概要应在0.5-1页内阐述核心思想
- 使用`\begin{proof}...\end{proof}`格式编写证明
- 为每个假设编号，并在定理中引用，例如：“在假设1-3成立的前提下……”

### 综述/教程类论文

**结构**：引言 → 分类/框架梳理 → 详细内容阐述 → 待解决课题 → 结论

**主要区别**：
- 贡献在于对现有研究的系统整理、综合分析以及待解决问题的识别，而非新方法的提出
- 需在给定范围内做到内容全面（审稿人会检查是否有遗漏的参考文献）
- 需有清晰的分类体系或结构框架
| 价值来源 | 说明 |
|----------|------|
| 理论类论文 | 通过跨论文间的关联分析，揭示现有研究的不足之处 |
| 综述类论文 | 对某一领域的研究进行系统性梳理，指出未来研究方向 |
| 教程类论文 | 提供清晰的学习路径，帮助读者掌握相关技术 |

| 最佳投稿期刊/会议 | 说明 |
|------------------|------|
| TMLR（综述专栏） | 专门收录高质量综述文章 |
| JMLR | 机器学习领域权威期刊，接受各类综述文章 |
| Foundations and Trends in ML | 该系列丛书中的综述文章尤为受欢迎 |
| ACM Computing Surveys | 计算机科学领域经典综述期刊 |

### 基准测试类论文

**结构**：引言 → 任务定义 → 数据集构建 → 基线评估 → 结果分析 → 适用场景与局限性说明

**主要区别**：
- 贡献在于基准测试工具本身——它必须填补现有的评估空白
| 关键要求 | 说明 |
|----------|------|
| 数据集文档 | 属于强制要求，而非可选内容（详见Step 5.11中的数据集模板） |
| 测试难度 | 需证明该基准测试具有足够挑战性（基线模型无法轻易达到理想性能） |
| 测量有效性 | 需证明该基准测试确实能衡量其所宣称的指标（即结构效度） |

| 最佳投稿期刊/会议 | 说明 |
|------------------|------|
| NeurIPS Datasets & Benchmarks专栏 | 专门收录高质量数据集与基准测试相关文章 |
| ACL（资源类论文栏目） | 接受用于方法评估的资源类论文 |
| LREC-COLING | 语言处理领域相关基准测试论文的合适投稿地 |

### 立场观点类论文

**结构**：引言 → 背景介绍 → 核心论点/论证 → 支持证据 → 反驳意见 → 后续影响分析

**主要区别**：
- 贡献在于提出的观点或论证，而非实验结果
- 需认真回应可能的反驳意见
| 证据类型 | 说明 |
|----------|------|
| 实证类 | 基于实验数据的证据 |
| 理论类 | 基于数学推导的证据 |
| 逻辑分析类 | 基于逻辑推理的证据 |

| 最佳投稿期刊/会议 | 说明 |
|------------------|------|
| ICML（立场观点专栏） | 专门收录此类观点性文章 |
| 各类研讨会 | 也适合发表此类观点文章 |
| TMLR | 该系列期刊也欢迎此类文章 |

---

## Hermes Agent集成功能

此技能专为Hermes智能体设计，它利用Hermes提供的工具、任务委托、调度及记忆功能，帮助用户完成整个研究生命周期。

### 相关技能

可结合其他Hermes技能，针对不同阶段使用本技能：

| 技能 | 适用阶段 | 加载方式 |
|------|----------|----------|
| **arxiv** | 第1阶段（文献综述）：搜索arXiv数据库、生成BibTeX格式的参考文献列表、通过Semantic Scholar查找相关论文 | `skill_view("arxiv")` |
| **subagent-driven-development** | 第5阶段（初稿撰写）：实现分模块并行写作，并进行两阶段评审（先检查是否符合结构要求，再评估内容质量） | `skill_view("subagent-driven-development")` |
| **plan** | 第0阶段（准备工作）：在执行任务前制定结构化计划，计划内容会保存到`.hermes/plans/`目录中 | `skill_view("plan")` |
| **qmd** | 第1阶段（文献调研）：通过混合BM25向量搜索技术，检索本地知识库中的笔记、会议记录及文档资料 | 需先执行`skill_manage("install", "qmd")`进行安装 |
| **diagramming** | 第4-5阶段：用于创建基于Excalidraw的图表及系统架构图 | `skill_view("diagramming")` |
| **data-science** | 第4阶段（数据分析）：提供Jupyter实时内核，支持交互式分析和可视化操作 | `skill_view("data-science")` |

**本技能可替代`ml-paper-writing`技能**——它不仅包含该技能的所有内容，还涵盖了完整的实验/分析流程以及自动推理方法。

### Hermes工具参考

| 工具 | 在本流程中的用途 |
|------|------------------|
| **`terminal`** | 用于LaTeX编译（`latexmk -pdf`）、git操作、启动实验脚本（`nohup python run.py &`）、监控进程状态 |
| **`process`** | 用于管理后台运行的实验任务：可执行`process("start", ...)`启动任务，`process("poll", pid)`轮询任务状态，`process("log", pid)`获取任务日志，`process("kill", pid)`终止任务 |
| **`execute_code`** | 用于运行Python代码，实现引用验证、统计分析及数据聚合等功能。该工具可通过RPC接口访问其他工具 |
| **`read_file`** / **`write_file`** / **`patch`** | 用于编辑论文内容、实验脚本及结果文件。对于大型.tex文件，可使用`patch`功能进行精准修改 |
| **`web_search`** | 用于文献检索，例如可执行`web_search("transformer attention mechanism 2024")`查找相关研究 |
| **`web_extract`** | 用于获取论文内容、验证引用信息，例如可执行`web_extract("https://arxiv.org/abs/2303.17651")`提取目标文档内容 |
| **`delegate_task`** | 用于实现分模块并行撰写——可为每个章节启动独立的子智能体，同时也可用于并行进行引用验证任务 |
| **`todo`** | 用于在多轮会话之间跟踪任务状态。每次阶段转换后都需更新该列表 |
| **`memory`** | 用于在多轮会话之间保留关键决策信息，如论文核心观点的定位、目标会议选择、审稿人反馈等 |
| **`cronjob`** | 用于安排实验监控、截止日期提醒以及自动检查arXiv上相关更新的任务 |
| **`clarify`** | 当用户遇到困惑时，可向智能体提出针对性问题，例如关于会议选择或论文核心观点的确定 |
| **cron `deliver:`** | 用于在实验完成或初稿准备好时通知用户，即使用户当前未处于聊天界面中。可通过cron任务设置`deliver:`消息目标，由系统自动发送通知——此时智能体已不再拥有`send_message`功能，外部消息发送由cron任务或`hermes send`功能处理 |

### 工具使用模式

**最常见的用途：实验监控**
```
terminal("ps aux | grep <pattern>")
→ terminal("tail -30 <logfile>")
→ terminal("ls results/")
→ execute_code("analyze results JSON, compute metrics")
→ terminal("git add -A && git commit -m '<descriptive message>' && git push")
→ (final response auto-delivers "Experiment complete: <summary>"; for unattended runs, schedule via cron with a deliver: target)
```

**并行段落撰写**（通过任务委派实现）：
```
delegate_task("Draft the Methods section based on these experiment scripts and configs. 
  Include: pseudocode, all hyperparameters, architectural details sufficient for 
  reproduction. Write in LaTeX using the neurips2025 template conventions.")

delegate_task("Draft the Related Work section. Use web_search and web_extract to 
  find papers. Verify every citation via Semantic Scholar. Group by methodology.")

delegate_task("Draft the Experiments section. Read all result files in results/. 
  State which claim each experiment supports. Include error bars and significance.")
```

每个代理都会作为独立的**子代理**运行，彼此之间没有共享的上下文——请在提示词中提供所有必要的信息。随后收集各子代理的输出并进行整合。

**引用验证**（通过 execute_code 功能实现）：
```python
# In execute_code:
from semanticscholar import SemanticScholar
import requests

sch = SemanticScholar()
results = sch.search_paper("attention mechanism transformers", limit=5)
for paper in results:
    doi = paper.externalIds.get('DOI', 'N/A')
    if doi != 'N/A':
        bibtex = requests.get(f"https://doi.org/{doi}", 
                              headers={"Accept": "application/x-bibtex"}).text
        print(bibtex)
```

### 使用 `memory` 和 `todo` 进行状态管理

**`memory` 工具**——用于持久化关键决策（容量有限：MEMORY.md 文件大小约为 2200 字符）：

```
memory("add", "Paper: autoreason. Venue: NeurIPS 2025 (9 pages). 
  Contribution: structured refinement works when generation-evaluation gap is wide.
  Key results: Haiku 42/42, Sonnet 3/5, S4.6 constrained 2/3.
  Status: Phase 5 — drafting Methods section.")
```

在做出重大决策或经历阶段转换后，需更新内存状态。该设置会在不同会话之间保持有效。

**`todo` 工具**——用于详细追踪进度：

```
todo("add", "Design constrained task experiments for Sonnet 4.6")
todo("add", "Run Haiku baseline comparison")
todo("add", "Draft Methods section")
todo("update", id=3, status="in_progress")
todo("update", id=1, status="completed")
```

**会话启动协议：**
```
1. todo("list")                           # Check current task list
2. memory("read")                         # Recall key decisions
3. terminal("git log --oneline -10")      # Check recent commits
4. terminal("ps aux | grep python")       # Check running experiments
5. terminal("ls results/ | tail -20")     # Check for new results
6. Report status to user, ask for direction
```

### 使用 `cronjob` 进行定时任务监控

可通过 `cronjob` 工具来安排定期的实验检查任务：

```
cronjob("create", {
  "schedule": "*/30 * * * *",  # Every 30 minutes
  "prompt": "Check experiment status:
    1. ps aux | grep run_experiment
    2. tail -30 logs/experiment_haiku.log
    3. ls results/haiku_baselines/
    4. If complete: read results, compute Borda scores, 
       git add -A && git commit -m 'Add Haiku results' && git push
    5. Report: table of results, key finding, next step
    6. If nothing changed: respond with [SILENT]"
})
```

**[SILENT] 协议**：若自上次检查以来没有任何变化，则仅回复 `[SILENT]`。这样即可避免向用户发送通知，仅在确实存在值得知晓的变化时再进行报告。

**截止日期跟踪**：
```
cronjob("create", {
  "schedule": "0 9 * * *",  # Daily at 9am
  "prompt": "NeurIPS 2025 deadline: May 22. Today is {date}. 
    Days remaining: {compute}. 
    Check todo list — are we on track? 
    If <7 days: warn user about remaining tasks."
})
```

### 通信模式

**何时通知用户**（通过您的直接/最终回复，或用于无人值守运行的 cron `deliver:` 目标）：
- 实验批次已完成（附带结果表格）
- 出现需要决策的意外发现或故障
- 草稿部分已准备好供审核
- 任务未完成且截止日期临近

**何时无需通知**：
- 实验仍在运行且无新结果 → `[静默处理]`
- 常规监控未出现变化 → `[静默处理]`
- 不需要关注的中间步骤

**报告格式** —— 必须始终包含结构化数据：
```
## Experiment: <name>
Status: Complete / Running / Failed

| Task | Method A | Method B | Method C |
|------|---------|---------|---------|
| Task 1 | 85.2 | 82.1 | **89.4** |

Key finding: <one sentence>
Next step: <what happens next>
```

### 需要人工决策的环节

当确实遇到决策难题时，可使用 `clarify` 功能针对具体问题进行询问：

| 决策事项 | 询问时机 |
|----------|----------|
| 目标会议 venue | 开始撰写论文之前（涉及页数限制、格式要求等） |
| 贡献内容的表述方式 | 当存在多种合理的表述方案时 |
| 实验优先级排序 | 当待处理的实验数量超过可用时间时 |
| 论文提交准备情况 | 最终提交之前 |

**请避免询问以下内容**（应主动决策并明确选择，或直接标记问题）：
- 用词选择、章节顺序
- 应重点强调哪些具体结果
- 引用完整性（先根据现有资料撰写初稿，再标注缺失部分）

---

## 审稿人评估标准

了解审稿人的关注点有助于更有针对性地完善论文：

| 评估标准 | 审稿人检查内容 |
|----------|----------------|
| **质量** | 技术合理性、论点有充分依据、基线选择合理 |
| **清晰度** | 表达清晰、专家可复现、符号使用统一 |
| **重要性** | 对社区的影响、是否推动领域理解进展 |
| **原创性** | 是否提供新见解（无需采用新方法） |

**评分标准（NeurIPS 6分制）：**
- 6分：强烈录用 —— 具有开创性且无瑕疵
- 5分：录用 —— 技术扎实，影响力高
- 4分：勉强录用 —— 内容扎实，但评估不足
- 3分：勉强拒收 —— 缺点超过优点
- 2分：拒收 —— 存在技术缺陷
- 1分：强烈拒收 —— 为已有成果或存在伦理问题

详细指南、常见问题及反驳策略请参阅 [references/reviewer-guidelines.md](references/reviewer-guidelines.md)。

---

## 常见问题与解决方案

| 问题 | 解决方案 |
|------|----------|
| 摘要过于笼统 | 若开头句适用于任何机器学习论文，则删除它，直接从具体贡献写起。 |
| 引言篇幅超过1.5页 | 将背景内容拆分到“相关工作”部分，将核心贡献要点提前列出。 |
| 实验部分缺乏明确论点 | 在每个实验前添加说明：“本实验旨在验证[具体论点]……” |
| 审稿人认为论文难以理解 | 增加引导性内容，统一术语使用，确保图表标题信息完整。 |
| 缺乏统计显著性说明 | 添加误差范围、实验重复次数、统计检验方法及置信区间。 |
| 实验范围过度扩展 | 每个实验都必须对应一个具体论点，删除无关实验。 |
| 论文被拒需重新提交 | 请参阅第7阶段的“会议重投指南”，在不提及审稿意见的情况下解决存在的问题。 |
| 缺少关于更广泛影响的说明 | 请参考步骤5.10，大多数会议都要求此项内容。“无负面影响”的声明几乎不可信。 |
| 人工评估结果被批评为质量不足 | 请参考步骤2.5及 [references/human-evaluation.md](references/human-evaluation.md)，需报告一致性指标、标注者信息及补偿情况。 |
| 审稿人质疑论文可复现性 | 需发布代码（步骤7.9），详细记录所有超参数，同时提供随机种子和计算细节。 |
| 理论类论文缺乏直观解释 | 在正式证明前添加附有通俗解释的证明概要，详情参见 [references/paper-types.md](references/paper-types.md)。 |
| 实验结果为负面或无显著效果 | 请参考第4.3阶段关于处理负面结果的指南，可考虑将成果发表在研讨会、TMLR系列会议，或重新定义为分析性内容。 |

---

## 参考文档

| 文档 | 内容概述 |
|------|----------|
| [references/writing-guide.md](references/writing-guide.md) | Gopen与Swan的7项写作原则、Perez的实用技巧、Lipton的用词建议、Steinhardt的精确性要求以及图表设计指南 |
| [references/citation-workflow.md](references/citation-workflow.md) | 引用相关API、Python代码、CitationManager类及BibTeX管理方法 |
| [references/checklists.md](references/checklists.md) | NeurIPS的16项检查项、ICML、ICLR、ACL的格式要求，以及通用预提交检查清单 |
| [references/reviewer-guidelines.md](references/reviewer-guidelines.md) | 评估标准、评分规则、常见问题及反驳模板 |
| [references/sources.md](references/sources.md) | 所有写作指南、会议规范及API的完整参考文献列表 |
| [references/experiment-patterns.md](references/experiment-patterns.md) | 实验设计模式、评估方案、监控方法及错误处理策略 |
| [references/autoreason-methodology.md](references/autoreason-methodology.md) | Autoreason循环机制、策略选择方法、模型指南、提示词设计、范围约束及Borda评分法 |
| [references/human-evaluation.md](references/human-evaluation.md) | 人工评估设计流程、标注指南、一致性指标、众包质量检测及IRB相关指导 |
| [references/paper-types.md](references/paper-types.md) | 理论类论文（证明写作、定理结构）、综述论文、基准测试论文及立场声明类论文的撰写规范 |

### LaTeX模板

`templates/`目录中提供以下会议的模板：**NeurIPS 2025**、**ICML 2026**、**ICLR 2026**、**ACL**、**AAAI 2026**、**COLM 2025**。

编译说明请参阅 [templates/README.md](templates/README.md)。

### 主要外部参考资源

**写作理念相关：**
- [Neel Nanda：如何撰写机器学习论文](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers)
- [Sebastian Farquhar：如何撰写机器学习论文](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/)
- [Gopen与Swan：科学写作的科学](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf)
- [Lipton：科学写作的启发式方法](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/)
- [Perez：简单易行的论文写作技巧](https://ethanperez.net/easy-paper-writing-tips/)

**API接口：** [Semantic Scholar](https://api.semanticscholar.org/api-docs/) | [CrossRef](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | [arXiv](https://info.arxiv.org/help/api/basics.html)

**目标会议格式规范：** [NeurIPS](https://neurips.cc/Conferences/2025/PaperInformation/StyleFiles) | [ICML](https://icml.cc/Conferences/2025/AuthorInstructions) | [ICLR](https://iclr.cc/Conferences/2026/AuthorGuide) | [ACL](https://github.com/acl-org/acl-style-files)
