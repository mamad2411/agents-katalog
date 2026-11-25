# Repo Ref
- source: https://github.com/hack-wu/skills (path: skills/auto-review/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: 写入 .md / 代码文件后自动做质量审查与修复闭环，判断是否属复杂场景（是则接力 challenger 二次质疑），并在契约面改动时提示影响面缺口（建议转 code-change-impact，不自动执行）。触发：每次 write_to_file / replace_in_file 写入后自动执行。
