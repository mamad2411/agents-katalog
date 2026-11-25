# Repo Ref
- source: https://github.com/adkun/dsh-adg-ptc (path: skills/adg-session-handoff/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 用户调用后，把当前会话交接给一个**全新会话**：提炼出一份可直接整块粘进新会话的**交接提示词**（目标与验收 / 硬约束 / 已定决策与理由 / 当前状态与产物 / 环境事实 / 未决项 / 已排除的路 / 下一步与起手句）。新会话除了这段字没有本会话的任何上下文，所以唯一判据是「它只读这份字就能不追问、不重走弯路地接着干」。用户输入 `/adg-session-handoff`，或说「把当前
