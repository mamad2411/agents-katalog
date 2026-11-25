---
name: review-latest-run
description: 基于已持久化证据，从战斗、构筑和路线三个角度复盘最新 run。
---

# 复盘最新 run

适用场景：需要从最新完成的 run 中提取 lesson、hypothesis 或开发改进点。

## 角色定位

这张 skill 对应的是**正式 review**，默认由 reviewer / 组织者来执行。

- player 可以提供自评和当时意图
- 但正式复盘必须以已持久化证据为主
- 不要把 player 的回忆当成 review 主体

## 阅读内容

1. `data\python-runtime\runs\` 下最新 run
2. `battle-summaries.json`
3. `scene-summaries.json`
4. `run-summary.json`
5. 最近的 `events.jsonl`
6. `data\python-runtime\knowledge\lessons.json`
7. `data\python-runtime\knowledge\playbook.json`

## 复盘角度

1. battle 执行
2. deck-building
3. route selection

## 输出结构

请分开：

- durable lessons
- tentative hypotheses
- developer / runtime gaps
- player self-report（如果有，也只作为补充材料）

## 约束

- 必须基于证据。
- 优先引用 event 和 summary，不要给泛泛而谈的攻略。
- 不要把一次 run 的现象直接升格为长期定律。
- battle / deck-building / route selection 三个角度的正式判断，优先由 reviewer / 组织者读记录完成。
