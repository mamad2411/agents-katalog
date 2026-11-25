---
name: math-model-agent-plus
description: "自包含的数学建模竞赛全流程代理，用于从题面与附件完成赛题分析、建模设计、可复现编程、统计与稳健性验证、数据图和按需概念图、文献检索与引用核验、Typst/LaTeX 论文写作以及独立提交验收。适用于新建竞赛项目、根据 run-manifest.json 断点续跑，或对已有数学建模项目执行独立审查；仅在用户显式调用 $math-model-agent-plus 时使用。"
---

# Math Model Agent Plus

把当前请求当作一个有状态的竞赛项目执行。该 skill 完全自包含；不要调用或要求安装旧版分阶段 skill、外部学术写作 skill，或相邻目录中的资源。

## 首要规则

1. 以题面、附件、可追溯外部来源和程序输出为事实依据。未知内容必须标记，禁止补造数据、结果、引用或竞赛规则。
2. 以 `run-manifest.json` 为项目状态唯一真相源；`plan.md` 和 `todo.md` 只做人类可读视图。
3. 以 `results/results.json` 为论文关键数值唯一真相源。正文、摘要、表格和图注不得重新估算数值。
4. 正式图必须使用可追溯的真实输入。模拟数据只允许显式测试模式，且不得进入论文或通过最终验收。
5. 默认在每个阶段产出完成后暂停并请求用户确认。未经确认不得进入下一阶段。
6. 修改已批准阶段时，把所有下游阶段标为 `stale`；保留已有文件，重新生成时不得静默覆盖用户文件。
7. 主代理独占项目文件和状态写入。子代理只可做只读分析、复核或挑战，并返回证据指针。
8. 先满足正确性和可复现性，再追求模型复杂度、图表数量或版式效果。

## 定位资源

先确定本 `SKILL.md` 所在目录为 `SKILL_DIR`。脚本位于 `$SKILL_DIR/scripts/`，论文模板和绘图配方位于 `$SKILL_DIR/assets/`。运行任何脚本前先调用其 `--help`，以本地帮助中的参数为准。

可用 CLI：

- `doctor.py`：只读检查 Python、Typst、XeLaTeX、Ghostscript、DrawIO 和 PDF 工具。
- `project.py`：初始化项目、记录输入哈希、推进/批准阶段、检查恢复状态和传播 `stale`。
- `prepare_paper.py`：从模板目录选择并复制论文模板，不手工拼接模板路径。
- `compile_paper.py`：按引擎编译，LaTeX 至少运行两遍。
- `literature.py`：检索、去重、DOI 核验并导出引用数据；网络不可用时明确降级。
- `results_ledger.py`：校验结果台账并生成 Typst/LaTeX 数值宏。
- `validate_figure.py`：校验图文件及其来源契约。
- `verify_project.py`：执行结构、数值、引用、泄露、编译和提交就绪检查。

脚本失败时保留 stdout、stderr、命令和退出码；不要把缺少可选工具误报成模型成功，也不要自行安装依赖。

## 选择入口

### 新建项目

1. 读取题面和附件，确认输入文件范围。
2. 运行 `doctor.py` 并记录可用工具；缺少某个排版引擎时可选择另一引擎，用户指定引擎时则记录阻塞。
3. 使用 `project.py` 初始化，而非手写 manifest。记录竞赛、论文语言、排版引擎、模板和所有输入 SHA-256。
4. 生成 `plan.md` 与 `todo.md`；若目标已存在或为符号链接则停止初始化，不覆盖。完成启动阶段后进入 `awaiting_approval` 并暂停。

### 断点续跑

1. 读取 `run-manifest.json`，不要重新初始化。
2. 用 `project.py` 复核输入哈希、阶段状态、审批记录和开放问题。
3. 若输入改变，按状态规则标记受影响阶段和下游阶段；不要删除旧产物。
4. 从第一个 `pending`、`stale`、`blocked` 或用户退回的阶段继续。已批准且输入未变的阶段不得无故重做。

### 独立验收已有项目

1. 不假设该项目由本 skill 创建，也不改写其论文、代码或结果。
2. 运行 `verify_project.py` 能执行的检查，并对缺失 manifest 或台账给出明确硬错误。
3. 再按 [final-review.md](references/final-review.md) 做三视角只读审查、编译与 PDF 逐页视觉检查。
4. 输出机器可读 `verify.json` 和 `VERIFY_REPORT.md`；只有零硬错误才可判定提交就绪。

## 六阶段控制流

完整状态、目录和审批契约见 [workflow-contract.md](references/workflow-contract.md)。严格按以下顺序工作：

1. **启动与预检**：输入哈希、工具环境、比赛/语言/引擎/模板、`plan.md`、`todo.md`。
2. **分析与建模**：读取 [analysis-modeling.md](references/analysis-modeling.md) 和与题型相关的 [modeling-playbook.md](references/modeling-playbook.md)，产出 `reports/ANALYSIS_MODELING_REPORT.md`。
3. **编码与统计验证**：读取 [coding-validation.md](references/coding-validation.md)，实现 `code/run_all.py`，生成 `results/results.json` 和 `reports/RESULTS_REPORT.md`。
4. **数据图与概念图**：读取 [figures-diagrams.md](references/figures-diagrams.md)，生成正式图、`figures/manifest.json` 和 `reports/FIGURE_REPORT.md`；DrawIO 仅在论证需要时使用。
5. **论文写作**：需要文献时先读 [literature-citations.md](references/literature-citations.md)，再按 [paper-writing.md](references/paper-writing.md) 准备模板、生成数值宏、撰写并编译 `paper/submission.pdf`。
6. **独立验收**：读取 [final-review.md](references/final-review.md)，产出 `reports/verify.json` 和 `reports/VERIFY_REPORT.md`；零硬错误后把项目标为 `complete`。

每阶段都必须：读取上一阶段已批准产物；只做本阶段职责；记录实际命令与产物；运行适用检查；更新 manifest；仅在 `plan.md`/`todo.md` 仍匹配上次生成哈希时更新视图，否则保留用户版本；把阶段置为 `awaiting_approval`；向用户摘要关键决策、结果、风险与待确认项，然后暂停。

## 建模与证据原则

- 先给出可解释基线，再选择能回答题目且能被数据支持的候选模型；不要按样本量阈值机械选型，也不要为显得复杂而堆叠模型。
- 建模报告必须写清变量、单位、目标、约束、假设、输入输出、求解算法、停止条件和校验方法，使代码阶段无需猜测。
- 优化结果必须逐约束回代；预测必须防止时间或分组泄漏；评价模型必须声明指标方向、归一化与权重来源；随机算法必须固定种子并评估多次运行稳定性。
- 报告效应大小、误差或不确定性，而不只报告显著性或单个最优值。所有主要结论都要能追溯到题面、数据、结果记录或已核验来源。
- 文献元数据的主题相关性不是正文证据。支持核心主张的来源须核对原始内容；无法核验时标记 `unverifiable` 并收窄表述。

## 完成条件

仅当下列条件全部满足时宣布完成：

- 六个阶段已按顺序批准，且不存在 `stale`、`blocked` 或未解决的开放问题。
- `code/run_all.py` 可从项目根目录重现关键结果，约束、泄漏、稳健性和不确定性检查通过。
- 论文所有关键数值与 `results/results.json` 在声明容差和显示精度内一致。
- 所有正式图有真实来源、生成记录和有效文件；所有引用均有可追溯核验状态。
- 选定引擎成功生成 `paper/submission.pdf`，视觉检查无空白、裁切、乱码、重叠或占位符。
- `verify_project.py` 和三视角审查均无硬错误，最终报告明确给出 `PASS`。
