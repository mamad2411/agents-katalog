# Repo Ref
- source: https://github.com/onescience-ai/oneskills (path: skills/onescience-cli/SKILL.md, branch: master)
- mined: 2026-11-23
- desc: 在远程 SSH/SLURM 环境中通过 `onescience` 命令执行任意 OneScience 子命令。根据命令级别（lightweight/normal/compute）自动选择执行通道。环境初始化由 `onescience-installer` 技能处理，计算节点申请与作业提交由 `onescience-runtime` 技能处理。本技能只负责 `onescience` 命令的调度与执行
