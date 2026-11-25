# Repo Ref
- source: https://github.com/po-et/workbuddy-skills (path: skills/api-diff/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 接口差分测试、两个环境响应对比、上线前后接口回归、灰度 vs 线上对比。当用户说「对比一下预发和线上这批接口的返回」「新版本接口有没有改坏」「同一个请求打两个环境看差异」「接口回归测试」「A/B 环境响应 diff」「重构后接口输出是否一致」「迁移后数据对不对」时使用。脚本把一份用例（方法、路径、头、体）同时打到环境 A 与 B，逐字段深度对比 JSON（可忽略时间戳、trace id 等易变字段
