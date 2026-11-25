# Repo Ref
- source: https://github.com/zhaoxinghua09-cell/agent-skills (path: skills/output-schema-guard/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 当用户说『模型返回的JSON又崩了』『字段缺失对不上』『下游解析失败』『怎么强制LLM输出合规结构』，或要把 LLM 的 JSON/结构化输出接进代码（API/数据库/表单）时使用。把模型输出当『不可信外部输入』：用 schema 校验必填字段·类型·枚举，缺则给可执行的修复提示而非裸报错。理论根基：LGD 三律（有籍·有证·有门禁）。触发词：结构化输出、JSON校验、schema guard、输
