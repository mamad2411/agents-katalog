---
name: 880-wrongbook
description: 查看/重生成错题本，更新复习状态（未复习/已重做/已掌握）。触发词：错题本、看错题、重练、复习错题。
---

# 错题本

错题本按章节组织，`不会/半会` 为重点，`错/粗心` 为轻标记；每条带复习状态。

## 步骤

1. **查看状态清单**：
   ```
   python3 scripts/wrong_book.py --list-states
   ```
   或直接读 `workspace/wrong-book/错题本.md`。
2. **重生成错题本**：
   ```
   python3 scripts/wrong_book.py
   ```
3. **更新复习状态**：
   ```
   python3 scripts/wrong_book.py --mark gs-c01-basic-choice-003=已掌握
   ```
   状态可选：未复习 / 已重做 / 已掌握。
   - Windows 把 `python3` 换成 `py -3`（或 `make wrongbook PYTHON='py -3'`）。

## 重练流程（对话式）

用户报"重练了某题，会了"时：
- 若该题在**某张卷子**里：走 `880-grade` 技能 `--redo`，直接记判分并联动状态；
- 若不在卷子里：先确认题号（qid），用 `wrong_book.py --mark <qid>=已掌握`。

## 禁止

- 不要随意把题从错题本删除（除非用户明确要求）；
- 复习状态由用户报告更新，不要自行推断。

## 内容规范

- 错题本 frontmatter（`total`/`focus_count`/`mastered_count`）与结构遵循 `.codebuddy/rules/common/obsidian-content.md` 的「错题本」一节；
- 每题条目带 `*来源卷子：[[卷子-XX]]*`（取最近一次判分的卷子）；
- 若 `workspace/records/external-links.json` 为该题配置了外部错题本关联（值为数组，每题可多条，每条含 `path`+`anchor`），自动输出 `*相关笔记：[[…]] · [[…]]*`（由 `wrong_book.py` 渲染，无需手改错题本）；
- 若 `workspace/records/analysis.json` 为该题配置了过程分析，条目末尾自动渲染「错因分析」callout（错因/出错环节/建议，由 `wrong_book.py` 输出）；分析由 `880-analysis` skill 写入，非错题本流程生成；
- 若需调整格式，先改规则文件，再改 `scripts/wrong_book.py`。
