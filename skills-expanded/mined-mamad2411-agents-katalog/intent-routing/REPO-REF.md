# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-TencentCloud-Octop-intent-routing/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 请求入口的意图识别与技能路由。按渐进式判断意图：先通用任务（直接做）、再高风险临床（拒绝）、再区分纯信源核验与医学学习、最后登记/订阅。纯信源核验先走 source-verify；原始路径受限时再进入 medical-source-failover。医学学习才调对应 skill + output-format 校验。
