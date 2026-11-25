# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-volcengine-ark-cli-arkcli-infer-endpoint/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: arkcli 推理接入点管理与显式 raw CRUD 创建能力。**正向触发：用户明确要求脚本化 / CI / 无护栏 / 原始 raw CRUD 创建 Endpoint 时，必须使用本 skill 的 `arkcli infer endpoint create` 路径，不能切到 `arkcli-deploy`**；模型缺失或只有品牌/家族名时仍留在本 skill，先执行实时有界候选与 0/1/N
