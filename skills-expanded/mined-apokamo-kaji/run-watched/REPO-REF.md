# Repo Ref
- source: https://github.com/apokamo/kaji (path: .claude/skills/run-watched/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 保守者が指定した Issue 群を series として直列に起動し、kaji watch で監視させる起動の入口。「#101, #102 を dev で直列に」のような明示的な依頼のときに使う。判断（workflow の選択・順番）は skill が行い、YAML 生成・commit・push・ラベル・タブ・起動は決定的な script（run_watched plan / execute）に任
