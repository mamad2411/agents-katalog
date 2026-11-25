# Repo Ref
- source: https://github.com/huanyu-hibiki/huanyu-skills (path: oracle-bone/skills/oracle-predict/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 给最终稿写一份 immutable 盲预测日志。这是 oracle-bone 整个校准循环的核心动作——预测段一旦写完不可改，由 hook 强制。**自动检测**：如目标文件已有预测段（被 oracle-shoot 或 review 改稿触发走 v2 模式），改成 append `## 预测 v2` 而非覆盖。触发词："启动预测"/"start prediction"/"给这稿子打分并预测"/"写
