# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-0xbb2b-bb-spec/observability-constraints/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 可观测性约束（日志/链路/指标）——三信号一处装配 + OTel 统一标准；JSON 日志 + trace_id 从 ctx 自动注入（无 trace 输出空串）；指标 `<domain>_<noun>_<unit>` + label 基数有限；body 凭证脱敏。触发：搭建/修改日志/链路/指标、新增指标或日志字段、接入 OTel/OTLP、设计日志级别或告警。跳过：前端埋点/RUM、纯三方托管
