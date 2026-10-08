---
name: handoff-resume
description: 从 `.codex/state/` 恢复完整项目上下文并输出可继续推进的 Resume 摘要（Current Focus / Next 3 / Blockers / Pitfalls）。当用户说“继续之前的任务”“恢复上一个窗口的工作”“恢复上下文”或输入 `/resume`、`/restore-context` 时使用。
---

# Handoff Resume

你现在要执行“恢复上下文”。

目标：从 `.codex/state/` 读取最小但足够的状态，快速恢复到可执行状态。

## 读取顺序

1. `.codex/state/HANDOFF.md`，若存在则优先
2. `.codex/state/progress.md`
3. `.codex/state/BRIEF.md`
4. `.codex/state/issues/` 中 Open / Doing / Blocked 的 Issue
5. `.codex/state/kb/` 中与当前焦点相关的 KB

## 如果状态目录不存在

- 明确说明当前项目未初始化持久上下文。
- 建议执行 `project-state-init` 并使用 `--init-state` 生成骨架。
- 不要假装已经恢复成功。

## 输出要求

- 只输出恢复后的行动摘要，不复述全部文件内容。
- 至少包含：`Current Focus`、`Why Now`、`Next 3`、`Blockers`、`Active Issues`、`Pitfalls`、`First Action`。
- 如果 HANDOFF 与 progress 或 BRIEF 有冲突，以较新的状态文件和当前事实为准，并点明冲突。
- 若信息不足，明确列出“待确认项”。

## 落地原则

- 本 skill 默认只读，不主动写文件。
- 如果本次恢复后立即进入执行阶段，可在后续由 `ops-sync` 记录“已完成一次 resume”这一动作。
