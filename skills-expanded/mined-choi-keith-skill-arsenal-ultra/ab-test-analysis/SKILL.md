---
name: ab-test-analysis
description: "分析 A/B 测试结果,包含统计显著性、样本量校验、置信区间,以及上线/延长/停止建议。适用于评估实验结果、检查测试是否达到显著性、解读分流测试数据,或决定是否发布某个变体。"
---

## A/B 测试分析

以严谨的统计方法评估 A/B 测试结果,并将发现转化为清晰的产品决策。

### 背景

你正在为 **$ARGUMENTS** 分析 A/B 测试结果。

如果用户提供了数据文件(CSV、Excel 或分析平台导出数据),直接读取并分析。需要时生成 Python 脚本进行统计计算。

### 操作说明

1. **理解实验**:
   - 假设是什么?
   - 改动了什么(变体内容)?
   - 主要指标是什么?有哪些护栏指标?
   - 测试运行了多久?
   - 流量如何分配?

2. **校验测试设置**:
   - **样本量**:样本量对于预期效应量是否足够?
     - 使用公式:n = (Z²α/2 × 2 × p × (1-p)) / MDE²
     - 如果检验效能不足(<80% power),需标记出来
   - **持续时间**:测试是否至少运行了 1-2 个完整的业务周期?
   - **随机化**:是否有样本比例失衡(SRM)的迹象?
   - **新奇/首因效应**:是否有足够时间消除初期行为变化?

3. **计算统计显著性**:
   - 对照组和变体组的**转化率**
   - **相对提升**:(变体 - 对照) / 对照 × 100
   - **p 值**:使用双尾 z 检验或卡方检验
   - **置信区间**:差异的 95% 置信区间
   - **统计显著性**:p < 0.05 是否成立?
   - **实际显著性**:提升幅度对业务是否有意义?

   如果用户提供了原始数据,生成并运行 Python 脚本进行计算。

4. **检查护栏指标**:
   - 是否有护栏指标(收入、参与度、页面加载时间)出现恶化?
   - 主要指标获胜但护栏指标恶化,可能不算真正的胜利

5. **解读结果**:

   | 结果 | 建议 |
   |---|---|
   | 显著正向提升,无护栏问题 | **上线** — 全量发布到 100% |
   | 显著正向提升,护栏有顾虑 | **调查** — 上线前先弄清权衡 |
   | 不显著,但趋势为正 | **延长测试** — 需要更多数据或更大效应 |
   | 不显著,走势持平 | **停止测试** — 未检测到有意义差异 |
   | 显著负向提升 | **不上线** — 回滚到对照组,分析原因 |

6. **提供分析摘要**:
   ```
   ## A/B Test Results: [Test Name]

   **Hypothesis**: [What we expected]
   **Duration**: [X days] | **Sample**: [N control / M variant]

   | Metric | Control | Variant | Lift | p-value | Significant? |
   |---|---|---|---|---|---|
   | [Primary] | X% | Y% | +Z% | 0.0X | Yes/No |
   | [Guardrail] | ... | ... | ... | ... | ... |

   **Recommendation**: [Ship / Extend / Stop / Investigate]
   **Reasoning**: [Why]
   **Next steps**: [What to do]
   ```

逐步思考。以 markdown 格式保存。如果提供了原始数据,生成 Python 脚本进行计算。

---

### 延伸阅读

- [A/B Testing 101 + Examples](https://www.productcompass.pm/p/ab-testing-101-for-pms)
- [Testing Product Ideas: The Ultimate Validation Experiments Library](https://www.productcompass.pm/p/the-ultimate-experiments-library)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
