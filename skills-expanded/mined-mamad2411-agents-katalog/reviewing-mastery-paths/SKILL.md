---
name: reviewing-mastery-paths
description: |
  SeedX 学习路径评估标准。用于独立评估学习产物是否覆盖充分、清晰、
  可执行，并能转化为输入中明确目标或通用应用场景下的行动。
---

# reviewing-mastery-paths

本 Skill 是 learning-evaluator 的唯一评估标准。Evaluator 必须独立、挑剔、可执行地评估，不得因为文本看起来丰富就放行。

---

## 一、评估立场

你不是润色员，而是 skeptical evaluator。

必须主动寻找：

- 看似完整但缺少主干概念。
- 看似清楚但术语未定义。
- 看似有行动但练习不可执行。
- 看似个性化但引入了输入中没有的个人、行业、职业或产品背景。
- 看似可迁移但无法变成具体行动、实验、决策、讲解或作品。

禁止自我安慰式评价，例如“整体不错，可以进一步完善”。如果低于标准，必须 FAIL。

---

## 二、评分维度

每个维度 1-5 分，阈值为 4 分。

### 1. Question Quality

检查：

- 原始问题是否被准确重述。
- 学习目标是否明确。
- 边界和非目标是否清楚。
- 是否避免问题过宽。
- 学完后能做什么是否明确。

低分信号：

- 仍停留在“学习某领域”的泛泛表达。
- 没有说明本轮不学什么。
- 学完后能做什么不清楚。

### 2. Coverage

检查：

- 核心概念是否遗漏。
- 前置知识是否说明。
- 主干、分支、边缘话题是否区分。
- 是否有常见误区。
- 是否避免把低价值细节放在核心位置。

低分信号：

- 缺少关键机制。
- 只有目录，没有关系。
- 概念堆砌但没有主干。

### 3. Clarity

检查：

- 结构是否清楚。
- 术语是否解释。
- 层级是否明显。
- 是否有例子或类比。
- 是否适合未来复习。

低分信号：

- 抽象名词过多。
- 段落很长但抓不住重点。
- 未来复习时无法快速定位。

### 4. Actionability

检查：

- 学习阶段是否有顺序。
- 每阶段是否有目标和完成标准。
- 练习是否具体。
- checkpoint 是否可验证。
- 是否有当天可开始的最小下一步。

低分信号：

- “继续学习/深入研究/多实践”这类空话。
- 练习不可执行。
- checkpoint 只是阅读任务，不验证掌握。

### 5. User Context Fit

检查：

- 是否准确使用了 learning contract 中明确记录的学习者背景、目标、应用场景和约束。
- 如果输入未指定背景，是否保持通用学习者视角。
- 是否避免引入输入中没有的个人、行业、职业、特定应用或产品场景。
- 应用计划是否服务输入中的真实目标，而不是泛泛建议。

低分信号：

- 默认写入某个具体人物、职业或行业背景。
- 输入未指定场景时，产物却强行绑定某行业或产品。
- 输入指定了场景，但产物没有贴合该场景。

### 6. Transferability

检查：

- 是否能把知识迁移为行动、实验、决策、讲解、项目步骤或作品。
- 是否有类比、例子或解释方式。
- 是否指出常见误解和解释方式。
- 是否给出明确的最小下一步。

低分信号：

- 只有“可以应用到实践”的泛泛说法。
- 没有具体行动或输出。
- 没有可迁移的解释或练习。

---

## 三、PASS/FAIL 规则

硬规则：

```text
所有维度必须 >= 4/5 才能 PASS。
任一维度 < 4/5 必须 FAIL。
```

不得因为平均分高而 PASS。

Additional hard gate:

```text
若产物引入输入中未明确提供的个人/行业/职业/产品背景，User Context Fit 必须 < 4，并且整体 FAIL。
```

---

## 四、任务相关评估重点

### Task 1: Framing

评估文件：

- `deliverables/question-brief.md`
- `deliverables/domain-map.md`

重点维度：

- Question Quality
- Coverage
- Clarity

User Context Fit 也必须检查：不能引入输入未提供的背景。Actionability 和 Transferability 可在本任务中只给预警。

### Task 2: Mastery Path

评估文件：

- `deliverables/learning-path.md`
- `deliverables/exercises.md`
- `deliverables/checkpoints.md`

重点维度：

- Coverage
- Clarity
- Actionability

必须检查 Task 2 是否与 Task 1 的领域地图一致。

### Task 3: Application & Transfer

评估文件：

- `deliverables/application-plan.md`
- `deliverables/transfer-plan.md`

重点维度：

- Actionability
- User Context Fit
- Transferability

必须检查应用是否只使用输入中明确的目标/场景；若输入未指定场景，则必须保持通用且具体可执行。

---

## 五、报告格式

报告写入当前任务对应文件：

```text
_agent/review-reports/task01-evaluation.md
_agent/review-reports/task02-evaluation.md
_agent/review-reports/task03-evaluation.md
```

每次评估追加一个新轮次，不覆盖旧内容。

PASS 格式：

```markdown
# Task{NN} Evaluation Report

## 第 {N} 次评估

### 判定：PASS

| 维度 | 分数 | 阈值 | 结论 |
|---|---:|---:|---|
| Question Quality | 4 | 4 | PASS |
| Coverage | 4 | 4 | PASS |
| Clarity | 4 | 4 | PASS |
| Actionability | 4 | 4 | PASS |
| User Context Fit | 4 | 4 | PASS |
| Transferability | 4 | 4 | PASS |
```

FAIL 格式：

```markdown
# Task{NN} Evaluation Report

## 第 {N} 次评估

### 判定：FAIL

| 维度 | 分数 | 阈值 | 结论 |
|---|---:|---:|---|
| Question Quality | 4 | 4 | PASS |
| Coverage | 3 | 4 | FAIL |
| Clarity | 4 | 4 | PASS |
| Actionability | 2 | 4 | FAIL |
| User Context Fit | 3 | 4 | FAIL |
| Transferability | 3 | 4 | FAIL |

## 必须修复

1. Coverage：具体说明缺什么、在哪个文件修。
2. Actionability：具体说明哪个练习/checkpoint 太虚，如何改。
3. User Context Fit：具体说明哪个文件引入了输入未提供的背景，必须删除或改为通用表达。
4. Transferability：具体说明缺少哪个行动、实验、讲解或迁移输出。
```

---

## 六、输出给主 Agent

只返回：

```text
测试结果：PASS
报告路径：{路径}
```

或：

```text
测试结果：FAIL
报告路径：{路径}
```

不要返回完整报告内容。
