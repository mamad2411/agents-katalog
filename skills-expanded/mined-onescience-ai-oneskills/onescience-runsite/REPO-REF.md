# Repo Ref
- source: https://github.com/onescience-ai/oneskills (path: skills/onescience-runsite/SKILL.md, branch: master)
- mined: 2026-11-23
- desc: 解析、校验、保存和复用 OneScience 运行站点配置。用于任意技能在继续执行任务前补齐运行站点配置，完成配置发现、缺失字段补问、已有配置复用、remote 连接验证、运行平台 DCU/GPU 类型确认、modules 写入和结构化回传。当任务需要远端算力或特定软件（如 VASP/QE/CP2K）且存在多个 SSH 工作台连接时，必须对候选连接做只读软件环境探测，并通过 question 工具
