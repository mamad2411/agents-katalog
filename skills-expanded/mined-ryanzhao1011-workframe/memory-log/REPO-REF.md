# Repo Ref
- source: https://github.com/ryanzhao1011/workframe (path: plugins/core/skills/memory-log/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 查看记忆层活动流水（promotion / migration / moved-out / decay / correction / memory rollback）——从 events.jsonl 重组时间线，展示模块纠正与迁出，并用 memory-index sidecar 补充 MEMORY 条目的当前状态。只读，不改记忆。用于排查记忆条目异常（该在的不在、该降级的还在）、回滚记忆前先看变更
