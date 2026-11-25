# Repo Ref
- source: https://github.com/i-stack/ai-coding-kit (path: skills-engineering/prompt-optimizer/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 提问优化器。用户主动请求优化提问/prompt（如「帮我优化提问」「优化这个 prompt」「改写我的问题」）时，先召回相似历史提问、复用 plan-grill 盘问澄清真实需求，再把模糊提问改写为结构化高质量提示词，透明展示供用户确认或修正，确认前不回答原问题；用户显式跳过确认时仍先展示优化稿并标注「未确认假设」，再基于优化稿回答；最后回写 .plan-reviews 形成闭环。仅主动触发，不做
