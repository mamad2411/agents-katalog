# Repo Ref
- source: https://github.com/yunshu0909/yunshu_skillshub (path: req-change-workflow/SKILL.md, branch: master)
- mined: 2026-09-20
- desc: 已有功能的需求变更闭环（门禁式七步）。触发硬条件：要改的功能已经实现并跑起来了。当用户说"改需求""需求变更""调整交互""改功能""重构流程"，或改动容易散到多个文件、碰到鉴权/存储/配置/权限、需要可靠验证 + 回滚方案时使用。流程：锁 scope 写 change brief → 从代码确认当前行为（不靠记忆和假设）→ 影响面与风险评估 + 回滚计划 → 提出新设计等用户批准（**未获批准绝
