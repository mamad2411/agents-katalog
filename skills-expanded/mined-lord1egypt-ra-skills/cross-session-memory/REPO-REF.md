# Repo Ref
- source: https://github.com/lord1egypt/ra-skills (path: skills/community/clawhub/c/cross-session-memory/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 给 AI agent/bot 做跨会话持久记忆的分层混合方案。当用户要"给 bot 加记忆""让 agent 记住之前的事""跨会话上下文持久化""记忆去重/断链/陈旧检查"，或要搭一个有长期记忆的 agent 时使用。方案=markdown 真理源(人可读可手改) + SQLite 派生索引(选择性召回) + 生命周期检查(断链/重复/陈旧)，纯标准库零依赖。
