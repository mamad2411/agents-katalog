# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/mstx-report-soft-sync-ascend-msagent/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 分析 AscendC 算子中自实现的软同步代码，判断其所属同步语义（核间 barrier/set-wait、卡间 barrier/signal），并接入 mssanitizer 的 Sanitizer 接口（sanitizer_report.h）上报软同步语义，避免 racecheck 对软同步误报。触发：算子存在自实现软同步（GM 地址轮询、flag 计数、跨核/跨卡信号等）需要配合 mssan
