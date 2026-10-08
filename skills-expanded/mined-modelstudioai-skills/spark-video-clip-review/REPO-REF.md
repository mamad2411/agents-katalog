# Repo Ref
- source: https://github.com/modelstudioai/skills (path: skills/spark-video/references/spark-video-clip-review/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: Per-clip quality reviewer + render retry state machine. After each rendered shot, score it on 6 axes via `bl omni` (qwen3.5-omni-plus), then decide ACCEPT / REJECT-and-rewrite / REJECT-and-escalate. H
