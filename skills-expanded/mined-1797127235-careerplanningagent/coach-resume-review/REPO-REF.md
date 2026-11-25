# Repo Ref
- source: https://github.com/1797127235/careerplanningagent (path: agent/skills/coach-resume-review/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户请求点评/审视/诊断自己的简历时使用（典型标志：'帮我看看简历'/'评价我的简历'/'我的简历怎么样'/'简历够不够'/'简历有什么问题'/'改改我的简历'/'简历给面试官看行不行' 等）。应用本 skill：先调 get_user_profile 拿到技能+项目清单，再从'面试官视角'给 3 个具体问题（项目深度/技术选型合理性/表述精度），最后给 1 个最紧迫的改进方向。禁止在没调 ge
