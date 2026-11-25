# Repo Ref
- source: https://github.com/lihongwei-cn/lihongwei-cn (path: global-specs/skills/cheat-on-content/skills/cheat-predict/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 给最终稿写一份 immutable 盲预测日志。这是 cheat-on-content 整个校准循环的核心动作——预测段一旦写完不可改，由 hook 强制。**自动检测**：如目标文件已有 `## 预测` / `## 预测 v1` 段（被 cheat-shoot 调用走 v2 模式），改成 append `## 预测 v2` 而非覆盖。**打分通过 Task tool 委派给 `cheat-sco
