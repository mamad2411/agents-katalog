# Repo Ref
- source: https://github.com/LeoYeAI/openclaw-master-skills (path: skills/spec-driven-dev/sub-skills/spec-driven-checkpoint/SKILL.md, branch: main)
- mined: 2026-10-14
- desc: 为 spec-driven-dev 提供流程中断保存与恢复能力。在任意阶段触发 checkpoint 保存当前 Git 快照、迭代状态、Session 元数据和上下文重建包；rollback 命令可将 Git 仓库和 Agent 上下文恢复到任意历史 checkpoint。支持 save_checkpoint-{us_id} 和 rollback {ckpt_id} 触发。
