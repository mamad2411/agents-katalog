# Repo Ref
- source: https://github.com/galact-byte/galact-skills (path: skills/hunt-request-smuggling/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 在授权渗透测试中系统性挖掘 HTTP 请求走私（HTTP Request Smuggling / desync）。当目标前面有反向代理/CDN/负载均衡（前端）转发给后端应用，且怀疑前后端对 Content-Length 与 Transfer-Encoding、畸形头、chunked trailer 的解析不一致时使用——典型场景：想毒化后端 socket 劫持他人请求、批量窃取会话 Cookie
