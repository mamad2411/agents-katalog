# Repo Ref
- source: https://github.com/thelobbi/claude (path: plugins/claude-code-expert/skills/cc-verify-between-waves/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: Checkpoint-between-waves cadence for multi-file refactors. After each logical batch (wave) of edits, run typecheck + tests; commit only on green; roll back the wave (not the whole branch) on red. Use 
