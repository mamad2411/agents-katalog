---
name: competition-workflow
description: 数学建模竞赛全流程总控。两条模式：A) 流水线模式——按阶段编排调用 analysis/modeling/coding/sensitivity/statistical-diagnosis/writing skills，各阶段用 reports/ 报告文件交接，数值从报告取；B) 时间线模式——Day1-3 人工节奏与检查点。含阶段0.5数据结构探索（EDA五问）、每问连贯链、验证三件套；模型选型决策树与交稿自查在 references/ 下按需查阅。
---

# 数学建模竞赛全流程总控（编排入口）

本 skill 是数模任务的**总控**：它不亲自建模，而是把任务拆成阶段、指定每个阶段调用哪个 skill、用报告文件做阶段交接、最后验收。

## 何时读哪个文件

本文件只管编排顺序。具体规则各有唯一真源，用到时再读：

| 什么时候 | 读什么 |
|---|---|
| 阶段 1 定题型、选模型 | `references/model-selection-tree.md`（决策树 + 每条选型的举证要求） |
| 阶段 5 交稿前 | `references/submission-checklist.md`（docgate 覆盖不了的人工自查） |
| 写正文（摘要 / R1-R4 / 检验 / 灵敏度措辞） | `../guozhan-paper/SKILL.md`；正反例与页码在 `../guozhan-paper/references/evidence-corpus.md` |
| 内容与严谨性规范 | `../math-modeling-paper/SKILL.md` |
| 排版（LaTeX 骨架 / 字号 / 三线表 / 图表工程） | `../math-paper-template/SKILL.md`；官方明文与通行惯例的分层见 `../../assets/official-paper-format.md` |
| 验收判级、声明措辞强度、docgate 协议 | `../paper-gate/SKILL.md`（约束分级约定也在这里） |
| 灵敏度方法分档 | `../sensitivity-analysis/SKILL.md`（该方法的唯一真源，本文件不复述其阈值） |
| 统计诊断判定 | `../statistical-diagnosis/SKILL.md` |
| 复制提示词用 | `../../assets/prompt-pack.md`（14 条实战提示词） |
| 优化类求解降级链、图表脚本化对账 | `../../assets/optimization-playbook.md`、`../../assets/figure-playbook.md` |

## 两种模式

- **流水线模式**（默认，一条命令跑到底）：按下方「五阶段流水线」执行。
- **时间线模式**（人工组队、Day1-3 真实赛制）：按下方「Day1-3 时间线」执行，阶段报告同样要写。

## 阶段产出物（两种模式都一样）

```text
plan.md                              # 本 skill 制定：题目拆解、阶段顺序、每阶段调用谁、产出什么
todo.md                              # 阶段 checklist（完成一项勾一项）
reports/ANALYSIS_MODELING_REPORT.md   # 阶段1产物：赛题分析+建模方案
reports/RESULTS_REPORT.md             # 阶段2产物：代码结果+图表清单+约束校验
reports/SENSITIVITY_REPORT.md         # 阶段3产物：灵敏度分析（sensitivity-analysis skill 产出）
reports/DIAGNOSIS_REPORT.md           # 阶段4产物：统计诊断（statistical-diagnosis skill 产出）
reports/VERIFY_REPORT.md              # 阶段5产物：提交前验收
reports/VERIFY_DOCGATE.md             # 阶段5产物：docgate.py 对最终提交工件的机械检查报告
```

报告的作用是让下游每个数字都有出处：论文里的数字指回 `reports/`，`reports/` 里的数字指回代码输出。核对协议与声明强度校准见 `../paper-gate/SKILL.md` G1。

**工件唯一性**：全程只维护一个真源工件（LaTeX master 或 docx master），其余格式由工具链确定性转换；验收认的是最终提交的那个文件，源文件通过不等于提交版通过。转换/另存/导出后重跑 docgate 的协议见 `../paper-gate/SKILL.md`。

**工具降级预案**：编排中依赖 MathModelAgent MCP 的环节（exec_python 等）先探测 `mma_status`，离线即降级本地 `python`（venv/conda 项目内环境），不阻塞流程。

**阶段报告不是审批关卡**：它的作用是让下一阶段的数字有出处。
常见误区是把阶段门做成审批——为了"通过"而调低自定门槛，或报告里写"已达标"却拿不出指标；结果是论文数字失去追溯链，答辩时说不清来源。
写完一阶段问自己：关键结论是否每条都有指标或代码输出支撑？求解不可行或指标异常时，是继续优化，还是如实记录局限？一个子问题迭代 2-3 轮通常够用，每轮把「改动→效果→指标」记进报告——这也是论文 R1-R4 衔接写作的事实来源。

**交付命名规范（跨会话可交接）**：`数据预处理-数据预处理.py`、`问题一-problem1.py`…`问题四-problem4.py`（各带附件说明）、每题一个 `报告N.md`（记录子问题分解、模型依据、迭代记录、最终指标）、`paper/main.tex`→PDF。

## 五阶段流水线

| 阶段 | 做什么 | 调用 | 产物 |
|------|--------|------|------|
| 0 读题 | OCR 题面 PDF/附件图片落盘；外部解题指南/参考方案逐条核验（对照题目+附件数据实测）；文献 DOI/卷期核验（Crossref/OpenAlex，检索不到即标"无法核实"，不补一个看起来合理的值） | `vision-ocr` + 直接执行（核验清单见 prompt-pack A1/A2） | 题面文本文件（不入对话，按需取段）+ 外部资料核验清单 |
| 0.5 数据结构探索 | 按 EDA 五问探数据，每条发现注明"→决定了哪个模型的哪个设计"与判定阈值 | 直接执行（见下） | 写入 ANALYSIS_MODELING_REPORT.md「数据结构发现」节 |
| 1 分析建模 | 子问题拆解、假设预检、符号、目标/约束、求解策略、代码任务清单 | 直接执行（见下） | ANALYSIS_MODELING_REPORT.md |
| 2 代码结果 | 按报告写可复现代码、跑数、画数据图、约束校验 | 直接执行 + `statistical-diagnosis`（模型诊断部分） | code/ + figures/ + RESULTS_REPORT.md |
| 3 灵敏度 | 按题型做灵敏度/稳健性分析 | `sensitivity-analysis` | SENSITIVITY_REPORT.md |
| 4 论文 | 内容走写作规范，排版走模板；措辞取自 DECLARATION_WHITELIST（`paper-gate` G1） | `math-modeling-paper` → `math-paper-template` →（可选）`tex-pdf-image-to-word` | paper/*.tex → PDF/docx |
| 5 验收 | docgate.py 机械检查（对最终提交工件）+ 人工自查 docgate 覆盖不了的部分 | `docgate.py`（`paper-gate` G3）→ `references/submission-checklist.md` + `statistical-diagnosis` 复核 | VERIFY_DOCGATE.md + VERIFY_REPORT.md |

### 阶段 0.5 要点（数据结构探索：EDA 五问）

大数据量题（尤其优化类）值得先做这一步：建模依据来自数据，比来自直觉更能撑住阶段 1 的选型举证。每条发现写入报告的「数据结构发现」节，格式为"发现 + 判定阈值/口径 + → 决定了哪个模型的哪个设计"。没有下游对应的发现标"仅描述性"就好——它仍是 EDA 的一部分，只是不能当建模依据用。

1. **序列结构**：自相关/Ljung-Box 检验 → 是否白噪声（判定阈值：|ACF|<0.1 且 Q 检验 p>0.05）→ 决定预测模型是否走分解结构；
2. **规模瓶颈**：峰值需求与可用容量逐时对比 → 超容位置与幅度 → 决定优化对象与时移/迁移必要性；
3. **口径审计**：字段结构、统一计算口径、边界条款逐条核对（判定：每条建模假设能找到题面出处；题面"说明"条款逐条落位）；
4. **信息极限**：可预测成分占比、水平跳变检验 → 哪些序列值得建模，哪些如实声明"已近信息极限"（判定：按步 R² 与在途成分占比）；
5. **相关结构**：目标间相关性的多口径检验（截面/时序/混合，分口径报相关系数）→ 多目标是否真冲突、前沿是否可能坍缩。

「发现→模型设计」映射表与求解降级链见 `../../assets/optimization-playbook.md`。

### 阶段 1 要点（分析建模，参考 MathModelAgent 2analysis 机制）

1. **子问题只认题面编号的顶层问题**（问题一/二/三…），别把背景、数据说明、小问当独立子问题。
2. **假设敏感性预检**：对影响结果的歧义至少给两种解释，用简单验算/递进性判断选一个；若后续问题的新增条件在当前解释下没有边际效果，回头改解释。
3. 每问写清：目标、符号变量、模型假设、目标函数、约束、求解方法、输入输出、结果校验方法；公式细到代码能直接实现。
4. 报告末尾写「代码实现任务清单」：| 任务 | 输入 | 输出 | 方法 | 校验 |。
5. 每问写「连贯链」三行：**继承**（复用上一问的符号/公式/参数，与符号表一致）／**新增**（本问新增决策变量/约束/目标项＝与前问构件集做差的结果）／**变因**（方法改变的原因，指向题目新增条件或数据发现）。——这是论文 R1 定位陈述的事实来源（写法与正反例见 `../guozhan-paper/SKILL.md` 3.5）。
6. 每个主要模型的选型引用一条「数据结构发现」或一组候选模型对比。无依据的"本文采用 X 模型"是国奖与非国奖最稳定的区分点之一——判据、决策树与正反例见 `references/model-selection-tree.md`。
7. 每问产出「流程图草稿」：四阶段节点文字（数据／模型／约束检验／求解与敏感性）+ 总体路线图的传递物标注；**草稿按 spec JSON 格式落盘**（格式、生成器与 OCR 复核链路见 `../../assets/figure-playbook.md` 第 4 节与 `../../assets/flowchart_gen.py`）——阶段 2 用生成器产出 .drawio/.mmd/.png，阶段 5 用 vision-ocr 读回 PNG 逐项复核。
8. 每个主要模型列出「可解释性更强的备选模型」并写明取舍理由（基础模型/组合模型优先、解释性优先于黑箱；取舍理由写入报告）。

### 阶段 2 要点（代码与结果）

1. 先保证**可行解**再优化目标；输出方案逐条回代检查约束（scipy 不等式是 `fun(x)>=0`，最大化要取负——常见翻车点）。
2. 随机算法固定种子、多跑报告均值±std；预测类防数据泄露（时序不 shuffle、scaler 只在训练集 fit）。
3. 每个关键数值写进 RESULTS_REPORT.md；图按「显示宽→figsize」规则渲染（见 `../../assets/huashubei-writing-guide.md` 2.1）。
4. 验证三件套（大数据量优化类性价比最高）：①可行性回代（判定：零违例）；②小规模精确对照（块级/子问题 MILP 重解报间隙；启发式不宣称全局最优）；③独立复算（按附件口径重算，判定：数值链零漂移）。优化类另附收敛性声明（迭代序列递减）与最优性声明（LP 对偶/间隙），证明不了就如实声明局限。求解降级链与决策表见 `../../assets/optimization-playbook.md`。
5. 性能门槛：求解器单次运行超过约 10 分钟就值得评估换算法（如滚动 MILP→贪心构造+局部搜索），并保留小规模精确求解做质量对照（华数杯实测：几小时→93 秒、块级 MILP 间隙 0%；触发条件见 `references/model-selection-tree.md` 与 playbook 降级链）。
6. RESULTS_REPORT.md 每个关键结论标注**证据等级**（解析证明 / MILP gap / 块级对照 / 收敛佐证 / 仅启发式 五档；措辞映射见 `paper-gate` G1 声明强度校准表），并附**公式↔代码对照表**（Σ上下界↔循环范围、连续/离散形式一致性——AI 生成公式的高发错误区；变量解释完整性由 docgate [12] 机械兜底）。

### 阶段 3-4 要点

- 灵敏度与诊断独立成节。调用前先把题面与 RESULTS_REPORT.md 交给对应 skill，让它们按题型自适应，而不是套 θ 模板；方法分档以 `sensitivity-analysis` 为准。
- 论文：`math-modeling-paper` 管内容（结构/摘要/表述/严谨性），`math-paper-template` 管排版（LaTeX/格式/编译）；两者都对齐 `../../assets/official-paper-format.md`。
- 论文写作前先从 RESULTS_REPORT 的证据等级生成 **DECLARATION_WHITELIST**（每条结论允许的措辞上限，规则见 `paper-gate` G1），摘要与结论的措辞从白名单取。
- 评委/组织方要求 Word 版时：走 `tex-pdf-image-to-word` 路线 A（tex→docx），并过它的 11 条交付检查清单。

### 阶段 5 要点（验收）

**第一步（机械检查）**：对**最终提交的那个文件**跑

```bash
python ../../assets/docgate.py <file> --results reports/RESULTS_REPORT.md \
    --problem 题面.txt --out reports/VERIFY_DOCGATE.md
```

【不变量】FAIL 项都是可机械验证的事实错误或真实性问题（编号断裂、摘要数字在正文找不到、变量解释空残骸、图片超版心、重述与题面重合过高、AI 工具混入参考文献区），修复源头 master 后重新转换重跑；WARN 项是手艺判断，逐条人工裁决。分级依据与完整协议见 `../paper-gate/SKILL.md` G3。

**第二步（人工复核）**：docgate 查不到的硬错误——占位符残留、图缺失、数值与报告冲突、编译失败、页眉没去掉、图内打印字号过小、表注漏特殊值。这些直接影响评委能否读懂，逐条过。

**第三步（档次自查）**：`references/submission-checklist.md` 是 docgate 覆盖不了的那部分（数值复现、外部意见复算、结构语义、统计严谨性、格式判断），已按问句组织；docgate 机械覆盖的项那里不再重列。档次对标用 `../guozhan-paper/SKILL.md` 的交稿前自查。验收结论写进 `reports/VERIFY_REPORT.md`。

---

# Day1-3 时间线模式（人工赛制节奏）

## Day 1：拆解 + 数据 + 建模
- 08:00-10:00 选题：读题（OCR 落盘）→ 评估数据可得性/知识储备/创新点 → 定题
- 10:00-12:00 拆解分工：子问题类型（评价/预测/优化/分类）→ 依赖链 Q1→Q4 → 分工
- 12:00-14:00 数据结构探索：EDA 五问落盘（每条发现标注"→ 模型设计"与判定阈值）。大数据量优化题跳过这一步，代价是后面所有选型都无据可依
- 14:00-22:00 Q1/Q2 建模求解：目标函数+约束显式化 → 代码 → 统计检验（效应量+CI+p值）
- 22:00-23:00 Day1 检查：假设条数与三来源要求见 `../../assets/official-paper-format.md` §八 ✓ 符号表 ✓ 数据结构发现已写入报告（每条有下游对应）✓ Q1 完整 ✓ Q2 框架 ✓（对照 ANALYSIS_MODELING_REPORT 骨架）

## Day 2：Q3Q4 + 灵敏度
- 08:00-12:00 Q2 收尾 + Q3：模型对比表 → 代码 → 检验
- 12:00-18:00 Q4：用 Q3 结果 → 蒙特卡洛/置换检验
- 18:00-22:00 灵敏度（调 `sensitivity-analysis`，按题型自适应）：方法分档与参数规模的对应关系以该 skill 为准，本表不复述
- 22:00-23:00 Day2 检查：四问完成、每问有对比表+检验、验证三件套齐备（回代/小规模精确对照/独立复算）、灵敏度独立成章、步骤可复现

## Day 3：论文 + 审校 + 提交
- 08:00-12:00 初稿：摘要（最后写）→ 1.3 贡献表 → 技术路线段 → 图表 → 结论 → 参考文献
- 12:00-16:00 审校：全局格式（`math-paper-template` + official-paper-format.md）→ 建模严谨性（`statistical-diagnosis`）→ 业务解释 → 创新点
- 16:00-18:00 整理：附录文件列表+可视化+伪代码 → 编译 PDF → 跑 docgate → 逐页核对 →（可选）转 Word 交付
