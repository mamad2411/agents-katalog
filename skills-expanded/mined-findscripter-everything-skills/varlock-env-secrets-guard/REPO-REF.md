# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 08-security/varlock-env-secrets-guard/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当在 AI Agent/Claude 会话、终端、日志或 git 提交中处理含密钥的环境变量、想让敏感值默认脱敏不外泄时使用；做法是用 varlock 在 .env.schema 中以 @sensitive/@type/@required 声明并校验 env，用 varlock run 注入运行时、用其自动脱敏的 redacted 输出替代明文 echo，产出可校验、可加密提交且日志安全的 env
