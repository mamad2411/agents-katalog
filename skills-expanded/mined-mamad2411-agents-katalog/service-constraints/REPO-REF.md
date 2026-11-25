# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-0xbb2b-bb-spec/service-constraints/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 后端服务运行时治理——启动 fail-fast；优雅生命周期（SIGTERM→排空→超时强退→LIFO 释放）；非幂等写经幂等键；跨进程必设超时、重试仅幂等且退避。触发：启动/关闭、健康检查、写幂等、下游超时/重试、错误传播。跳过：配置载体与密钥分层（→config-constraints）、代码风格（→golang-constraints）、API 契约（→api-design）、可观测性（→o
