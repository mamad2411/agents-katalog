# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-0xbb2b-bb-spec/auth-constraints/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 认证与会话约束（authN，不含 authZ）——双 token、refresh 原地轮换 + 重放即吊销、滑动续期、密码 argon2id。触发：实现/设计登录注册、token 签发/刷新/校验、会话或设备管理、密码哈希、登出/吊销、前端 token 携带与刷新。跳过：权限判定（→authz-constraints）、第三方 SSO 托管、与认证无关的业务端点。
