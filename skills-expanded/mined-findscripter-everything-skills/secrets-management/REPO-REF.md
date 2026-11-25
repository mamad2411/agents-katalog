# Repo Ref
- source: https://github.com/findscripter/everything-skills (path: 08-security/secrets-management/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当在 CI/CD 流水线或运行时需要安全存取 API 密钥、数据库口令、TLS 证书等敏感信息时使用；做法是选定密钥后端（Vault / AWS Secrets Manager / Azure Key Vault / GCP / GitHub-GitLab 内置变量）并以最小权限拉取、轮转与审计，产出可落地的存取与轮转配置；不适用于把明文密钥硬编码进源码或仅需本地不外发的开发值。触发词：密钥管理、
