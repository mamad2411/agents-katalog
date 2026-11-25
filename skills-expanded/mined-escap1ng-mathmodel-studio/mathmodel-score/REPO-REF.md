# Repo Ref
- source: https://github.com/escap1ng/mathmodel-studio (path: skills/mathmodel-score/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 论文评分与质量自检模块：按百分制五维（摘要 30 / 算法模型 20 / 创新性 20 / 写作 15 / 排版 15）对论文打分，交付前逐项自检并给出扣分明细、优化轮次与达标判定。用 score_card.py 把评分卡 JSON 校验并渲染成评分表（达标线 85，一票否决直接淘汰，熔断 3 轮）。当用户要求给论文打分、自检、生成评分表、评估能否交付、判断 AI/合规风险时触发。建模与写作规范以
