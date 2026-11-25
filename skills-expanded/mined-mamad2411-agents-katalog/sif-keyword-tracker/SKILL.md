---
name: sif-keyword-tracker
description: >-
  Sif 关键词动态跟踪（Skill 2）。同一 ASIN 有历史时由 sif-keyword-scout 自动触发，
  按 1~7 天窗口对比 PD 主攻词单，输出词库更新报告。Agent 必须写 insights_tracker.md，
  且在写 insights 前完成暂停点 ③ 与用户确认投放策略。
---

# Sif 关键词动态跟踪（Skill 2）

> 通常由 Skill 1 Step 10 触发。单独运行时同样遵循 **暂停点 ③**（见 scout 的 `amazon-expert-guide.md`）。

## 对比基准选择（1~7 天窗口）

```powershell
python "{scripts.check_history}" --asin {ASIN} --output-dir "{output_dir}" --curr-date {DATE}
```

返回 `compare_prev_result_dir`、`compare_note`、`compare_days_apart`。

| 规则 | 说明 |
|------|------|
| **优先** | 按**原数据日期**（文件夹 `YYYYMMDD` / 原始表后缀）在 1~7 天窗口内选上一期，如 `20260610 → 20260611` |
| 同日多次 | 仅当没有可比的异日数据时，才对比同日前一次运行（同日重跑） |
| 超出窗口 | 回退到紧邻上一次异日数据（报告会标注 warning） |

**注意**：`0611` 是数据日期，不是「今天跑脚本的日子」。对比的是两期 Sif 导出数据，不是同日重复执行。

## 两轮流程（与 Skill 1 相同）

**第一轮：对比 + stats**

```powershell
python "{scripts.compare_versions}" --auto --output-root "{output_dir}" --output-dir "{result_dir}" --asin {ASIN} --curr-date {DATE} --skip-word
```

**暂停点 ③（强制）**

读取 `{ASIN}_tracker_stats_{DATE}.json`，向用户解读：

- 新增 / 消失词（含 S 级变化）
- SS 稳定词、搜索量与份额波动
- 试投 / 暂停 / 观察 建议

**用户确认后**才写 `insights_tracker.md`（必须针对本次数据，勿用模板凑数）。

**第二轮：生成 Word**

```powershell
python "{scripts.compare_versions}" --auto --output-root "{output_dir}" --output-dir "{result_dir}" --asin {ASIN} --curr-date {DATE} --insights-file "{result_dir}/insights_tracker.md"
```

## 报告结构

- **数据段（脚本）**：变化摘要、新增/消失清单（含 S 级）、SS 稳定词、搜索量/份额表
- **AI 段（Agent）**：策略解读、逐词建议、投放调整行动清单（须反映暂停点 ③ 与用户达成的共识）

## 产出

`{result_dir}/{ASIN}_词库更新报告_{DATE}.docx`
