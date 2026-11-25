# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/mined-dirtytrii-codex-skills/cheat-migrate/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 把老用户的 .cheat-state.json 升级到当前 schema_version。读 migrations/registry.md 算迁移链，按顺序应用每一步迁移文件。幂等：跑两次结果一样。失败停在中间版本不前进。触发词："迁移"/"升级 state"/"migrate"/"我的 state 是老版本"/"schema 版本不对"。
