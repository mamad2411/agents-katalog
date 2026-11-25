# Repo Ref
- source: https://github.com/eosphoros-ai/DB-GPT (path: assets/suites/db-analysis/skills/multi-step-analysis/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 智能分析场景的多步取数与跨步口径一致性技能。在已圈定的数据集上按分析计划分步生成并执行只读 SQL，每步引用同一指标定义（版本 pin）、统一注入默认过滤与时间粒度，保证跨图跨步口径一致。当用户要求"分析/归因/趋势/对比/占比/复盘/出报告"，需要多步取数（总量趋势+维度拆解+环比同比+异动定位）、需要保证多张图口径一致、需要量价拆解或结构拆解、或出现"两次查的数不一样/口径不一致"问题时使用。
