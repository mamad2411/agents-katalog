---
name: weekly-comprehension-check
pack: universal
description: 架构师每周自检——抽 3~5 个本周合并的 PR,用一句话写它做了什么 + 说出一个潜在风险。抽不出来 = 你已经在认知投降。结果写入 state/comprehension-log.jsonl,被 daily-health 周度报告引用。
when_to_use: 每周一架构师的第一件事(daily-health 周一会自动 ping 提醒);或合并量首次超过历史 1.5 倍那一周。
when_NOT_to_use: 不要让 agent 替你做这件事——本 skill 的全部价值在于"你亲手做",代做就是骗自己。
---

# Skill: Weekly Comprehension Check(给人,不给 agent)

> **这个 skill 是写给"使用 harness 的那个人"——架构师自己。**
> agent 看到它要做的事是:**提醒并且只提醒**,不要替架构师填答案。

## 为什么必须做(读一次)

harness 跑得越顺,你越容易停止阅读。
Addy Osmani 把这叫 **cognitive surrender(认知投降)**:同一个 loop,两个人用会得出相反结果——一个在他懂的事上跑得更快,另一个在用它绕开理解。**loop 不知道差别,你知道**。

这个 skill 是结构性护栏,不是仪式。**没有它,harness 把你变成按钮工。**

## 步骤(15 分钟,不能多)

1. 打开 GitHub,看本周合并到 main 的 PR 列表。
2. **随机抽 3~5 个**(可以用 `shuf` 或闭眼点),不抽你自己写的、不抽你已经评过的。
3. **不读 AI 评审,不读描述**——直接读 diff。
4. 对每个 PR,用**自己的话**写两句:
   - 「它做了什么(一句话,小学生能懂)」
   - 「我看到的一个潜在风险或弱点」
5. 把答案存到 `state/comprehension-log.jsonl`:
   ```json
   {"week":"2026-W23","pr":"#142","summary":"...","risk":"...","timestamp":"..."}
   ```

## 自评(对自己诚实)

打完后问自己:

- 我有几个 PR 看 diff 看到一半就想去读 AI 评审了?(每次 +1 个负分)
- 我有几个"风险"是真发现的,几个是凭感觉编的?
- 我有几个 PR 看完仍然不知道为什么这么改?(这意味着 AGENTS.md 或 skill 文档不够)

## 红线信号

任意一条触发,**当周停止合并新 PR 一天**,反思流程或调小灰度:

- 3+ 个 PR 你写不出"它做了什么"——你停止读了
- 0 个 PR 你找到真实风险——你停止思考了
- 5+ 分钟你写不出第一个 summary——你脱离代码了

## 落到指标

`scripts/comprehension_metrics.py` 会读 `state/comprehension-log.jsonl`,
连同 GitHub API 拉来的"本周架构师 review 行为",出三个数:

- `weekly-prs-comprehended`:本周写了 summary 的 PR 数
- `weekly-prs-merged`:本周合并的 PR 总数
- `comprehension-coverage`:= 前者 / 后者

每周一的 daily-health 报告里推送。**低于 5% 是真危险**(不是低于 100%)。

## 反模式

- ❌ 让 agent 帮你写 summary——这就是字面意义的认知投降
- ❌ 抽 PR 时只挑你写过的——丧失外部样本意义
- ❌ "潜在风险" 写"没看到风险"——这条不算回答,重抽
- ❌ 跳过当周——下周补两倍?不,跳过就是跳过,记在日志里
