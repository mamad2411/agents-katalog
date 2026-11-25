# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-volcengine-ark-cli-arkcli-deploy/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: arkcli +deploy：普通创建推理接入点（Endpoint）的统一首选入口。用户说『创建/新建/create 一个 endpoint/接入点』或『部署/上线/deploy 某模型』时优先走这里；**但脚本化 / CI / 无护栏 / 原始 raw CRUD 创建是唯一例外，必须改走 `arkcli-infer-endpoint`，不能由本 skill 截获**。只有不命中该例外的普通创建，
