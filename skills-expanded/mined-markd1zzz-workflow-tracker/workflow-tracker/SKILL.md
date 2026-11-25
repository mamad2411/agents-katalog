---
name: workflow-tracker
description: 全程自动记录ML/AI实验工作流。检测模型训练、超参数调优、精度对比、数据分析时自动触发并结构化存储。Auto-records ML/AI experiment workflows silently. Detects model training, hyperparameter tuning, accuracy comparisons, data analysis in real time. Engineering projects output workflow.json+workflow.md; paper projects output CHANGELOG.md+experiment_log.md. Generates docx.json+pptx.json on demand.
---

# Workflow & Experiment Tracker

自动拆解为 Phase → Task → Experiment 三级结构。识别项目类型后输出对应格式。

## 触发

检测到以下任一信号即**静默记录，不打断用户**：

- 看到数字变化（"精度从X变到Y"、"loss降到Z"、"F1从A变到B"）
- 用户口述实验结论（"试了X"/"不行"/"有效"/"放弃"）
- 运行脚本后看到结果输出
- 参数变更（"把A改成B"、"新增了C"）
- 用户说"记录"/"保存"/"更新日志"

**不必等到用户说"记录"才行动**。在回复中自然地追加一条记录即可。

## 项目类型识别

首次进入项目时，扫描目录+用户对话，判定类型：

| 信号 | 类型 | 存储 |
|------|------|------|
| 含 `tex/`、`manuscript`、`figures/`、`投稿`、`论文`、`ablation` | **论文** | `CHANGELOG.md` + `experiment_log.md` |
| 含 `data/train/`、`models/`、`train.py`、`pipeline`、`main.py` | **工程** | `workflow.json` + `workflow.md` |
| 用户说"部署"/"产品"/"上线"/"API" | **工程** | `workflow.json` + `workflow.md` |
| 无法判断 | 默认**工程** | `workflow.json` + `workflow.md` |

## 论文模式

直接追加两个 Markdown 文件，**不建 JSON**：

### CHANGELOG.md

按时间线累积。每条格式：

```markdown
## 2026-06-14 — 简短标题

### 背景
（1-2句说明为什么做这个改动）

### 改动
| 参数 | 旧值 | 新值 | 原因 |
|------|------|------|------|

### 效果
（关键数字变化）
```

### experiment_log.md

每次实验一条，可独立阅读：

```markdown
## 2026-06-14 — 实验标题

- **假设**: ...
- **方法**: ...
- **参数**: ...
- **结果**: 基线X → 新Y (delta)
- **结论**: SUCCESS / FAILED / PARTIAL
- **备注**: ...
```

## 工程模式

维护 `.claude/workflow/workflow.json` + 自动导出 `.claude/workflow/workflow.md`。

### JSON 最小结构

```json
{
  "project": "项目名",
  "updated": "2026-06-14T14:30",
  "phases": [{
    "name": "Phase 1: XXX",
    "status": "in_progress",
    "tasks": [{
      "name": "Task 1.1: XXX",
      "status": "completed",
      "experiments": [{
        "date": "2026-06-14",
        "title": "实验标题",
        "method": "一句话方法",
        "params": {"old_lr": 0.001, "new_lr": 0.0002},
        "results": {"baseline": 93.75, "new": 94.79, "delta": 1.04},
        "conclusion": "SUCCESS",
        "tags": ["classifier", "svm"]
      }]
    }]
  }]
}
```

字段说明：
- `title/method/results/conclusion` 必填，其他可选
- `params` 用 old_xxx / new_xxx 格式记录变更
- `results.delta` 统一用 pp（百分点）或绝对值
- `tags` 至少一个分类标签
- `conclusion` 取值: `SUCCESS | FAILED | PARTIAL | INCONCLUSIVE`

### workflow.md 自动导出

每次更新 JSON 后同步重写。格式：

```markdown
# 项目工作流程记录
> 自动生成于 2026-06-14 14:30 | 3阶段 8任务 12实验

## Phase 1: 精度优化 (in_progress)
### Task 1.1: 数据增强尝试 (completed)
| # | 日期 | 方法 | 基线→新 | Delta | 结论 |
|---|------|------|---------|-------|------|
| 1 | 06-14 | 图像增强 | 93.75→91.67 | -2.08 | FAILED |
```

### 写入时机

**批量写入**：在对话结束或用户说"保存"时一次性写入 workflow.json + workflow.md。不要每次实验后立即写——等用户明显完成一轮实验后再写。

## 报告生成

用户说"生成报告"/"出PPT"/"汇报"/"写总结"时：

1. 读取已有数据
2. **论文项目** → 更新 CHANGELOG.md + experiment_log.md（无需生成额外文件）
3. **工程项目** → 生成两个 JSON 中间文件到 `.claude/workflow/reports/`：
   - `report_YYYYMMDD.docx.json` — Word 报告结构化内容
   - `report_YYYYMMDD.pptx.json` — PPT 结构化内容
4. 提示：*"中间文件已生成。可用 node build_ppt.js 或 python render.py 渲染。"*

### .docx.json / .pptx.json 结构

只存内容和结构，不存样式：

```json
{
  "meta": {"title": "...", "date": "2026-06-14"},
  "cover": {"title": "...", "key_metrics": "准确率 94.79%"},
  "sections": [
    {"heading": "一、概述", "paragraphs": ["..."], "bullets": ["..."], "tables": []}
  ]
}
```

```json
{
  "meta": {"title": "...", "style": "dark-cover"},
  "slides": [
    {"type": "title", "title": "...", "subtitle": "..."},
    {"type": "content", "title": "...", "layout": "two-cards", "cards": []},
    {"type": "table", "title": "...", "table": {"headers":[], "rows":[]}},
    {"type": "summary", "title": "...", "achievements":[], "next":[]}
  ]
}
```

## 关键规则

1. **批量写**：不要每次实验后立即写文件，积累到用户明显完成一轮后再统一写入
2. **只写一处**：工程模式只写 `.claude/workflow/`，论文模式只写项目根目录的两个 md
3. **安静执行**：记录时不要长篇解释"我已保存了XX"，一句话带过即可
4. **delta 必算**：只要看到新旧数值，自动算 delta
5. **合理推断**：缺字段时从上下文推断，标注 `(推断)`
6. **避免重复**：同名、同日、同方法的实验合并为一条，不要创建重复记录

## 示例

用户说："把MLP换成了SVM(linear, C=1)，结果从93.75%提到94.79%，SVM是确定性的"

→ 追加实验: method="SVC(linear,C=1)", results={baseline:93.75,new:94.79,delta:1.04}, conclusion=SUCCESS, tags=["classifier","svm"]
→ 同步更新 workflow.json + workflow.md
