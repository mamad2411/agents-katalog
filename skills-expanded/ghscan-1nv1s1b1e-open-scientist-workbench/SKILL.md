---
name: hypothesis-mutation
description: Evolutionary mutation operators for scientific hypothesis space exploration. Use when generating variant hypotheses from a parent hypothesis.
---

# Hypothesis Mutation

你是 Oracle 或 Prometheus，负责对父假设施加变异算子生成子假设。本 skill 定义 AlphaEvolve 风格的 4 类变异算子与约束。Oracle 在锦标赛中变异，Prometheus 在规划时建议变异方向。

## 4 类变异算子

### 1. 参数变异（parameter_mutation）

调整 filter 函数中的物理参数阈值，机制不变。适用：filter 机制正确但阈值偏差导致 FP/FN。

例子：

- `magnetic_strength > 50` → `> 30`（放宽阈值提升 recall）
- `temperature > 1.5e6` → `> 2.0e6`（收紧阈值降低 FP）
- 加热率系数 `0.3` → `0.5`

约束：单次变异改动 ≤ 3 个参数，且改动幅度有物理依据（不能凭空调）。rationale 必须说明为何新阈值更合理（引用 Explore 反例或文献观测分布）。

### 2. 结构变异（structural_mutation）

替换 filter 的物理机制子模块，整体换一种加热机制判断逻辑。适用：机制本身失效，参数微调无救。

例子：

- 波加热判据（Alfvén 速度幅值 + 频谱幂律）→ 重联判据（电流片厚度 + 磁场剪切角）
- 单波段判据 → 多波段组合判据（要求 171Å + 193Å 同时增亮）

约束：替换后假设陈述必须同步改写，保持物理可解释性。不能只换 filter 代码而不改 statement——statement 与 pythonCode 必须一致。

### 3. 组合变异（crossover_mutation）

融合两个父假设的优势组件。适用：两条假设互补（A 擅长能量传输判据，B 擅长能量释放判据）。

例子：

- 父 A：wave heating 的能量传输（Alfvén 波幅值判据，recall 高）
- 父 B：nanoflare 的能量释放（温度突变判据，precision 高）
- 子：wave-driven nanoflare（要求 Alfvén 波幅值高 且 温度突变同时满足）

约束：

- 必须有两个 `parentHypoId` 链接（演化链支持多父节点，用 helix-query 的 `addMutationLink` 分别建边）
- 子假设的物理机制陈述要解释融合后的图景，不能只是两条 statement 拼接
- 融合后 filter 的逻辑运算符（AND/OR）要有物理理由

### 4. 反例驱动变异（counterexample_mutation）

针对 Explore 报告的特定反例快照，定向修正 filter。适用：反例集中且失效模式清晰。

流程：

1. 从 `EvalResult.counterexamples` 提取反例快照的物理参数
2. 聚类反例（共享同一参数区间 → 同一失效模式）
3. 对每类失效模式：在 filter 中增加约束或收紧条件，使该类反例不再被误判
4. 验证修正后不引入新的 FN（不能为消除 FP 而把真阳性也滤掉）

约束：每次反例驱动变异必须引用至少一条具体反例（snapshotId + 物理参数）作为 rationale。

## 变异前后约束

- **物理可解释性**：变异后的 filter 必须能用物理语言解释每一行判据。无意义拼接（如随机加约束）禁止
- **statement 与 pythonCode 一致**：变异后两者必须同步更新，Oracle 不能只改代码不改陈述
- **不回到已淘汰形式**：变异后用 `getEvolutionChain` 检查演化链，若新 filter 等价于已淘汰假设的 filter，终止该变异分支（避免循环变异）
- **保留可证伪性**：变异不能让 filter 退化为永真/永假，必须仍有可证伪场景

## 变异记录

每次变异必须产出 `Mutation`（`MutationSchema`）：

- `parentHypoId`：父假设 ID（组合变异可记主父，副父写入 rationale）
- `mutatedHypothesis`：完整新假设（新 `id` + 新 `statement` + 新 `pythonCode` + `parentId` 指向父 + `round` + `status: 'mutated'`）
- `mutationRationale`：含变异类型 + 改了什么 + 为何改（引用反例或物理理由）
- `round`：当前轮次

## 演化链追踪

用 helix-query 维护演化图：

- `addMutationLink(parentId, childId, mutationType)`：在 Hypothesis 节点间建 `MUTATED_FROM` 边，边上记录 mutationType
- `getEvolutionChain(hypoId)`：从某假设回溯所有祖先，用于检测循环变异
- 组合变异建两条 `MUTATED_FROM` 边（两个父 → 同一子）

## 变异后流程

变异产生的子假设**不能直接进锦标赛**：

1. 变异写入 `Mutation` 记录
2. 子假设状态置 `mutated`，加入下一轮 `HypothesisPool`
3. 下一轮 Explore 重新评估 F1（与父假设同口径）
4. Oracle 下一轮据新 F1 决定保留/再变异/淘汰

这保证每条假设的 F1 都来自 Explore 的真实评估，而非 Oracle 的预估。

## 输出

Oracle 在 `OracleOutputSchema.mutations[]` 中输出本轮所有变异。Prometheus 在 `PlanSchema.rationale` 中可建议下一轮的变异方向（如"建议对假设 #3 做反例驱动变异，针对 AR1140 类快照"），但实际变异仍由 Oracle 执行。
