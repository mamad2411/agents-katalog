# Repo Ref
- source: https://github.com/NeverSight/learn-skills.dev (path: data/skills-md/brilliantrough/agent-skills/model-datasets/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: 模型与数据集的统一下载、落盘与加载约定：平台（HF / ModelScope）只是下载手段，本地一律 /data/models/<org>__<name>、/data/datasets/<org>__<name>，只用绝对路径喂给 transformers / datasets。含新机器的 /data 磁盘准备规则（无 /data 时初始化或软链）。Use when downloading or 
