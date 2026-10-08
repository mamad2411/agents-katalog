---
name: 880-progress
description: 生成或查看进度总览——哪些题已完成/未完成/做错，章节完成率与弱点排行。触发词：预览、进度、看进度、进度总览。
---

# 进度总览

预览文件 `workspace/preview/进度总览.md` 展示：每题状态（✅对/❌错/⚠️不会/🔶半会/🟡粗心/📝做过未判/⬜未做）、章节完成率、弱点排行。

## 步骤

1. 运行：
   ```
   python3 scripts/progress.py
   ```
   - Windows 把 `python3` 换成 `py -3`（或 `make progress PYTHON='py -3'`）。
2. 向用户展示关键统计：
   - 总题数 / 已判 / 做过未判（欠账）/ 未做 / 非"对"数量；
   - 章节弱点排行；
   - 直接打开或摘录 `workspace/preview/进度总览.md`。

## 说明

- "做过未判" = 抽到过但还没判分的题（欠账），提醒用户尽快判分；
- 弱点分 = 章节加权错误率（时间衰减），用于下一张卷的配额浮动。

## 禁止

- 不要臆造判分数据，一切以 `workspace/records/attempts.json` 为准。

## 内容规范

- 进度总览 frontmatter（`total`/`graded`/`pending`/`undone`/`wrong`）与结构遵循 `.codebuddy/rules/common/obsidian-content.md` 的「进度总览」一节；
- 若需调整格式，先改规则文件，再改 `scripts/progress.py`。
