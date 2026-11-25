---
name: blueprint-compare-report
description: "Write the comparison table of the two versions from the checked pairing, and what was checked."
---

# The comparison table

`.blueprint/comparison.json` is the pairing the person approved. Write `.blueprint/compare-report.md` for them,
in their language and in plain words:

- `## 新旧対照表` / `## Comparison table` — one row per pair that is not `same`, in the order of the new version
  (a removed article where it stood in the old one): the old article, the new article, and what changed. Name
  each article as the document does (`第4条`, `Article 4`), and quote the words or numbers that differ from each
  version. A Markdown table works well:

  | 旧 | 新 | 変わったこと |
  |---|---|---|
  | 第4条（委託料と支払） | 第4条（委託料と支払） | 月額「200,000円」→「220,000円」 |
  | （なし） | 第5条（報告） | 足された: 毎月5日までに前月の報告書を納める |

  The check looks for every changed, added and removed article's name in this section.
- A line after the table on the articles that are the same, including those that only moved or were renumbered
  (「旧第9条は新第8条になった。中身は同じ」).
- `## 確かめたこと` / `## What was checked` — that every article of both versions is in one pair; that whether each
  pair changed was decided by comparing the text by machine, not by reading; that neither document was changed.
  Say what was not checked: a change's effect on other articles that refer to it (a renumbered article that other
  articles still cite by its old number), and anything outside the articles (the title, the preamble).

When `focus` names something, put the pairs that touch it first under the table's heading, and say so.

## Done when

`node <usecase pack>/checks/report.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set) passes.
